# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_it__learned_s42`

All scores in %, with 95% bootstrap confidence intervals in brackets.

## Parameters and compression

- Backbone: Qwen/Qwen2.5-0.5B-Instruct (decoder-only), base parameters: 494,032,768
- LoRA parameters per adapter: {'compressor': 2162688, 'generator': 2162688, 'query_reasoner': 2162688}
- Memory-embedding parameters: 57,344
- Average passage length: 132.5 tokens; compression rate by prefix: m=4: 33.1x, m=8: 16.6x, m=16: 8.3x, m=32: 4.1x

## Compressor-only QA on held-out synthetic questions (SCP checkpoint)

| Prefix m | EM | F1 | n |
|---|---|---|---|
| 4 | 5.6 [3.7, 7.5] | 16.3 [13.9, 18.8] | 520 |
| 8 | 5.4 [3.5, 7.3] | 16.0 [13.4, 18.5] | 520 |
| 16 | 5.8 [3.8, 7.7] | 16.2 [13.8, 18.7] | 520 |
| 32 | 5.0 [3.3, 6.9] | 15.8 [13.5, 18.2] | 520 |

## Oracle: gold passages only

| Input | EM | F1 | Context size |
|---|---|---|---|
| compressed_m4 | 14.3 [10.7, 18.3] | 23.3 [19.3, 27.5] | 8 vectors |
| compressed_m8 | 14.0 [10.3, 18.0] | 22.8 [18.9, 27.1] | 16 vectors |
| compressed_m16 | 14.0 [10.3, 18.3] | 23.2 [19.1, 27.5] | 32 vectors |
| compressed_m32 | 12.7 [9.0, 16.7] | 21.8 [17.7, 25.9] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 50.0 | 67.0 | 80.3 | 92.3 | 0.0 | 12.7 | 25.3 | 47.3 |
| query reasoner (before E2E) | 36.7 | 51.0 | 62.7 | 81.7 | 0.0 | 8.3 | 16.3 | 29.3 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.3, 16.3] | 19.5 [15.6, 23.6] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.3, 16.3] | 19.5 [15.6, 23.6] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.3, 16.3] | 19.5 [15.6, 23.6] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.3, 16.3] | 19.5 [15.6, 23.6] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 11.7 [8.3, 15.3] | 19.4 [15.5, 23.3] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 12.3 [9.0, 16.0] | 19.6 [15.7, 23.6] |
| score@32 | [15.5, 8.0, 4.2, 4.2] | 32.0 vectors | 12.3 [9.0, 16.0] | 19.8 [15.9, 23.8] |
| learned@32 | [10.0, 8.0, 7.2, 6.8] | 32.0 vectors | 11.3 [8.0, 15.0] | 19.5 [15.7, 23.4] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 13.3 [9.7, 17.3] | 20.1 [16.1, 24.2] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 13.7 [10.0, 17.7] | 20.6 [16.6, 24.6] |
| score@64 | [31.0, 16.0, 8.5, 8.5] | 64.0 vectors | 13.7 [10.0, 17.7] | 20.6 [16.6, 24.6] |
| learned@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 13.3 [9.7, 17.3] | 20.1 [16.1, 24.2] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.0] | 19.4 [15.5, 23.4] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.0] | 19.4 [15.5, 23.4] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.0] | 19.4 [15.5, 23.4] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.0] | 19.4 [15.5, 23.4] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [10.0, 8.0, 7.2, 6.8] | 8.9 | 7.6 |
| 64 | [16.0, 16.0, 16.0, 16.0] | 16.0 | 16.0 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (150) | rank 2 (51) | rank 3+ (61) | not retrieved (38) |
|---|---|---|---|---|
| uniform@16 | 25.1 | 11.0 | 16.5 | 13.5 |
| top_heavy@16 | 25.1 | 11.0 | 16.5 | 13.5 |
| score@16 | 25.1 | 11.0 | 16.5 | 13.5 |
| learned@16 | 25.1 | 11.0 | 16.5 | 13.5 |
| uniform@32 | 24.1 | 15.0 | 15.9 | 12.2 |
| top_heavy@32 | 25.0 | 11.8 | 15.6 | 15.4 |
| score@32 | 25.0 | 12.6 | 15.6 | 15.4 |
| learned@32 | 24.5 | 14.6 | 16.0 | 12.2 |
| uniform@64 | 26.1 | 9.7 | 17.5 | 14.5 |
| top_heavy@64 | 26.9 | 10.9 | 17.4 | 13.8 |
| score@64 | 26.9 | 10.9 | 17.4 | 13.8 |
| learned@64 | 26.1 | 9.7 | 17.5 | 14.5 |
| uniform@128 | 24.9 | 12.7 | 16.3 | 11.5 |
| top_heavy@128 | 24.9 | 12.7 | 16.3 | 11.5 |
| score@128 | 24.9 | 12.7 | 16.3 | 11.5 |
| learned@128 | 24.9 | 12.7 | 16.3 | 11.5 |
| raw_bm25 | 23.2 | 19.4 | 20.3 | 21.1 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | +0.7 [-0.7, +2.3] | 0.237 | +0.3 [-0.9, +1.6] | 0.348 |
| score@32 vs uniform@32 | +0.7 [-0.7, +2.3] | 0.237 | +0.4 [-0.8, +1.7] | 0.268 |
| learned@32 vs uniform@32 | -0.3 [-1.3, +0.7] | 0.819 | +0.2 [-0.2, +0.6] | 0.239 |
| learned@32 vs top_heavy@32 | -1.0 [-2.3, +0.0] | 1.000 | -0.1 [-1.4, +1.0] | 0.558 |
| top_heavy@64 vs uniform@64 | +0.3 [+0.0, +1.0] | 0.357 | +0.5 [-0.4, +1.4] | 0.144 |
| score@64 vs uniform@64 | +0.3 [+0.0, +1.0] | 0.357 | +0.5 [-0.4, +1.4] | 0.144 |
| learned@64 vs uniform@64 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@64 vs top_heavy@64 | -0.3 [-1.0, +0.0] | 1.000 | -0.5 [-1.4, +0.4] | 0.856 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
