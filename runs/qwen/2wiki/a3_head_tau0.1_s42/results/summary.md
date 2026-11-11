# Evaluation summary

Run: `runs/qwen/2wiki/a3_head_tau0.1_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 70.3 | 86.3 | 92.7 | 97.3 | 0.0 | 22.0 | 35.0 | 62.0 |
| query reasoner (before E2E) | 25.7 | 46.0 | 58.3 | 82.3 | 0.0 | 1.0 | 4.3 | 16.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 32.7 [27.3, 38.0] | 36.1 [30.7, 41.3] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 32.3 [27.0, 37.7] | 35.9 [30.8, 41.3] |
| learned@32 | [7.8, 7.9, 8.0, 8.3] | 32.0 vectors | 32.7 [27.3, 38.0] | 36.1 [30.7, 41.3] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 32.7 [27.3, 38.0] | 36.5 [31.2, 41.8] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 32.7 [27.3, 38.0] | 36.4 [31.1, 41.7] |
| learned@64 | [16.2, 15.1, 19.2, 13.6] | 64.0 vectors | 32.3 [27.0, 37.7] | 35.7 [30.4, 41.1] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 32 | [7.8, 7.9, 8.0, 8.3] | 7.9 | 8.1 |
| 64 | [16.2, 15.1, 19.2, 13.6] | 15.9 | 16.1 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (211) | rank 2 (48) | rank 3+ (27) | not retrieved (14) |
|---|---|---|---|---|
| uniform@32 | 34.2 | 36.9 | 37.8 | 59.5 |
| top_heavy@32 | 34.7 | 33.1 | 37.8 | 59.5 |
| learned@32 | 34.2 | 36.9 | 37.8 | 59.5 |
| uniform@64 | 35.4 | 30.7 | 38.8 | 66.7 |
| top_heavy@64 | 35.3 | 31.5 | 37.8 | 66.7 |
| learned@64 | 34.7 | 29.0 | 38.8 | 66.7 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | -0.3 [-2.0, +1.3] | 0.712 | -0.2 [-2.1, +1.6] | 0.589 |
| learned@32 vs uniform@32 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@32 vs top_heavy@32 | +0.3 [-1.3, +2.0] | 0.433 | +0.2 [-1.6, +2.1] | 0.411 |
| top_heavy@64 vs uniform@64 | +0.0 [-1.3, +1.3] | 0.607 | -0.0 [-1.3, +1.3] | 0.515 |
| learned@64 vs uniform@64 | -0.3 [-1.0, +0.0] | 1.000 | -0.8 [-1.8, -0.1] | 0.994 |
| learned@64 vs top_heavy@64 | -0.3 [-1.7, +1.0] | 0.750 | -0.8 [-2.5, +0.8] | 0.820 |
