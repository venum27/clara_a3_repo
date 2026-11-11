# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_itgen_s44`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Parameters and compression

- Backbone: Qwen/Qwen2.5-0.5B-Instruct (decoder-only), base parameters: 494,032,768
- LoRA parameters per adapter: {'compressor': 2162688, 'generator': 2162688, 'query_reasoner': 2162688}
- Memory-embedding parameters: 57,344
- Average passage length: 95.3 tokens; compression rate by prefix: m=4: 23.8x, m=8: 11.9x, m=16: 6.0x, m=32: 3.0x

## Compressor-only QA on held-out synthetic questions (SCP checkpoint)

| Prefix m | EM | F1 | n |
|---|---|---|---|
| 4 | 5.0 [3.2, 6.9] | 19.3 [16.8, 21.9] | 525 |
| 8 | 6.5 [4.4, 8.6] | 20.8 [18.2, 23.5] | 525 |
| 16 | 9.1 [6.9, 11.6] | 23.9 [21.2, 26.8] | 525 |
| 32 | 7.8 [5.5, 10.1] | 23.8 [21.0, 26.6] | 525 |

## Oracle: gold passages only

| Input | EM | F1 | Context size |
|---|---|---|---|
| compressed_m4 | 38.0 [32.3, 43.7] | 41.0 [35.6, 46.6] | 10 vectors |
| compressed_m8 | 38.3 [32.7, 44.0] | 42.5 [37.1, 48.2] | 20 vectors |
| compressed_m16 | 39.0 [33.3, 44.7] | 43.5 [38.2, 48.9] | 40 vectors |
| compressed_m32 | 37.0 [31.7, 42.7] | 41.6 [36.5, 47.0] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 69.3 | 80.3 | 89.7 | 96.7 | 0.0 | 16.7 | 29.7 | 53.0 |
| query reasoner (before E2E) | 25.7 | 46.0 | 58.3 | 82.3 | 0.0 | 1.0 | 4.3 | 16.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 35.7 [30.3, 41.3] | 38.7 [33.3, 44.2] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 35.7 [30.3, 41.3] | 38.7 [33.3, 44.2] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 35.7 [30.3, 41.3] | 38.7 [33.3, 44.2] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 35.7 [30.7, 41.3] | 39.5 [34.3, 45.0] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 35.3 [30.0, 40.7] | 39.4 [34.2, 44.8] |
| score@32 | [15.4, 8.0, 4.3, 4.3] | 32.0 vectors | 35.3 [30.0, 40.7] | 39.4 [34.3, 44.8] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 35.3 [29.7, 41.0] | 39.2 [33.9, 44.9] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 35.7 [30.3, 41.3] | 39.5 [34.2, 45.2] |
| score@64 | [30.9, 16.0, 8.6, 8.6] | 64.0 vectors | 35.7 [30.3, 41.3] | 39.4 [34.1, 45.0] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.7 [30.3, 41.3] | 39.2 [33.9, 44.9] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.7 [30.3, 41.3] | 39.2 [33.9, 44.9] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.7 [30.3, 41.3] | 39.2 [33.9, 44.9] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (208) | rank 2 (33) | rank 3+ (39) | not retrieved (20) |
|---|---|---|---|---|
| uniform@16 | 35.8 | 40.5 | 46.9 | 50.0 |
| top_heavy@16 | 35.8 | 40.5 | 46.9 | 50.0 |
| score@16 | 35.8 | 40.5 | 46.9 | 50.0 |
| uniform@32 | 37.2 | 39.7 | 44.9 | 52.0 |
| top_heavy@32 | 37.4 | 39.7 | 43.3 | 52.0 |
| score@32 | 37.6 | 39.7 | 42.5 | 52.0 |
| uniform@64 | 37.3 | 36.7 | 45.0 | 52.0 |
| top_heavy@64 | 37.9 | 36.0 | 45.9 | 50.0 |
| score@64 | 37.9 | 36.0 | 45.0 | 50.0 |
| uniform@128 | 36.7 | 39.0 | 43.3 | 57.0 |
| top_heavy@128 | 36.7 | 39.0 | 43.3 | 57.0 |
| score@128 | 36.7 | 39.0 | 43.3 | 57.0 |
| raw_bm25 | 23.3 | 24.0 | 20.2 | 32.7 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | -0.3 [-1.3, +0.7] | 0.824 | -0.1 [-1.6, +1.3] | 0.567 |
| score@32 vs uniform@32 | -0.3 [-1.3, +0.7] | 0.824 | -0.1 [-1.4, +1.3] | 0.546 |
| top_heavy@64 vs uniform@64 | +0.3 [+0.0, +1.0] | 0.386 | +0.3 [-0.7, +1.4] | 0.294 |
| score@64 vs uniform@64 | +0.3 [+0.0, +1.0] | 0.386 | +0.2 [-0.8, +1.2] | 0.405 |
