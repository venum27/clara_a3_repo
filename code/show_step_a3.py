"""Assignment 3 -- print the saved evidence of one pipeline step, for the execution screenshots in the report.

Reads only the A3 logs (logs/) and result tables (runs/); progress bars and library warnings are left out, so each
step fits on one screen. Nothing is run or changed. Standalone: imports nothing from this project.

    python3 show_step_a3.py          # list the steps
    python3 show_step_a3.py 2        # print step 2
"""
import argparse
import glob
import importlib
import os
import platform
import re

STEPS = {
    1: "environment and A3 files",
    2: "instruction tuning (compressor + generator): training logs",
    3: "instruction tuning, generator only (compressor frozen): training logs",
    4: "E2E ablations: training logs (official choices on fixed-16, budget-head hyperparameters)",
    5: "official SCP target (all QA pairs in one target): training log",
    6: "ablation table, 300 evaluation questions",
    7: "ablation table, 3,000 evaluation questions",
    8: "instruction tuning vs A2: answers and retrieval (3 seeds)",
    9: "instruction tuning vs A2: memory diagnostic and compressor-only QA (3 seeds)",
    10: "all A3 runs and the outputs each one has",
}
A3_FILES = ["train_it_nested.py", "train_e2e_a3.py", "train_scp_allqa.py", "summarize_ablations.py",
            "analyze_metrics.py", "compare_it.py", "demo_app.py", "pack_a3.py", "show_step_a3.py",
            "scripts/13_it_nested.sh", "scripts/14_e2e_ablations.sh", "scripts/15_scp_allqa.sh",
            "scripts/16_big_eval_a3.sh", "scripts/17_it_gen_only.sh"]
# Lines worth showing from the training logs; everything else (progress bars, warnings, file copies) is dropped.
EVIDENCE = re.compile(r"^(== (?!evaluate|memory diagnostic)|\[IT\]|\[E2E|\[SCP|  all-QA targets|"
                      r"  epoch \d+: CE by prefix|  epoch 3: loss|  changed vs SCP|  compressor changed|"
                      r"  adapter changes|  saved -> \S+/scp\b)")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("step", nargs="?", type=int, help="step number (omit to list the steps)")
    p.add_argument("--runs_dir", default="runs")
    p.add_argument("--logs_dir", default="logs")
    p.add_argument("--datasets", default="hotpotqa,2wiki", help="datasets for the instruction-tuning steps")
    p.add_argument("--ablation_dataset", default="2wiki")
    p.add_argument("--width", type=int, default=170, help="cut longer lines at this many characters")
    return p


def print_header(step):
    bar = "=" * 100
    print(f"{bar}\nStep {step}: {STEPS[step]}\n{bar}")


def final_text_of_each_line(path):
    """Log lines as they finally appeared on screen (a progress bar rewrites its line with carriage returns)."""
    with open(path, errors="replace") as f:
        return [line.rstrip("\n").split("\r")[-1] for line in f]


def print_log_evidence(path, width):
    if not os.path.exists(path):
        print(f"-- {path}: not found")
        return
    lines = final_text_of_each_line(path)
    restarts = sum("OutOfMemoryError" in line for line in lines)
    print(f"-- {path}")
    for line in lines:
        if EVIDENCE.match(line):
            print(line[:width])
    if restarts:
        print(f"   (note: {restarts} job(s) in this log stopped with a CUDA out-of-memory error on the shared GPU "
              f"and were restarted; finished steps were skipped on restart)")
    print()


def print_file(path, width, keep=None):
    if not os.path.exists(path):
        print(f"-- {path}: not found (has this step finished?)")
        return
    print(f"-- {path}")
    with open(path) as f:
        lines = f.read().splitlines()
    section_kept = True
    for line in lines:
        if keep is not None:
            if line.startswith("**"):
                section_kept = any(k in line for k in keep)
            elif line.startswith("## ") or line.startswith("# "):
                section_kept = True
            if not section_kept:
                continue
        print(line[:width])
    print()


def show_environment(args):
    print(f"python {platform.python_version()} | {platform.platform()}")
    for module in ("torch", "transformers", "peft"):
        try:
            print(f"{module:13s} {importlib.import_module(module).__version__}")
        except ImportError:
            print(f"{module:13s} not installed")
    try:
        import torch
        for i in range(torch.cuda.device_count()):
            p = torch.cuda.get_device_properties(i)
            print(f"GPU {i}: {p.name}, {p.total_memory / 2**30:.1f} GiB")
    except Exception as err:
        print(f"GPUs: not available ({err.__class__.__name__})")
    print("\nA3 files:")
    for f in A3_FILES:
        print(f"  {'ok' if os.path.exists(f) else 'MISSING':8s} {f:32s} "
              f"{os.path.getsize(f) if os.path.exists(f) else 0:>7,} bytes")


def show_run_inventory(args):
    runs = sorted(glob.glob(os.path.join(args.runs_dir, "qwen", "*", "r3_*")) +
                  glob.glob(os.path.join(args.runs_dir, "qwen", "*", "a3_*")))
    for run in runs:
        have = [name for name, rel in (("scp", "scp/meta.json"), ("e2e", "e2e/meta.json"),
                                       ("results", "results/eval.json"), ("diagnose", "results/diagnose.json"),
                                       ("results_big", "results_big/eval.json"))
                if os.path.exists(os.path.join(run, rel))]
        print(f"{os.path.relpath(run, args.runs_dir):58s} {' + '.join(have)}")
    print(f"\n{len(runs)} A3 runs")


def main(args):
    if args.step is None or args.step not in STEPS:
        for n, title in STEPS.items():
            print(f"{n:3d}  {title}")
        print("\nusage: python3 show_step_a3.py <step>")
        return
    print_header(args.step)
    datasets = args.datasets.split(",")
    ds = args.ablation_dataset
    if args.step == 1:
        show_environment(args)
    elif args.step == 2:
        for d in datasets:
            print_log_evidence(os.path.join(args.logs_dir, f"it_nested_{d}.log"), args.width)
    elif args.step == 3:
        for d in datasets:
            print_log_evidence(os.path.join(args.logs_dir, f"it_gen_{d}.log"), args.width)
    elif args.step == 4:
        for q in (1, 2):
            print_log_evidence(os.path.join(args.logs_dir, f"a3_ablations_{ds}_q{q}.log"), args.width)
    elif args.step == 5:
        print_log_evidence(os.path.join(args.logs_dir, f"a3_scp_allqa_{ds}.log"), args.width)
    elif args.step == 6:
        print_file(os.path.join(args.runs_dir, f"a3_ablations_{ds}.md"), args.width)
    elif args.step == 7:
        for q in (1, 2):
            print_log_evidence(os.path.join(args.logs_dir, f"a3_big_eval_{ds}_q{q}.log"), args.width)
        print_file(os.path.join(args.runs_dir, f"a3_ablations_{ds}_big.md"), args.width)
    elif args.step == 8:
        print_file(os.path.join(args.runs_dir, "a3_it_comparison.md"), args.width,
                   keep=["End-to-end", "Retrieval"])
    elif args.step == 9:
        print_file(os.path.join(args.runs_dir, "a3_it_comparison.md"), args.width,
                   keep=["Memory diagnostic", "Compressor-only"])
    elif args.step == 10:
        show_run_inventory(args)


if __name__ == "__main__":
    main(build_parser().parse_args())
