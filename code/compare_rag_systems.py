"""Assignment 3 (deployment) -- compare our compressed-memory RAG with a standard text RAG on more metrics.

Systems (all Qwen2.5-0.5B-Instruct, the same 300 held-out questions per dataset, 4 retrieved passages):
  Standard text RAG   the base model with no training, reading BM25's top-4 passages as raw text (~500 tokens).
                      Its answers were saved by A2's evaluate.py (preds["raw_bm25"]); they are identical in every run.
  Official CLaRa      the authors' code trained on our data, 16 memory vectors per passage (64 in total)
  Our CLaRa           our re-implementation, fixed-16 (64 vectors)
  A2 nested + head    nested memory + learned budget head, learned split of 64 vectors (3 seeds)
  A3 tuned generator  the same after instruction tuning of the generator only (3 seeds; shown once the runs exist)
Metrics, per question then averaged (seeds of one system are averaged per question first):
  EM, F1        the SQuAD answer metrics used in A1-A3
  ROUGE-1/2/L   F-measures, computed exactly like the rouge-score package (lowercase, non-alphanumerics removed,
                no stemming); ROUGE-1 is close to F1 by construction, ROUGE-2 and ROUGE-L add word order
  Containment   share of answers that contain the normalised gold answer (lenient: long answers are not penalised)
Differences against the text RAG are paired over the same questions, with bootstrap 95% intervals.
Standalone: imports nothing from this project.

    python3 compare_rag_systems.py                          # -> runs/a3_rag_comparison.md
    python3 compare_rag_systems.py --runs_dir results/runs  # on the A2 GitHub repo's saved results
"""
import argparse
import collections
import json
import os
import random
import re
import string

SYSTEMS = [  # (label, run name, prediction key)
    ("Standard text RAG (BM25 top-4 raw text, untrained)", "r2_nested_M32_all_e6__learned", "raw_bm25"),
    ("Official CLaRa code (16 vectors x 4)", "clara_official_CR16", "pred"),
    ("Our CLaRa re-implementation (fixed-16)", "r2_fixed_M16_e6", "uniform@64"),
    ("A2: nested memory + budget head", "r2_nested_M32_all_e6__learned", "learned@64"),
    ("A3: + instruction tuning (generator only)", "r3_nested_M32_all_e6_itgen__learned", "learned@64"),
]
BASELINE = 0
METRICS = ["EM", "F1", "ROUGE-1", "ROUGE-2", "ROUGE-L", "Containment"]


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--runs_dir", default="runs")
    p.add_argument("--datasets", default="hotpotqa,2wiki")
    p.add_argument("--seeds", default="42,43,44")
    p.add_argument("--n_boot", type=int, default=2000)
    p.add_argument("--out", default=None, help="default: <runs_dir>/a3_rag_comparison.md")
    return p


# ---------------------------------------------------------------------------------------------- answer metrics
def normalize_answer(s):
    s = str(s).lower()
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    s = "".join(ch for ch in s if ch not in set(string.punctuation))
    return " ".join(s.split())


def squad_exact_match(pred, gold):
    return float(normalize_answer(pred) == normalize_answer(gold))


def squad_f1(pred, gold):
    p, g = normalize_answer(pred).split(), normalize_answer(gold).split()
    same = sum((collections.Counter(p) & collections.Counter(g)).values())
    if same == 0:
        return 0.0
    precision, recall = same / len(p), same / len(g)
    return 2 * precision * recall / (precision + recall)


def rouge_tokens(text):
    """Tokenisation of the rouge-score package without stemming: lowercase, keep runs of [a-z0-9]."""
    return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).split()


def f_measure(overlap, n_pred, n_ref):
    precision = overlap / max(n_pred, 1)
    recall = overlap / max(n_ref, 1)
    return 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0


def rouge_n(pred_tokens, ref_tokens, n):
    grams = lambda t: collections.Counter(tuple(t[i:i + n]) for i in range(len(t) - n + 1))
    p, r = grams(pred_tokens), grams(ref_tokens)
    return f_measure(sum((p & r).values()), sum(p.values()), sum(r.values()))


def longest_common_subsequence(a, b):
    previous = [0] * (len(b) + 1)
    for x in a:
        current = [0]
        for j, y in enumerate(b):
            current.append(previous[j] + 1 if x == y else max(previous[j + 1], current[j]))
        previous = current
    return previous[-1]


def rouge_l(pred_tokens, ref_tokens):
    if not pred_tokens or not ref_tokens:
        return 0.0
    return f_measure(longest_common_subsequence(pred_tokens, ref_tokens), len(pred_tokens), len(ref_tokens))


def contains_gold(pred, gold):
    g = normalize_answer(gold)
    return float(bool(g) and f" {g} " in f" {normalize_answer(pred)} ")


def score_answer(pred, gold):
    p, g = rouge_tokens(pred), rouge_tokens(gold)
    return {"EM": squad_exact_match(pred, gold), "F1": squad_f1(pred, gold), "ROUGE-1": rouge_n(p, g, 1),
            "ROUGE-2": rouge_n(p, g, 2), "ROUGE-L": rouge_l(p, g), "Containment": contains_gold(pred, gold),
            "words": len(p)}


# ---------------------------------------------------------------------------------------------- loading
def load_system(runs_dir, ds, run, key, seeds):
    """{question id: per-question scores averaged over the seeds that exist}, number of seeds, context note."""
    per_question, n_seeds, context = collections.defaultdict(list), 0, None
    for s in seeds:
        path = os.path.join(runs_dir, "qwen", ds, f"{run}_s{s}", "results", "qa_predictions.json")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            rows = json.load(f)
        if key != "pred" and key not in rows[0].get("preds", {}):
            continue
        n_seeds += 1
        for r in rows:
            pred = r["pred"] if key == "pred" else r["preds"][key]
            per_question[r["id"]].append(score_answer(pred, r["gold"]))
        if key == "raw_bm25":
            context = f"{sum(r.get('raw_context_tokens', 0) for r in rows) / len(rows):.0f} text tokens"
            break                                          # untrained base model: identical in every run
    averaged = {q: {m: sum(s[m] for s in v) / len(v) for m in v[0]} for q, v in per_question.items()}
    return averaged, n_seeds, context or "64 memory vectors"


def bootstrap_interval(values, n_boot, rng):
    n = len(values)
    means = sorted(sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(n_boot))
    return means[int(0.025 * n_boot)], means[int(0.975 * n_boot) - 1]


# ---------------------------------------------------------------------------------------------- main
def main(args):
    seeds = [s.strip() for s in args.seeds.split(",") if s.strip()]
    rng = random.Random(0)
    lines = ["# Compressed-memory RAG vs standard text RAG (Qwen2.5-0.5B, 300 questions per dataset)\n",
             "Scores in %. Multi-seed systems are averaged per question over their seeds. Differences are paired "
             "against the standard text RAG over the same questions, with bootstrap 95% intervals. ROUGE as in the "
             "rouge-score package (F-measure, no stemming).\n"]
    for ds in args.datasets.split(","):
        loaded = [(label, *load_system(args.runs_dir, ds, run, key, seeds)) for label, run, key in SYSTEMS]
        loaded = [x for x in loaded if x[2] > 0]
        if not loaded or loaded[0][0] != SYSTEMS[BASELINE][0]:
            lines.append(f"## {ds}\n\nthe text-RAG answers (preds['raw_bm25']) were not found\n")
            continue
        base = loaded[0][1]
        lines += [f"## {ds}\n", "| System | seeds | Input per question | " + " | ".join(METRICS) + " | answer words |",
                  "|---" * (len(METRICS) + 4) + "|"]
        for label, scores, n, context in loaded:
            ids = sorted(scores)
            cells = [f"{100 * sum(scores[i][m] for i in ids) / len(ids):.1f}" for m in METRICS]
            words = sum(scores[i]["words"] for i in ids) / len(ids)
            lines.append(f"| {label} | {n} | {context} | " + " | ".join(cells) + f" | {words:.1f} |")
        lines += ["", "Difference against the standard text RAG (paired, 95% interval):\n",
                  "| System | F1 | ROUGE-L | EM |", "|---|---|---|---|"]
        for label, scores, n, context in loaded[1:]:
            ids = sorted(set(scores) & set(base))
            cells = []
            for m in ("F1", "ROUGE-L", "EM"):
                d = [100 * (scores[i][m] - base[i][m]) for i in ids]
                lo, hi = bootstrap_interval(d, args.n_boot, rng)
                cells.append(f"{sum(d) / len(d):+.1f} [{lo:+.1f}, {hi:+.1f}]")
            lines.append(f"| {label} | " + " | ".join(cells) + " |")
        lines.append("")
    text = "\n".join(lines)
    print(text)
    path = args.out or os.path.join(args.runs_dir, "a3_rag_comparison.md")
    with open(path, "w") as f:
        f.write(text + "\n")
    print(f"saved -> {path}")


if __name__ == "__main__":
    main(build_parser().parse_args())
