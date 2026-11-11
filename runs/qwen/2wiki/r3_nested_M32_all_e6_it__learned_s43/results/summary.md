# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_it__learned_s43`

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
| compressed_m4 | 34.3 [29.3, 39.7] | 38.8 [33.7, 44.0] | 10 vectors |
| compressed_m8 | 36.3 [31.0, 41.7] | 40.2 [35.0, 45.6] | 20 vectors |
| compressed_m16 | 36.3 [31.0, 41.7] | 40.1 [34.7, 45.4] | 40 vectors |
| compressed_m32 | 36.0 [31.0, 41.3] | 40.2 [34.9, 45.3] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 37.7 | 60.0 | 74.7 | 94.7 | 0.0 | 4.3 | 16.0 | 49.3 |
| query reasoner (before E2E) | 15.7 | 25.0 | 36.7 | 59.7 | 0.0 | 1.0 | 3.0 | 7.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 39.7] | 37.7 [32.5, 43.0] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 39.7] | 37.7 [32.5, 43.0] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 39.7] | 37.7 [32.5, 43.0] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 39.7] | 37.7 [32.5, 43.0] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 34.3 [29.0, 39.7] | 37.8 [32.7, 42.9] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 34.3 [29.0, 39.7] | 37.0 [31.9, 42.3] |
| score@32 | [13.9, 8.0, 5.1, 5.1] | 32.0 vectors | 34.3 [29.0, 39.7] | 37.4 [32.3, 42.5] |
| learned@32 | [10.6, 8.3, 6.1, 6.9] | 32.0 vectors | 34.7 [29.3, 40.0] | 37.8 [32.8, 43.0] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 34.3 [29.0, 39.7] | 37.5 [32.4, 42.8] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 34.0 [29.0, 39.3] | 36.8 [31.6, 42.2] |
| score@64 | [27.7, 16.0, 10.1, 10.1] | 64.0 vectors | 33.7 [28.3, 39.0] | 36.8 [31.6, 42.1] |
| learned@64 | [15.7, 14.6, 16.0, 17.7] | 64.0 vectors | 35.0 [29.7, 40.3] | 38.1 [32.9, 43.4] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.3, 39.7] | 37.8 [32.7, 43.0] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.3, 39.7] | 37.8 [32.7, 43.0] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.3, 39.7] | 37.8 [32.7, 43.0] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.3, 39.7] | 37.8 [32.7, 43.0] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [10.6, 8.3, 6.1, 6.9] | 9.8 | 7.1 |
| 64 | [15.7, 14.6, 16.0, 17.7] | 16.8 | 15.6 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (113) | rank 2 (67) | rank 3+ (85) | not retrieved (35) |
|---|---|---|---|---|
| uniform@16 | 34.8 | 34.9 | 39.3 | 48.6 |
| top_heavy@16 | 34.8 | 34.9 | 39.3 | 48.6 |
| score@16 | 34.8 | 34.9 | 39.3 | 48.6 |
| learned@16 | 34.8 | 34.9 | 39.3 | 48.6 |
| uniform@32 | 33.9 | 37.1 | 39.1 | 48.6 |
| top_heavy@32 | 33.0 | 35.5 | 38.7 | 48.6 |
| score@32 | 33.9 | 35.5 | 38.9 | 48.6 |
| learned@32 | 33.9 | 37.4 | 38.9 | 48.6 |
| uniform@64 | 33.9 | 34.3 | 40.2 | 48.6 |
| top_heavy@64 | 32.7 | 32.9 | 40.5 | 48.6 |
| score@64 | 33.1 | 32.9 | 39.9 | 48.6 |
| learned@64 | 34.8 | 34.3 | 41.4 | 48.6 |
| uniform@128 | 34.6 | 37.0 | 38.2 | 48.6 |
| top_heavy@128 | 34.6 | 37.0 | 38.2 | 48.6 |
| score@128 | 34.6 | 37.0 | 38.2 | 48.6 |
| learned@128 | 34.6 | 37.0 | 38.2 | 48.6 |
| raw_bm25 | 21.5 | 22.1 | 25.0 | 29.6 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | +0.0 [-1.3, +1.3] | 0.619 | -0.8 [-2.2, +0.4] | 0.899 |
| score@32 vs uniform@32 | +0.0 [-1.0, +1.0] | 0.662 | -0.4 [-1.2, +0.2] | 0.889 |
| learned@32 vs uniform@32 | +0.3 [+0.0, +1.0] | 0.365 | +0.0 [-0.5, +0.4] | 0.439 |
| learned@32 vs top_heavy@32 | +0.3 [-1.0, +2.0] | 0.414 | +0.8 [-0.4, +2.2] | 0.096 |
| top_heavy@64 vs uniform@64 | -0.3 [-1.7, +1.0] | 0.740 | -0.7 [-2.0, +0.8] | 0.818 |
| score@64 vs uniform@64 | -0.7 [-2.0, +0.7] | 0.897 | -0.7 [-1.9, +0.4] | 0.878 |
| learned@64 vs uniform@64 | +0.7 [+0.0, +1.7] | 0.142 | +0.7 [+0.0, +1.7] | 0.142 |
| learned@64 vs top_heavy@64 | +1.0 [-0.7, +2.7] | 0.174 | +1.3 [-0.4, +3.1] | 0.068 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
