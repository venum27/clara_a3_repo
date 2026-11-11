# Evaluation summary

Run: `runs/qwen/2wiki/a3_fixed16_tau0.02_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 60.8 | 79.7 | 88.0 | 94.8 | 0.0 | 11.1 | 19.9 | 36.8 |
| query reasoner (after E2E) | 68.9 | 85.1 | 91.5 | 97.7 | 0.0 | 20.8 | 34.6 | 55.6 |
| query reasoner (before E2E) | 15.3 | 35.4 | 52.3 | 77.0 | 0.0 | 1.2 | 4.3 | 17.4 |
| random (expected) | 24.5 | 44.2 | 60.1 | 82.2 | 0.0 | 1.7 | 5.2 | 17.8 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 32.7 [30.9, 34.5] | 37.9 [36.1, 39.6] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (2066) | rank 2 (488) | rank 3+ (307) | not retrieved (139) |
|---|---|---|---|---|
| uniform@64 | 35.1 | 41.1 | 44.3 | 53.2 |
