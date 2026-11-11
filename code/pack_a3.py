"""Pack the Assignment 3 code and results into one zip to share with the team (no model weights).

Run it from the project folder on the server; it writes ~/a3_share.zip (re-run any time to refresh it with new results).
Included:
  code      the A3 files (train_it_nested.py, train_e2e_a3.py, train_scp_allqa.py, summarize_ablations.py,
            analyze_metrics.py, compare_it.py, demo_app.py) and scripts 13-17
  tables    runs/*.md  (a3_it_comparison.md, a3_ablations_2wiki.md, a3_ablations_2wiki_big.md, results_summary.md, ...)
  runs      every A3 run folder (r3_* and a3_*): results (eval.json, qa_predictions.json, diagnose.json, summary.md),
            results_big, and scp/ + e2e/ meta.json and train_log.json -- but no *.pt weight files
  logs      logs/it_*.log, logs/a3_*.log
A CONTENTS.txt inside the zip says where everything is. The A2 runs used as baselines are already in the A2 GitHub repo
(results/runs). Standalone: imports nothing from this project.

    python3 pack_a3.py
"""
import argparse
import glob
import os
import zipfile

CODE = ["train_it_nested.py", "train_e2e_a3.py", "train_scp_allqa.py", "summarize_ablations.py", "analyze_metrics.py",
        "compare_it.py", "demo_app.py", "pack_a3.py", "scripts/13_it_nested.sh", "scripts/14_e2e_ablations.sh",
        "scripts/15_scp_allqa.sh", "scripts/16_big_eval_a3.sh", "scripts/17_it_gen_only.sh"]
SKIP_EXT = (".pt", ".bin", ".safetensors", ".pth", ".ckpt")

CONTENTS = """Assignment 3 -- code and results (model weights not included)

code/        the A3 code: new standalone files + scripts 13-17 (scripts/)
tables/      summary tables
   a3_it_comparison.md        instruction tuning vs A2 (answers, retrieval, memory diagnostic, compressor-only QA)
   a3_ablations_2wiki.md      ablations, 300 questions (official choices on fixed-16; budget-head hyperparameters)
   a3_ablations_2wiki_big.md  the same ablations on 3,000 questions (if finished)
   results_summary.md, diagnose_summary.md   all runs (A2 + A3)
runs/qwen/<dataset>/<run>/    one folder per A3 run
   results/   eval.json, qa_predictions.json (one answer per question), diagnose.json, summary.md
   results_big/   the same on 3,000 questions (ablation runs)
   scp/, e2e/     meta.json (settings) and train_log.json (losses per epoch, budget-head statistics)
   r3_nested_M32_all_e6_it[__learned]_s<seed>      instruction tuning (compressor + generator tuned)
   r3_nested_M32_all_e6_itgen[__learned]_s42       instruction tuning, generator only (compressor frozen)
   a3_fixed16_*_s42   our CLaRa re-implementation with the official choices (lr, temperature, SCP target)
   a3_head_*_s42      budget-head hyperparameters (entropy bonus, temperature)
logs/        training and evaluation logs
A2 baselines (r2_*, clara_official_CR16) are in the A2 repo: https://github.com/venum27/clara_a2_repo (results/runs)
"""


def main(args):
    files = []
    for f in CODE:
        if os.path.exists(f):
            files.append((f, os.path.join("code", f)))
    for f in sorted(glob.glob(os.path.join(args.runs_dir, "*.md"))):
        files.append((f, os.path.join("tables", os.path.basename(f))))
    run_dirs = sorted(glob.glob(os.path.join(args.runs_dir, "qwen", "*", "r3_*")) +
                      glob.glob(os.path.join(args.runs_dir, "qwen", "*", "a3_*")))
    for d in run_dirs:
        for root, _, names in os.walk(d):
            for n in names:
                if n.endswith(SKIP_EXT):
                    continue
                p = os.path.join(root, n)
                files.append((p, os.path.join("runs", os.path.relpath(p, args.runs_dir))))
    for f in sorted(glob.glob("logs/it_*.log") + glob.glob("logs/a3_*.log")):
        files.append((f, f))
    out = os.path.expanduser(args.out)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("CONTENTS.txt", CONTENTS)
        for src, arc in files:
            z.write(src, os.path.join("a3_share", arc))
    size = os.path.getsize(out) / 1e6
    print(f"{len(files)} files from {len(run_dirs)} runs -> {out} ({size:.1f} MB)")
    print("on your laptop:  scp <user>@<server>:a3_share.zip .")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--runs_dir", default="runs")
    p.add_argument("--out", default="~/a3_share.zip")
    main(p.parse_args())
