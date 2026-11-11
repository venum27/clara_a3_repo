# Evaluation summary

Run: `runs/qwen/2wiki/a3_head_ent0_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 60.8 | 79.7 | 88.0 | 94.8 | 0.0 | 11.1 | 19.9 | 36.8 |
| query reasoner (after E2E) | 73.1 | 87.5 | 93.7 | 98.4 | 0.0 | 29.9 | 44.4 | 68.0 |
| query reasoner (before E2E) | 25.8 | 45.1 | 60.6 | 80.4 | 0.0 | 2.1 | 5.9 | 17.1 |
| random (expected) | 24.5 | 44.2 | 60.1 | 82.2 | 0.0 | 1.7 | 5.2 | 17.8 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 30.4 [28.7, 32.1] | 35.4 [33.7, 37.0] |
| learned@64 | [12.3, 16.9, 13.0, 21.8] | 64.0 vectors | 30.2 [28.5, 31.8] | 35.1 [33.3, 36.6] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 64 | [12.3, 16.9, 13.0, 21.8] | 15.0 | 16.9 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (2193) | rank 2 (433) | rank 3+ (279) | not retrieved (95) |
|---|---|---|---|---|
| uniform@64 | 35.4 | 36.4 | 36.1 | 30.2 |
| learned@64 | 35.0 | 35.5 | 36.0 | 31.5 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@64 vs uniform@64 | -0.3 [-0.6, +0.1] | 0.926 | -0.3 [-0.7, +0.0] | 0.963 |
