# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_itgen__learned_s44`

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
| compressed_m4 | 34.3 [29.0, 40.0] | 37.4 [32.1, 42.9] | 10 vectors |
| compressed_m8 | 35.3 [29.7, 41.0] | 39.3 [34.0, 44.9] | 20 vectors |
| compressed_m16 | 35.7 [30.3, 41.3] | 39.9 [34.6, 45.4] | 40 vectors |
| compressed_m32 | 34.3 [28.7, 40.0] | 38.7 [33.2, 44.2] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 68.0 | 83.3 | 91.0 | 97.7 | 0.0 | 22.3 | 35.0 | 59.3 |
| query reasoner (before E2E) | 25.7 | 46.0 | 58.3 | 82.3 | 0.0 | 1.0 | 4.3 | 16.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.7 [29.3, 40.3] | 37.2 [31.8, 42.6] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.7 [29.3, 40.3] | 37.2 [31.8, 42.6] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.7 [29.3, 40.3] | 37.2 [31.8, 42.6] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.7 [29.3, 40.3] | 37.2 [31.8, 42.6] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 33.7 [28.3, 39.3] | 37.4 [32.0, 42.9] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 34.0 [28.7, 39.7] | 36.7 [31.2, 42.2] |
| score@32 | [15.1, 8.0, 4.5, 4.5] | 32.0 vectors | 34.0 [28.7, 39.7] | 36.8 [31.4, 42.3] |
| learned@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 33.7 [28.3, 39.3] | 37.4 [32.0, 42.9] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 34.0 [28.7, 39.7] | 37.3 [31.9, 42.9] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 35.0 [29.3, 40.7] | 38.2 [32.7, 43.8] |
| score@64 | [30.2, 16.0, 8.9, 8.9] | 64.0 vectors | 35.0 [29.3, 40.7] | 38.1 [32.7, 43.8] |
| learned@64 | [18.9, 12.3, 19.1, 13.7] | 64.0 vectors | 35.0 [29.7, 40.7] | 38.1 [32.7, 43.8] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.7 [29.0, 40.3] | 37.9 [32.3, 43.5] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.7 [29.0, 40.3] | 37.9 [32.3, 43.5] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.7 [29.0, 40.3] | 37.9 [32.3, 43.5] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.7 [29.0, 40.3] | 37.9 [32.3, 43.5] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [8.0, 8.0, 8.0, 8.0] | 8.0 | 8.0 |
| 64 | [18.9, 12.3, 19.1, 13.7] | 16.8 | 15.3 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (204) | rank 2 (46) | rank 3+ (39) | not retrieved (11) |
|---|---|---|---|---|
| uniform@16 | 36.5 | 37.0 | 34.9 | 57.6 |
| top_heavy@16 | 36.5 | 37.0 | 34.9 | 57.6 |
| score@16 | 36.5 | 37.0 | 34.9 | 57.6 |
| learned@16 | 36.5 | 37.0 | 34.9 | 57.6 |
| uniform@32 | 36.9 | 39.4 | 35.7 | 45.5 |
| top_heavy@32 | 36.8 | 37.5 | 32.4 | 45.5 |
| score@32 | 36.8 | 37.5 | 33.1 | 45.5 |
| learned@32 | 36.9 | 39.4 | 35.7 | 45.5 |
| uniform@64 | 37.8 | 37.2 | 35.4 | 36.4 |
| top_heavy@64 | 38.7 | 37.2 | 34.9 | 45.5 |
| score@64 | 38.5 | 37.2 | 34.9 | 45.5 |
| learned@64 | 37.9 | 37.2 | 35.4 | 54.5 |
| uniform@128 | 38.0 | 37.5 | 35.4 | 45.5 |
| top_heavy@128 | 38.0 | 37.5 | 35.4 | 45.5 |
| score@128 | 38.0 | 37.5 | 35.4 | 45.5 |
| learned@128 | 38.0 | 37.5 | 35.4 | 45.5 |
| raw_bm25 | 22.4 | 21.7 | 27.9 | 38.4 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | +0.3 [-0.7, +1.7] | 0.398 | -0.8 [-1.9, +0.3] | 0.923 |
| score@32 vs uniform@32 | +0.3 [-0.7, +1.7] | 0.398 | -0.7 [-1.8, +0.3] | 0.894 |
| learned@32 vs uniform@32 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@32 vs top_heavy@32 | -0.3 [-1.7, +0.7] | 0.821 | +0.8 [-0.3, +1.9] | 0.078 |
| top_heavy@64 vs uniform@64 | +1.0 [+0.0, +2.3] | 0.052 | +0.9 [-0.4, +2.2] | 0.085 |
| score@64 vs uniform@64 | +1.0 [+0.0, +2.3] | 0.052 | +0.8 [-0.4, +2.1] | 0.108 |
| learned@64 vs uniform@64 | +1.0 [+0.0, +2.3] | 0.043 | +0.8 [-0.4, +2.3] | 0.124 |
| learned@64 vs top_heavy@64 | +0.0 [-1.3, +1.3] | 0.609 | -0.1 [-1.4, +1.3] | 0.574 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
