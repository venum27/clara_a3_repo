# Evaluation summary

Run: `runs/qwen/2wiki/a3_head_tau0.1_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 60.8 | 79.7 | 88.0 | 94.8 | 0.0 | 11.1 | 19.9 | 36.8 |
| query reasoner (after E2E) | 71.8 | 86.8 | 93.0 | 98.2 | 0.0 | 27.9 | 41.1 | 64.9 |
| query reasoner (before E2E) | 25.8 | 45.1 | 60.6 | 80.4 | 0.0 | 2.1 | 5.9 | 17.1 |
| random (expected) | 24.5 | 44.2 | 60.1 | 82.2 | 0.0 | 1.7 | 5.2 | 17.8 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 31.0 [29.2, 32.7] | 35.9 [34.3, 37.6] |
| learned@64 | [15.5, 14.8, 20.0, 13.6] | 64.0 vectors | 31.0 [29.3, 32.7] | 35.8 [34.2, 37.6] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 64 | [15.5, 14.8, 20.0, 13.6] | 15.9 | 16.1 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (2153) | rank 2 (452) | rank 3+ (276) | not retrieved (119) |
|---|---|---|---|---|
| uniform@64 | 35.9 | 35.6 | 37.0 | 35.4 |
| learned@64 | 35.6 | 36.1 | 37.6 | 35.3 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@64 vs uniform@64 | +0.0 [-0.3, +0.4] | 0.468 | -0.1 [-0.4, +0.3] | 0.677 |
