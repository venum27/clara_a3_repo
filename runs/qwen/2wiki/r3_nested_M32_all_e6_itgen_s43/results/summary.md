# Evaluation summary

Run: `runs/qwen/2wiki/r3_nested_M32_all_e6_itgen_s43`

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
| compressed_m4 | 36.3 [30.7, 42.0] | 39.2 [33.5, 44.6] | 10 vectors |
| compressed_m8 | 37.7 [32.0, 43.3] | 41.7 [36.4, 47.3] | 20 vectors |
| compressed_m16 | 38.7 [33.0, 44.7] | 42.6 [37.1, 48.2] | 40 vectors |
| compressed_m32 | 38.3 [33.0, 44.0] | 42.5 [37.1, 48.2] | 80 vectors |
| raw_text_gold | 21.3 [17.0, 26.0] | 33.9 [29.4, 38.5] | 391 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 58.3 | 80.0 | 85.7 | 94.7 | 0.0 | 12.0 | 22.0 | 36.0 |
| query reasoner (after E2E) | 66.3 | 84.3 | 92.0 | 97.7 | 0.0 | 21.3 | 34.0 | 59.7 |
| query reasoner (before E2E) | 25.7 | 46.0 | 58.3 | 82.3 | 0.0 | 1.0 | 4.3 | 16.3 |
| random (expected) | 24.9 | 44.9 | 60.7 | 82.7 | 0.0 | 1.7 | 5.0 | 17.3 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 35.0 [29.7, 40.7] | 38.1 [32.8, 43.9] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 35.0 [29.7, 40.7] | 38.1 [32.8, 43.9] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 35.0 [29.7, 40.7] | 38.1 [32.8, 43.9] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 35.0 [29.7, 40.7] | 38.5 [33.3, 44.0] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 35.3 [30.0, 41.0] | 39.1 [33.8, 44.5] |
| score@32 | [15.3, 8.0, 4.4, 4.4] | 32.0 vectors | 35.3 [30.0, 41.0] | 39.0 [33.7, 44.4] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 36.7 [31.3, 42.3] | 40.6 [35.2, 46.0] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 36.3 [30.7, 42.0] | 40.0 [34.6, 45.4] |
| score@64 | [30.6, 16.0, 8.7, 8.7] | 64.0 vectors | 36.3 [30.7, 42.0] | 40.0 [34.6, 45.4] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.7 [30.3, 41.7] | 39.2 [34.1, 44.8] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.7 [30.3, 41.7] | 39.2 [34.1, 44.8] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 35.7 [30.3, 41.7] | 39.2 [34.1, 44.8] |
| raw_bm25 | - | 490 tokens | 15.7 [11.7, 20.0] | 23.6 [19.8, 27.8] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (199) | rank 2 (54) | rank 3+ (35) | not retrieved (12) |
|---|---|---|---|---|
| uniform@16 | 35.9 | 39.9 | 47.6 | 39.9 |
| top_heavy@16 | 35.9 | 39.9 | 47.6 | 39.9 |
| score@16 | 35.9 | 39.9 | 47.6 | 39.9 |
| uniform@32 | 38.0 | 36.6 | 44.7 | 36.7 |
| top_heavy@32 | 38.7 | 37.5 | 44.7 | 36.7 |
| score@32 | 38.6 | 37.5 | 44.7 | 36.7 |
| uniform@64 | 39.3 | 40.8 | 46.8 | 44.0 |
| top_heavy@64 | 38.8 | 40.8 | 43.9 | 44.0 |
| score@64 | 38.8 | 40.8 | 43.9 | 44.0 |
| uniform@128 | 37.9 | 40.1 | 43.9 | 44.0 |
| top_heavy@128 | 37.9 | 40.1 | 43.9 | 44.0 |
| score@128 | 37.9 | 40.1 | 43.9 | 44.0 |
| raw_bm25 | 24.9 | 19.6 | 18.8 | 33.1 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +0.3 [+0.0, +1.0] | 0.354 | +0.6 [-0.1, +1.5] | 0.053 |
| score@32 vs uniform@32 | +0.3 [+0.0, +1.0] | 0.354 | +0.5 [-0.2, +1.4] | 0.080 |
| top_heavy@64 vs uniform@64 | -0.3 [-1.7, +0.7] | 0.826 | -0.7 [-2.0, +0.5] | 0.871 |
| score@64 vs uniform@64 | -0.3 [-1.7, +0.7] | 0.826 | -0.7 [-2.0, +0.5] | 0.871 |
