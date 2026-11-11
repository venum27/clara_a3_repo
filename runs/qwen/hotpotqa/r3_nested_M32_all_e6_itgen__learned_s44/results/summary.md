# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_itgen__learned_s44`

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
| compressed_m4 | 16.3 [12.3, 20.7] | 24.7 [20.5, 29.1] | 8 vectors |
| compressed_m8 | 15.7 [11.7, 20.0] | 24.4 [20.1, 28.8] | 16 vectors |
| compressed_m16 | 16.3 [12.3, 20.7] | 24.4 [19.9, 28.9] | 32 vectors |
| compressed_m32 | 16.0 [11.7, 20.3] | 24.2 [19.9, 28.6] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 59.3 | 78.7 | 88.0 | 96.0 | 0.0 | 20.7 | 35.7 | 62.3 |
| query reasoner (before E2E) | 39.0 | 54.7 | 66.7 | 85.3 | 0.0 | 10.3 | 17.7 | 34.0 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 16.7 [12.7, 21.0] | 23.0 [18.8, 27.4] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 16.7 [12.7, 21.0] | 23.0 [18.8, 27.4] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 16.7 [12.7, 21.0] | 23.0 [18.8, 27.4] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 16.7 [12.7, 21.0] | 23.0 [18.8, 27.4] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 15.7 [11.7, 20.0] | 22.5 [18.4, 26.8] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 16.3 [12.3, 20.7] | 23.0 [18.7, 27.3] |
| score@32 | [15.5, 8.0, 4.3, 4.3] | 32.0 vectors | 16.0 [12.0, 20.3] | 22.7 [18.5, 27.1] |
| learned@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 15.7 [11.7, 20.0] | 22.5 [18.4, 26.8] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 16.3 [12.3, 20.7] | 21.6 [17.4, 26.1] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 16.3 [12.3, 20.7] | 22.3 [18.1, 26.7] |
| score@64 | [31.0, 16.0, 8.5, 8.5] | 64.0 vectors | 16.0 [12.0, 20.3] | 22.0 [17.7, 26.3] |
| learned@64 | [31.9, 13.0, 9.7, 9.4] | 64.0 vectors | 16.7 [12.7, 21.0] | 22.4 [18.1, 26.8] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 16.0 [12.0, 20.3] | 23.3 [19.1, 27.6] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 16.0 [12.0, 20.3] | 23.3 [19.1, 27.6] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 16.0 [12.0, 20.3] | 23.3 [19.1, 27.6] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 16.0 [12.0, 20.3] | 23.3 [19.1, 27.6] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [8.0, 8.0, 8.0, 8.0] | 8.0 | 8.0 |
| 64 | [31.9, 13.0, 9.7, 9.4] | 19.5 | 14.0 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (178) | rank 2 (58) | rank 3+ (41) | not retrieved (23) |
|---|---|---|---|---|
| uniform@16 | 26.0 | 21.9 | 17.0 | 14.2 |
| top_heavy@16 | 26.0 | 21.9 | 17.0 | 14.2 |
| score@16 | 26.0 | 21.9 | 17.0 | 14.2 |
| learned@16 | 26.0 | 21.9 | 17.0 | 14.2 |
| uniform@32 | 25.1 | 23.9 | 11.0 | 19.3 |
| top_heavy@32 | 25.7 | 24.3 | 11.0 | 19.3 |
| score@32 | 25.5 | 23.7 | 11.0 | 19.3 |
| learned@32 | 25.1 | 23.9 | 11.0 | 19.3 |
| uniform@64 | 23.0 | 22.1 | 15.9 | 19.4 |
| top_heavy@64 | 23.8 | 23.5 | 13.8 | 23.1 |
| score@64 | 23.3 | 23.5 | 13.8 | 23.1 |
| learned@64 | 24.4 | 23.7 | 13.8 | 19.4 |
| uniform@128 | 24.3 | 23.4 | 18.7 | 24.1 |
| top_heavy@128 | 24.3 | 23.4 | 18.7 | 24.1 |
| score@128 | 24.3 | 23.4 | 18.7 | 24.1 |
| learned@128 | 24.3 | 23.4 | 18.7 | 24.1 |
| raw_bm25 | 22.5 | 22.6 | 20.4 | 15.3 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | +0.7 [-0.7, +2.0] | 0.220 | +0.4 [-0.8, +1.8] | 0.262 |
| score@32 vs uniform@32 | +0.3 [-0.7, +1.7] | 0.392 | +0.2 [-1.0, +1.5] | 0.390 |
| learned@32 vs uniform@32 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@32 vs top_heavy@32 | -0.7 [-2.0, +0.7] | 0.899 | -0.4 [-1.8, +0.8] | 0.738 |
| top_heavy@64 vs uniform@64 | +0.0 [-1.3, +1.3] | 0.599 | +0.8 [-0.9, +2.4] | 0.167 |
| score@64 vs uniform@64 | -0.3 [-1.7, +0.7] | 0.813 | +0.4 [-1.0, +1.9] | 0.288 |
| learned@64 vs uniform@64 | +0.3 [-1.0, +1.7] | 0.411 | +0.8 [-0.8, +2.5] | 0.159 |
| learned@64 vs top_heavy@64 | +0.3 [+0.0, +1.0] | 0.385 | +0.1 [-0.8, +1.0] | 0.410 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
