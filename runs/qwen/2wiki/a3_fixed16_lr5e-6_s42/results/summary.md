# Evaluation summary

Run: `runs/qwen/2wiki/a3_fixed16_lr5e-6_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 54.0 | 72.0 | 81.7 | 92.3 | 0.0 | 15.3 | 27.0 | 43.7 |
| query reasoner (before E2E) | 15.3 | 35.0 | 49.7 | 74.7 | 0.0 | 1.3 | 4.3 | 13.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 33.7 [28.3, 39.0] | 36.2 [31.0, 41.4] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 35.7 [30.3, 41.0] | 38.7 [33.2, 43.9] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 37.3 [31.7, 42.7] | 40.2 [34.6, 45.7] |
| top_heavy@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 37.3 [31.7, 42.7] | 40.2 [34.6, 45.7] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (162) | rank 2 (54) | rank 3+ (53) | not retrieved (31) |
|---|---|---|---|---|
| uniform@32 | 28.8 | 33.6 | 48.0 | 59.1 |
| top_heavy@32 | 33.0 | 33.5 | 49.3 | 59.1 |
| uniform@64 | 35.1 | 34.6 | 48.6 | 62.6 |
| top_heavy@64 | 35.1 | 34.6 | 48.6 | 62.6 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +2.0 [-0.3, +4.3] | 0.049 | +2.5 [+0.1, +4.8] | 0.021 |
