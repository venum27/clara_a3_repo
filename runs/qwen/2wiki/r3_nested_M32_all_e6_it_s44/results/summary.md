# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_it_s44`

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
| compressed_m4 | 35.3 [30.3, 40.7] | 38.9 [33.9, 44.4] | 10 vectors |
| compressed_m8 | 36.3 [31.0, 42.0] | 40.4 [35.3, 46.0] | 20 vectors |
| compressed_m16 | 36.3 [31.0, 42.0] | 40.7 [35.5, 46.3] | 40 vectors |
| compressed_m32 | 34.3 [29.3, 40.0] | 38.5 [33.7, 44.0] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 29.7 | 46.3 | 54.3 | 73.0 | 0.0 | 2.3 | 6.0 | 15.7 |
| query reasoner (before E2E) | 15.7 | 25.0 | 36.7 | 59.7 | 0.0 | 1.0 | 3.0 | 7.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.0 [29.0, 39.7] | 37.4 [32.2, 42.8] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.0 [29.0, 39.7] | 37.4 [32.2, 42.8] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.0 [29.0, 39.7] | 37.4 [32.2, 42.8] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 34.7 [29.3, 40.3] | 37.9 [32.8, 43.3] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 35.0 [29.7, 40.3] | 38.4 [33.4, 43.6] |
| score@32 | [15.0, 8.0, 4.5, 4.5] | 32.0 vectors | 35.0 [29.7, 40.3] | 38.4 [33.4, 43.6] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 33.0 [28.0, 38.7] | 36.4 [31.2, 41.8] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 33.3 [28.3, 39.0] | 36.5 [31.4, 41.9] |
| score@64 | [30.0, 16.0, 9.0, 9.0] | 64.0 vectors | 33.3 [28.3, 39.0] | 36.5 [31.4, 41.9] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.7 [30.3, 41.3] | 38.7 [33.5, 44.2] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.7 [30.3, 41.3] | 38.7 [33.5, 44.2] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.7 [30.3, 41.3] | 38.7 [33.5, 44.2] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (89) | rank 2 (50) | rank 3+ (50) | not retrieved (111) |
|---|---|---|---|---|
| uniform@16 | 41.5 | 41.5 | 38.0 | 31.9 |
| top_heavy@16 | 41.5 | 41.5 | 38.0 | 31.9 |
| score@16 | 41.5 | 41.5 | 38.0 | 31.9 |
| uniform@32 | 42.6 | 42.2 | 39.3 | 31.7 |
| top_heavy@32 | 44.2 | 42.2 | 39.4 | 31.7 |
| score@32 | 44.2 | 42.2 | 39.4 | 31.7 |
| uniform@64 | 43.3 | 41.4 | 33.3 | 30.0 |
| top_heavy@64 | 41.9 | 41.5 | 34.5 | 30.9 |
| score@64 | 41.9 | 41.5 | 34.5 | 30.9 |
| uniform@128 | 44.4 | 40.8 | 42.1 | 31.6 |
| top_heavy@128 | 44.4 | 40.8 | 42.1 | 31.6 |
| score@128 | 44.4 | 40.8 | 42.1 | 31.6 |
| raw_bm25 | 25.9 | 23.0 | 25.5 | 21.1 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +0.3 [+0.0, +1.0] | 0.378 | +0.5 [-0.2, +1.4] | 0.104 |
| score@32 vs uniform@32 | +0.3 [+0.0, +1.0] | 0.378 | +0.5 [-0.2, +1.4] | 0.104 |
| top_heavy@64 vs uniform@64 | +0.3 [-0.7, +1.3] | 0.382 | +0.1 [-0.9, +1.2] | 0.389 |
| score@64 vs uniform@64 | +0.3 [-0.7, +1.3] | 0.382 | +0.1 [-0.9, +1.2] | 0.389 |
