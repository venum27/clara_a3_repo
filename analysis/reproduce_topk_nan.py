"""
Sumanjali's CPU-only reproduction of the CLaRa Assignment 2 ST top-k NaN bug.

Source checked against:
- A2 nclara/modeling.py: NestedCLaRa.st_topk
- A3 a3_share/code/train_e2e_a3.py: NestedCLaRa.st_topk

Run:
    python sumanjali_nan_repro.py

Requirement:
    python -m pip install torch

This is a unit test of the selection function. It does not load the LLM,
CLaRa checkpoint, dataset, or use a GPU.
"""

import torch
import torch.nn.functional as F


# ---------------------------------------------------------------------
# 1) Original A2 function.
#    The function body below follows the A2 source implementation.
# ---------------------------------------------------------------------
def a2_st_topk(scores, k, tau=0.5):
    D = scores.shape[0]
    taken = torch.zeros(D, device=scores.device)
    hard = torch.zeros(k, D, device=scores.device)
    soft = []
    for j in range(k):
        logits = scores / tau + torch.log(1 - taken + 1e-9)
        p = F.softmax(logits, dim=0)
        soft.append(p)
        idx = int(torch.argmax(p.detach()))
        hard[j, idx] = 1.0
        taken = taken + hard[j]
    soft = torch.stack(soft)
    return hard + (soft - soft.detach())


# ---------------------------------------------------------------------
# 2) A2 trace version.
#    Same operations/order as A2, with diagnostics printed.
#    It deliberately continues after NaN, like the original function.
#    Any argmax selection made after NaN is NOT meaningful.
# ---------------------------------------------------------------------
def trace_a2_st_topk(scores, k, tau, label):
    print("\n" + "=" * 76)
    print(label)
    print("=" * 76)

    D = scores.shape[0]
    taken = torch.zeros(D, device=scores.device)
    hard = torch.zeros(k, D, device=scores.device)
    soft = []
    selected_indices = []
    first_nan_iteration = None

    for j in range(k):
        logits = scores / tau + torch.log(1 - taken + 1e-9)
        p = F.softmax(logits, dim=0)
        soft.append(p)

        print(f"\nIteration {j + 1}")
        print("taken before selection :", taken.tolist())
        print("logits                 :", logits.tolist())
        print("probabilities          :", p.tolist())

        if first_nan_iteration is None and (
            torch.isnan(logits).any() or torch.isnan(p).any()
        ):
            first_nan_iteration = j + 1
            print("*** FIRST NaN appears in this iteration. ***")

        idx = int(torch.argmax(p.detach()))
        selected_indices.append(idx)
        hard[j, idx] = 1.0
        taken = taken + hard[j]

        print("argmax index            :", idx)
        print("taken after selection  :", taken.tolist())

    soft = torch.stack(soft)
    result = hard + (soft - soft.detach())

    print("\nHard selection matrix:\n", hard)
    print("Indices returned by argmax:", selected_indices)
    print("First NaN iteration:", first_nan_iteration)
    print("Final ST output contains NaN:", torch.isnan(result).any().item())

    return result, first_nan_iteration


# ---------------------------------------------------------------------
# 3) A3 function.
#    This follows the implementation in train_e2e_a3.py:
#    boolean taken mask, clone, then taken[idx] = True.
# ---------------------------------------------------------------------
def a3_st_topk(scores, k, tau=0.5):
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


def trace_a3_st_topk(scores, k, tau, label):
    print("\n" + "=" * 76)
    print(label)
    print("=" * 76)

    D = scores.shape[0]
    taken = torch.zeros(D, dtype=torch.bool, device=scores.device)
    hard = torch.zeros(k, D, device=scores.device)
    soft = []
    selected_indices = []

    for j in range(k):
        logits = (scores / tau).masked_fill(taken, float("-inf"))
        p = F.softmax(logits, dim=0)
        soft.append(p)

        idx = int(torch.argmax(p.detach()))
        selected_indices.append(idx)
        hard[j, idx] = 1.0
        taken = taken.clone()
        taken[idx] = True

        print(f"\nIteration {j + 1}")
        print("taken after selection  :", taken.tolist())
        print("logits                 :", logits.tolist())
        print("probabilities          :", p.tolist())
        print("selected document      :", f"D{idx + 1}")
        print("NaN in probabilities   :", torch.isnan(p).any().item())

    soft = torch.stack(soft)
    result = hard + (soft - soft.detach())

    print("\nHard selection matrix:\n", hard)
    print("Selected documents:", [f"D{i + 1}" for i in selected_indices])
    print("All selections distinct:", len(set(selected_indices)) == k)
    print("Final ST output contains NaN:", torch.isnan(result).any().item())

    return result, selected_indices


def main():
    # Four candidates and k=4 match the default E2E retrieval setup.
    # The 0.60 top-two score gap becomes 30 after division by tau=0.02.
    scores = torch.tensor(
        [0.90, 0.30, 0.20, 0.10],
        dtype=torch.float32,
        device="cpu",
    )
    k = 4

    print("CPU-only CLaRa ST top-k unit test")
    print("device:", scores.device)
    print("scores:", scores.tolist())
    print("k:", k)
    print("scaled top-two gap at tau=0.02:",
          (scores[0].item() - scores[1].item()) / 0.02)
    print("old selected-document penalty log(1e-9):",
          torch.log(torch.tensor(1e-9)).item())

    # Control: original A2 function at tau=0.5.
    a2_normal, nan_normal = trace_a2_st_topk(
        scores, k, 0.5, "A2 ORIGINAL: CONTROL (tau=0.5)"
    )

    # Reproduction: original A2 function at tau=0.02.
    a2_low, nan_low = trace_a2_st_topk(
        scores, k, 0.02, "A2 ORIGINAL: BUG REPRODUCTION (tau=0.02)"
    )

    # A3 fix at the same low temperature.
    a3_low, a3_ids = trace_a3_st_topk(
        scores, k, 0.02, "A3 CORRECTION (tau=0.02)"
    )

    print("\n" + "=" * 76)
    print("AUTOMATIC ASSERTIONS")
    print("=" * 76)
    print("A2 tau=0.5 output is finite:",
          torch.isfinite(a2_normal).all().item())
    print("A2 tau=0.02 first NaN iteration:", nan_low)
    print("A2 tau=0.02 output contains NaN:",
          torch.isnan(a2_low).any().item())
    print("A3 tau=0.02 selects k distinct documents:",
          len(set(a3_ids)) == k)
    print("A3 tau=0.02 output is finite:",
          torch.isfinite(a3_low).all().item())

    assert torch.isfinite(a2_normal).all()
    assert nan_normal is None
    assert nan_low == 3
    assert torch.isnan(a2_low).any()
    assert a3_ids == [0, 1, 2, 3]
    assert torch.isfinite(a3_low).all()

    print("\nPASS: A2 NaN mechanism reproduced; A3 mask avoids it for this test.")


if __name__ == "__main__":
    main()
