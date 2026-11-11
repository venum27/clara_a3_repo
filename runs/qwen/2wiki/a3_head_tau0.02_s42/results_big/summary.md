# Evaluation summary

Run: `runs/qwen/2wiki/a3_head_tau0.02_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 60.8 | 79.7 | 88.0 | 94.8 | 0.0 | 11.1 | 19.9 | 36.8 |
| query reasoner (after E2E) | 74.1 | 87.3 | 93.2 | 97.8 | 0.0 | 22.9 | 35.1 | 59.0 |
| query reasoner (before E2E) | 25.8 | 45.1 | 60.6 | 80.4 | 0.0 | 2.1 | 5.9 | 17.1 |
| random (expected) | 24.5 | 44.2 | 60.1 | 82.2 | 0.0 | 1.7 | 5.2 | 17.8 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 30.9 [29.2, 32.6] | 36.0 [34.3, 37.7] |
| learned@64 | [15.9, 19.3, 14.1, 14.7] | 64.0 vectors | 30.7 [29.0, 32.5] | 36.0 [34.3, 37.6] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 64 | [15.9, 19.3, 14.1, 14.7] | 16.6 | 15.5 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (2224) | rank 2 (396) | rank 3+ (264) | not retrieved (116) |
|---|---|---|---|---|
| uniform@64 | 36.0 | 37.5 | 38.4 | 25.5 |
| learned@64 | 36.0 | 37.0 | 38.3 | 26.4 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@64 vs uniform@64 | -0.1 [-0.5, +0.2] | 0.803 | -0.0 [-0.4, +0.3] | 0.553 |
