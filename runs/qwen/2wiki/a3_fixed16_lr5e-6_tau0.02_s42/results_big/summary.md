# Evaluation summary

Run: `runs/qwen/2wiki/a3_fixed16_lr5e-6_tau0.02_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 60.8 | 79.7 | 88.0 | 94.8 | 0.0 | 11.1 | 19.9 | 36.8 |
| query reasoner (after E2E) | 54.4 | 70.7 | 81.4 | 93.1 | 0.0 | 15.3 | 25.3 | 43.5 |
| query reasoner (before E2E) | 15.3 | 35.4 | 52.3 | 77.0 | 0.0 | 1.2 | 4.3 | 17.4 |
| random (expected) | 24.5 | 44.2 | 60.1 | 82.2 | 0.0 | 1.7 | 5.2 | 17.8 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 29.5 [27.9, 31.1] | 33.3 [31.7, 34.9] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (1631) | rank 2 (490) | rank 3+ (534) | not retrieved (345) |
|---|---|---|---|---|
| uniform@64 | 27.5 | 37.4 | 37.8 | 48.0 |
