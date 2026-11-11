# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_it_s43`

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
| compressed_m4 | 35.7 [30.3, 41.3] | 40.4 [35.1, 46.0] | 10 vectors |
| compressed_m8 | 37.7 [32.0, 43.0] | 42.2 [37.0, 47.6] | 20 vectors |
| compressed_m16 | 39.0 [33.3, 44.3] | 43.4 [38.2, 48.8] | 40 vectors |
| compressed_m32 | 38.3 [32.7, 44.0] | 43.0 [37.6, 48.5] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 42.0 | 64.7 | 76.0 | 94.3 | 0.0 | 7.7 | 19.7 | 49.3 |
| query reasoner (before E2E) | 15.7 | 25.0 | 36.7 | 59.7 | 0.0 | 1.0 | 3.0 | 7.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 40.0] | 38.9 [33.8, 44.3] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 40.0] | 38.9 [33.8, 44.3] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 40.0] | 38.9 [33.8, 44.3] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 36.7 [31.3, 42.0] | 40.6 [35.5, 45.9] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 35.3 [30.0, 40.7] | 39.6 [34.4, 45.0] |
| score@32 | [13.8, 8.0, 5.1, 5.1] | 32.0 vectors | 36.0 [30.7, 41.3] | 40.0 [34.7, 45.2] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 36.0 [30.7, 41.3] | 40.5 [35.4, 45.8] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 37.0 [31.7, 42.3] | 41.2 [36.2, 46.7] |
| score@64 | [27.7, 16.0, 10.2, 10.2] | 64.0 vectors | 36.7 [31.3, 42.0] | 40.9 [35.8, 46.2] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 36.7 [31.3, 42.3] | 40.9 [35.8, 46.3] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 36.7 [31.3, 42.3] | 40.9 [35.8, 46.3] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 36.7 [31.3, 42.3] | 40.9 [35.8, 46.3] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (126) | rank 2 (68) | rank 3+ (74) | not retrieved (32) |
|---|---|---|---|---|
| uniform@16 | 35.5 | 33.6 | 46.1 | 46.9 |
| top_heavy@16 | 35.5 | 33.6 | 46.1 | 46.9 |
| score@16 | 35.5 | 33.6 | 46.1 | 46.9 |
| uniform@32 | 37.8 | 33.5 | 47.8 | 50.0 |
| top_heavy@32 | 35.6 | 34.4 | 46.8 | 50.0 |
| score@32 | 36.4 | 34.4 | 46.8 | 50.0 |
| uniform@64 | 37.9 | 34.2 | 47.9 | 46.9 |
| top_heavy@64 | 37.8 | 33.8 | 48.8 | 53.1 |
| score@64 | 38.0 | 33.8 | 48.2 | 50.0 |
| uniform@128 | 38.3 | 34.3 | 50.0 | 43.8 |
| top_heavy@128 | 38.3 | 34.3 | 50.0 | 43.8 |
| score@128 | 38.3 | 34.3 | 50.0 | 43.8 |
| raw_bm25 | 21.7 | 24.6 | 24.8 | 26.1 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | -1.3 [-3.0, +0.0] | 0.979 | -1.0 [-2.6, +0.3] | 0.921 |
| score@32 vs uniform@32 | -0.7 [-2.0, +0.7] | 0.917 | -0.7 [-2.0, +0.4] | 0.854 |
| top_heavy@64 vs uniform@64 | +1.0 [+0.0, +2.3] | 0.051 | +0.7 [-0.6, +2.2] | 0.148 |
| score@64 vs uniform@64 | +0.7 [+0.0, +1.7] | 0.142 | +0.4 [-0.8, +1.6] | 0.276 |
