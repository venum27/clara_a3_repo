# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_it_s42`

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
| compressed_m4 | 15.0 [11.3, 19.0] | 21.7 [17.8, 26.1] | 8 vectors |
| compressed_m8 | 14.0 [10.3, 18.3] | 21.9 [18.2, 26.1] | 16 vectors |
| compressed_m16 | 12.3 [9.0, 16.3] | 21.1 [17.2, 25.1] | 32 vectors |
| compressed_m32 | 14.7 [10.7, 18.7] | 21.8 [17.9, 25.8] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 40.3 | 61.7 | 74.7 | 88.7 | 0.0 | 9.7 | 21.7 | 42.0 |
| query reasoner (before E2E) | 36.7 | 51.0 | 62.7 | 81.7 | 0.0 | 8.3 | 16.3 | 29.3 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.0 [8.7, 16.0] | 18.7 [15.1, 22.7] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.0 [8.7, 16.0] | 18.7 [15.1, 22.7] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.0 [8.7, 16.0] | 18.7 [15.1, 22.7] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 12.0 [8.7, 16.0] | 18.9 [15.2, 22.9] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 12.3 [8.7, 16.3] | 18.7 [14.9, 22.7] |
| score@32 | [15.4, 8.0, 4.3, 4.3] | 32.0 vectors | 12.3 [8.7, 16.3] | 18.5 [14.7, 22.5] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 12.7 [9.0, 16.3] | 19.5 [15.7, 23.5] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 11.7 [8.0, 15.3] | 17.7 [14.0, 21.6] |
| score@64 | [30.7, 16.0, 8.6, 8.6] | 64.0 vectors | 11.7 [8.0, 15.3] | 17.8 [14.1, 21.6] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.7 [10.0, 17.7] | 20.1 [16.1, 24.2] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.7 [10.0, 17.7] | 20.1 [16.1, 24.2] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.7 [10.0, 17.7] | 20.1 [16.1, 24.2] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (121) | rank 2 (64) | rank 3+ (63) | not retrieved (52) |
|---|---|---|---|---|
| uniform@16 | 20.9 | 16.8 | 21.2 | 12.9 |
| top_heavy@16 | 20.9 | 16.8 | 21.2 | 12.9 |
| score@16 | 20.9 | 16.8 | 21.2 | 12.9 |
| uniform@32 | 21.7 | 19.7 | 17.2 | 13.3 |
| top_heavy@32 | 21.5 | 18.2 | 17.4 | 14.3 |
| score@32 | 21.5 | 18.2 | 16.6 | 14.3 |
| uniform@64 | 24.0 | 18.8 | 18.2 | 11.6 |
| top_heavy@64 | 21.9 | 17.3 | 17.3 | 8.9 |
| score@64 | 21.9 | 17.3 | 17.5 | 8.9 |
| uniform@128 | 23.6 | 20.8 | 21.4 | 9.8 |
| top_heavy@128 | 23.6 | 20.8 | 21.4 | 9.8 |
| score@128 | 23.6 | 20.8 | 21.4 | 9.8 |
| raw_bm25 | 23.3 | 19.6 | 22.9 | 19.1 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +0.3 [+0.0, +1.0] | 0.380 | -0.2 [-1.2, +0.8] | 0.686 |
| score@32 vs uniform@32 | +0.3 [+0.0, +1.0] | 0.380 | -0.4 [-1.3, +0.6] | 0.810 |
| top_heavy@64 vs uniform@64 | -1.0 [-2.3, +0.0] | 1.000 | -1.8 [-3.2, -0.6] | 1.000 |
| score@64 vs uniform@64 | -1.0 [-2.3, +0.0] | 1.000 | -1.8 [-3.2, -0.6] | 1.000 |
