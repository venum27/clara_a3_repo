# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_it_s43`

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
| compressed_m4 | 14.0 [10.3, 18.3] | 22.2 [18.5, 26.5] | 8 vectors |
| compressed_m8 | 15.0 [11.0, 19.3] | 22.8 [18.8, 27.1] | 16 vectors |
| compressed_m16 | 15.3 [11.7, 19.7] | 23.3 [19.4, 27.7] | 32 vectors |
| compressed_m32 | 15.3 [11.3, 19.7] | 22.7 [18.6, 26.9] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 52.3 | 69.3 | 82.0 | 95.0 | 0.0 | 13.7 | 28.0 | 52.0 |
| query reasoner (before E2E) | 36.7 | 51.0 | 62.7 | 81.7 | 0.0 | 8.3 | 16.3 | 29.3 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.3 [9.7, 17.3] | 19.3 [15.4, 23.5] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.3 [9.7, 17.3] | 19.3 [15.4, 23.5] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.3 [9.7, 17.3] | 19.3 [15.4, 23.5] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 13.7 [10.0, 17.7] | 19.3 [15.6, 23.5] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 13.7 [10.0, 17.7] | 19.9 [16.2, 24.2] |
| score@32 | [15.6, 8.0, 4.2, 4.2] | 32.0 vectors | 13.7 [10.0, 17.7] | 19.9 [16.1, 24.1] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 14.0 [10.3, 18.3] | 19.3 [15.4, 23.5] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 14.0 [10.0, 18.3] | 19.8 [15.7, 23.9] |
| score@64 | [31.1, 16.0, 8.4, 8.4] | 64.0 vectors | 14.0 [10.0, 18.3] | 19.9 [15.8, 24.0] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.0] | 19.2 [15.3, 23.2] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.0] | 19.2 [15.3, 23.2] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.0] | 19.2 [15.3, 23.2] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (157) | rank 2 (51) | rank 3+ (62) | not retrieved (30) |
|---|---|---|---|---|
| uniform@16 | 21.1 | 30.5 | 8.6 | 13.0 |
| top_heavy@16 | 21.1 | 30.5 | 8.6 | 13.0 |
| score@16 | 21.1 | 30.5 | 8.6 | 13.0 |
| uniform@32 | 21.9 | 30.2 | 6.5 | 14.0 |
| top_heavy@32 | 22.5 | 31.2 | 6.9 | 14.0 |
| score@32 | 22.4 | 31.2 | 6.9 | 14.0 |
| uniform@64 | 19.6 | 33.0 | 9.3 | 15.4 |
| top_heavy@64 | 20.8 | 32.3 | 8.9 | 15.4 |
| score@64 | 21.1 | 32.3 | 8.9 | 15.4 |
| uniform@128 | 21.9 | 29.3 | 8.0 | 11.4 |
| top_heavy@128 | 21.9 | 29.3 | 8.0 | 11.4 |
| score@128 | 21.9 | 29.3 | 8.0 | 11.4 |
| raw_bm25 | 23.4 | 15.2 | 23.6 | 19.9 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +0.0 [+0.0, +0.0] | 1.000 | +0.6 [-0.1, +1.3] | 0.050 |
| score@32 vs uniform@32 | +0.0 [+0.0, +0.0] | 1.000 | +0.5 [-0.2, +1.3] | 0.069 |
| top_heavy@64 vs uniform@64 | +0.0 [-1.0, +1.0] | 0.673 | +0.4 [-0.8, +1.5] | 0.212 |
| score@64 vs uniform@64 | +0.0 [-1.0, +1.0] | 0.673 | +0.6 [-0.6, +1.6] | 0.141 |
