# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_it__learned_s44`

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
| compressed_m4 | 34.3 [29.0, 40.0] | 38.3 [33.1, 43.7] | 10 vectors |
| compressed_m8 | 37.3 [32.0, 42.7] | 41.6 [36.3, 46.9] | 20 vectors |
| compressed_m16 | 36.0 [30.7, 41.3] | 41.0 [35.8, 46.4] | 40 vectors |
| compressed_m32 | 35.7 [30.7, 41.0] | 40.4 [35.3, 45.7] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 21.7 | 47.3 | 69.7 | 94.0 | 0.0 | 4.0 | 14.7 | 48.7 |
| query reasoner (before E2E) | 15.7 | 25.0 | 36.7 | 59.7 | 0.0 | 1.0 | 3.0 | 7.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 33.7 [28.3, 39.0] | 37.4 [32.2, 42.8] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 33.7 [28.3, 39.0] | 37.4 [32.2, 42.8] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 33.7 [28.3, 39.0] | 37.4 [32.2, 42.8] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 33.7 [28.3, 39.0] | 37.4 [32.2, 42.8] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 35.0 [29.7, 40.3] | 39.3 [34.1, 44.6] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 34.3 [29.0, 39.7] | 38.5 [33.1, 43.7] |
| score@32 | [13.7, 8.0, 5.1, 5.1] | 32.0 vectors | 34.0 [28.7, 39.3] | 38.1 [32.9, 43.4] |
| learned@32 | [8.1, 8.1, 7.9, 7.9] | 32.0 vectors | 35.0 [29.7, 40.3] | 39.3 [34.1, 44.6] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 33.7 [28.3, 39.0] | 38.4 [33.3, 43.6] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 34.3 [29.0, 39.7] | 38.4 [33.3, 43.7] |
| score@64 | [27.4, 16.0, 10.3, 10.3] | 64.0 vectors | 33.7 [28.3, 39.0] | 38.0 [32.8, 43.4] |
| learned@64 | [15.1, 15.1, 19.9, 13.9] | 64.0 vectors | 33.7 [28.3, 39.0] | 38.2 [33.1, 43.4] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 33.7 [28.3, 39.0] | 38.1 [33.1, 43.4] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 33.7 [28.3, 39.0] | 38.1 [33.1, 43.4] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 33.7 [28.3, 39.0] | 38.1 [33.1, 43.4] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 33.7 [28.3, 39.0] | 38.1 [33.1, 43.4] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [8.1, 8.1, 7.9, 7.9] | 8.1 | 8.0 |
| 64 | [15.1, 15.1, 19.9, 13.9] | 16.3 | 15.9 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (65) | rank 2 (77) | rank 3+ (122) | not retrieved (36) |
|---|---|---|---|---|
| uniform@16 | 38.6 | 23.7 | 41.6 | 50.0 |
| top_heavy@16 | 38.6 | 23.7 | 41.6 | 50.0 |
| score@16 | 38.6 | 23.7 | 41.6 | 50.0 |
| learned@16 | 38.6 | 23.7 | 41.6 | 50.0 |
| uniform@32 | 36.7 | 29.8 | 43.5 | 50.0 |
| top_heavy@32 | 37.4 | 28.3 | 42.0 | 50.0 |
| score@32 | 36.8 | 28.3 | 41.4 | 50.0 |
| learned@32 | 36.7 | 29.8 | 43.5 | 50.0 |
| uniform@64 | 40.5 | 29.7 | 40.1 | 47.2 |
| top_heavy@64 | 40.3 | 29.8 | 40.2 | 47.2 |
| score@64 | 41.1 | 28.5 | 39.8 | 47.2 |
| learned@64 | 40.5 | 29.1 | 40.1 | 47.2 |
| uniform@128 | 39.5 | 26.5 | 42.7 | 44.4 |
| top_heavy@128 | 39.5 | 26.5 | 42.7 | 44.4 |
| score@128 | 39.5 | 26.5 | 42.7 | 44.4 |
| learned@128 | 39.5 | 26.5 | 42.7 | 44.4 |
| raw_bm25 | 20.2 | 19.2 | 27.0 | 27.5 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | -0.7 [-2.3, +0.7] | 0.852 | -0.8 [-2.3, +0.6] | 0.870 |
| score@32 vs uniform@32 | -1.0 [-2.3, +0.3] | 0.958 | -1.2 [-2.6, -0.0] | 0.978 |
| learned@32 vs uniform@32 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@32 vs top_heavy@32 | +0.7 [-0.7, +2.3] | 0.260 | +0.8 [-0.6, +2.3] | 0.131 |
| top_heavy@64 vs uniform@64 | +0.7 [-0.7, +2.0] | 0.220 | +0.0 [-1.5, +1.6] | 0.477 |
| score@64 vs uniform@64 | +0.0 [-1.0, +1.0] | 0.660 | -0.3 [-1.4, +0.8] | 0.742 |
| learned@64 vs uniform@64 | +0.0 [+0.0, +0.0] | 1.000 | -0.2 [-0.5, +0.0] | 1.000 |
| learned@64 vs top_heavy@64 | -0.7 [-2.0, +0.7] | 0.908 | -0.2 [-1.8, +1.3] | 0.607 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
