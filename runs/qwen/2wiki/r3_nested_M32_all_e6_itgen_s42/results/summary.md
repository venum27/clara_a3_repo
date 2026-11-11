# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_itgen_s42`

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
| compressed_m4 | 33.3 [28.0, 39.0] | 36.4 [31.1, 41.8] | 10 vectors |
| compressed_m8 | 34.7 [29.3, 40.3] | 38.8 [33.5, 44.4] | 20 vectors |
| compressed_m16 | 35.3 [30.3, 41.0] | 39.2 [33.9, 44.6] | 40 vectors |
| compressed_m32 | 35.7 [30.7, 41.0] | 39.7 [34.6, 44.9] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 67.7 | 87.3 | 93.7 | 97.3 | 0.0 | 23.3 | 37.7 | 64.3 |
| query reasoner (before E2E) | 25.7 | 46.0 | 58.3 | 82.3 | 0.0 | 1.0 | 4.3 | 16.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 31.7 [26.3, 37.0] | 34.5 [29.2, 40.0] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 31.7 [26.3, 37.0] | 34.5 [29.2, 40.0] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 31.7 [26.3, 37.0] | 34.5 [29.2, 40.0] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 32.7 [27.7, 38.0] | 35.8 [30.7, 41.3] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 33.3 [28.0, 38.7] | 36.6 [31.4, 42.0] |
| score@32 | [15.3, 8.0, 4.4, 4.4] | 32.0 vectors | 33.3 [28.0, 38.7] | 36.7 [31.5, 42.0] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 32.7 [27.7, 38.3] | 36.1 [31.0, 41.6] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 32.7 [27.3, 38.3] | 36.6 [31.5, 42.1] |
| score@64 | [30.5, 16.0, 8.7, 8.7] | 64.0 vectors | 32.7 [27.3, 38.3] | 36.6 [31.5, 42.1] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 32.7 [27.7, 38.0] | 36.7 [31.8, 42.1] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 32.7 [27.7, 38.0] | 36.7 [31.8, 42.1] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 32.7 [27.7, 38.0] | 36.7 [31.8, 42.1] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (203) | rank 2 (59) | rank 3+ (27) | not retrieved (11) |
|---|---|---|---|---|
| uniform@16 | 33.5 | 34.2 | 41.6 | 36.4 |
| top_heavy@16 | 33.5 | 34.2 | 41.6 | 36.4 |
| score@16 | 33.5 | 34.2 | 41.6 | 36.4 |
| uniform@32 | 36.7 | 29.5 | 41.6 | 39.4 |
| top_heavy@32 | 37.5 | 31.1 | 41.6 | 36.4 |
| score@32 | 37.7 | 31.1 | 41.6 | 36.4 |
| uniform@64 | 36.7 | 31.1 | 41.6 | 39.4 |
| top_heavy@64 | 37.3 | 31.5 | 41.6 | 39.4 |
| score@64 | 37.3 | 31.5 | 41.6 | 39.4 |
| uniform@128 | 36.6 | 33.4 | 41.6 | 45.5 |
| top_heavy@128 | 36.6 | 33.4 | 41.6 | 45.5 |
| score@128 | 36.6 | 33.4 | 41.6 | 45.5 |
| raw_bm25 | 23.0 | 23.9 | 20.8 | 39.0 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +0.7 [-0.7, +2.0] | 0.226 | +0.8 [-0.7, +2.3] | 0.152 |
| score@32 vs uniform@32 | +0.7 [-0.7, +2.0] | 0.226 | +0.9 [-0.6, +2.3] | 0.120 |
| top_heavy@64 vs uniform@64 | +0.0 [-1.3, +1.3] | 0.619 | +0.5 [-1.0, +2.0] | 0.260 |
| score@64 vs uniform@64 | +0.0 [-1.3, +1.3] | 0.619 | +0.5 [-1.0, +2.0] | 0.260 |
