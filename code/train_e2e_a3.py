"""Stage 2 for the Assignment 3 ablations -- train_e2e.py with a NaN-safe straight-through top-k.

Why this file exists. train_e2e.py removes an already-picked document from the next top-k slot by adding
log(1 - taken + 1e-9), i.e. about -20.7, to its logit. At the temperature we used (0.5) that is plenty, but at the
official CLaRa temperature (0.02) a cosine gap of 0.6 becomes 30 > 20.7: the same document is picked again,
1 - taken turns negative and log() gives NaN. Training then silently runs on NaN (rule splits) or crashes (budget
head). Here a picked document is masked with -inf instead, so every temperature works. Everything else -- data,
prompts, losses, budget head, REINFORCE, logging and the checkpoint format -- is the same as train_e2e.py, so
evaluate.py and diagnose_memory.py read the result unchanged. At temperature 0.5 it reproduces train_e2e.py.

Standalone: imports nothing from this project (the model is rebuilt exactly as nclara/modeling.py does, with the
same parameter names). Qwen (decoder-only) only.

    python3 train_e2e_a3.py --run_dir runs/qwen/2wiki/a3_fixed16_tau0.02_s42 --dataset 2wiki --train_alloc uniform \
        --tau 0.02 --amp bf16
"""
import argparse
import contextlib
import itertools
import json
import math
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
E2E_INSTRUCTION = ("Answer the question using the retrieved documents. Reply with a short answer only.\n"
                   "Question: {q}\nAnswer:")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--run_dir", required=True)
    p.add_argument("--dataset", required=True)
    p.add_argument("--data_dir", default="data")
    p.add_argument("--k", type=int, default=4, help="documents passed to the generator")
    p.add_argument("--total_budget", type=int, default=64, help="total memory vectors across the k documents")
    p.add_argument("--train_alloc", choices=["learned", "mixed", "uniform", "top_heavy", "score"], default="mixed")
    p.add_argument("--train_totals", default="", help="learned: totals sampled per step, e.g. 32,64")
    p.add_argument("--budget_samples", type=int, default=2)
    p.add_argument("--budget_lr", type=float, default=1e-3)
    p.add_argument("--entropy_coef", type=float, default=0.02)
    p.add_argument("--r_score", type=int, default=16)
    p.add_argument("--tau", type=float, default=0.5, help="straight-through softmax temperature")
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--lr", type=float, default=5e-5)
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


def hit_at_k(ranked, gold, k):
    return int(len(set(ranked[:k]) & set(gold)) > 0)


def all_gold_at_k(ranked, gold, k):
    return int(set(gold) <= set(ranked[:k]))


# ---------------------------------------------------------------------------------------------- rule-based splits
def _snap_down(x, allowed):
    fits = [a for a in allowed if a <= x]
    return max(fits) if fits else None


def allocate(policy, k, total, allowed, scores=None, temperature=0.1):
    allowed = sorted(set(int(a) for a in allowed))
    lo = allowed[0]
    if total < lo * k:
        raise ValueError(f"total budget {total} is below the minimum {lo} x {k} slots")
    if policy == "uniform":
        return [_snap_down(total // k, allowed)] * k
    if policy == "top_heavy":
        out, remaining = [], total
        for i in range(k):
            b = _snap_down(remaining - lo * (k - i - 1), allowed)
            out.append(b)
            remaining -= b
        return out
    if policy == "score":
        s = [float(x) for x in scores][:k]
        mx = max(s)
        w = [math.exp((x - mx) / temperature) for x in s]
        z = sum(w)
        out = [_snap_down(total * wi / z, allowed) or lo for wi in w]
        while sum(out) > total:
            j = max(range(k), key=lambda i: (out[i], i))
            out[j] = _snap_down(out[j] - 1, allowed) or lo
        upgraded = True
        while upgraded:
            upgraded = False
            for i in range(k):
                bigger = [a for a in allowed if a > out[i]]
                if bigger and sum(out) - out[i] + bigger[0] <= total:
                    out[i] = bigger[0]
                    upgraded = True
                    break
        return out
    raise ValueError(f"unknown policy {policy!r}")


# ---------------------------------------------------------------------------------------------- budget head
class BudgetHead(nn.Module):
    """Same architecture, initialisation and file format as nclara/budget.py (evaluate.py loads it unchanged)."""

    def __init__(self, hidden_size, lengths, k, proj=128, width=128):
        super().__init__()
        self.lengths = sorted(int(x) for x in lengths)
        self.k = k
        self.proj_q = nn.Linear(hidden_size, proj)
        self.proj_d = nn.Linear(hidden_size, proj)
        self.mlp = nn.Sequential(nn.Linear(3 * proj + 2 + k, width), nn.GELU(), nn.Linear(width, len(self.lengths)))
        nn.init.zeros_(self.mlp[-1].weight)
        nn.init.zeros_(self.mlp[-1].bias)
        self._cache = {}

    def forward(self, q_pool, d_pools, scores):
        n = d_pools.shape[0]
        q = self.proj_q(F.normalize(q_pool.float(), dim=-1)).unsqueeze(0).expand(n, -1)
        d = self.proj_d(F.normalize(d_pools.float(), dim=-1))
        s = scores.float()
        rank = torch.eye(self.k, device=d.device)[:n]
        extra = torch.cat([s[:, None], (s - s.max())[:, None], rank], dim=-1)
        return self.mlp(torch.cat([q, d, q * d, extra], dim=-1))

    def patterns(self, n, total, device):
        key = (n, total)
        if key not in self._cache:
            pats = [p for p in itertools.product(range(len(self.lengths)), repeat=n)
                    if sum(self.lengths[i] for i in p) == total]
            if not pats:
                raise ValueError(f"no split of {total} vectors over {n} documents uses lengths {self.lengths}")
            self._cache[key] = torch.tensor(pats, dtype=torch.long)
        return self._cache[key].to(device)

    def choose(self, logits, total, greedy=False):
        pats = self.patterns(logits.shape[0], total, logits.device)
        rows = torch.arange(logits.shape[0], device=logits.device)
        dist = torch.distributions.Categorical(logits=logits[rows, pats].sum(dim=1))
        j = dist.probs.argmax() if greedy else dist.sample()
        return [self.lengths[i] for i in pats[j].tolist()], dist.log_prob(j), dist.entropy()


def head_features(query_mem, cand_mems, chosen, scores, r, min_len):
    q_pool = query_mem[:r].mean(0).detach()
    d_pools = torch.stack([cand_mems[c][:min_len].mean(0) for c in chosen]).detach()
    return q_pool, d_pools, scores.detach()[chosen]


def save_head(head, path):
    torch.save({"state": head.state_dict(), "lengths": head.lengths, "k": head.k,
                "hidden_size": head.proj_q.in_features}, path)


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
    """The parts of the project's QwenCLaRa that E2E needs, built in the same order with the same names."""

    def __init__(self, base, tokenizer, meta, model_name, device):
        super().__init__()
        self.rescale_memory = bool(meta.get("rescale_memory", False))
        self.backbone, self.model_name = "qwen", model_name
        self.tokenizer = tokenizer
        self.max_mem, self.lora_r = meta["max_mem"], meta["lora_r"]
        self.max_doc_tokens = meta.get("max_doc_tokens", 256)
        self.max_query_tokens = meta.get("max_query_tokens", 64)
        self.max_target_tokens = meta.get("max_target_tokens", 96)
        self.device = device
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

    def copy_adapter(self, src, dst):
        params = dict(self._lora)
        copied = 0
        with torch.no_grad():
            for n, p in self._lora:
                if f".{src}." in n:
                    target = n.replace(f".{src}.", f".{dst}.")
                    if target in params:
                        params[target].copy_(p)
                        copied += 1
        return copied

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

    def load_state(self, in_dir):
        state = torch.load(os.path.join(in_dir, "lora_state.pt"), map_location=self.device, weights_only=True)
        own = dict(self._lora)
        missing = [n for n in own if n not in state]
        with torch.no_grad():
            for n, t in state.items():
                if n in own:
                    own[n].copy_(t.to(self.device))
            mem = torch.load(os.path.join(in_dir, "mem_embeddings.pt"), map_location=self.device, weights_only=True)
            self.mem_doc.copy_(mem["mem_doc"].to(self.device))
            self.mem_query.copy_(mem["mem_query"].to(self.device))
        if missing:
            raise SystemExit(f"{len(missing)} LoRA tensors missing from checkpoint {in_dir}")

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

    def compress(self, text, adapter="compressor", is_query=False):
        ids = self.ids(text, self.max_query_tokens if is_query else self.max_doc_tokens)
        tok = self.embed(ids)
        mem = (self.mem_query if is_query else self.mem_doc).unsqueeze(0)
        x = torch.cat([tok, mem], dim=1)
        self.use(adapter)
        h = self._decoder()(inputs_embeds=x, attention_mask=torch.ones(x.shape[:2], dtype=torch.long,
                                                                      device=self.device)).last_hidden_state[0]
        T = tok.shape[1]
        return h[T:], h[:T]

    @staticmethod
    def score(query_mem, cand_mems, r):
        q = F.normalize(query_mem[:r].flatten(), dim=0)
        C = torch.stack([F.normalize(c[:r].flatten(), dim=0) for c in cand_mems])
        return C @ q

    @staticmethod
    def st_topk(scores, k, tau=0.5):
        """Straight-through top-k without replacement. THE ONLY CHANGE vs the project: picked documents are masked
        with -inf (exactly removed) instead of log(1 - taken + 1e-9) ~ -20.7, which fails for small tau."""
        D = scores.shape[0]
        taken = torch.zeros(D, dtype=torch.bool, device=scores.device)
        hard = torch.zeros(k, D, device=scores.device)
        soft = []
        for j in range(k):
            logits = (scores / tau).masked_fill(taken, float("-inf"))
            p = F.softmax(logits, dim=0)
            soft.append(p)
            idx = int(torch.argmax(p.detach()))
            hard[j, idx] = 1.0
            taken = taken.clone()
            taken[idx] = True
        soft = torch.stack(soft)
        return hard + (soft - soft.detach())

    @staticmethod
    def gather_slots(Z, cand_mems, budgets):
        slots = []
        for j, b in enumerate(budgets):
            stack = torch.stack([c[:b] for c in cand_mems])
            slots.append(torch.einsum("d,dbh->bh", Z[j], stack))
        return slots

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


def load_from_checkpoint(ckpt_dir, device, tiny):
    meta = read_json(os.path.join(ckpt_dir, "meta.json"))
    if meta.get("backbone", "qwen") != "qwen":
        raise SystemExit("train_e2e_a3.py supports the Qwen (decoder-only) backbone only")
    if tiny:
        base, tok, model_name = build_tiny_qwen()
    else:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        model_name = meta.get("model_name") or os.environ.get("QWEN_MODEL") or MODEL_ID
        tok = AutoTokenizer.from_pretrained(model_name)
        base = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)
    model = NestedQwen(base, tok, meta, model_name, device)
    model.load_state(ckpt_dir)
    return model, meta


# ---------------------------------------------------------------------------------------------- training (= train_e2e.py)
def main(args):
    set_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ac = precision_context(args.amp, device)
    model, meta = load_from_checkpoint(os.path.join(args.run_dir, "scp"), device=device, tiny=args.tiny)
    allowed = meta["prefix_set"]
    r = min(args.r_score, model.max_mem)
    learned = args.train_alloc == "learned"
    if learned and meta["mode"] == "fixed":
        raise SystemExit("learned budgets need a nested compressor (a fixed one has a single valid length)")
    policies = ["uniform", "top_heavy"] if args.train_alloc == "mixed" else [args.train_alloc]
    if meta["mode"] == "fixed":
        policies = ["uniform"]
    if not learned:
        for pol in policies:
            allocate(pol, args.k, args.total_budget, allowed, scores=[0.0] * args.k)

    n = model.copy_adapter("compressor", "query_reasoner")
    with torch.no_grad():
        model.mem_query.copy_(model.mem_doc)
    model.set_trainable(["query_reasoner", "generator"], mem_query=True)
    params = model.trainable_parameters()
    groups = [{"params": params, "lr": args.lr}]
    head, baseline, totals = None, None, None
    if learned:
        head = BudgetHead(model.hidden_size, allowed, args.k).to(device)
        totals = [int(x) for x in args.train_totals.split(",") if x.strip()] if args.train_totals \
            else [args.total_budget]
        for t in totals:
            head.patterns(args.k, t, device)
        groups.append({"params": list(head.parameters()), "lr": args.budget_lr})
        min_len = min(allowed)
    opt = torch.optim.AdamW(groups)
    clip_params = params + (list(head.parameters()) if head is not None else [])

    records = read_json(os.path.join(args.data_dir, f"{args.dataset}_train.json"))
    records = [rec for rec in records if len(rec["paragraphs"]) >= args.k]
    model.model.eval()
    cache = {}
    with torch.no_grad(), ac():
        for rec in tqdm(records, desc="caching compressed passages", mininterval=30):
            for ptxt in rec["paragraphs"]:
                if ptxt not in cache:
                    cache[ptxt] = model.compress(ptxt, "compressor")[0].detach()
    before = model.lora_snapshot()
    print(f"[E2E a3, NaN-safe top-k] {len(records)} questions | {len(cache)} cached passages | copied {n} tensors "
          f"compressor->query_reasoner | k={args.k} | r={r} | tau={args.tau} | lr={args.lr} | " +
          (f"learned budgets, totals {totals}, lengths {allowed}, entropy {args.entropy_coef}" if learned
           else f"budget={args.total_budget} policies={policies}"))

    rng = random.Random(args.seed)
    log = {"args": vars(args), "epochs": []}
    model.model.train()
    t0 = time.time()
    for epoch in range(args.epochs):
        rng.shuffle(records)
        hits, full, losses, non_finite = 0, 0, [], 0
        gold_b, other_b, ents, top_share = [], [], [], []
        for rec in tqdm(records, desc=f"E2E epoch {epoch + 1}/{args.epochs}", mininterval=30):
            instr = E2E_INSTRUCTION.format(q=rec["question"])
            with ac():
                cands = [cache[ptxt] for ptxt in rec["paragraphs"]]
                q, _ = model.compress(rec["question"], "query_reasoner", is_query=True)
                scores = model.score(q, cands, r)
                Z = model.st_topk(scores, args.k, args.tau)
                chosen = Z.detach().argmax(dim=1).tolist()
                if not learned:
                    policy = rng.choice(policies)
                    budgets = allocate(policy, args.k, args.total_budget, allowed,
                                       scores=scores.detach()[chosen].tolist())
                    loss = model.gen_loss(instr, model.gather_slots(Z, cands, budgets), rec["answer"])
                    ntp = loss
                else:
                    logits = head(*head_features(q, cands, chosen, scores, r, min_len))
                    total = rng.choice(totals)
                    sample_losses, logps = [], []
                    for _ in range(args.budget_samples):
                        budgets, logp, ent = head.choose(logits, total)
                        sample_losses.append(model.gen_loss(instr, model.gather_slots(Z, cands, budgets),
                                                            rec["answer"]))
                        logps.append(logp)
                        for c, b in zip(chosen, budgets):
                            (gold_b if c in rec["gold_idx"] else other_b).append(b)
                        top_share.append(budgets[0] / total)
                    ntp = torch.stack(sample_losses).mean()
                    L = torch.stack([x.detach().float() for x in sample_losses])
                    if args.budget_samples > 1:
                        adv = (L.sum() - L) / (len(L) - 1) - L
                    else:
                        baseline = L.mean().item() if baseline is None else 0.9 * baseline + 0.1 * L.mean().item()
                        adv = baseline - L
                    policy_loss = -(adv * torch.stack(logps)).mean()
                    loss = ntp + policy_loss - args.entropy_coef * ent
                    ents.append(ent.item())
            if not torch.isfinite(loss):
                raise SystemExit(f"non-finite loss at epoch {epoch + 1}: stopping instead of training on NaN")
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(clip_params, 1.0)
            opt.step()
            losses.append(ntp.item())
            hits += hit_at_k(chosen, rec["gold_idx"], args.k)
            full += all_gold_at_k(chosen, rec["gold_idx"], args.k)
        ep = {"epoch": epoch + 1, "loss": sum(losses) / len(losses),
              "train_hit@k": 100 * hits / len(records), "train_all_gold@k": 100 * full / len(records)}
        if learned:
            mean = lambda v: sum(v) / len(v) if v else float("nan")
            ep.update({"split_entropy": mean(ents), "top1_share_of_budget": mean(top_share),
                       "avg_budget_gold_docs": mean(gold_b), "avg_budget_other_docs": mean(other_b)})
        log["epochs"].append(ep)
        print(f"  epoch {epoch + 1}: loss {ep['loss']:.3f} | train hit@{args.k} {ep['train_hit@k']:.1f}% | "
              f"all-gold@{args.k} {ep['train_all_gold@k']:.1f}%" +
              (f" | rank-1 share {ep['top1_share_of_budget']:.2f} | split entropy {ep['split_entropy']:.2f}"
               f" | budget gold {ep['avg_budget_gold_docs']:.1f} vs other {ep['avg_budget_other_docs']:.1f}"
               if learned else ""))

    log["minutes"] = (time.time() - t0) / 60
    log["delta_vs_start"] = model.delta_report(before)
    out = os.path.join(args.run_dir, "e2e")
    model.save(out, extra_meta={**{k: v for k, v in meta.items() if k not in model.meta()},
                                "stage": "e2e", "k": args.k, "total_budget": args.total_budget,
                                "train_alloc": args.train_alloc, "r_score": r, "tau": args.tau,
                                "train_totals": totals if learned else None,
                                "budget_samples": args.budget_samples if learned else None,
                                "entropy_coef": args.entropy_coef if learned else None,
                                "topk_mask": "-inf (train_e2e_a3.py)"})
    if learned:
        save_head(head, os.path.join(out, "budget_head.pt"))
    write_json(log, os.path.join(out, "train_log.json"))
    d = log["delta_vs_start"]
    print(f"  compressor changed {d['compressor']['changed']}/{d['compressor']['tensors']} (expect 0) | "
          f"query_reasoner {d['query_reasoner']['changed']}/{d['query_reasoner']['tensors']} | "
          f"generator {d['generator']['changed']}/{d['generator']['tensors']}")
    print(f"  saved -> {out}")


if __name__ == "__main__":
    main(build_parser().parse_args())
