# Evaluation summary

Run: `runs/qwen/2wiki/a3_fixed16_tau0.02_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 67.3 | 82.3 | 92.0 | 97.3 | 0.0 | 21.3 | 36.0 | 52.7 |
| query reasoner (before E2E) | 15.3 | 35.0 | 49.7 | 74.7 | 0.0 | 1.3 | 4.3 | 13.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 32.7 [27.3, 38.0] | 36.3 [31.0, 41.5] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 36.3 [31.0, 42.0] | 40.0 [34.6, 45.5] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 36.3 [31.0, 42.0] | 39.9 [34.7, 45.5] |
| top_heavy@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 36.3 [31.0, 42.0] | 39.9 [34.7, 45.5] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (202) | rank 2 (45) | rank 3+ (36) | not retrieved (17) |
|---|---|---|---|---|
| uniform@32 | 30.7 | 29.9 | 62.9 | 62.7 |
| top_heavy@32 | 37.7 | 27.7 | 60.1 | 56.9 |
| uniform@64 | 37.4 | 35.2 | 54.7 | 51.4 |
| top_heavy@64 | 37.4 | 35.2 | 54.7 | 51.4 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +3.7 [+1.0, +6.3] | 0.003 | +3.7 [+0.8, +6.6] | 0.004 |
