# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_it_s44`

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
| compressed_m4 | 15.3 [11.7, 19.7] | 22.4 [18.3, 26.9] | 8 vectors |
| compressed_m8 | 14.3 [10.7, 18.7] | 22.6 [18.7, 26.7] | 16 vectors |
| compressed_m16 | 15.0 [11.3, 19.0] | 23.3 [19.1, 27.6] | 32 vectors |
| compressed_m32 | 15.0 [11.3, 19.3] | 22.7 [18.7, 27.0] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 53.7 | 71.7 | 85.0 | 95.0 | 0.0 | 15.3 | 30.0 | 55.0 |
| query reasoner (before E2E) | 36.7 | 51.0 | 62.7 | 81.7 | 0.0 | 8.3 | 16.3 | 29.3 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.0, 16.7] | 19.4 [15.6, 23.3] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.0, 16.7] | 19.4 [15.6, 23.3] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.0, 16.7] | 19.4 [15.6, 23.3] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 13.0 [9.3, 17.0] | 19.7 [15.8, 23.8] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 12.7 [9.0, 16.7] | 19.1 [15.4, 23.2] |
| score@32 | [15.7, 8.0, 4.1, 4.1] | 32.0 vectors | 12.7 [9.0, 16.7] | 19.1 [15.4, 23.2] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 14.0 [10.3, 18.0] | 21.5 [17.5, 25.8] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 13.3 [9.7, 17.3] | 20.8 [16.8, 24.9] |
| score@64 | [31.4, 16.0, 8.3, 8.3] | 64.0 vectors | 13.3 [9.7, 17.3] | 20.9 [17.0, 25.1] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.3 [9.7, 17.3] | 20.9 [17.1, 25.0] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.3 [9.7, 17.3] | 20.9 [17.1, 25.0] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.3 [9.7, 17.3] | 20.9 [17.1, 25.0] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (161) | rank 2 (54) | rank 3+ (58) | not retrieved (27) |
|---|---|---|---|---|
| uniform@16 | 22.0 | 20.8 | 13.2 | 14.2 |
| top_heavy@16 | 22.0 | 20.8 | 13.2 | 14.2 |
| score@16 | 22.0 | 20.8 | 13.2 | 14.2 |
| uniform@32 | 21.4 | 21.6 | 14.2 | 17.4 |
| top_heavy@32 | 22.3 | 18.1 | 13.4 | 15.0 |
| score@32 | 22.3 | 18.1 | 13.4 | 15.0 |
| uniform@64 | 24.2 | 19.6 | 18.2 | 16.7 |
| top_heavy@64 | 23.6 | 20.3 | 14.8 | 17.8 |
| score@64 | 23.6 | 20.3 | 14.8 | 19.3 |
| uniform@128 | 23.8 | 22.3 | 14.5 | 14.5 |
| top_heavy@128 | 23.8 | 22.3 | 14.5 | 14.5 |
| score@128 | 23.8 | 22.3 | 14.5 | 14.5 |
| raw_bm25 | 23.1 | 19.1 | 17.8 | 27.3 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | -0.3 [-1.0, +0.0] | 1.000 | -0.5 [-1.6, +0.4] | 0.837 |
| score@32 vs uniform@32 | -0.3 [-1.0, +0.0] | 1.000 | -0.5 [-1.6, +0.4] | 0.837 |
| top_heavy@64 vs uniform@64 | -0.7 [-2.0, +0.7] | 0.908 | -0.7 [-2.2, +0.5] | 0.882 |
| score@64 vs uniform@64 | -0.7 [-2.0, +0.7] | 0.908 | -0.6 [-2.0, +0.6] | 0.837 |
