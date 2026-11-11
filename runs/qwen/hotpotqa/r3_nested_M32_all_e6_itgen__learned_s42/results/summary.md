# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_itgen__learned_s42`

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
| compressed_m4 | 14.3 [10.7, 18.3] | 22.0 [18.0, 26.2] | 8 vectors |
| compressed_m8 | 14.7 [11.0, 19.0] | 23.2 [19.2, 27.7] | 16 vectors |
| compressed_m16 | 14.3 [10.7, 18.7] | 23.0 [18.8, 27.3] | 32 vectors |
| compressed_m32 | 16.0 [12.0, 20.7] | 24.8 [20.6, 29.4] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 53.3 | 70.3 | 81.3 | 94.3 | 0.0 | 20.7 | 36.0 | 60.0 |
| query reasoner (before E2E) | 39.0 | 54.7 | 66.7 | 85.3 | 0.0 | 10.3 | 17.7 | 34.0 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.3 [9.7, 17.3] | 19.9 [16.0, 24.0] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.3 [9.7, 17.3] | 19.9 [16.0, 24.0] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.3 [9.7, 17.3] | 19.9 [16.0, 24.0] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 13.3 [9.7, 17.3] | 19.9 [16.0, 24.0] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 14.0 [10.3, 18.0] | 20.2 [16.2, 24.3] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 14.0 [10.3, 18.0] | 20.5 [16.7, 24.7] |
| score@32 | [15.3, 8.0, 4.3, 4.3] | 32.0 vectors | 14.0 [10.3, 18.0] | 20.5 [16.7, 24.7] |
| learned@32 | [13.1, 9.9, 4.2, 4.9] | 32.0 vectors | 14.0 [10.3, 18.0] | 20.1 [16.3, 24.4] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 14.0 [10.3, 18.0] | 20.7 [16.8, 24.9] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 14.7 [11.0, 19.0] | 21.4 [17.5, 25.7] |
| score@64 | [30.7, 16.0, 8.7, 8.7] | 64.0 vectors | 14.7 [11.0, 19.0] | 21.4 [17.4, 25.7] |
| learned@64 | [14.4, 14.7, 22.0, 12.9] | 64.0 vectors | 14.0 [10.3, 18.0] | 21.6 [17.6, 25.7] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.0 [10.3, 18.3] | 20.7 [16.8, 24.9] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.0 [10.3, 18.3] | 20.7 [16.8, 24.9] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.0 [10.3, 18.3] | 20.7 [16.8, 24.9] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 14.0 [10.3, 18.3] | 20.7 [16.8, 24.9] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [13.1, 9.9, 4.2, 4.9] | 9.3 | 7.3 |
| 64 | [14.4, 14.7, 22.0, 12.9] | 16.3 | 15.8 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (160) | rank 2 (51) | rank 3+ (56) | not retrieved (33) |
|---|---|---|---|---|
| uniform@16 | 23.6 | 19.3 | 19.7 | 3.7 |
| top_heavy@16 | 23.6 | 19.3 | 19.7 | 3.7 |
| score@16 | 23.6 | 19.3 | 19.7 | 3.7 |
| learned@16 | 23.6 | 19.3 | 19.7 | 3.7 |
| uniform@32 | 23.4 | 17.8 | 21.6 | 6.1 |
| top_heavy@32 | 24.0 | 19.1 | 20.8 | 5.4 |
| score@32 | 24.0 | 19.1 | 20.8 | 5.4 |
| learned@32 | 23.8 | 17.8 | 20.5 | 5.4 |
| uniform@64 | 25.5 | 17.0 | 18.9 | 6.4 |
| top_heavy@64 | 25.2 | 19.4 | 21.1 | 6.8 |
| score@64 | 25.2 | 19.0 | 21.1 | 6.8 |
| learned@64 | 25.3 | 17.5 | 22.3 | 8.3 |
| uniform@128 | 23.4 | 20.2 | 20.9 | 7.8 |
| top_heavy@128 | 23.4 | 20.2 | 20.9 | 7.8 |
| score@128 | 23.4 | 20.2 | 20.9 | 7.8 |
| learned@128 | 23.4 | 20.2 | 20.9 | 7.8 |
| raw_bm25 | 22.4 | 27.1 | 19.2 | 14.2 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | +0.0 [-1.3, +1.3] | 0.609 | +0.3 [-0.9, +1.7] | 0.311 |
| score@32 vs uniform@32 | +0.0 [-1.3, +1.3] | 0.609 | +0.3 [-0.9, +1.7] | 0.311 |
| learned@32 vs uniform@32 | +0.0 [-1.3, +1.3] | 0.609 | -0.0 [-1.2, +1.1] | 0.553 |
| learned@32 vs top_heavy@32 | +0.0 [+0.0, +0.0] | 1.000 | -0.4 [-1.2, +0.2] | 0.902 |
| top_heavy@64 vs uniform@64 | +0.7 [+0.0, +1.7] | 0.141 | +0.7 [-0.4, +2.1] | 0.130 |
| score@64 vs uniform@64 | +0.7 [+0.0, +1.7] | 0.141 | +0.6 [-0.5, +2.0] | 0.170 |
| learned@64 vs uniform@64 | +0.0 [+0.0, +0.0] | 1.000 | +0.8 [-0.2, +1.9] | 0.056 |
| learned@64 vs top_heavy@64 | -0.7 [-1.7, +0.0] | 1.000 | +0.1 [-1.2, +1.2] | 0.388 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
