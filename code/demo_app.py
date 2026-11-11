"""Assignment 3 -- local demo of nested CLaRa with a learned budget head (Gradio).

Pick a held-out question (or type your own question over that example's passages). The app shows
  1. the 10 candidate passages, ranked by the trained query reasoner (cosine score), gold passages marked
  2. the 4 passages the generator reads
  3. how the memory budget is split across them: learned (budget head) vs uniform (CLaRa) vs top-heavy
  4. the answer generated with each split, and EM / F1 against the gold answer
Every passage is compressed once into 32 nested memory vectors; each split only decides how many of them to read.

Standalone: imports nothing from this project. It rebuilds the model exactly as nclara/modeling.py does and loads a
trained run's e2e/ checkpoint and budget head. Qwen (decoder-only) only. Runs on a GPU or, more slowly, on a CPU.

    python3 demo_app.py                                   # default run: final config, budget head, 2Wiki, seed 42
    python3 demo_app.py --dataset hotpotqa --run runs/qwen/hotpotqa/r2_nested_M32_all_e6__learned_s42
    python3 demo_app.py --share                           # also print a public gradio.live link
Viewing from a laptop when it runs on the server: ssh -L 7860:localhost:7860 <user>@<server>, then open
http://localhost:7860 in the laptop's browser.
"""
import argparse
import collections
import contextlib
import itertools
import json
import os
import re
import string
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
from peft import LoraConfig, get_peft_model

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
LORA_TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj"]
MEMORY_PLACEHOLDER = "<<<MEMORY>>>"
E2E_INSTRUCTION = ("Answer the question using the retrieved documents. Reply with a short answer only.\n"
                   "Question: {q}\nAnswer:")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", default="2wiki")
    p.add_argument("--run", default=None, help="run folder with e2e/ (default: <runs_dir>/qwen/<dataset>/"
                                               "r2_nested_M32_all_e6__learned_s42)")
    p.add_argument("--runs_dir", default="runs")
    p.add_argument("--data_dir", default="data")
    p.add_argument("--n_examples", type=int, default=50, help="held-out questions offered in the drop-down")
    p.add_argument("--k", type=int, default=4)
    p.add_argument("--port", type=int, default=7860)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--share", action="store_true")
    p.add_argument("--tiny", action="store_true", help="tiny random model (UI test only)")
    return p


# ---------------------------------------------------------------------------------------------- metrics
def normalize_answer(s):
    s = str(s).lower()
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    s = "".join(ch for ch in s if ch not in set(string.punctuation))
    return " ".join(s.split())


def f1_score(pred, gold):
    p, g = normalize_answer(pred).split(), normalize_answer(gold).split()
    same = sum((collections.Counter(p) & collections.Counter(g)).values())
    if same == 0:
        return 0.0
    precision, recall = same / len(p), same / len(g)
    return 2 * precision * recall / (precision + recall)


def clean_prediction(text):
    for line in str(text).split("\n"):
        line = line.strip()
        if line:
            return re.sub(r"^(answer|a)\s*[:\-]\s*", "", line, flags=re.I).strip()
    return ""


# ---------------------------------------------------------------------------------------------- splits
def _snap_down(x, allowed):
    fits = [a for a in allowed if a <= x]
    return max(fits) if fits else None


def rule_split(policy, k, total, allowed):
    allowed = sorted(allowed)
    if policy == "uniform":
        return [_snap_down(total // k, allowed)] * k
    out, remaining, lo = [], total, allowed[0]
    for i in range(k):
        b = _snap_down(remaining - lo * (k - i - 1), allowed)
        out.append(b)
        remaining -= b
    return out


class BudgetHead(nn.Module):
    """Same architecture as nclara/budget.py, so the saved budget_head.pt loads directly."""

    def __init__(self, hidden_size, lengths, k, proj=128, width=128):
        super().__init__()
        self.lengths = sorted(int(x) for x in lengths)
        self.k = k
        self.proj_q = nn.Linear(hidden_size, proj)
        self.proj_d = nn.Linear(hidden_size, proj)
        self.mlp = nn.Sequential(nn.Linear(3 * proj + 2 + k, width), nn.GELU(), nn.Linear(width, len(self.lengths)))

    def forward(self, q_pool, d_pools, scores):
        n = d_pools.shape[0]
        q = self.proj_q(F.normalize(q_pool.float(), dim=-1)).unsqueeze(0).expand(n, -1)
        d = self.proj_d(F.normalize(d_pools.float(), dim=-1))
        s = scores.float()
        rank = torch.eye(self.k, device=d.device)[:n]
        extra = torch.cat([s[:, None], (s - s.max())[:, None], rank], dim=-1)
        return self.mlp(torch.cat([q, d, q * d, extra], dim=-1))

    def best_split(self, logits, total):
        pats = [p for p in itertools.product(range(len(self.lengths)), repeat=logits.shape[0])
                if sum(self.lengths[i] for i in p) == total]
        if not pats:
            return None, None
        pats = torch.tensor(pats, dtype=torch.long, device=logits.device)
        rows = torch.arange(logits.shape[0], device=logits.device)
        probs = F.softmax(logits[rows, pats].sum(dim=1), dim=0)
        j = int(probs.argmax())
        return [self.lengths[i] for i in pats[j].tolist()], float(probs[j])


# ---------------------------------------------------------------------------------------------- the model
def build_tiny_qwen():
    from tokenizers import Tokenizer, models, normalizers, pre_tokenizers
    from transformers import PreTrainedTokenizerFast, Qwen2Config, Qwen2ForCausalLM
    words = (["where", "does", "live", "lives", "in", "is", "a", "friend", "of", "the", "was", "born", "and",
              "?", ".", ":", "[", "]", "answer", "question", "based", "on", "document", "using", "retrieved",
              "documents", "rewrite", "your", "own", "words", "paraphrase", "context", "only", "be", "brief",
              "who", "what", "year", "user", "assistant", "that", "person", "city", "home", "one", "which",
              "friends", "with", "resides", "town"]
             + [f"person{i}" for i in range(60)] + [f"city{i}" for i in range(20)]
             + [str(i) for i in range(10)] + [f"{y}" for y in range(1900, 2000)])
    torch.manual_seed(0)
    specials = ["<pad>", "</s>", "<unk>", "<user>", "<assistant>"]
    tk = Tokenizer(models.WordLevel(vocab={w: i for i, w in enumerate(specials + words)}, unk_token="<unk>"))
    tk.normalizer = normalizers.Lowercase()
    tk.pre_tokenizer = pre_tokenizers.Sequence([pre_tokenizers.WhitespaceSplit(), pre_tokenizers.Punctuation()])
    tok = PreTrainedTokenizerFast(tokenizer_object=tk, pad_token="<pad>", eos_token="</s>", unk_token="<unk>")
    tok.chat_template = ("{% for m in messages %}<user> {{ m['content'] }} {% endfor %}"
                         "{% if add_generation_prompt %}<assistant> {% endif %}")
    cfg = Qwen2Config(vocab_size=len(tok), hidden_size=64, intermediate_size=128, num_hidden_layers=2,
                      num_attention_heads=4, num_key_value_heads=2, max_position_embeddings=512,
                      tie_word_embeddings=True, pad_token_id=0, eos_token_id=1, bos_token_id=1)
    return Qwen2ForCausalLM(cfg), tok, "tiny-qwen"


class NestedQwen(nn.Module):
    def __init__(self, base, tokenizer, meta, device):
        super().__init__()
        self.tokenizer, self.device = tokenizer, device
        self.max_mem, self.lora_r = meta["max_mem"], meta["lora_r"]
        self.max_doc_tokens = meta.get("max_doc_tokens", 256)
        self.max_query_tokens = meta.get("max_query_tokens", 64)
        self.rescale_memory = bool(meta.get("rescale_memory", False))
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        self.hidden_size = base.config.hidden_size
        cfg = LoraConfig(r=self.lora_r, lora_alpha=2 * self.lora_r, lora_dropout=0.05,
                         target_modules=LORA_TARGETS, task_type="CAUSAL_LM")
        self.model = get_peft_model(base, cfg, adapter_name="compressor")
        self.model.add_adapter("generator", cfg)
        self.model.add_adapter("query_reasoner", cfg)
        self.mem_doc = nn.Parameter(torch.zeros(self.max_mem, self.hidden_size))
        self.mem_query = nn.Parameter(torch.zeros(self.max_mem, self.hidden_size))
        self.to(device)
        with torch.no_grad():
            self.embed_norm = self.model.get_input_embeddings().weight.norm(dim=-1).mean().item()
        self._lora = [(n, p) for n, p in self.model.named_parameters() if "lora_" in n]

    def load_state(self, in_dir):
        state = torch.load(os.path.join(in_dir, "lora_state.pt"), map_location=self.device, weights_only=True)
        own = dict(self._lora)
        missing = [n for n in own if n not in state]
        if missing:
            raise SystemExit(f"{len(missing)} LoRA tensors missing from {in_dir}")
        with torch.no_grad():
            for n, t in state.items():
                if n in own:
                    own[n].copy_(t.to(self.device))
            mem = torch.load(os.path.join(in_dir, "mem_embeddings.pt"), map_location=self.device, weights_only=True)
            self.mem_doc.copy_(mem["mem_doc"].to(self.device))
            self.mem_query.copy_(mem["mem_query"].to(self.device))

    def _decoder(self):
        return self.model.get_base_model().model

    def ids(self, text, max_len=None):
        enc = self.tokenizer(text, add_special_tokens=False, truncation=max_len is not None, max_length=max_len,
                             return_tensors="pt")
        return enc.input_ids.to(self.device)

    def embed(self, ids):
        return self.model.get_input_embeddings()(ids)

    @torch.no_grad()
    def compress(self, text, adapter="compressor", is_query=False):
        tok = self.embed(self.ids(text, self.max_query_tokens if is_query else self.max_doc_tokens))
        mem = (self.mem_query if is_query else self.mem_doc).unsqueeze(0)
        x = torch.cat([tok, mem], dim=1)
        self.model.set_adapter(adapter)
        h = self._decoder()(inputs_embeds=x, attention_mask=torch.ones(x.shape[:2], dtype=torch.long,
                                                                      device=self.device)).last_hidden_state[0]
        return h[tok.shape[1]:]

    def _chat_parts(self, user_text):
        if getattr(self.tokenizer, "chat_template", None):
            s = self.tokenizer.apply_chat_template([{"role": "user", "content": user_text}],
                                                   tokenize=False, add_generation_prompt=True)
        else:
            s = f"User: {user_text}\nAssistant:"
        if MEMORY_PLACEHOLDER in s:
            pre, post = s.split(MEMORY_PLACEHOLDER)
            return pre, post
        return s, ""

    @torch.no_grad()
    def generate(self, question, slots, max_new_tokens=24):
        self.model.set_adapter("generator")
        pre, post = self._chat_parts(f"{E2E_INSTRUCTION.format(q=question)}\n{MEMORY_PLACEHOLDER}")
        parts = [self.embed(self.ids(pre))]
        for i, s in enumerate(slots):
            parts.append(self.embed(self.ids(f"{chr(10) if i else ''}[Document {i + 1}] ")))
            if self.rescale_memory:
                s = s * (self.embed_norm / (s.norm(dim=-1, keepdim=True) + 1e-6))
            parts.append(s.unsqueeze(0))
        if post:
            parts.append(self.embed(self.ids(post)))
        x = torch.cat(parts, dim=1)
        out = self.model.generate(inputs_embeds=x, attention_mask=torch.ones(x.shape[:2], dtype=torch.long,
                                                                             device=self.device),
                                  max_new_tokens=max_new_tokens, do_sample=False,
                                  pad_token_id=self.tokenizer.pad_token_id, eos_token_id=self.tokenizer.eos_token_id)
        return clean_prediction(self.tokenizer.decode(out[0], skip_special_tokens=True))


class Demo:
    def __init__(self, args):
        run = args.run or os.path.join(args.runs_dir, "qwen", args.dataset, "r2_nested_M32_all_e6__learned_s42")
        e2e = os.path.join(run, "e2e")
        with open(os.path.join(e2e, "meta.json")) as f:
            self.meta = json.load(f)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if args.tiny:
            base, tok, _ = build_tiny_qwen()
        else:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            name = self.meta.get("model_name") or os.environ.get("QWEN_MODEL") or MODEL_ID
            tok = AutoTokenizer.from_pretrained(name)
            base = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float32)
        self.model = NestedQwen(base, tok, self.meta, self.device)
        self.model.load_state(e2e)
        self.model.eval()
        self.allowed = sorted(self.meta.get("prefix_set", [self.model.max_mem]))
        self.r = self.meta.get("r_score", min(16, self.model.max_mem))
        self.k = args.k
        self.head = None
        head_path = os.path.join(e2e, "budget_head.pt")
        if os.path.exists(head_path):
            ck = torch.load(head_path, map_location=self.device, weights_only=False)
            self.head = BudgetHead(ck["hidden_size"], ck["lengths"], ck["k"]).to(self.device)
            self.head.load_state_dict(ck["state"])
            self.head.eval()
        with open(os.path.join(args.data_dir, f"{args.dataset}_eval.json")) as f:
            recs = [r for r in json.load(f) if len(r["paragraphs"]) >= self.k]
        self.examples = recs[: args.n_examples]
        self.run = run
        self.cache = {}

    def totals(self):
        return [t for t in (16, 32, 64, 128) if self.allowed[0] * self.k <= t <= self.allowed[-1] * self.k]

    def label(self, i):
        r = self.examples[i]
        return f"{i + 1}. [{r.get('type', '?')}] {r['question']}"

    @torch.no_grad()
    def answer(self, example_label, own_question, total):
        t0 = time.time()
        i = int(example_label.split(".")[0]) - 1
        rec = self.examples[i]
        question = own_question.strip() or rec["question"]
        gold = rec["answer"] if not own_question.strip() else None
        total = int(total)
        mems = []
        for p in rec["paragraphs"]:
            if p not in self.cache:
                self.cache[p] = self.model.compress(p)
            mems.append(self.cache[p])
        q = self.model.compress(question, "query_reasoner", is_query=True)
        qv = F.normalize(q[: self.r].flatten(), dim=0)
        scores = torch.stack([F.normalize(m[: self.r].flatten(), dim=0) for m in mems]) @ qv
        ranking = scores.argsort(descending=True).tolist()
        top = ranking[: self.k]

        titles = rec.get("titles", [f"passage {j + 1}" for j in range(len(rec["paragraphs"]))])
        gold_idx = set(rec["gold_idx"]) if gold is not None else set()
        rows = ["| Rank | Score | Title | Gold | Read by generator | Passage (start) |", "|---|---|---|---|---|---|"]
        for pos, j in enumerate(ranking):
            text = rec["paragraphs"][j].replace("|", "/")
            rows.append(f"| {pos + 1} | {scores[j]:.3f} | {titles[j]} | {'yes' if j in gold_idx else ''} | "
                        f"{'yes (doc ' + str(pos + 1) + ')' if pos < self.k else ''} | {text[:110]}... |")

        splits = {"uniform (CLaRa)": rule_split("uniform", self.k, total, self.allowed),
                  "top-heavy (rule)": rule_split("top_heavy", self.k, total, self.allowed)}
        note = ""
        if self.head is not None:
            d_pools = torch.stack([mems[j][: self.allowed[0]].mean(0) for j in top])
            logits = self.head(q[: self.r].mean(0), d_pools, scores[top])
            b, prob = self.head.best_split(logits, total)
            if b is not None:
                splits = {"learned (budget head)": b, **splits}
                note = f"The budget head gives its chosen split probability {prob:.2f}."
        memo, out = {}, ["| Split | Vectors per retrieved doc (rank 1 to 4) | Answer | EM | F1 |", "|---|---|---|---|---|"]
        for name, b in splits.items():
            key = tuple(b)
            if key not in memo:
                memo[key] = self.model.generate(question, [mems[j][:bj] for j, bj in zip(top, b)])
            pred = memo[key]
            em = f1 = "-"
            if gold is not None:
                em = "1" if normalize_answer(pred) == normalize_answer(gold) else "0"
                f1 = f"{100 * f1_score(pred, gold):.0f}"
            out.append(f"| {name} | {b} (total {sum(b)}) | {pred} | {em} | {f1} |")
        hits = sum(j in gold_idx for j in top)
        summary = (f"**Question:** {question}  \n" + (f"**Gold answer:** {gold}  \n" if gold is not None else
                   "**Own question:** no gold answer, so no EM/F1.  \n") +
                   (f"**Retrieval:** {hits} of the {len(gold_idx)} gold passages are among the {self.k} read.  \n"
                    if gold is not None else "") +
                   f"**Budget:** {total} memory vectors in total; each passage is stored as {self.model.max_mem} "
                   f"nested vectors and a split decides how many of them the generator reads. {note}  \n"
                   f"Run: `{self.run}` | device {self.device} | {time.time() - t0:.1f} s")
        return summary, "\n".join(out), "\n".join(rows)


def main(args):
    import gradio as gr
    demo = Demo(args)
    totals = demo.totals()
    default_total = 64 if 64 in totals else totals[-1]
    with gr.Blocks(title="Nested CLaRa with learned memory budgets") as app:
        gr.Markdown("## Nested CLaRa: adaptive memory budgets for retrieved documents\n"
                    "Choose a held-out question. The query reasoner ranks the candidate passages, the generator "
                    "reads the top 4 from compressed memory, and the memory budget is split across them in three "
                    "ways. Optionally type your own question about the same passages.")
        with gr.Row():
            ex = gr.Dropdown([demo.label(i) for i in range(len(demo.examples))], value=demo.label(0),
                             label="Held-out question", scale=3)
            total = gr.Radio([str(t) for t in totals], value=str(default_total), label="Total memory vectors",
                             scale=1)
        own = gr.Textbox(label="Or your own question (uses the selected example's passages)", value="")
        go = gr.Button("Run", variant="primary")
        summary = gr.Markdown()
        splits = gr.Markdown()
        cands = gr.Markdown()
        go.click(demo.answer, inputs=[ex, own, total], outputs=[summary, splits, cands])
        app.load(demo.answer, inputs=[ex, own, total], outputs=[summary, splits, cands])
    app.launch(server_name=args.host, server_port=args.port, share=args.share)


if __name__ == "__main__":
    main(build_parser().parse_args())
