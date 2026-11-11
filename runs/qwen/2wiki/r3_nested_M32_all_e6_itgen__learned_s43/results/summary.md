# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_itgen__learned_s43`

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
| compressed_m4 | 36.3 [31.0, 42.3] | 39.5 [34.2, 45.3] | 10 vectors |
| compressed_m8 | 37.0 [31.7, 42.7] | 41.8 [36.7, 47.6] | 20 vectors |
| compressed_m16 | 36.3 [31.0, 42.0] | 41.0 [35.8, 46.5] | 40 vectors |
| compressed_m32 | 36.3 [31.0, 42.3] | 41.2 [36.1, 46.8] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 71.3 | 87.7 | 94.0 | 98.3 | 0.0 | 26.0 | 36.7 | 57.7 |
| query reasoner (before E2E) | 25.7 | 46.0 | 58.3 | 82.3 | 0.0 | 1.0 | 4.3 | 16.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 40.0] | 37.4 [32.1, 42.9] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 40.0] | 37.4 [32.1, 42.9] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 40.0] | 37.4 [32.1, 42.9] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 34.3 [29.0, 40.0] | 37.4 [32.1, 42.9] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 35.7 [30.0, 41.3] | 39.4 [34.0, 45.0] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 35.7 [30.3, 41.3] | 40.0 [34.8, 45.8] |
| score@32 | [15.3, 8.0, 4.3, 4.3] | 32.0 vectors | 35.7 [30.3, 41.3] | 40.0 [34.8, 45.8] |
| learned@32 | [10.9, 9.1, 4.5, 7.4] | 32.0 vectors | 35.7 [30.3, 41.3] | 39.4 [34.0, 45.1] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 34.7 [29.7, 40.3] | 38.4 [33.3, 43.8] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 35.0 [30.0, 40.7] | 38.6 [33.5, 44.0] |
| score@64 | [30.6, 16.0, 8.7, 8.7] | 64.0 vectors | 35.0 [30.0, 40.7] | 38.6 [33.5, 44.0] |
| learned@64 | [22.6, 15.8, 11.3, 14.3] | 64.0 vectors | 33.7 [28.3, 39.3] | 37.4 [32.4, 42.7] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.0 [29.7, 40.7] | 38.7 [33.6, 44.2] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.0 [29.7, 40.7] | 38.7 [33.6, 44.2] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.0 [29.7, 40.7] | 38.7 [33.6, 44.2] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.0 [29.7, 40.7] | 38.7 [33.6, 44.2] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [10.9, 9.1, 4.5, 7.4] | 9.2 | 7.0 |
| 64 | [22.6, 15.8, 11.3, 14.3] | 18.2 | 14.2 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (214) | rank 2 (49) | rank 3+ (29) | not retrieved (8) |
|---|---|---|---|---|
| uniform@16 | 34.6 | 39.5 | 53.8 | 41.1 |
| top_heavy@16 | 34.6 | 39.5 | 53.8 | 41.1 |
| score@16 | 34.6 | 39.5 | 53.8 | 41.1 |
| learned@16 | 34.6 | 39.5 | 53.8 | 41.1 |
| uniform@32 | 37.5 | 37.9 | 51.5 | 53.6 |
| top_heavy@32 | 38.1 | 37.9 | 53.8 | 53.6 |
| score@32 | 38.1 | 37.9 | 53.8 | 53.6 |
| learned@32 | 37.6 | 37.9 | 51.5 | 53.6 |
| uniform@64 | 37.1 | 37.9 | 51.5 | 28.6 |
| top_heavy@64 | 36.9 | 37.9 | 51.5 | 41.1 |
| score@64 | 36.9 | 37.9 | 51.5 | 41.1 |
| learned@64 | 35.7 | 37.9 | 52.1 | 28.6 |
| uniform@128 | 37.2 | 38.8 | 48.1 | 42.5 |
| top_heavy@128 | 37.2 | 38.8 | 48.1 | 42.5 |
| score@128 | 37.2 | 38.8 | 48.1 | 42.5 |
| learned@128 | 37.2 | 38.8 | 48.1 | 42.5 |
| raw_bm25 | 22.5 | 30.1 | 16.6 | 37.1 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | +0.0 [-1.3, +1.3] | 0.588 | +0.6 [-0.3, +1.7] | 0.093 |
| score@32 vs uniform@32 | +0.0 [-1.3, +1.3] | 0.588 | +0.6 [-0.3, +1.7] | 0.093 |
| learned@32 vs uniform@32 | +0.0 [-1.0, +1.0] | 0.648 | +0.0 [-1.0, +1.0] | 0.450 |
| learned@32 vs top_heavy@32 | +0.0 [-1.0, +1.0] | 0.671 | -0.6 [-1.6, +0.1] | 0.946 |
| top_heavy@64 vs uniform@64 | +0.3 [-1.3, +2.0] | 0.420 | +0.2 [-1.2, +1.7] | 0.382 |
| score@64 vs uniform@64 | +0.3 [-1.3, +2.0] | 0.420 | +0.2 [-1.2, +1.7] | 0.382 |
| learned@64 vs uniform@64 | -1.0 [-2.3, +0.0] | 1.000 | -0.9 [-2.3, +0.1] | 0.969 |
| learned@64 vs top_heavy@64 | -1.3 [-3.0, +0.0] | 0.981 | -1.2 [-2.7, +0.0] | 0.974 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
