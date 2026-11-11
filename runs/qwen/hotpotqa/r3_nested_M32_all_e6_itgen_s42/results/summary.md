# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_itgen_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Parameters and compression

- Backbone: Qwen/Qwen2.5-0.5B-Instruct (decoder-only), base parameters: 494,032,768
- LoRA parameters per adapter: {'compressor': 2162688, 'generator': 2162688, 'query_reasoner': 2162688}
- Memory-embedding parameters: 57,344
- Average passage length: 132.5 tokens; compression rate by prefix: m=4: 33.1x, m=8: 16.6x, m=16: 8.3x, m=32: 4.1x

## Compressor-only QA on held-out synthetic questions (SCP checkpoint)

| Prefix m | EM | F1 | n |
|---|---|---|---|
| 4 | 6.7 [4.6, 9.0] | 17.2 [14.7, 19.8] | 520 |
| 8 | 7.1 [5.0, 9.4] | 18.0 [15.4, 20.5] | 520 |
| 16 | 6.3 [4.4, 8.5] | 16.9 [14.4, 19.4] | 520 |
| 32 | 7.1 [5.0, 9.2] | 17.4 [14.8, 20.0] | 520 |

## Oracle: gold passages only

| Input | EM | F1 | Context size |
|---|---|---|---|
| compressed_m4 | 15.3 [11.3, 19.7] | 23.7 [19.5, 28.2] | 8 vectors |
| compressed_m8 | 15.0 [11.0, 19.3] | 23.2 [19.1, 27.7] | 16 vectors |
| compressed_m16 | 15.7 [11.7, 20.0] | 23.1 [18.9, 27.5] | 32 vectors |
| compressed_m32 | 15.7 [11.7, 19.7] | 24.5 [20.4, 28.9] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 57.0 | 78.3 | 86.3 | 96.7 | 0.0 | 20.7 | 34.7 | 60.7 |
| query reasoner (before E2E) | 39.0 | 54.7 | 66.7 | 85.3 | 0.0 | 10.3 | 17.7 | 34.0 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.7 [10.0, 17.7] | 20.4 [16.4, 24.6] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.7 [10.0, 17.7] | 20.4 [16.4, 24.6] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.7 [10.0, 17.7] | 20.4 [16.4, 24.6] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 13.3 [9.7, 17.3] | 19.4 [15.6, 23.6] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 13.7 [10.0, 17.7] | 20.1 [16.1, 24.3] |
| score@32 | [15.5, 8.0, 4.3, 4.3] | 32.0 vectors | 13.7 [10.0, 17.7] | 19.8 [15.9, 24.1] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 14.0 [10.3, 18.0] | 21.3 [17.2, 25.5] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 14.3 [10.3, 18.3] | 20.6 [16.6, 24.8] |
| score@64 | [31.0, 16.0, 8.5, 8.5] | 64.0 vectors | 14.3 [10.3, 18.3] | 21.0 [16.9, 25.2] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.7 [11.0, 18.7] | 21.9 [17.9, 26.1] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.7 [11.0, 18.7] | 21.9 [17.9, 26.1] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.7 [11.0, 18.7] | 21.9 [17.9, 26.1] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (171) | rank 2 (64) | rank 3+ (45) | not retrieved (20) |
|---|---|---|---|---|
| uniform@16 | 22.2 | 18.8 | 17.3 | 16.9 |
| top_heavy@16 | 22.2 | 18.8 | 17.3 | 16.9 |
| score@16 | 22.2 | 18.8 | 17.3 | 16.9 |
| uniform@32 | 19.7 | 21.4 | 17.0 | 15.9 |
| top_heavy@32 | 21.2 | 21.4 | 15.6 | 16.2 |
| score@32 | 20.8 | 21.4 | 15.6 | 16.2 |
| uniform@64 | 23.2 | 22.5 | 17.1 | 9.7 |
| top_heavy@64 | 22.2 | 21.8 | 17.8 | 9.7 |
| score@64 | 22.9 | 21.8 | 17.8 | 9.7 |
| uniform@128 | 24.3 | 20.1 | 20.0 | 10.9 |
| top_heavy@128 | 24.3 | 20.1 | 20.0 | 10.9 |
| score@128 | 24.3 | 20.1 | 20.0 | 10.9 |
| raw_bm25 | 24.4 | 18.7 | 14.9 | 23.3 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +0.3 [-0.7, +1.3] | 0.409 | +0.7 [-0.3, +1.9] | 0.127 |
| score@32 vs uniform@32 | +0.3 [-0.7, +1.3] | 0.409 | +0.5 [-0.4, +1.5] | 0.223 |
| top_heavy@64 vs uniform@64 | +0.3 [+0.0, +1.0] | 0.363 | -0.6 [-1.8, +0.7] | 0.846 |
| score@64 vs uniform@64 | +0.3 [+0.0, +1.0] | 0.363 | -0.3 [-1.4, +0.9] | 0.690 |
