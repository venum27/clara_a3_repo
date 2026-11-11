"""Assignment 3 -- extra metrics from saved predictions (no training, CPU only).

Reads every <runs_dir>/qwen/<dataset>/<run>/<results dir>/qa_predictions.json and breaks EM / F1 down by
  question type    from data/<dataset>_<eval>.json ("type": bridge / comparison / compositional / inference ...)
  answer type      yes/no answers vs everything else (entity, date, number ...)
  gold rank        where the first gold passage sits among the k documents the generator read
Seeds of the same run are pooled (all question-seed pairs), as in the report's larger evaluation.
The prediction used per run: learned@<B> if the run has a budget head, else uniform@<B>, else the single "pred"
(official CLaRa code). Standalone: imports nothing from this project.

    python3 analyze_metrics.py                          # 3,000-question set (results_big), B = 64
    python3 analyze_metrics.py --results results        # 300-question set, includes runs without results_big
"""
import argparse
import collections
import glob
import json
import math
import os
import re
import string

SHORT = {"clara_official_CR16": "official CLaRa", "r2_fixed_M16_e6": "our CLaRa (fixed-16)",
         "r2_nested_M32_all_e6": "nested, rule splits", "r2_nested_M32_all_e6__learned": "nested + budget head",
         "r3_nested_M32_all_e6_it": "nested + IT, rule splits",
         "r3_nested_M32_all_e6_it__learned": "nested + IT + budget head"}


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--runs_dir", default="runs")
    p.add_argument("--data_dir", default="data")
    p.add_argument("--datasets", default="hotpotqa,2wiki")
    p.add_argument("--results", default="results_big", help="results_big (3,000 questions) or results (300)")
    p.add_argument("--budget", type=int, default=64)
    p.add_argument("--runs", default="", help="comma-separated run names (without _s<seed>); default: all found")
    p.add_argument("--out", default=None, help="default: <runs_dir>/a3_metrics_<results>.md")
    return p


def normalize_answer(s):
    s = str(s).lower()
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    s = "".join(ch for ch in s if ch not in set(string.punctuation))
    return " ".join(s.split())


def exact_match(pred, gold):
    return float(normalize_answer(pred) == normalize_answer(gold))


def f1_score(pred, gold):
    p, g = normalize_answer(pred).split(), normalize_answer(gold).split()
    same = sum((collections.Counter(p) & collections.Counter(g)).values())
    if same == 0:
        return 0.0
    precision, recall = same / len(p), same / len(g)
    return 2 * precision * recall / (precision + recall)


def gold_rank(topk, gold_idx):
    for pos, i in enumerate(topk):
        if i in gold_idx:
            return "rank 1" if pos == 0 else ("rank 2" if pos == 1 else "rank 3+")
    return "not retrieved"


def mean_ci(vals):
    n = len(vals)
    if n == 0:
        return float("nan"), float("nan")
    m = sum(vals) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1)) if n > 1 else 0.0
    return 100 * m, 100 * 1.96 * sd / math.sqrt(n)


def load_runs(args, ds):
    """{run name: [prediction rows over all seeds]} with question type, answer type and gold rank attached."""
    eval_name = "evalbig" if args.results == "results_big" else "eval"
    meta = {}
    for name in (f"{ds}_{eval_name}.json", f"{ds}_eval.json", f"{ds}_evalbig.json"):
        path = os.path.join(args.data_dir, name)
        if os.path.exists(path):
            with open(path) as f:
                for rec in json.load(f):
                    meta.setdefault(rec["id"], rec.get("type", "unknown"))
    wanted = [r for r in args.runs.split(",") if r]
    runs = collections.defaultdict(list)
    seeds = collections.defaultdict(list)
    for path in sorted(glob.glob(os.path.join(args.runs_dir, "qwen", ds, "*", args.results, "qa_predictions.json"))):
        run_seed = path.split(os.sep)[-3]
        name, seed = re.match(r"(.*)_s(\d+)$", run_seed).groups()
        if wanted and name not in wanted:
            continue
        with open(path) as f:
            rows = json.load(f)
        keys = rows[0].get("preds", {})
        key = next((k for k in (f"learned@{args.budget}", f"uniform@{args.budget}") if k in keys), None)
        if key is None and "pred" not in rows[0]:
            continue
        for r in rows:
            pred = r["preds"][key] if key else r["pred"]
            ans = normalize_answer(r["gold"])
            runs[name].append({"type": meta.get(r["id"], "unknown"),
                               "answer": "yes/no" if ans in ("yes", "no") else "other",
                               "rank": r.get("gold_rank") or gold_rank(r["topk"], r["gold_idx"]),
                               "em": exact_match(pred, r["gold"]), "f1": f1_score(pred, r["gold"])})
        seeds[name].append(f"s{seed}" + (f" ({key})" if key else ""))
    return runs, seeds


def table(title, runs, field, order=None):
    names = list(runs)
    groups = order or sorted({row[field] for rows in runs.values() for row in rows})
    head = "| " + title + " | " + " | ".join(SHORT.get(n, n) for n in names) + " |"
    lines = [head, "|---" * (len(names) + 1) + "|"]
    for g in groups:
        cells = []
        for n in names:
            sub = [row for row in runs[n] if row[field] == g]
            if not sub:
                cells.append("-")
                continue
            f1, ci = mean_ci([row["f1"] for row in sub])
            share = 100 * len(sub) / len(runs[n])
            cells.append(f"{f1:.1f} ±{ci:.1f} ({share:.0f}%)")
        lines.append(f"| {g} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main(args):
    out = [f"# Extra metrics ({args.results}, {args.budget} memory vectors per question)\n",
           "Cells: F1 (%) ± 95% half-interval, (share of that run's question-seed pairs in the group).\n"]
    for ds in args.datasets.split(","):
        runs, seeds = load_runs(args, ds)
        if not runs:
            out.append(f"## {ds}\n\nno {args.results}/qa_predictions.json found\n")
            continue
        out.append(f"## {ds}\n")
        out.append("Runs: " + "; ".join(f"{SHORT.get(n, n)} = {n} [{', '.join(seeds[n])}]" for n in runs) + "\n")
        overall = ["| | " + " | ".join(SHORT.get(n, n) for n in runs) + " |", "|---" * (len(runs) + 1) + "|"]
        for metric in ("em", "f1"):
            overall.append(f"| {metric.upper()} | " + " | ".join(
                "{:.1f} ±{:.1f}".format(*mean_ci([row[metric] for row in runs[n]])) for n in runs) + " |")
        out += [overall_text for overall_text in ["\n".join(overall)]]
        out.append("\n" + table("Question type", runs, "type") + "\n")
        out.append(table("Answer type", runs, "answer", ["yes/no", "other"]) + "\n")
        out.append(table("First gold passage", runs, "rank", ["rank 1", "rank 2", "rank 3+", "not retrieved"]) + "\n")
    text = "\n".join(out)
    print(text)
    path = args.out or os.path.join(args.runs_dir, f"a3_metrics_{args.results}.md")
    with open(path, "w") as f:
        f.write(text + "\n")
    print(f"saved -> {path}")


if __name__ == "__main__":
    main(build_parser().parse_args())
