# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_itgen__learned_s42`

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
| compressed_m4 | 36.0 [30.7, 41.7] | 38.9 [33.6, 44.6] | 10 vectors |
| compressed_m8 | 38.3 [33.0, 44.0] | 42.2 [37.0, 47.8] | 20 vectors |
| compressed_m16 | 37.0 [31.7, 42.7] | 41.1 [35.9, 46.6] | 40 vectors |
| compressed_m32 | 36.0 [30.7, 41.7] | 40.1 [34.9, 45.5] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 66.7 | 85.3 | 93.7 | 97.0 | 0.0 | 20.7 | 35.0 | 61.3 |
| query reasoner (before E2E) | 25.7 | 46.0 | 58.3 | 82.3 | 0.0 | 1.0 | 4.3 | 16.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 35.0 [29.7, 40.7] | 37.7 [32.5, 43.2] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 35.0 [29.7, 40.7] | 37.7 [32.5, 43.2] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 35.0 [29.7, 40.7] | 37.7 [32.5, 43.2] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 35.0 [29.7, 40.7] | 37.7 [32.5, 43.2] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 36.0 [30.7, 41.7] | 39.4 [34.1, 44.9] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 36.0 [30.7, 41.7] | 39.3 [33.9, 44.8] |
| score@32 | [15.3, 8.0, 4.4, 4.4] | 32.0 vectors | 36.0 [30.7, 41.7] | 39.3 [33.9, 44.8] |
| learned@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 36.0 [30.7, 41.7] | 39.4 [34.1, 44.9] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 34.7 [29.3, 40.3] | 38.1 [33.0, 43.6] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 34.7 [29.3, 40.0] | 37.7 [32.3, 43.0] |
| score@64 | [30.5, 16.0, 8.7, 8.7] | 64.0 vectors | 34.7 [29.3, 40.0] | 37.5 [32.2, 42.8] |
| learned@64 | [14.5, 16.9, 16.6, 15.9] | 64.0 vectors | 34.0 [28.7, 39.3] | 37.4 [32.1, 42.7] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.3, 40.0] | 37.7 [32.5, 43.1] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.3, 40.0] | 37.7 [32.5, 43.1] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.3, 40.0] | 37.7 [32.5, 43.1] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 34.3 [29.3, 40.0] | 37.7 [32.5, 43.1] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [8.0, 8.0, 8.0, 8.0] | 8.0 | 8.0 |
| 64 | [14.5, 16.9, 16.6, 15.9] | 17.0 | 15.2 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (200) | rank 2 (56) | rank 3+ (30) | not retrieved (14) |
|---|---|---|---|---|
| uniform@16 | 36.7 | 35.1 | 38.9 | 58.9 |
| top_heavy@16 | 36.7 | 35.1 | 38.9 | 58.9 |
| score@16 | 36.7 | 35.1 | 38.9 | 58.9 |
| learned@16 | 36.7 | 35.1 | 38.9 | 58.9 |
| uniform@32 | 39.6 | 35.7 | 35.6 | 58.9 |
| top_heavy@32 | 39.4 | 35.9 | 35.6 | 59.2 |
| score@32 | 39.4 | 35.9 | 35.6 | 59.2 |
| learned@32 | 39.6 | 35.7 | 35.6 | 58.9 |
| uniform@64 | 38.6 | 35.7 | 34.1 | 50.0 |
| top_heavy@64 | 38.6 | 32.6 | 34.1 | 52.0 |
| score@64 | 38.5 | 32.6 | 34.1 | 50.0 |
| learned@64 | 37.7 | 33.9 | 35.6 | 50.0 |
| uniform@128 | 38.7 | 34.5 | 30.7 | 52.0 |
| top_heavy@128 | 38.7 | 34.5 | 30.7 | 52.0 |
| score@128 | 38.7 | 34.5 | 30.7 | 52.0 |
| learned@128 | 38.7 | 34.5 | 30.7 | 52.0 |
| raw_bm25 | 23.6 | 24.3 | 20.5 | 26.7 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | +0.0 [+0.0, +0.0] | 1.000 | -0.1 [-0.5, +0.1] | 0.684 |
| score@32 vs uniform@32 | +0.0 [+0.0, +0.0] | 1.000 | -0.1 [-0.5, +0.1] | 0.684 |
| learned@32 vs uniform@32 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@32 vs top_heavy@32 | +0.0 [+0.0, +0.0] | 1.000 | +0.1 [-0.1, +0.5] | 0.368 |
| top_heavy@64 vs uniform@64 | +0.0 [-1.7, +1.7] | 0.597 | -0.5 [-1.9, +0.8] | 0.757 |
| score@64 vs uniform@64 | +0.0 [-1.7, +1.7] | 0.597 | -0.7 [-2.0, +0.6] | 0.841 |
| learned@64 vs uniform@64 | -0.7 [-2.3, +1.0] | 0.869 | -0.8 [-2.3, +0.5] | 0.867 |
| learned@64 vs top_heavy@64 | -0.7 [-1.7, +0.0] | 1.000 | -0.3 [-1.6, +0.8] | 0.670 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
