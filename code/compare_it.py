"""Assignment 3 -- instruction tuning vs Assignment 2, from the saved result files (no GPU, a few seconds).

Compares, per dataset, the four Qwen runs of the final configuration:
  A2, rule splits           r2_nested_M32_all_e6            A2, budget head           r2_nested_M32_all_e6__learned
  A3 tuned, rule splits     r3_nested_M32_all_e6_it         A3 tuned, budget head     r3_nested_M32_all_e6_it__learned
(plus, once they exist, the generator-only runs r3_nested_M32_all_e6_itgen[__learned]) and prints four tables: end-to-end answers (F1 at 32/64/128 vectors, EM at 64, learned - uniform), retrieval
(hit@1), the memory diagnostic (no / wrong / gold memory and the memory gain) and the compressor-only F1 per prefix
length. Several seeds are averaged when given (--seeds 42,43,44); missing runs show "-".
Standalone: imports nothing from this project.

    python3 compare_it.py                     # seed 42, both datasets -> runs/a3_it_comparison.md
    python3 compare_it.py --seeds 42,43,44    # mean over the seeds that have finished
"""
import argparse
import json
import os

RUNS = [("A2, rule splits", "r2_nested_M32_all_e6"), ("A2, budget head", "r2_nested_M32_all_e6__learned"),
        ("A3 tuned, rule splits", "r3_nested_M32_all_e6_it"),
        ("A3 tuned, budget head", "r3_nested_M32_all_e6_it__learned"),
        ("A3 tuned generator only, rule splits", "r3_nested_M32_all_e6_itgen"),
        ("A3 tuned generator only, budget head", "r3_nested_M32_all_e6_itgen__learned")]
OPTIONAL = {"r3_nested_M32_all_e6_itgen", "r3_nested_M32_all_e6_itgen__learned"}   # shown once they exist


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--runs_dir", default="runs")
    p.add_argument("--datasets", default="hotpotqa,2wiki")
    p.add_argument("--seeds", default="42")
    p.add_argument("--out", default=None, help="default: <runs_dir>/a3_it_comparison.md")
    return p


def load(runs_dir, ds, name, seeds):
    """List of (eval.json, diagnose.json or None) for every seed of this run that has finished."""
    out = []
    for s in seeds:
        d = os.path.join(runs_dir, "qwen", ds, f"{name}_s{s}", "results")
        if os.path.exists(os.path.join(d, "eval.json")):
            with open(os.path.join(d, "eval.json")) as f:
                ev = json.load(f)
            dg = None
            if os.path.exists(os.path.join(d, "diagnose.json")):
                with open(os.path.join(d, "diagnose.json")) as f:
                    dg = json.load(f)
            out.append((ev, dg))
    return out


def avg(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def fmt(v, sign=False):
    if v is None:
        return "-"
    return f"{v:+.1f}" if sign else f"{v:.1f}"


def qa(ev, key, metric="F1"):
    r = ev.get("qa", {}).get("results", {}).get(key)
    return r[metric]["mean"] if r else None


def main(args):
    seeds = [s.strip() for s in args.seeds.split(",") if s.strip()]
    lines = [f"# Instruction tuning (A3) vs Assignment 2, seed(s) {', '.join(seeds)}\n",
             "Same nested compressor family, Qwen2.5-0.5B, 300 evaluation questions per dataset. "
             "With one seed, differences under about 2 F1 are within the seed-to-seed spread measured in A2.\n"]
    for ds in args.datasets.split(","):
        data = {label: load(args.runs_dir, ds, name, seeds) for label, name in RUNS}
        shown = [(label, name) for label, name in RUNS if name not in OPTIONAL or data[label]]
        lines.append(f"## {ds}\n")

        lines += ["**End-to-end answers** (F1 at a total of 32 / 64 / 128 memory vectors; budget-head runs use their "
                  "learned split)\n",
                  "| Run | seeds | F1 @32 | F1 @64 | F1 @128 | EM @64 | learned - uniform @64 |",
                  "|---|---|---|---|---|---|---|"]
        for label, _ in shown:
            evs = [ev for ev, _ in data[label]]
            pol = "learned" if "budget head" in label else "uniform"
            f = {b: avg([qa(ev, f"{pol}@{b}") or qa(ev, f"uniform@{b}") for ev in evs]) for b in (32, 64, 128)}
            em = avg([qa(ev, f"{pol}@64", "EM") or qa(ev, "uniform@64", "EM") for ev in evs])
            lu = avg([(qa(ev, "learned@64") - qa(ev, "uniform@64")) for ev in evs
                      if qa(ev, "learned@64") is not None and qa(ev, "uniform@64") is not None])
            lines.append(f"| {label} | {len(evs)} | {fmt(f[32])} | {fmt(f[64])} | {fmt(f[128])} | {fmt(em)} | "
                         f"{fmt(lu, True) if 'budget head' in label else '-'} |")

        lines += ["\n**Retrieval** (%; after E2E = the trained query reasoner; before E2E = the copy of the compressor it "
                  "starts from, which shows whether the compressor's memories still support retrieval)\n",
                  "| Run | hit@1 | hit@2 | all-gold@2 | hit@1 before E2E |", "|---|---|---|---|---|"]
        for label, _ in shown:
            evs = [ev for ev, _ in data[label]]
            r = [ev.get("retrieval", {}).get("query reasoner (after E2E)") for ev in evs]
            r0 = [ev.get("retrieval", {}).get("query reasoner (before E2E)") for ev in evs]
            g = lambda k: avg([x[k]["mean"] for x in r if x and k in x])
            b = avg([x["hit@1"]["mean"] for x in r0 if x and "hit@1" in x])
            lines.append(f"| {label} | {fmt(g('hit@1'))} | {fmt(g('hit@2'))} | {fmt(g('all_gold@2'))} | {fmt(b)} |")

        lines += ["\n**Memory diagnostic** (F1 answering with: no memory / another question's memory / gold passages "
                  "cut to 4 vectors / gold passages complete; gain = gold complete - no memory)\n",
                  "| Run | no memory | wrong memory | gold (4) | gold (all) | memory gain |", "|---|---|---|---|---|---|"]
        for label, _ in shown:
            dgs = [dg for _, dg in data[label] if dg]
            g = lambda k: avg([dg[k]["F1"]["mean"] for dg in dgs if k in dg])
            none, allg = g("no memory"), g("gold memory (all)")
            gain = allg - none if none is not None and allg is not None else None
            lines.append(f"| {label} | {fmt(none)} | {fmt(g('wrong memory (all)'))} | {fmt(g('gold memory (4)'))} | "
                         f"{fmt(allg)} | {fmt(gain, True)} |")

        lines += ["\n**Compressor-only QA** (F1 on held-out synthetic questions, first m memory vectors; shows "
                  "whether nesting survives instruction tuning)\n",
                  "| Run | m=4 | m=8 | m=16 | m=32 |", "|---|---|---|---|---|"]
        for label, _ in shown:
            evs = [ev for ev, _ in data[label]]
            c = lambda m: avg([ev["scp_curve"][m]["F1"]["mean"] for ev in evs if m in ev.get("scp_curve", {})])
            lines.append(f"| {label} | {fmt(c('4'))} | {fmt(c('8'))} | {fmt(c('16'))} | {fmt(c('32'))} |")
        lines.append("")

    text = "\n".join(lines)
    print(text)
    path = args.out or os.path.join(args.runs_dir, "a3_it_comparison.md")
    with open(path, "w") as f:
        f.write(text + "\n")
    print(f"saved -> {path}")


if __name__ == "__main__":
    main(build_parser().parse_args())
