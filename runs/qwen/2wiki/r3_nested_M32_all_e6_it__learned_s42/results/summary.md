# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_it__learned_s42`

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
| compressed_m4 | 35.0 [29.7, 40.3] | 39.0 [33.9, 44.2] | 10 vectors |
| compressed_m8 | 36.7 [31.3, 42.0] | 40.6 [35.4, 45.8] | 20 vectors |
| compressed_m16 | 37.0 [31.7, 42.3] | 41.3 [35.9, 46.5] | 40 vectors |
| compressed_m32 | 37.3 [32.0, 42.7] | 41.6 [36.2, 46.7] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 37.7 | 60.3 | 77.0 | 96.0 | 0.0 | 4.3 | 17.0 | 49.3 |
| query reasoner (before E2E) | 15.7 | 25.0 | 36.7 | 59.7 | 0.0 | 1.0 | 3.0 | 7.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 33.0 [27.7, 38.3] | 37.0 [31.7, 42.2] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 33.0 [27.7, 38.3] | 37.0 [31.7, 42.2] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 33.0 [27.7, 38.3] | 37.0 [31.7, 42.2] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 33.0 [27.7, 38.3] | 37.0 [31.7, 42.2] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 34.3 [29.0, 39.7] | 37.9 [32.5, 42.9] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 33.7 [28.3, 39.0] | 37.6 [32.2, 42.7] |
| score@32 | [13.3, 8.0, 5.3, 5.3] | 32.0 vectors | 33.7 [28.3, 39.0] | 37.3 [32.0, 42.3] |
| learned@32 | [5.4, 7.7, 8.9, 10.0] | 32.0 vectors | 34.3 [29.0, 39.3] | 37.7 [32.4, 42.7] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 33.7 [28.3, 38.7] | 38.0 [32.7, 43.1] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 34.7 [29.3, 40.0] | 38.2 [32.8, 43.3] |
| score@64 | [26.7, 16.0, 10.7, 10.7] | 64.0 vectors | 34.3 [29.0, 39.7] | 38.5 [33.1, 43.7] |
| learned@64 | [12.2, 12.0, 24.8, 15.0] | 64.0 vectors | 34.3 [29.0, 39.7] | 38.3 [32.9, 43.4] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.0, 39.7] | 38.6 [33.5, 43.8] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.0, 39.7] | 38.6 [33.5, 43.8] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.0, 39.7] | 38.6 [33.5, 43.8] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.0, 39.7] | 38.6 [33.5, 43.8] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [5.4, 7.7, 8.9, 10.0] | 9.1 | 7.5 |
| 64 | [12.2, 12.0, 24.8, 15.0] | 16.8 | 15.6 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (113) | rank 2 (68) | rank 3+ (89) | not retrieved (30) |
|---|---|---|---|---|
| uniform@16 | 36.2 | 35.3 | 37.2 | 43.3 |
| top_heavy@16 | 36.2 | 35.3 | 37.2 | 43.3 |
| score@16 | 36.2 | 35.3 | 37.2 | 43.3 |
| learned@16 | 36.2 | 35.3 | 37.2 | 43.3 |
| uniform@32 | 35.8 | 37.9 | 38.0 | 45.3 |
| top_heavy@32 | 34.6 | 38.7 | 37.8 | 45.3 |
| score@32 | 34.0 | 38.2 | 37.8 | 45.3 |
| learned@32 | 34.9 | 37.7 | 38.6 | 45.3 |
| uniform@64 | 35.8 | 36.9 | 39.2 | 45.6 |
| top_heavy@64 | 38.5 | 36.2 | 36.9 | 45.6 |
| score@64 | 37.8 | 36.6 | 38.4 | 45.6 |
| learned@64 | 37.4 | 36.5 | 38.3 | 45.6 |
| uniform@128 | 38.8 | 35.8 | 38.4 | 44.8 |
| top_heavy@128 | 38.8 | 35.8 | 38.4 | 44.8 |
| score@128 | 38.8 | 35.8 | 38.4 | 44.8 |
| learned@128 | 38.8 | 35.8 | 38.4 | 44.8 |
| raw_bm25 | 21.5 | 23.0 | 25.1 | 28.2 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | -0.7 [-1.7, +0.0] | 1.000 | -0.3 [-1.5, +0.7] | 0.717 |
| score@32 vs uniform@32 | -0.7 [-1.7, +0.0] | 1.000 | -0.7 [-1.7, +0.1] | 0.933 |
| learned@32 vs uniform@32 | +0.0 [-1.0, +1.0] | 0.636 | -0.2 [-1.1, +0.4] | 0.699 |
| learned@32 vs top_heavy@32 | +0.7 [+0.0, +1.7] | 0.120 | +0.1 [-0.9, +1.2] | 0.429 |
| top_heavy@64 vs uniform@64 | +1.0 [+0.0, +2.0] | 0.050 | +0.2 [-1.1, +1.6] | 0.410 |
| score@64 vs uniform@64 | +0.7 [+0.0, +1.7] | 0.142 | +0.5 [-0.6, +1.7] | 0.218 |
| learned@64 vs uniform@64 | +0.7 [+0.0, +1.7] | 0.132 | +0.2 [-0.7, +1.4] | 0.356 |
| learned@64 vs top_heavy@64 | -0.3 [-1.3, +0.7] | 0.807 | +0.0 [-1.3, +1.4] | 0.444 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
