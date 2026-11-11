# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_itgen_s43`

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
| compressed_m4 | 13.7 [10.0, 18.0] | 21.4 [17.5, 25.9] | 8 vectors |
| compressed_m8 | 13.3 [9.7, 17.3] | 21.6 [17.5, 25.9] | 16 vectors |
| compressed_m16 | 14.3 [10.7, 18.7] | 22.1 [17.9, 26.5] | 32 vectors |
| compressed_m32 | 15.0 [11.3, 19.3] | 23.3 [19.1, 27.7] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 60.3 | 76.0 | 85.0 | 96.0 | 0.0 | 20.7 | 34.0 | 59.3 |
| query reasoner (before E2E) | 39.0 | 54.7 | 66.7 | 85.3 | 0.0 | 10.3 | 17.7 | 34.0 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.3 [9.7, 17.3] | 19.3 [15.4, 23.5] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.3 [9.7, 17.3] | 19.3 [15.4, 23.5] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.3 [9.7, 17.3] | 19.3 [15.4, 23.5] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 13.7 [10.0, 18.0] | 20.3 [16.3, 24.6] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 14.0 [10.3, 18.3] | 20.9 [17.0, 25.4] |
| score@32 | [15.5, 8.0, 4.3, 4.3] | 32.0 vectors | 14.0 [10.3, 18.3] | 20.9 [17.0, 25.4] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 13.7 [10.0, 17.7] | 20.4 [16.6, 24.6] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 14.3 [10.7, 18.7] | 21.0 [17.0, 25.3] |
| score@64 | [30.9, 16.0, 8.5, 8.5] | 64.0 vectors | 14.3 [10.7, 18.7] | 20.9 [17.0, 25.2] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.3 [10.0, 17.3] | 20.7 [16.7, 24.9] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.3 [10.0, 17.3] | 20.7 [16.7, 24.9] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.3 [10.0, 17.3] | 20.7 [16.7, 24.9] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (181) | rank 2 (47) | rank 3+ (46) | not retrieved (26) |
|---|---|---|---|---|
| uniform@16 | 21.2 | 12.9 | 21.8 | 13.0 |
| top_heavy@16 | 21.2 | 12.9 | 21.8 | 13.0 |
| score@16 | 21.2 | 12.9 | 21.8 | 13.0 |
| uniform@32 | 22.7 | 18.7 | 15.7 | 14.6 |
| top_heavy@32 | 24.0 | 16.5 | 16.6 | 14.6 |
| score@32 | 24.0 | 16.5 | 16.6 | 14.6 |
| uniform@64 | 22.4 | 17.5 | 19.4 | 13.5 |
| top_heavy@64 | 23.6 | 15.2 | 21.2 | 12.6 |
| score@64 | 23.5 | 15.2 | 21.2 | 12.6 |
| uniform@128 | 21.3 | 20.1 | 22.6 | 13.8 |
| top_heavy@128 | 21.3 | 20.1 | 22.6 | 13.8 |
| score@128 | 21.3 | 20.1 | 22.6 | 13.8 |
| raw_bm25 | 21.8 | 17.9 | 27.5 | 17.1 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| top_heavy@32 vs uniform@32 | +0.3 [+0.0, +1.0] | 0.364 | +0.6 [-0.4, +1.7] | 0.132 |
| score@32 vs uniform@32 | +0.3 [+0.0, +1.0] | 0.364 | +0.6 [-0.4, +1.7] | 0.128 |
| top_heavy@64 vs uniform@64 | +0.7 [-0.7, +2.0] | 0.232 | +0.6 [-0.9, +2.1] | 0.240 |
| score@64 vs uniform@64 | +0.7 [-0.7, +2.0] | 0.232 | +0.5 [-1.0, +2.0] | 0.258 |
