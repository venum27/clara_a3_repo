"""Stage 1.5 -- nested compression instruction tuning (CLaRa's middle stage, adapted to nested memory).

Official CLaRa trains in three stages: SCP -> compression instruction tuning -> end-to-end. Assignment 2 skipped the
middle stage. This file adds it between our nested SCP and our unchanged end-to-end script:

    nested SCP (train_scp.py)  ->  THIS FILE  ->  train_e2e.py  ->  evaluate.py / diagnose_memory.py

Per training question (the same training questions that E2E uses):
  documents   its gold passages + the highest-BM25 distractors, k in total, shown in BM25 order (like a retriever)
  compressor  compresses each document once into max_mem vectors (trained here, as in the official stage1_2)
  generator   reads [instruction ; doc 1 prefix ; ... ; doc k prefix] and predicts the gold answer
  nesting     the loss is averaged over EVERY prefix length m of the checkpoint (4, 8, 16, 32), each document cut to
              m vectors, so short prefixes stay usable even though this stage changes the compressor
  loss        mean over m of   NTP(answer)  +  lambda * mean over docs || mean(M[:m]) - sg(mean(h_doc)) ||^2

Mirrors the official stage1_2: compressor and generator trained, answer loss + 0.1 * MSE, lr 1e-4, 1 epoch.
One default differs: the generator continues from the SCP generator. The official code starts a fresh generator
adapter in stage1_2; --generator_init fresh does that.

Standalone: imports nothing from this project. It rebuilds the model exactly as nclara/modeling.py does (same base
model, same LoRA adapters and parameter names, same prompts) and saves a checkpoint in the same format, so the
existing train_e2e.py, evaluate.py and diagnose_memory.py read it unchanged. Qwen (decoder-only) only.

The tuned checkpoint is written to <runs_dir>/qwen/<dataset>/<name>_s<seed>/scp and <name>__learned_s<seed>/scp for
every seed in --seeds (rule-split and budget-head E2E runs, all seeds starting from one tuned compressor, like the
round-2 seeds). If it already exists it is only copied to missing seeds, so re-running is safe.

    python3 train_it_nested.py --dataset 2wiki --seeds 42,43,44 --amp bf16
    python3 train_it_nested.py --dataset hotpotqa --n_train 20 --name smoke_it --amp bf16   # 1-minute check
    rm -r runs/qwen/hotpotqa/smoke_it*                                                      # then remove it
    python3 train_it_nested.py --tiny --dataset hotpotqa --data_dir tiny_data --runs_dir tiny_runs  # CPU, no GPU
"""
import argparse
import contextlib
import json
import math
import os
import random
import shutil
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
from peft import LoraConfig, get_peft_model
from tqdm import tqdm

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
LORA_TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj"]
ADAPTERS = ("compressor", "generator", "query_reasoner")
MEMORY_PLACEHOLDER = "<<<MEMORY>>>"
# Same prompt as train_e2e.py and evaluate.py, so the generator is tuned on exactly what it reads later.
E2E_INSTRUCTION = ("Answer the question using the retrieved documents. Reply with a short answer only.\n"
                   "Question: {q}\nAnswer:")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", required=True)
    p.add_argument("--data_dir", default="data")
    p.add_argument("--runs_dir", default="runs")
    p.add_argument("--src_run", default=None,
                   help="run whose scp/ checkpoint is tuned (default: <runs_dir>/qwen/<dataset>/"
                        "r2_nested_M32_all_e6_s42, the final nested compressor of Assignment 2)")
    p.add_argument("--name", default="r3_nested_M32_all_e6_it", help="run name of the tuned checkpoint")
    p.add_argument("--seeds", default="42", help="first seed trains; the checkpoint is written for every seed")
    p.add_argument("--k", type=int, default=4, help="documents per question (gold + BM25 distractors)")
    p.add_argument("--doc_order", choices=["bm25", "gold_first", "shuffle"], default="bm25")
    p.add_argument("--epochs", type=int, default=1)
    p.add_argument("--lr", type=float, default=1e-4)
    p.add_argument("--lambda_mse", type=float, default=None, help="default: the value used in SCP (0.1)")
    p.add_argument("--train_compressor", type=int, default=1, help="1: compressor + memory tokens train (official)")
    p.add_argument("--generator_init", choices=["scp", "fresh"], default="scp")
    p.add_argument("--n_train", type=int, default=None, help="use only the first N questions (quick check)")
    p.add_argument("--amp", choices=["none", "bf16"], default="none", help="bf16 on the L40S")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--tiny", action="store_true", help="tiny random model on CPU (plumbing test only)")
    return p


# ---------------------------------------------------------------------------------------------- small utilities
def read_json(path):
    with open(path) as f:
        return json.load(f)


def write_json(obj, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def set_seed(seed):
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def precision_context(amp, device):
    if device == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
    if amp == "bf16" and device == "cuda" and torch.cuda.is_bf16_supported():
        return lambda: torch.autocast("cuda", dtype=torch.bfloat16)
    return contextlib.nullcontext


def resolve_model():
    """Same lookup order as the project: $QWEN_MODEL, then <project>/models/<name>, then the Hugging Face id."""
    env = os.environ.get("QWEN_MODEL")
    if env:
        return env
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", MODEL_ID.split("/")[-1])
    return local if os.path.isfile(os.path.join(local, "config.json")) else MODEL_ID


def bm25_ranking(question, paragraphs):
    try:
        from rank_bm25 import BM25Okapi
        scores = BM25Okapi([p.lower().split() for p in paragraphs]).get_scores(question.lower().split())
    except ImportError:                                     # plain word overlap if rank_bm25 is missing
        q = set(question.lower().split())
        scores = [len(q & set(p.lower().split())) for p in paragraphs]
    return sorted(range(len(paragraphs)), key=lambda i: -scores[i])


# ---------------------------------------------------------------------------------------------- tiny test model
_TINY_WORDS = (["where", "does", "live", "lives", "in", "is", "a", "friend", "of", "the", "was", "born", "and",
                "?", ".", ":", "[", "]", "answer", "question", "based", "on", "document", "using", "retrieved",
                "documents", "rewrite", "your", "own", "words", "paraphrase", "context", "only", "be", "brief",
                "who", "what", "year", "user", "assistant", "that", "person", "city", "home", "one", "which",
                "friends", "with", "resides", "town"]
               + [f"person{i}" for i in range(60)] + [f"city{i}" for i in range(20)]
               + [str(i) for i in range(10)] + [f"{y}" for y in range(1900, 2000)])


def build_tiny_qwen():
    """Identical to the project's tiny Qwen (same seed, sizes and vocabulary), so checkpoints are interchangeable."""
    from tokenizers import Tokenizer, models, normalizers, pre_tokenizers
    from transformers import PreTrainedTokenizerFast, Qwen2Config, Qwen2ForCausalLM
    torch.manual_seed(0)
    specials = ["<pad>", "</s>", "<unk>", "<user>", "<assistant>"]
    tk = Tokenizer(models.WordLevel(vocab={w: i for i, w in enumerate(specials + _TINY_WORDS)}, unk_token="<unk>"))
    tk.normalizer = normalizers.Lowercase()
    tk.pre_tokenizer = pre_tokenizers.Sequence([pre_tokenizers.WhitespaceSplit(), pre_tokenizers.Punctuation()])
    tok = PreTrainedTokenizerFast(tokenizer_object=tk, pad_token="<pad>", eos_token="</s>", unk_token="<unk>")
    tok.chat_template = ("{% for m in messages %}<user> {{ m['content'] }} {% endfor %}"
                         "{% if add_generation_prompt %}<assistant> {% endif %}")
    cfg = Qwen2Config(vocab_size=len(tok), hidden_size=64, intermediate_size=128, num_hidden_layers=2,
                      num_attention_heads=4, num_key_value_heads=2, max_position_embeddings=512,
                      tie_word_embeddings=True, pad_token_id=0, eos_token_id=1, bos_token_id=1)
    return Qwen2ForCausalLM(cfg), tok, "tiny-qwen"


# ---------------------------------------------------------------------------------------------- the model
class NestedQwen(nn.Module):
    """The parts of the project's QwenCLaRa that this stage needs, built the same way (same parameter names)."""

    def __init__(self, base, tokenizer, model_name, meta, device):
        super().__init__()
        self.tokenizer, self.model_name, self.device = tokenizer, model_name, device
        self.max_mem, self.lora_r = meta["max_mem"], meta["lora_r"]
        self.max_doc_tokens = meta.get("max_doc_tokens", 256)
        self.max_target_tokens = meta.get("max_target_tokens", 96)
        self.rescale_memory = bool(meta.get("rescale_memory", False))
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        self.hidden_size = base.config.hidden_size
        cfg = LoraConfig(r=self.lora_r, lora_alpha=2 * self.lora_r, lora_dropout=0.05,
                         target_modules=LORA_TARGETS, task_type="CAUSAL_LM")
        self.model = get_peft_model(base, cfg, adapter_name="compressor")
        self.model.add_adapter("generator", cfg)
        self.model.add_adapter("query_reasoner", cfg)
        self.mem_doc = nn.Parameter(0.02 * torch.randn(self.max_mem, self.hidden_size))
        self.mem_query = nn.Parameter(self.mem_doc.detach().clone())
        self.to(device)
        with torch.no_grad():
            self.embed_norm = self.model.get_input_embeddings().weight.norm(dim=-1).mean().item()
        self._lora = [(n, p) for n, p in self.model.named_parameters() if "lora_" in n]
        self._trainable = set()
        self.set_trainable([])

    # trainability: switching the active adapter must not change which adapters learn (the A1 bug)
    def set_trainable(self, adapters, mem_doc=False):
        for p in self.model.parameters():
            p.requires_grad_(False)
        self._trainable = {n for n, _ in self._lora if any(f".{a}." in n for a in adapters)}
        for n, p in self._lora:
            p.requires_grad_(n in self._trainable)
        self.mem_doc.requires_grad_(mem_doc)
        self.mem_query.requires_grad_(False)

    def use(self, adapter):
        self.model.set_adapter(adapter)
        for n, p in self._lora:
            p.requires_grad_(n in self._trainable)

    def trainable_parameters(self):
        return [p for p in self.parameters() if p.requires_grad]

    def reset_adapter(self, adapter):
        """Fresh LoRA weights, initialised the way PEFT does (A: Kaiming uniform, B: zero)."""
        with torch.no_grad():
            for n, p in self._lora:
                if f".{adapter}." in n:
                    if "lora_A" in n:
                        nn.init.kaiming_uniform_(p, a=math.sqrt(5))
                    elif "lora_B" in n:
                        nn.init.zeros_(p)

    def lora_snapshot(self):
        return {n: p.detach().float().cpu().clone() for n, p in self._lora}

    def changed_report(self, before):
        after = self.lora_snapshot()
        return {a: {"tensors": sum(f".{a}." in k for k in after),
                    "changed": sum(f".{a}." in k and not torch.equal(before[k], after[k]) for k in after)}
                for a in ADAPTERS}

    # checkpoint format = nclara/modeling.py (lora_state.pt, mem_embeddings.pt, meta.json)
    def load_state(self, in_dir):
        state = torch.load(os.path.join(in_dir, "lora_state.pt"), map_location=self.device, weights_only=True)
        own = dict(self._lora)
        missing = [n for n in own if n not in state]
        if missing:
            raise SystemExit(f"{len(missing)} LoRA tensors missing from {in_dir}; is it a Qwen checkpoint?")
        with torch.no_grad():
            for n, t in state.items():
                if n in own:
                    own[n].copy_(t.to(self.device))
            mem = torch.load(os.path.join(in_dir, "mem_embeddings.pt"), map_location=self.device, weights_only=True)
            self.mem_doc.copy_(mem["mem_doc"].to(self.device))
            self.mem_query.copy_(mem["mem_query"].to(self.device))

    def save(self, out_dir, meta):
        os.makedirs(out_dir, exist_ok=True)
        torch.save({n: p.detach().cpu() for n, p in self._lora}, os.path.join(out_dir, "lora_state.pt"))
        torch.save({"mem_doc": self.mem_doc.detach().cpu(), "mem_query": self.mem_query.detach().cpu()},
                   os.path.join(out_dir, "mem_embeddings.pt"))
        write_json(meta, os.path.join(out_dir, "meta.json"))

    # forward passes, identical to QwenCLaRa
    def _decoder(self):
        return self.model.get_base_model().model

    def _lm_head(self):
        return self.model.get_base_model().lm_head

    def ids(self, text, max_len=None):
        enc = self.tokenizer(text, add_special_tokens=False, truncation=max_len is not None, max_length=max_len,
                             return_tensors="pt")
        return enc.input_ids.to(self.device)

    def embed(self, ids):
        return self.model.get_input_embeddings()(ids)

    def compress(self, text):
        """[passage tokens][m_1 .. m_max] through the compressor; returns (memory vectors, passage states)."""
        tok = self.embed(self.ids(text, self.max_doc_tokens))
        x = torch.cat([tok, self.mem_doc.unsqueeze(0)], dim=1)
        self.use("compressor")
        h = self._decoder()(inputs_embeds=x, attention_mask=torch.ones(x.shape[:2], dtype=torch.long,
                                                                      device=self.device)).last_hidden_state[0]
        T = tok.shape[1]
        return h[T:], h[:T]

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

    def _build_inputs(self, instruction, slots):
        pre, post = self._chat_parts(f"{instruction}\n{MEMORY_PLACEHOLDER}")
        parts = [self.embed(self.ids(pre))]
        for i, s in enumerate(slots):
            parts.append(self.embed(self.ids(f"{chr(10) if i else ''}[Document {i + 1}] ")))
            if self.rescale_memory:
                s = s * (self.embed_norm / (s.norm(dim=-1, keepdim=True) + 1e-6))
            parts.append(s.unsqueeze(0))
        if post:
            parts.append(self.embed(self.ids(post)))
        return torch.cat(parts, dim=1)

    def gen_loss(self, instruction, slots, target):
        self.use("generator")
        x = self._build_inputs(instruction, slots)
        tgt = self.tokenizer(target, add_special_tokens=False).input_ids[: self.max_target_tokens - 1]
        tgt = torch.tensor([tgt + [self.tokenizer.eos_token_id]], device=self.device)
        inp = torch.cat([x, self.embed(tgt)], dim=1)
        h = self._decoder()(inputs_embeds=inp, attention_mask=torch.ones(inp.shape[:2], dtype=torch.long,
                                                                        device=self.device)).last_hidden_state
        L, A = x.shape[1], tgt.shape[1]
        logits = self._lm_head()(h[:, L - 1: L - 1 + A])
        return F.cross_entropy(logits.reshape(-1, logits.shape[-1]).float(), tgt.reshape(-1))


# ---------------------------------------------------------------------------------------------- main
def target_dirs(args, seeds):
    base = os.path.join(args.runs_dir, "qwen", args.dataset)
    return [os.path.join(base, f"{args.name}{suffix}_s{s}", "scp") for s in seeds for suffix in ("", "__learned")]


def copy_to(primary, targets):
    for t in targets:
        if t != primary and not os.path.exists(os.path.join(t, "meta.json")):
            if os.path.exists(t):
                shutil.rmtree(t)
            shutil.copytree(primary, t)
            print(f"  copied -> {t}")


def main(args):
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    set_seed(seeds[0])
    targets = target_dirs(args, seeds)
    primary = targets[0]
    exists = [os.path.exists(os.path.join(t, "meta.json")) for t in targets]
    if exists[0] and not args.overwrite:
        print(f"[IT] {primary} already exists: not retraining, only copying to missing seeds")
        copy_to(primary, targets)
        return
    if any(exists[1:]) and not args.overwrite:
        raise SystemExit("some target checkpoints exist but the main one does not; use --overwrite to rebuild all")

    src_run = args.src_run or os.path.join(args.runs_dir, "qwen", args.dataset, "r2_nested_M32_all_e6_s42")
    src = os.path.join(src_run, "scp")
    if not os.path.exists(os.path.join(src, "meta.json")):
        raise SystemExit(f"{src} not found: the nested SCP checkpoint must exist first")
    meta = read_json(os.path.join(src, "meta.json"))
    if meta.get("backbone", "qwen") != "qwen":
        raise SystemExit("this stage supports the Qwen (decoder-only) backbone only")
    prefix_set = sorted(meta.get("prefix_set", [meta["max_mem"]]))
    lam = meta.get("lambda_mse", 0.1) if args.lambda_mse is None else args.lambda_mse

    device = "cuda" if torch.cuda.is_available() else "cpu"
    ac = precision_context(args.amp, device)
    if args.tiny:
        base, tok, model_name = build_tiny_qwen()
    else:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        model_name = meta.get("model_name") or resolve_model()
        tok = AutoTokenizer.from_pretrained(model_name)
        base = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)
    model = NestedQwen(base, tok, model_name, meta, device)
    model.load_state(src)
    if args.generator_init == "fresh":
        model.reset_adapter("generator")
    trained = ["compressor", "generator"] if args.train_compressor else ["generator"]
    model.set_trainable(trained, mem_doc=bool(args.train_compressor))
    params = model.trainable_parameters()
    opt = torch.optim.AdamW(params, lr=args.lr)
    before = model.lora_snapshot()

    records = read_json(os.path.join(args.data_dir, f"{args.dataset}_train.json"))
    records = [r for r in records if len(r["paragraphs"]) >= args.k][: args.n_train]
    items = []
    for r in records:
        paras = r["paragraphs"]
        gold = [i for i in r["gold_idx"] if i < len(paras)]
        ranking = bm25_ranking(r["question"], paras)
        chosen = (gold + [i for i in ranking if i not in gold])[: args.k]
        if args.doc_order == "bm25":
            chosen.sort(key=ranking.index)
        items.append({"question": r["question"], "answer": r["answer"], "docs": [paras[i] for i in chosen]})
    print(f"[IT] {args.dataset}: {len(items)} questions x {args.k} docs ({args.doc_order} order) | prefixes "
          f"{prefix_set} | trains {trained}{' + memory tokens' if args.train_compressor else ''} | generator "
          f"from {args.generator_init} | lr {args.lr} | lambda {lam} | epochs {args.epochs} | "
          f"params {sum(p.numel() for p in params):,} | from {src}")

    rng = random.Random(seeds[0])
    log = {"args": vars(args), "src": src, "prefix_set": prefix_set, "epochs": []}
    model.model.train()
    t0 = time.time()
    for epoch in range(args.epochs):
        rng.shuffle(items)
        ce_by_m = {m: [] for m in prefix_set}
        mses = []
        for it in tqdm(items, desc=f"IT epoch {epoch + 1}/{args.epochs}", mininterval=30):
            docs = list(it["docs"])
            if args.doc_order == "shuffle":
                rng.shuffle(docs)
            instr = E2E_INSTRUCTION.format(q=it["question"])
            opt.zero_grad(set_to_none=True)
            grad_ctx = contextlib.nullcontext() if args.train_compressor else torch.no_grad()
            with ac(), grad_ctx:
                comp = [model.compress(d) for d in docs]
            Ms = [M for M, _ in comp]
            means = [h.mean(0).detach() for _, h in comp]
            # one prefix term at a time, backpropagated at once (as in train_scp.py): only one generator graph is
            # in memory; the shared compressor graph is kept until the last term. Same gradients as one backward.
            for j, m in enumerate(prefix_set):
                with ac():
                    ce = model.gen_loss(instr, [M[:m] for M in Ms], it["answer"])
                    mse = torch.stack([F.mse_loss(M[:m].mean(0), t) for M, t in zip(Ms, means)]).mean()
                    term = (ce + lam * mse) / len(prefix_set)
                term.backward(retain_graph=bool(args.train_compressor) and j < len(prefix_set) - 1)
                ce_by_m[m].append(ce.item())
                mses.append(mse.item())
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            opt.step()
        ep = {"epoch": epoch + 1, "ce_by_prefix": {m: sum(v) / len(v) for m, v in ce_by_m.items()},
              "mse": sum(mses) / max(len(mses), 1)}
        log["epochs"].append(ep)
        print(f"  epoch {epoch + 1}: CE by prefix " +
              " ".join(f"m={m}:{v:.3f}" for m, v in ep["ce_by_prefix"].items()) + f" | MSE {ep['mse']:.4f}")

    log["minutes"] = (time.time() - t0) / 60
    log["changed_vs_src"] = model.changed_report(before)
    out_meta = {**meta, "stage": "scp+it",
                "it": {"src": src, "k": args.k, "doc_order": args.doc_order, "epochs": args.epochs, "lr": args.lr,
                       "lambda_mse": lam, "train_compressor": args.train_compressor,
                       "generator_init": args.generator_init, "n_questions": len(items), "seed": seeds[0]}}
    model.save(primary, out_meta)
    write_json(log, os.path.join(primary, "train_log.json"))
    d = log["changed_vs_src"]
    print(f"  changed vs SCP: compressor {d['compressor']['changed']}/{d['compressor']['tensors']} | generator "
          f"{d['generator']['changed']}/{d['generator']['tensors']} | query_reasoner "
          f"{d['query_reasoner']['changed']}/{d['query_reasoner']['tensors']} (expect 0) | "
          f"{log['minutes']:.1f} min")
    print(f"  saved -> {primary}")
    copy_to(primary, targets)


if __name__ == "__main__":
    main(build_parser().parse_args())
