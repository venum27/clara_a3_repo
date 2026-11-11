# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_it_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Parameters and compression

- Backbone: Qwen/Qwen2.5-0.5B-Instruct (decoder-only), base parameters: 494,032,768
- LoRA parameters per adapter: {'compressor': 2162688, 'generator': 2162688, 'query_reasoner': 2162688}
- Memory-embedding parameters: 57,344
- Average passage length: 95.3 tokens; compression rate by prefix: m=4: 23.8x, m=8: 11.9x, m=16: 6.0x, m=32: 3.0x

## Compressor-only QA on held-out synthetic questions (SCP checkpoint)

| Prefix m | EM | F1 | n |
|---|---|---|---|
| 4 | 2.5 [1.3, 3.8] | 11.2 [9.2, 13.2] | 525 |
| 8 | 2.1 [1.0, 3.4] | 11.2 [9.2, 13.2] | 525 |
| 16 | 1.9 [0.8, 3.2] | 11.0 [9.1, 12.9] | 525 |
| 32 | 2.3 [1.1, 3.6] | 11.2 [9.4, 13.2] | 525 |

## Oracle: gold passages only

| Input | EM | F1 | Context size |
|---|---|---|---|
| compressed_m4 | 36.0 [30.7, 41.7] | 40.2 [35.0, 45.6] | 10 vectors |
| compressed_m8 | 37.7 [32.3, 43.3] | 42.2 [36.9, 47.6] | 20 vectors |
| compressed_m16 | 37.7 [32.3, 43.3] | 41.2 [35.9, 46.7] | 40 vectors |
| compressed_m32 | 35.7 [30.3, 41.0] | 40.2 [35.0, 45.6] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 36.7 | 60.0 | 74.3 | 95.0 | 0.0 | 5.0 | 16.0 | 48.7 |
| query reasoner (before E2E) | 15.7 | 25.0 | 36.7 | 59.7 | 0.0 | 1.0 | 3.0 | 7.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 39.7] | 37.4 [32.2, 42.7] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 39.7] | 37.4 [32.2, 42.7] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 39.7] | 37.4 [32.2, 42.7] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 36.3 [31.0, 41.7] | 40.0 [34.8, 45.4] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 35.3 [30.0, 41.0] | 38.3 [32.9, 43.7] |
| score@32 | [13.7, 8.0, 5.1, 5.1] | 32.0 vectors | 36.0 [30.3, 41.3] | 38.7 [33.3, 44.2] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 33.7 [28.3, 39.0] | 37.6 [32.5, 42.9] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 33.7 [28.3, 39.0] | 37.3 [32.1, 42.5] |
| score@64 | [27.5, 16.0, 10.3, 10.3] | 64.0 vectors | 33.7 [28.3, 39.0] | 37.5 [32.4, 42.7] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.0 [29.7, 40.7] | 37.9 [32.7, 43.5] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.0 [29.7, 40.7] | 37.9 [32.7, 43.5] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.0 [29.7, 40.7] | 37.9 [32.7, 43.5] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (110) | rank 2 (70) | rank 3+ (87) | not retrieved (33) |
|---|---|---|---|---|
| uniform@16 | 33.4 | 31.4 | 43.0 | 48.5 |
| top_heavy@16 | 33.4 | 31.4 | 43.0 | 48.5 |
| score@16 | 33.4 | 31.4 | 43.0 | 48.5 |
| uniform@32 | 35.2 | 37.0 | 45.4 | 48.5 |
| top_heavy@32 | 34.0 | 34.0 | 43.2 | 48.5 |
| score@32 | 35.1 | 34.0 | 43.4 | 48.5 |
| uniform@64 | 36.1 | 32.8 | 42.9 | 39.4 |
| top_heavy@64 | 35.4 | 31.1 | 42.5 | 42.4 |
| score@64 | 35.9 | 31.1 | 42.7 | 42.4 |
| uniform@128 | 35.8 | 31.4 | 43.1 | 45.5 |
| top_heavy@128 | 35.8 | 31.4 | 43.1 | 45.5 |
| score@128 | 35.8 | 31.4 | 43.1 | 45.5 |
| raw_bm25 | 21.9 | 23.8 | 23.2 | 30.1 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | -1.0 [-2.7, +0.7] | 0.923 | -1.8 [-3.6, -0.0] | 0.978 |
| score@32 vs uniform@32 | -0.3 [-2.0, +1.0] | 0.766 | -1.3 [-2.8, +0.0] | 0.969 |
| top_heavy@64 vs uniform@64 | +0.0 [-1.0, +1.0] | 0.650 | -0.4 [-1.6, +0.8] | 0.747 |
| score@64 vs uniform@64 | +0.0 [-1.0, +1.0] | 0.650 | -0.2 [-1.3, +0.9] | 0.608 |
