"""Assignment 3 -- table for the E2E-only ablations (scripts/14_e2e_ablations.sh).

Every ablation run changes one E2E setting of an Assignment 2 run and is scored on the same 300 evaluation
questions, so each row is compared with its baseline question by question (paired bootstrap, 95% interval).
Reads only results/qa_predictions.json. Standalone: imports nothing from this project.

    python3 summarize_ablations.py --dataset 2wiki                          # 300 questions
    python3 summarize_ablations.py --dataset 2wiki --results results_big    # 3,000 questions
"""
import argparse
import collections
import json
import os
import random
import re
import string

GROUPS = [
    {"title": "Why our pipeline beats the official code: our CLaRa re-implementation (fixed-16) with official choices",
     "baseline": ("r2_fixed_M16_e6", "ours: E2E lr 5e-5, ST temperature 0.5"), "key": "uniform",
     "rows": [("a3_fixed16_lr5e-6", "E2E lr 5e-6 (official)"),
              ("a3_fixed16_tau0.02", "ST temperature 0.02 (official)"),
              ("a3_fixed16_lr5e-6_tau0.02", "both (official E2E settings)"),
              ("a3_fixed16_allqa", "SCP target: all QA pairs in one target (official)")],
     "reference": ("clara_official_CR16", "official CLaRa code (reference)")},
    {"title": "Hyperparameters of our method (nested memory + learned budget head)",
     "baseline": ("r2_nested_M32_all_e6__learned", "ours: entropy bonus 0.02, ST temperature 0.5"), "key": "learned",
     "rows": [("a3_head_ent0", "entropy bonus beta = 0"), ("a3_head_ent0.1", "entropy bonus beta = 0.1"),
              ("a3_head_tau0.1", "ST temperature 0.1"), ("a3_head_tau0.02", "ST temperature 0.02")]},
]


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--runs_dir", default="runs")
    p.add_argument("--dataset", default="2wiki")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--budget", type=int, default=64)
    p.add_argument("--results", default="results", help="results (300 questions) or results_big (3,000 questions)")
    p.add_argument("--out", default=None, help="default: <runs_dir>/a3_ablations_<dataset>[_big].md")
    return p


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


def load(args, name, key):
    """{question id: (F1, EM, hit@1, F1 at uniform)} for one run, or None if it has no predictions yet."""
    path = os.path.join(args.runs_dir, "qwen", args.dataset, f"{name}_s{args.seed}", args.results, "qa_predictions.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        rows = json.load(f)
    out = {}
    for r in rows:
        preds = r.get("preds")
        pred = preds.get(f"{key}@{args.budget}", preds.get(f"uniform@{args.budget}")) if preds else r["pred"]
        uni = preds.get(f"uniform@{args.budget}", pred) if preds else r["pred"]
        out[r["id"]] = (f1_score(pred, r["gold"]), float(normalize_answer(pred) == normalize_answer(r["gold"])),
                        float(r["topk"][0] in r["gold_idx"]), f1_score(uni, r["gold"]))
    return out


def paired(a, b, n_boot=2000):
    ids = sorted(set(a) & set(b))
    d = [100 * (a[i][0] - b[i][0]) for i in ids]
    rng = random.Random(0)
    means = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(n_boot))
    return sum(d) / len(d), means[int(0.025 * n_boot)], means[int(0.975 * n_boot) - 1]


def mean(res, j):
    return 100 * sum(v[j] for v in res.values()) / len(res)


def main(args):
    n_q = "3,000" if args.results == "results_big" else "300"
    lines = [f"# E2E-only ablations: {args.dataset}, seed {args.seed}, {args.budget} memory vectors, "
             f"{n_q} evaluation questions ({args.results})\n",
             "One seed: differences smaller than about 2 F1 are within the seed-to-seed spread measured in "
             "Assignment 2. Difference = run minus baseline, paired over the same questions, with 95% interval.\n"]
    for g in GROUPS:
        base_name, base_label = g["baseline"]
        base = load(args, base_name, g["key"])
        lines += [f"## {g['title']}\n", "| Setting | Run | F1 | EM | hit@1 | learned - uniform | F1 difference |",
                  "|---|---|---|---|---|---|---|"]
        rows = [(base_name, base_label)] + g["rows"] + ([g["reference"]] if "reference" in g else [])
        for name, label in rows:
            res = load(args, name, g["key"])
            if res is None:
                lines.append(f"| {label} | {name} | not run yet | | | | |")
                continue
            lu = f"{mean(res, 0) - mean(res, 3):+.1f}" if g["key"] == "learned" else "-"
            if name == base_name or base is None:
                diff = "baseline" if name == base_name else "-"
            else:
                m, lo, hi = paired(res, base)
                diff = f"{m:+.1f} [{lo:+.1f}, {hi:+.1f}]"
            lines.append(f"| {label} | {name} | {mean(res, 0):.1f} | {mean(res, 1):.1f} | {mean(res, 2):.1f} | "
                         f"{lu} | {diff} |")
        lines.append("")
    text = "\n".join(lines)
    print(text)
    suffix = "_big" if args.results == "results_big" else ""
    path = args.out or os.path.join(args.runs_dir, f"a3_ablations_{args.dataset}{suffix}.md")
    with open(path, "w") as f:
        f.write(text + "\n")
    print(f"saved -> {path}")


if __name__ == "__main__":
    main(build_parser().parse_args())
