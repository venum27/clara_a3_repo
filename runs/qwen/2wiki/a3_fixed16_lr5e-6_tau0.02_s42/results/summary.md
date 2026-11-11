# Evaluation summary

Run: `runs/qwen/2wiki/a3_fixed16_lr5e-6_tau0.02_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 52.0 | 71.7 | 81.3 | 92.3 | 0.0 | 12.7 | 26.3 | 40.3 |
| query reasoner (before E2E) | 15.3 | 35.0 | 49.7 | 74.7 | 0.0 | 1.3 | 4.3 | 13.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 34.0 [28.7, 39.3] | 36.4 [31.2, 41.7] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 36.0 [30.7, 41.3] | 39.2 [33.7, 44.3] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 38.3 [33.0, 44.0] | 40.9 [35.4, 46.3] |
| top_heavy@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 38.3 [33.0, 44.0] | 40.9 [35.4, 46.3] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (156) | rank 2 (59) | rank 3+ (50) | not retrieved (35) |
|---|---|---|---|---|
| uniform@32 | 29.1 | 36.6 | 45.9 | 55.2 |
| top_heavy@32 | 33.1 | 36.5 | 51.9 | 52.4 |
| uniform@64 | 35.5 | 40.9 | 49.5 | 52.4 |
| top_heavy@64 | 35.5 | 40.9 | 49.5 | 52.4 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +2.0 [-0.3, +4.3] | 0.059 | +2.7 [+0.2, +5.4] | 0.018 |
