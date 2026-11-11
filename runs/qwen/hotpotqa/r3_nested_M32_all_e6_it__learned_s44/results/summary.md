# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_it__learned_s44`

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
| compressed_m4 | 14.3 [10.7, 18.3] | 22.4 [18.4, 26.5] | 8 vectors |
| compressed_m8 | 14.3 [10.7, 18.3] | 22.8 [18.7, 27.0] | 16 vectors |
| compressed_m16 | 14.3 [10.7, 18.3] | 23.5 [19.5, 27.6] | 32 vectors |
| compressed_m32 | 14.3 [10.3, 18.7] | 23.5 [19.5, 27.8] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 50.3 | 71.0 | 83.3 | 95.3 | 0.0 | 13.7 | 29.0 | 54.0 |
| query reasoner (before E2E) | 36.7 | 51.0 | 62.7 | 81.7 | 0.0 | 8.3 | 16.3 | 29.3 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.0, 16.3] | 20.1 [16.3, 24.1] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.0, 16.3] | 20.1 [16.3, 24.1] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.0, 16.3] | 20.1 [16.3, 24.1] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 12.7 [9.0, 16.3] | 20.1 [16.3, 24.1] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 12.7 [9.0, 16.7] | 20.3 [16.4, 24.3] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 12.7 [9.0, 16.7] | 20.1 [16.2, 24.1] |
| score@32 | [15.3, 8.0, 4.3, 4.3] | 32.0 vectors | 12.7 [9.0, 16.7] | 20.1 [16.2, 24.1] |
| learned@32 | [15.3, 7.2, 5.2, 4.2] | 32.0 vectors | 12.7 [9.0, 16.7] | 20.3 [16.3, 24.4] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 14.7 [11.0, 18.7] | 21.7 [17.6, 26.0] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 14.0 [10.3, 18.0] | 20.6 [16.6, 24.7] |
| score@64 | [30.7, 16.0, 8.7, 8.7] | 64.0 vectors | 14.0 [10.3, 18.0] | 20.6 [16.6, 24.7] |
| learned@64 | [16.2, 30.2, 9.5, 8.1] | 64.0 vectors | 14.7 [11.0, 18.7] | 20.9 [17.0, 25.1] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.3 [10.3, 18.3] | 20.7 [16.7, 24.9] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.3 [10.3, 18.3] | 20.7 [16.7, 24.9] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.3 [10.3, 18.3] | 20.7 [16.7, 24.9] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.3 [10.3, 18.3] | 20.7 [16.7, 24.9] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [15.3, 7.2, 5.2, 4.2] | 9.6 | 7.2 |
| 64 | [16.2, 30.2, 9.5, 8.1] | 17.4 | 15.3 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (151) | rank 2 (62) | rank 3+ (56) | not retrieved (31) |
|---|---|---|---|---|
| uniform@16 | 23.8 | 21.2 | 12.7 | 13.1 |
| top_heavy@16 | 23.8 | 21.2 | 12.7 | 13.1 |
| score@16 | 23.8 | 21.2 | 12.7 | 13.1 |
| learned@16 | 23.8 | 21.2 | 12.7 | 13.1 |
| uniform@32 | 23.4 | 21.3 | 13.9 | 14.5 |
| top_heavy@32 | 23.2 | 19.6 | 14.5 | 16.1 |
| score@32 | 23.2 | 19.6 | 14.5 | 16.1 |
| learned@32 | 23.0 | 20.3 | 14.5 | 17.7 |
| uniform@64 | 25.1 | 20.9 | 13.6 | 21.2 |
| top_heavy@64 | 23.7 | 19.8 | 12.4 | 21.2 |
| score@64 | 23.7 | 19.9 | 12.4 | 21.2 |
| learned@64 | 23.2 | 21.9 | 13.2 | 21.2 |
| uniform@128 | 23.5 | 22.4 | 14.2 | 16.0 |
| top_heavy@128 | 23.5 | 22.4 | 14.2 | 16.0 |
| score@128 | 23.5 | 22.4 | 14.2 | 16.0 |
| learned@128 | 23.5 | 22.4 | 14.2 | 16.0 |
| raw_bm25 | 23.3 | 21.3 | 18.8 | 20.1 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | +0.0 [-1.3, +1.3] | 0.632 | -0.2 [-1.1, +0.9] | 0.652 |
| score@32 vs uniform@32 | +0.0 [-1.3, +1.3] | 0.632 | -0.2 [-1.0, +0.9] | 0.647 |
| learned@32 vs uniform@32 | +0.0 [-1.3, +1.3] | 0.632 | +0.0 [-0.8, +1.1] | 0.491 |
| learned@32 vs top_heavy@32 | +0.0 [+0.0, +0.0] | 1.000 | +0.2 [-0.2, +0.7] | 0.212 |
| top_heavy@64 vs uniform@64 | -0.7 [-2.0, +0.7] | 0.898 | -1.1 [-2.6, +0.5] | 0.918 |
| score@64 vs uniform@64 | -0.7 [-2.0, +0.7] | 0.898 | -1.1 [-2.6, +0.5] | 0.915 |
| learned@64 vs uniform@64 | +0.0 [-1.0, +1.0] | 0.626 | -0.8 [-2.1, +0.5] | 0.892 |
| learned@64 vs top_heavy@64 | +0.7 [+0.0, +1.7] | 0.126 | +0.3 [-0.6, +1.4] | 0.274 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
