# Evaluation summary

Run: `runs/qwen/2wiki/a3_head_ent0.1_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 69.3 | 85.0 | 93.0 | 97.7 | 0.0 | 21.0 | 34.3 | 62.3 |
| query reasoner (before E2E) | 25.7 | 46.0 | 58.3 | 82.3 | 0.0 | 1.0 | 4.3 | 16.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 32.0 [26.7, 37.3] | 36.0 [30.9, 41.3] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 32.3 [27.0, 37.7] | 35.9 [30.6, 41.3] |
| learned@32 | [10.8, 8.7, 6.0, 6.5] | 32.0 vectors | 32.3 [26.7, 37.7] | 35.9 [30.6, 41.2] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 31.7 [26.3, 37.0] | 35.9 [30.7, 41.1] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 31.7 [26.3, 37.0] | 35.3 [29.9, 40.5] |
| learned@64 | [21.4, 17.7, 12.7, 12.2] | 64.0 vectors | 32.0 [26.7, 37.3] | 35.7 [30.5, 41.1] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 32 | [10.8, 8.7, 6.0, 6.5] | 9.2 | 7.0 |
| 64 | [21.4, 17.7, 12.7, 12.2] | 18.7 | 13.8 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (208) | rank 2 (47) | rank 3+ (33) | not retrieved (12) |
|---|---|---|---|---|
| uniform@32 | 33.8 | 41.9 | 38.5 | 44.4 |
| top_heavy@32 | 33.4 | 41.1 | 38.5 | 52.8 |
| learned@32 | 33.0 | 41.9 | 40.0 | 52.8 |
| uniform@64 | 32.6 | 44.4 | 39.0 | 52.8 |
| top_heavy@64 | 31.9 | 43.7 | 38.5 | 52.8 |
| learned@64 | 32.8 | 42.4 | 38.5 | 52.8 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +0.3 [-0.7, +1.7] | 0.398 | -0.1 [-1.3, +1.2] | 0.557 |
| learned@32 vs uniform@32 | +0.3 [-0.7, +1.3] | 0.407 | -0.1 [-1.2, +1.2] | 0.574 |
| learned@32 vs top_heavy@32 | +0.0 [-1.0, +1.0] | 0.668 | +0.0 [-1.1, +1.1] | 0.497 |
| top_heavy@64 vs uniform@64 | +0.0 [-1.0, +1.0] | 0.652 | -0.6 [-1.8, +0.5] | 0.857 |
| learned@64 vs uniform@64 | +0.3 [+0.0, +1.0] | 0.357 | -0.2 [-1.1, +0.8] | 0.654 |
| learned@64 vs top_heavy@64 | +0.3 [+0.0, +1.3] | 0.370 | +0.5 [-0.4, +1.5] | 0.161 |
