# Evaluation summary

Run: `runs/qwen/2wiki/a3_head_ent0.1_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 60.8 | 79.7 | 88.0 | 94.8 | 0.0 | 11.1 | 19.9 | 36.8 |
| query reasoner (after E2E) | 71.9 | 86.8 | 92.2 | 97.9 | 0.0 | 27.4 | 41.8 | 65.5 |
| query reasoner (before E2E) | 25.8 | 45.1 | 60.6 | 80.4 | 0.0 | 2.1 | 5.9 | 17.1 |
| random (expected) | 24.5 | 44.2 | 60.1 | 82.2 | 0.0 | 1.7 | 5.2 | 17.8 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 30.0 [28.4, 31.7] | 34.8 [33.1, 36.4] |
| learned@64 | [21.2, 18.4, 12.2, 12.1] | 64.0 vectors | 30.0 [28.4, 31.7] | 34.8 [33.2, 36.5] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 64 | [21.2, 18.4, 12.2, 12.1] | 18.8 | 13.6 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (2156) | rank 2 (449) | rank 3+ (271) | not retrieved (124) |
|---|---|---|---|---|
| uniform@64 | 35.1 | 35.1 | 32.1 | 33.6 |
| learned@64 | 35.2 | 34.6 | 32.2 | 35.2 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@64 vs uniform@64 | -0.0 [-0.3, +0.3] | 0.641 | +0.1 [-0.3, +0.4] | 0.379 |
