# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_it__learned_s43`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Parameters and compression

- Backbone: Qwen/Qwen2.5-0.5B-Instruct (decoder-only), base parameters: 494,032,768
- LoRA parameters per adapter: {'compressor': 2162688, 'generator': 2162688, 'query_reasoner': 2162688}
- Memory-embedding parameters: 57,344
- Average passage length: 132.5 tokens; compression rate by prefix: m=4: 33.1x, m=8: 16.6x, m=16: 8.3x, m=32: 4.1x

## Compressor-only QA on held-out synthetic questions (SCP checkpoint)

| Prefix m | EM | F1 | n |
|---|---|---|---|
| 4 | 5.6 [3.7, 7.5] | 16.3 [13.9, 18.8] | 520 |
| 8 | 5.4 [3.5, 7.3] | 16.0 [13.4, 18.5] | 520 |
| 16 | 5.8 [3.8, 7.7] | 16.2 [13.8, 18.7] | 520 |
| 32 | 5.0 [3.3, 6.9] | 15.8 [13.5, 18.2] | 520 |

## Oracle: gold passages only

| Input | EM | F1 | Context size |
|---|---|---|---|
| compressed_m4 | 12.7 [9.0, 16.7] | 20.9 [16.9, 24.9] | 8 vectors |
| compressed_m8 | 13.0 [9.3, 17.0] | 20.7 [16.7, 24.9] | 16 vectors |
| compressed_m16 | 13.0 [9.3, 17.0] | 21.6 [17.9, 25.7] | 32 vectors |
| compressed_m32 | 14.0 [10.3, 18.0] | 22.8 [18.8, 27.0] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 51.3 | 71.3 | 80.7 | 94.3 | 0.0 | 14.7 | 29.7 | 51.3 |
| query reasoner (before E2E) | 36.7 | 51.0 | 62.7 | 81.7 | 0.0 | 8.3 | 16.3 | 29.3 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.3, 16.3] | 19.7 [15.9, 23.8] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.3, 16.3] | 19.7 [15.9, 23.8] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.3, 16.3] | 19.7 [15.9, 23.8] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.3, 16.3] | 19.7 [15.9, 23.8] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 13.0 [9.3, 16.7] | 19.0 [15.1, 23.0] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 13.0 [9.3, 17.0] | 19.3 [15.2, 23.3] |
| score@32 | [15.5, 8.0, 4.2, 4.2] | 32.0 vectors | 13.0 [9.3, 17.0] | 19.3 [15.2, 23.3] |
| learned@32 | [12.5, 9.7, 4.7, 5.1] | 32.0 vectors | 12.7 [9.0, 16.7] | 18.4 [14.6, 22.3] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 14.0 [10.3, 18.0] | 20.5 [16.6, 24.5] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 13.7 [10.0, 17.3] | 20.9 [16.9, 24.8] |
| score@64 | [31.1, 16.0, 8.5, 8.5] | 64.0 vectors | 13.7 [10.0, 17.3] | 20.9 [16.9, 24.8] |
| learned@64 | [22.6, 18.3, 11.1, 11.9] | 64.0 vectors | 14.3 [10.7, 18.3] | 20.9 [16.9, 25.1] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 11.7 [8.3, 15.3] | 17.8 [14.1, 21.8] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 11.7 [8.3, 15.3] | 17.8 [14.1, 21.8] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 11.7 [8.3, 15.3] | 17.8 [14.1, 21.8] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 11.7 [8.3, 15.3] | 17.8 [14.1, 21.8] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [12.5, 9.7, 4.7, 5.1] | 9.3 | 7.3 |
| 64 | [22.6, 18.3, 11.1, 11.9] | 18.5 | 14.8 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (154) | rank 2 (60) | rank 3+ (55) | not retrieved (31) |
|---|---|---|---|---|
| uniform@16 | 21.4 | 24.0 | 10.4 | 19.9 |
| top_heavy@16 | 21.4 | 24.0 | 10.4 | 19.9 |
| score@16 | 21.4 | 24.0 | 10.4 | 19.9 |
| learned@16 | 21.4 | 24.0 | 10.4 | 19.9 |
| uniform@32 | 21.1 | 23.7 | 9.3 | 16.8 |
| top_heavy@32 | 21.3 | 24.1 | 9.0 | 18.3 |
| score@32 | 21.3 | 24.1 | 9.0 | 18.3 |
| learned@32 | 20.3 | 23.1 | 9.0 | 16.7 |
| uniform@64 | 21.7 | 28.0 | 10.5 | 18.3 |
| top_heavy@64 | 23.1 | 27.3 | 9.5 | 17.3 |
| score@64 | 23.1 | 27.3 | 9.5 | 17.3 |
| learned@64 | 23.0 | 27.3 | 10.7 | 16.7 |
| uniform@128 | 19.0 | 22.3 | 10.1 | 17.1 |
| top_heavy@128 | 19.0 | 22.3 | 10.1 | 17.1 |
| score@128 | 19.0 | 22.3 | 10.1 | 17.1 |
| learned@128 | 19.0 | 22.3 | 10.1 | 17.1 |
| raw_bm25 | 23.0 | 19.1 | 20.8 | 21.9 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | +0.0 [-1.0, +1.0] | 0.642 | +0.3 [-1.1, +1.7] | 0.355 |
| score@32 vs uniform@32 | +0.0 [-1.0, +1.0] | 0.642 | +0.3 [-1.1, +1.7] | 0.355 |
| learned@32 vs uniform@32 | -0.3 [-1.7, +0.7] | 0.800 | -0.6 [-2.1, +0.8] | 0.811 |
| learned@32 vs top_heavy@32 | -0.3 [-1.0, +0.0] | 1.000 | -0.9 [-1.8, -0.2] | 1.000 |
| top_heavy@64 vs uniform@64 | -0.3 [-1.7, +1.0] | 0.750 | +0.3 [-0.9, +1.6] | 0.308 |
| score@64 vs uniform@64 | -0.3 [-1.7, +1.0] | 0.750 | +0.3 [-0.9, +1.6] | 0.308 |
| learned@64 vs uniform@64 | +0.3 [-1.0, +2.0] | 0.405 | +0.4 [-1.0, +1.9] | 0.292 |
| learned@64 vs top_heavy@64 | +0.7 [+0.0, +1.7] | 0.127 | +0.1 [-0.7, +1.0] | 0.462 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
