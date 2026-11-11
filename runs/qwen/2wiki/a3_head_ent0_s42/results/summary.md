# Evaluation summary

Run: `runs/qwen/2wiki/a3_head_ent0_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 71.7 | 89.0 | 94.3 | 98.0 | 0.0 | 25.3 | 39.3 | 64.7 |
| query reasoner (before E2E) | 25.7 | 46.0 | 58.3 | 82.3 | 0.0 | 1.0 | 4.3 | 16.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 32.3 [27.0, 37.7] | 36.0 [30.8, 41.3] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 32.0 [27.0, 37.3] | 35.4 [30.2, 40.8] |
| learned@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 32.3 [27.0, 37.7] | 36.0 [30.8, 41.3] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 32.3 [27.0, 37.7] | 36.4 [31.2, 41.7] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 32.7 [27.3, 38.3] | 36.4 [31.2, 41.9] |
| learned@64 | [11.9, 18.1, 12.8, 21.1] | 64.0 vectors | 31.0 [26.0, 36.7] | 34.6 [29.6, 40.0] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 32 | [8.0, 8.0, 8.0, 8.0] | 8.0 | 8.0 |
| 64 | [11.9, 18.1, 12.8, 21.1] | 15.1 | 16.8 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (215) | rank 2 (52) | rank 3+ (21) | not retrieved (12) |
|---|---|---|---|---|
| uniform@32 | 33.2 | 38.4 | 43.8 | 61.1 |
| top_heavy@32 | 33.6 | 33.2 | 43.8 | 61.1 |
| learned@32 | 33.2 | 38.4 | 43.8 | 61.1 |
| uniform@64 | 33.4 | 40.0 | 43.8 | 61.1 |
| top_heavy@64 | 34.2 | 38.8 | 39.0 | 61.1 |
| learned@64 | 31.6 | 39.0 | 39.0 | 61.1 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | -0.3 [-1.7, +1.0] | 0.750 | -0.6 [-2.3, +1.0] | 0.758 |
| learned@32 vs uniform@32 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@32 vs top_heavy@32 | +0.3 [-1.0, +1.7] | 0.413 | +0.6 [-1.0, +2.3] | 0.241 |
| top_heavy@64 vs uniform@64 | +0.3 [-0.7, +1.7] | 0.382 | +0.0 [-1.3, +1.5] | 0.480 |
| learned@64 vs uniform@64 | -1.3 [-3.0, +0.0] | 0.979 | -1.8 [-3.6, -0.2] | 0.986 |
| learned@64 vs top_heavy@64 | -1.7 [-3.3, -0.3] | 1.000 | -1.8 [-3.6, -0.2] | 0.990 |
