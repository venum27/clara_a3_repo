# Evaluation summary

Run: `runs/qwen/2wiki/a3_fixed16_allqa_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 53.7 | 77.0 | 86.7 | 96.0 | 0.0 | 12.3 | 21.7 | 42.0 |
| query reasoner (before E2E) | 17.3 | 39.0 | 51.7 | 77.3 | 0.0 | 1.0 | 3.3 | 13.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 32.7 [27.7, 38.0] | 35.0 [30.0, 40.4] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 33.3 [28.3, 38.7] | 35.9 [30.8, 41.1] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 34.3 [29.0, 39.7] | 36.8 [31.6, 42.3] |
| top_heavy@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 34.3 [29.0, 39.7] | 36.8 [31.6, 42.3] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (161) | rank 2 (70) | rank 3+ (49) | not retrieved (20) |
|---|---|---|---|---|
| uniform@32 | 34.4 | 35.0 | 37.0 | 35.4 |
| top_heavy@32 | 35.7 | 36.3 | 35.6 | 36.0 |
| uniform@64 | 34.3 | 40.8 | 39.4 | 36.0 |
| top_heavy@64 | 34.3 | 40.8 | 39.4 | 36.0 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +0.7 [+0.0, +1.7] | 0.123 | +0.8 [-0.5, +2.3] | 0.107 |
