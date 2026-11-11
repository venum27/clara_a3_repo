# Evaluation summary

Run: `runs/qwen/2wiki/a3_head_tau0.02_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 69.7 | 86.3 | 95.0 | 98.0 | 0.0 | 20.3 | 32.0 | 55.0 |
| query reasoner (before E2E) | 25.7 | 46.0 | 58.3 | 82.3 | 0.0 | 1.0 | 4.3 | 16.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 33.3 [28.0, 39.0] | 37.6 [32.6, 43.0] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 34.3 [29.0, 39.7] | 38.1 [32.9, 43.5] |
| learned@32 | [14.8, 6.8, 5.4, 5.0] | 32.0 vectors | 34.3 [29.0, 39.7] | 38.2 [33.0, 43.5] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 33.0 [27.7, 38.3] | 37.4 [32.3, 42.8] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 33.0 [28.0, 38.3] | 37.3 [32.2, 42.7] |
| learned@64 | [15.9, 19.3, 14.4, 14.5] | 64.0 vectors | 34.0 [28.7, 39.3] | 38.3 [33.3, 43.7] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 32 | [14.8, 6.8, 5.4, 5.0] | 9.5 | 6.8 |
| 64 | [15.9, 19.3, 14.4, 14.5] | 16.8 | 15.4 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (209) | rank 2 (50) | rank 3+ (31) | not retrieved (10) |
|---|---|---|---|---|
| uniform@32 | 35.8 | 33.7 | 51.7 | 50.0 |
| top_heavy@32 | 36.2 | 35.4 | 51.2 | 50.0 |
| learned@32 | 36.8 | 35.4 | 51.7 | 40.0 |
| uniform@64 | 35.6 | 36.0 | 50.6 | 40.0 |
| top_heavy@64 | 35.7 | 33.3 | 50.6 | 50.0 |
| learned@64 | 36.7 | 37.3 | 50.6 | 40.0 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +1.0 [-0.3, +2.3] | 0.122 | +0.5 [-0.9, +2.1] | 0.266 |
| learned@32 vs uniform@32 | +1.0 [-0.7, +2.7] | 0.172 | +0.7 [-1.2, +2.5] | 0.248 |
| learned@32 vs top_heavy@32 | +0.0 [-1.3, +1.3] | 0.610 | +0.1 [-1.1, +1.4] | 0.420 |
| top_heavy@64 vs uniform@64 | +0.0 [-1.3, +1.7] | 0.570 | -0.1 [-1.6, +1.4] | 0.516 |
| learned@64 vs uniform@64 | +1.0 [+0.0, +2.3] | 0.057 | +1.0 [-0.1, +2.3] | 0.049 |
| learned@64 vs top_heavy@64 | +1.0 [-1.0, +3.0] | 0.210 | +1.0 [-0.8, +3.0] | 0.147 |
