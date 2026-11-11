# Evaluation summary

Run: `runs/qwen/hotpotqa/r3_nested_M32_all_e6_itgen__learned_s43`

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
| compressed_m4 | 12.3 [8.7, 16.3] | 19.9 [15.9, 24.1] | 8 vectors |
| compressed_m8 | 13.3 [9.7, 17.7] | 20.4 [16.4, 24.7] | 16 vectors |
| compressed_m16 | 14.0 [10.3, 18.3] | 21.1 [17.0, 25.5] | 32 vectors |
| compressed_m32 | 12.7 [9.0, 16.7] | 21.6 [17.6, 25.8] | 64 vectors |
| raw_text_gold | 20.3 [16.0, 25.0] | 35.5 [31.2, 39.8] | 210 tokens |

## Retrieval

| Method | hit@1 | hit@2 | hit@3 | hit@5 | all_gold@1 | all_gold@2 | all_gold@3 | all_gold@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 | 68.7 | 84.0 | 89.3 | 95.0 | 0.0 | 20.7 | 34.3 | 51.3 |
| query reasoner (after E2E) | 55.3 | 77.3 | 83.7 | 95.7 | 0.0 | 18.3 | 34.0 | 60.7 |
| query reasoner (before E2E) | 39.0 | 54.7 | 66.7 | 85.3 | 0.0 | 10.3 | 17.7 | 34.0 |
| random (expected) | 20.1 | 37.9 | 53.4 | 77.9 | 0.0 | 2.2 | 6.7 | 22.4 |

## End-to-end QA

| Setting | Budgets | Context | EM | F1 |
|---|---|---|---|---|
| uniform@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 11.7 [8.3, 15.3] | 17.7 [14.2, 21.7] |
| top_heavy@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 11.7 [8.3, 15.3] | 17.7 [14.2, 21.7] |
| score@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 11.7 [8.3, 15.3] | 17.7 [14.2, 21.7] |
| learned@16 | [4.0, 4.0, 4.0, 4.0] | 16.0 vectors | 11.7 [8.3, 15.3] | 17.7 [14.2, 21.7] |
| uniform@32 | [8.0, 8.0, 8.0, 8.0] | 32.0 vectors | 12.0 [8.7, 16.0] | 18.2 [14.4, 22.4] |
| top_heavy@32 | [16.0, 8.0, 4.0, 4.0] | 32.0 vectors | 12.7 [9.0, 16.7] | 18.3 [14.4, 22.4] |
| score@32 | [15.6, 8.0, 4.2, 4.2] | 32.0 vectors | 12.3 [9.0, 16.3] | 18.4 [14.4, 22.6] |
| learned@32 | [12.3, 6.1, 5.8, 7.7] | 32.0 vectors | 12.0 [8.7, 16.0] | 18.6 [14.8, 22.8] |
| uniform@64 | [16.0, 16.0, 16.0, 16.0] | 64.0 vectors | 13.0 [9.3, 17.0] | 18.9 [15.1, 23.2] |
| top_heavy@64 | [32.0, 16.0, 8.0, 8.0] | 64.0 vectors | 12.7 [9.0, 16.7] | 18.2 [14.4, 22.3] |
| score@64 | [31.1, 16.0, 8.4, 8.4] | 64.0 vectors | 12.7 [9.0, 16.7] | 18.2 [14.4, 22.3] |
| learned@64 | [27.3, 14.2, 9.6, 13.0] | 64.0 vectors | 13.3 [9.7, 17.3] | 19.0 [15.1, 23.2] |
| uniform@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.3] | 20.0 [16.2, 24.1] |
| top_heavy@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.3] | 20.0 [16.2, 24.1] |
| score@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.3] | 20.0 [16.2, 24.1] |
| learned@128 | [32.0, 32.0, 32.0, 32.0] | 128.0 vectors | 13.0 [9.3, 17.3] | 20.0 [16.2, 24.1] |
| raw_bm25 | - | 528 tokens | 8.0 [5.0, 11.0] | 21.7 [18.2, 25.4] |

How the learned head spends its budget (mean vectors per document):

| Total | By rank slot | Gold documents | Other documents |
|---|---|---|---|
| 16 | [4.0, 4.0, 4.0, 4.0] | 4.0 | 4.0 |
| 32 | [12.3, 6.1, 5.8, 7.7] | 8.7 | 7.6 |
| 64 | [27.3, 14.2, 9.6, 13.0] | 19.1 | 14.3 |
| 128 | [32.0, 32.0, 32.0, 32.0] | 32.0 | 32.0 |

F1 by where the first gold document was ranked (number of questions in brackets):

| Setting | rank 1 (166) | rank 2 (66) | rank 3+ (42) | not retrieved (26) |
|---|---|---|---|---|
| uniform@16 | 20.7 | 16.9 | 15.2 | 4.9 |
| top_heavy@16 | 20.7 | 16.9 | 15.2 | 4.9 |
| score@16 | 20.7 | 16.9 | 15.2 | 4.9 |
| learned@16 | 20.7 | 16.9 | 15.2 | 4.9 |
| uniform@32 | 21.1 | 16.6 | 16.4 | 6.9 |
| top_heavy@32 | 22.1 | 16.0 | 14.9 | 4.9 |
| score@32 | 22.1 | 15.8 | 14.9 | 6.9 |
| learned@32 | 22.0 | 16.6 | 15.6 | 6.9 |
| uniform@64 | 22.4 | 14.9 | 18.9 | 6.9 |
| top_heavy@64 | 21.9 | 14.9 | 15.3 | 6.9 |
| score@64 | 21.9 | 14.9 | 15.3 | 6.9 |
| learned@64 | 22.0 | 15.5 | 20.1 | 6.9 |
| uniform@128 | 23.3 | 16.8 | 20.3 | 6.5 |
| top_heavy@128 | 23.3 | 16.8 | 20.3 | 6.5 |
| score@128 | 23.3 | 16.8 | 20.3 | 6.5 |
| learned@128 | 23.3 | 16.8 | 20.3 | 6.5 |
| raw_bm25 | 23.0 | 22.7 | 21.8 | 10.7 |

Paired bootstrap at equal budget, first setting minus second (percentage points):

| Comparison | dEM [95% CI] | P(not better) | dF1 [95% CI] | P(not better) |
|---|---|---|---|---|
| learned@16 vs uniform@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@16 vs top_heavy@16 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| top_heavy@32 vs uniform@32 | +0.7 [+0.0, +1.7] | 0.144 | +0.0 [-1.2, +1.2] | 0.513 |
| score@32 vs uniform@32 | +0.3 [+0.0, +1.0] | 0.385 | +0.1 [-1.0, +1.3] | 0.434 |
| learned@32 vs uniform@32 | +0.0 [-1.0, +1.0] | 0.666 | +0.4 [-0.7, +1.4] | 0.285 |
| learned@32 vs top_heavy@32 | -0.7 [-1.7, +0.0] | 1.000 | +0.3 [-0.8, +1.5] | 0.275 |
| top_heavy@64 vs uniform@64 | -0.3 [-1.0, +0.0] | 1.000 | -0.8 [-1.7, -0.1] | 0.990 |
| score@64 vs uniform@64 | -0.3 [-1.0, +0.0] | 1.000 | -0.8 [-1.7, -0.1] | 0.990 |
| learned@64 vs uniform@64 | +0.3 [+0.0, +1.0] | 0.359 | +0.0 [-0.9, +1.0] | 0.508 |
| learned@64 vs top_heavy@64 | +0.7 [+0.0, +1.7] | 0.139 | +0.8 [-0.2, +1.9] | 0.058 |
| learned@128 vs uniform@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
| learned@128 vs top_heavy@128 | +0.0 [+0.0, +0.0] | 1.000 | +0.0 [+0.0, +0.0] | 1.000 |
