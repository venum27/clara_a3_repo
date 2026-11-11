import json, os
import numpy as np
import matplotlib.pyplot as plt

root = "runs/qwen/2wiki"
B = 64
runs = {"β=0, τ=0.5": "a3_head_ent0_s42",
        "β=0.1, τ=0.5": "a3_head_ent0.1_s42",
        "β=0.02, τ=0.02": "a3_head_tau0.02_s42",
        "β=0.02, τ=0.1": "a3_head_tau0.1_s42"}

def load(r, f):
    return json.load(open(f"{root}/{r}/{f}"))

fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.5))
xs = np.arange(1, 5); w = 0.8 / len(runs)

# Panel A: learned split at B=64
for i, (lab, r) in enumerate(runs.items()):
    b = load(r, "results/eval.json")["qa"]["results"][f"learned@{B}"]["budgets"]
    ax[0].bar(xs - 0.4 + w * (i + 0.5), b, w, label=lab)
r0 = list(runs.values())[0]
ev0 = load(r0, "results/eval.json")["qa"]["results"]
ax[0].plot(xs, ev0[f"uniform@{B}"]["budgets"], "k--", label="uniform")
ax[0].plot(xs, ev0[f"top_heavy@{B}"]["budgets"], "k:", marker="o", label="top-heavy rule")
ax[0].set_xticks(xs)
ax[0].set_xlabel("Retrieved rank slot (1 = top-ranked)")
ax[0].set_ylabel(f"Avg memory vectors (total budget {B})")
ax[0].set_title("A. Learned budget split per rank slot")
ax[0].set_ylim(0, 36)
ax[0].legend(fontsize=7, loc="upper right")

# Panel B: entropy over epochs
for lab, r in runs.items():
    tl = load(r, "e2e/train_log.json")
    ax[1].plot([1, 2, 3], [e["split_entropy"] for e in tl["epochs"]], marker="o", label=lab)
ax[1].axhline(np.log(13), color="k", ls="--", lw=1, label="max entropy ln 13 = 2.56")
ax[1].set_xticks([1, 2, 3]); ax[1].set_ylim(0, 2.8)
ax[1].set_xlabel("E2E epoch"); ax[1].set_ylabel("Split entropy")
ax[1].set_title("B. Budget-head split entropy during training")
ax[1].legend(fontsize=7, loc="center right")

plt.tight_layout()
plt.savefig("budget_split_final.png", dpi=200)

# Job 2: print top1 share for the no-entropy run (and the others for contrast)
print("\ntop1_share_of_budget per epoch:")
for lab, r in runs.items():
    tl = load(r, "e2e/train_log.json")
    print(f"  {lab:16s}", [round(e["top1_share_of_budget"], 3) for e in tl["epochs"]])
print("saved budget_split_final.png")