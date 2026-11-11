# Evaluation summary

Run: `runs/qwen/2wiki/a3_fixed16_allqa_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 60.8 | 79.7 | 88.0 | 94.8 | 0.0 | 11.1 | 19.9 | 36.8 |
| query reasoner (after E2E) | 57.0 | 73.8 | 84.2 | 93.9 | 0.0 | 12.7 | 21.4 | 39.3 |
| query reasoner (before E2E) | 22.2 | 42.8 | 57.4 | 79.5 | 0.0 | 1.1 | 4.1 | 14.0 |
| random (expected) | 24.5 | 44.2 | 60.1 | 82.2 | 0.0 | 1.7 | 5.2 | 17.8 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 30.6 [29.0, 32.3] | 35.4 [33.8, 37.1] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (1711) | rank 2 (502) | rank 3+ (485) | not retrieved (302) |
|---|---|---|---|---|
| uniform@64 | 34.5 | 38.4 | 36.0 | 34.3 |
