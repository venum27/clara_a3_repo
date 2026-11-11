"""Assignment 3 -- SCP with the official CLaRa target: all QA pairs of a passage written as ONE target.

Our A2 SCP (train_scp.py) turns every synthetic QA pair into its own example: the generator gets the memory and one
question and must produce that answer. The official CLaRa code instead gives the generator only the memory and asks it
to write out all question-answer pairs of the passage in a single target, e.g.
    Question: Who directed the 1930 film Charlotte Lowenskold? Answer: Gustaf Molander
    Question: ...? Answer: ...
This file is train_scp.py with exactly that change (--target allqa, the default); everything else -- data, model
construction order, seed, shuffling, paraphrase example, loss (NTP + lambda * MSE), optimiser, epochs and the saved
checkpoint format -- is the same, so the result feeds train_e2e.py / train_e2e_a3.py / evaluate.py unchanged.
With --target perqa it reproduces train_scp.py (used to check the copy is faithful).

The target limit is raised from 96 to 256 tokens: four QA pairs together can exceed 96 and would be cut off.
Standalone: imports nothing from this project. Qwen (decoder-only) only.

    python3 train_scp_allqa.py --dataset 2wiki --mode fixed --max_mem 16 --epochs 6 --amp bf16 \
        --run_dir runs/qwen/2wiki/a3_fixed16_allqa_s42          (the setting of r2_fixed_M16_e6_s42, new target)
"""
import argparse
import collections
import contextlib
import json
import os
import random
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
QA_INSTRUCTION = "Answer the question based on the document. Reply with a short answer only.\nQuestion: {q}\nAnswer:"
PARA_INSTRUCTION = "Rewrite the document in your own words."
ALLQA_INSTRUCTION = "Write all question-answer pairs about the document."


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", required=True)
    p.add_argument("--data_dir", default="data")
    p.add_argument("--run_dir", required=True, help="the checkpoint is saved to <run_dir>/scp")
    p.add_argument("--target", choices=["allqa", "perqa"], default="allqa",
                   help="allqa: official CLaRa target (default); perqa: our A2 target (faithfulness check)")
    p.add_argument("--mode", choices=["nested", "fixed"], default="fixed")
    p.add_argument("--max_mem", type=int, default=16)
    p.add_argument("--prefix_set", default="4,8,16,32")
    p.add_argument("--nest_loss", choices=["sample", "all"], default="sample")
    p.add_argument("--epochs", type=int, default=6)
    p.add_argument("--lr", type=float, default=1e-4)
    p.add_argument("--lambda_mse", type=float, default=0.1)
    p.add_argument("--mse_detach_doc", type=int, default=1)
    p.add_argument("--lora_r", type=int, default=16)
    p.add_argument("--max_doc_tokens", type=int, default=256)
    p.add_argument("--max_target_tokens", type=int, default=None, help="default: 256 for allqa, 96 for perqa")
    p.add_argument("--max_paraphrase_chars", type=int, default=400)
    p.add_argument("--rescale_memory", type=int, default=0)
    p.add_argument("--amp", choices=["none", "bf16"], default="none")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--tiny", action="store_true")
    return p


# ---------------------------------------------------------------------------------------------- utilities
def read_json(path):
    with open(path) as f:
        return json.load(f)


def write_json(obj, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def set_seed(seed):
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass
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
    env = os.environ.get("QWEN_MODEL")
    if env:
        return env
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", MODEL_ID.split("/")[-1])
    return local if os.path.isfile(os.path.join(local, "config.json")) else MODEL_ID


def examples_for(doc_rec, max_para_chars, target):
    pairs = doc_rec.get("simple_qa", []) + doc_rec.get("complex_qa", [])
    if target == "perqa":
        ex = [(QA_INSTRUCTION.format(q=qa["question"]), qa["answer"], "qa") for qa in pairs]
    else:
        ex = [(ALLQA_INSTRUCTION, "\n".join(f"Question: {qa['question']} Answer: {qa['answer']}" for qa in pairs),
               "allqa")] if pairs else []
    if doc_rec.get("paraphrase"):
        ex.append((PARA_INSTRUCTION, doc_rec["paraphrase"][:max_para_chars], "para"))
    return ex


# ---------------------------------------------------------------------------------------------- the model
def build_tiny_qwen():
    """Identical to the project's tiny Qwen (plumbing tests on CPU)."""
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
    """The parts of the project's QwenCLaRa that SCP needs, built in the same order with the same names."""

    def __init__(self, base, tokenizer, model_name, max_mem, lora_r, max_doc_tokens, max_target_tokens,
                 rescale_memory, device, max_query_tokens=64):
        super().__init__()
        self.rescale_memory = bool(rescale_memory)
        self.backbone, self.model_name, self.tokenizer = "qwen", model_name, tokenizer
        self.max_mem, self.lora_r = max_mem, lora_r
        self.max_doc_tokens, self.max_query_tokens = max_doc_tokens, max_query_tokens
        self.max_target_tokens = max_target_tokens
        self.device = device
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        self.hidden_size = base.config.hidden_size
        cfg = LoraConfig(r=lora_r, lora_alpha=2 * lora_r, lora_dropout=0.05,
                         target_modules=LORA_TARGETS, task_type="CAUSAL_LM")
        self.model = get_peft_model(base, cfg, adapter_name="compressor")
        self.model.add_adapter("generator", cfg)
        self.model.add_adapter("query_reasoner", cfg)
        self.mem_doc = nn.Parameter(0.02 * torch.randn(max_mem, self.hidden_size))
        self.mem_query = nn.Parameter(self.mem_doc.detach().clone())
        self.to(device)
        with torch.no_grad():
            self.embed_norm = self.model.get_input_embeddings().weight.norm(dim=-1).mean().item()
        self._lora = [(n, p) for n, p in self.model.named_parameters() if "lora_" in n]
        self._trainable = set()
        self.set_trainable([])

    def set_trainable(self, adapters, mem_doc=False, mem_query=False):
        for p in self.model.parameters():
            p.requires_grad_(False)
        self._trainable = {n for n, _ in self._lora if any(f".{a}." in n for a in adapters)}
        for n, p in self._lora:
            p.requires_grad_(n in self._trainable)
        self.mem_doc.requires_grad_(mem_doc)
        self.mem_query.requires_grad_(mem_query)

    def use(self, adapter):
        self.model.set_adapter(adapter)
        for n, p in self._lora:
            p.requires_grad_(n in self._trainable)

    def trainable_parameters(self):
        return [p for p in self.parameters() if p.requires_grad]

    def lora_snapshot(self):
        return {n: p.detach().float().cpu().clone() for n, p in self._lora}

    def delta_report(self, before):
        after = self.lora_snapshot()
        report = {}
        for a in ADAPTERS:
            keys = [k for k in after if f".{a}." in k]
            changed = sum(not torch.equal(before[k], after[k]) for k in keys)
            total_abs = sum((after[k] - before[k]).abs().sum().item() for k in keys)
            numel = sum(after[k].numel() for k in keys)
            nonzero_b = sum(after[k].abs().sum().item() > 0 for k in keys if "lora_B" in k)
            report[a] = {"tensors": len(keys), "changed": changed, "mean_abs_delta": total_abs / max(numel, 1),
                         "lora_B_nonzero": f"{nonzero_b}/{sum('lora_B' in k for k in keys)}"}
        return report

    def meta(self):
        return {"backbone": self.backbone, "model_name": self.model_name, "max_mem": self.max_mem,
                "lora_r": self.lora_r, "max_doc_tokens": self.max_doc_tokens,
                "max_query_tokens": self.max_query_tokens, "max_target_tokens": self.max_target_tokens,
                "rescale_memory": self.rescale_memory}

    def save(self, out_dir, extra_meta=None):
        os.makedirs(out_dir, exist_ok=True)
        torch.save({n: p.detach().cpu() for n, p in self._lora}, os.path.join(out_dir, "lora_state.pt"))
        torch.save({"mem_doc": self.mem_doc.detach().cpu(), "mem_query": self.mem_query.detach().cpu()},
                   os.path.join(out_dir, "mem_embeddings.pt"))
        write_json({**self.meta(), **(extra_meta or {})}, os.path.join(out_dir, "meta.json"))

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


# ---------------------------------------------------------------------------------------------- training (= train_scp.py)
def main(args):
    set_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ac = precision_context(args.amp, device)
    if os.path.exists(os.path.join(args.run_dir, "scp", "meta.json")):
        raise SystemExit(f"{args.run_dir}/scp already exists; delete it first to retrain")
    prefix_set = [args.max_mem] if args.mode == "fixed" else sorted(int(x) for x in args.prefix_set.split(","))
    assert max(prefix_set) <= args.max_mem, "prefix lengths cannot exceed max_mem"
    max_target = args.max_target_tokens or (256 if args.target == "allqa" else 96)

    docs = [d for d in read_json(os.path.join(args.data_dir, f"{args.dataset}_scp.json")) if d["split"] == "train"]
    if args.tiny:
        base, tok, model_name = build_tiny_qwen()
    else:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        model_name = resolve_model()
        tok = AutoTokenizer.from_pretrained(model_name)
        base = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)
    model = NestedQwen(base, tok, model_name, args.max_mem, args.lora_r, args.max_doc_tokens, max_target,
                       args.rescale_memory, device)
    model.set_trainable(["compressor", "generator"], mem_doc=True)
    params = model.trainable_parameters()
    opt = torch.optim.AdamW(params, lr=args.lr)
    before = model.lora_snapshot()
    if args.target == "allqa":
        lengths = [len(tok("\n".join(f"Question: {q['question']} Answer: {q['answer']}"
                                     for q in d.get("simple_qa", []) + d.get("complex_qa", [])),
                           add_special_tokens=False).input_ids) for d in docs]
        cut = sum(n >= max_target for n in lengths)
        print(f"  all-QA targets: mean {sum(lengths) / len(lengths):.0f} tokens, max {max(lengths)}, "
              f"{cut} of {len(docs)} cut at {max_target}")
    print(f"[SCP {args.mode}, target {args.target}] qwen/{args.dataset}: {len(docs)} passages | prefixes "
          f"{prefix_set} | trainable params {sum(p.numel() for p in params):,} | device {device}")

    rng = random.Random(args.seed)
    log = {"args": vars(args), "prefix_set": prefix_set, "epochs": []}
    model.model.train()
    t0 = time.time()
    for epoch in range(args.epochs):
        rng.shuffle(docs)
        ce_by_m = collections.defaultdict(list)
        ce_by_kind = collections.defaultdict(list)
        mse_all, steps = [], 0
        for d in tqdm(docs, desc=f"SCP epoch {epoch + 1}/{args.epochs}", mininterval=30):
            exs = examples_for(d, args.max_paraphrase_chars, args.target)
            if not exs:
                continue
            jobs = [(instr, tgt, kind, m) for instr, tgt, kind in exs
                    for m in (prefix_set if args.nest_loss == "all" else [rng.choice(prefix_set)])]
            opt.zero_grad(set_to_none=True)
            with ac():
                M, doc_h = model.compress(d["document"])
                target_mean = doc_h.mean(0).detach() if args.mse_detach_doc else doc_h.mean(0)
            for j, (instr, tgt, kind, m) in enumerate(jobs):
                with ac():
                    ce = model.gen_loss(instr, [M[:m]], tgt)
                    mse = F.mse_loss(M[:m].mean(0), target_mean)
                    term = (ce + args.lambda_mse * mse) / len(jobs)
                term.backward(retain_graph=j < len(jobs) - 1)
                ce_by_m[m].append(ce.item())
                ce_by_kind[kind].append(ce.item())
                mse_all.append(mse.item())
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            opt.step()
            steps += 1
        ep = {"epoch": epoch + 1, "steps": steps,
              "ce_by_prefix": {m: sum(v) / len(v) for m, v in sorted(ce_by_m.items())},
              "ce_by_target": {k: sum(v) / len(v) for k, v in ce_by_kind.items()},
              "mse": sum(mse_all) / max(len(mse_all), 1)}
        log["epochs"].append(ep)
        print(f"  epoch {epoch + 1}: CE by prefix " +
              " ".join(f"m={m}:{v:.3f}" for m, v in ep["ce_by_prefix"].items()) +
              " | by target " + " ".join(f"{k}:{v:.3f}" for k, v in ep["ce_by_target"].items()) +
              f" | MSE {ep['mse']:.4f}")

    log["minutes"] = (time.time() - t0) / 60
    log["delta_vs_start"] = model.delta_report(before)
    out = os.path.join(args.run_dir, "scp")
    model.save(out, extra_meta={"stage": "scp", "mode": args.mode, "prefix_set": prefix_set,
                                "nest_loss": args.nest_loss, "lambda_mse": args.lambda_mse,
                                "dataset": args.dataset, "seed": args.seed, "scp_target": args.target})
    write_json(log, os.path.join(out, "train_log.json"))
    print(f"  adapter changes since start: " +
          ", ".join(f"{a} {r['changed']}/{r['tensors']}" for a, r in log["delta_vs_start"].items()))
    print(f"  saved -> {out} ({log['minutes']:.1f} min)")


if __name__ == "__main__":
    main(build_parser().parse_args())
