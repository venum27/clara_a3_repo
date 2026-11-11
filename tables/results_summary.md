# Results across runs

F1 (%) unless stated. Per-run details and confidence intervals are in each run's results/summary.md.

## Compressor-only QA on held-out synthetic questions, by prefix length (F1)

| Backbone | Dataset | Run | m=4 | m=8 | m=16 | m=32 |
|---|---|---|---|---|---|---|
| qwen | 2wiki | a3_fixed16_allqa_s42 | - | - | - | - |
| qwen | 2wiki | a3_fixed16_lr5e-6_s42 | - | - | - | - |
| qwen | 2wiki | a3_fixed16_lr5e-6_tau0.02_s42 | - | - | - | - |
| qwen | 2wiki | a3_fixed16_tau0.02_s42 | - | - | - | - |
| qwen | 2wiki | a3_head_ent0.1_s42 | - | - | - | - |
| qwen | 2wiki | a3_head_ent0_s42 | - | - | - | - |
| qwen | 2wiki | a3_head_tau0.02_s42 | - | - | - | - |
| qwen | 2wiki | a3_head_tau0.1_s42 | - | - | - | - |
| qwen | 2wiki | clara_official_CR16_s42 | - | - | - | - |
| qwen | 2wiki | fixed_M16_s42 | 13.2 | 21.5 | 25.4 | - |
| qwen | 2wiki | nested_M32__learned_s42 | 20.5 | 21.8 | 22.1 | 22.6 |
| qwen | 2wiki | nested_M32_s42 | 20.5 | 21.8 | 22.1 | 22.6 |
| qwen | 2wiki | r2_fixed_M16_e6_s42 | 13.8 | 17.0 | 27.9 | - |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s42 | 21.6 | 23.8 | 25.7 | 26.6 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s43 | 21.6 | 23.8 | 25.7 | 26.6 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s44 | 21.6 | 23.8 | 25.7 | 26.6 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s42 | 21.6 | 23.8 | 25.7 | 26.6 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s43 | 21.6 | 23.8 | 25.7 | 26.6 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s44 | 21.6 | 23.8 | 25.7 | 26.6 |
| qwen | 2wiki | r2_nested_M32_all_e6_s42 | 21.6 | 23.8 | 25.7 | 26.6 |
| qwen | 2wiki | r2_nested_M32_all_e6_s43 | 21.6 | 23.8 | 25.7 | 26.6 |
| qwen | 2wiki | r2_nested_M32_all_e6_s44 | 21.6 | 23.8 | 25.7 | 26.6 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s42 | 11.2 | 11.2 | 11.0 | 11.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s43 | 11.2 | 11.2 | 11.0 | 11.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s44 | 11.2 | 11.2 | 11.0 | 11.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s42 | 11.2 | 11.2 | 11.0 | 11.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s43 | 11.2 | 11.2 | 11.0 | 11.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s44 | 11.2 | 11.2 | 11.0 | 11.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s42 | 19.3 | 20.8 | 23.9 | 23.8 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s43 | 19.3 | 20.8 | 23.9 | 23.8 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s44 | 19.3 | 20.8 | 23.9 | 23.8 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s42 | 19.3 | 20.8 | 23.9 | 23.8 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s43 | 19.3 | 20.8 | 23.9 | 23.8 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s44 | 19.3 | 20.8 | 23.9 | 23.8 |
| qwen | hotpotqa | clara_official_CR16_s42 | - | - | - | - |
| qwen | hotpotqa | fixed_M16_s42 | 13.0 | 13.5 | 18.8 | - |
| qwen | hotpotqa | nested_M32__learned_s42 | 16.5 | 15.8 | 16.4 | 16.2 |
| qwen | hotpotqa | nested_M32_s42 | 16.5 | 15.8 | 16.4 | 16.2 |
| qwen | hotpotqa | r2_fixed_M16_e6_s42 | 18.5 | 19.6 | 21.8 | - |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s42 | 19.4 | 19.6 | 19.3 | 18.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s43 | 19.4 | 19.6 | 19.3 | 18.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s44 | 19.4 | 19.6 | 19.3 | 18.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s42 | 19.4 | 19.6 | 19.3 | 18.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s43 | 19.4 | 19.6 | 19.3 | 18.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s44 | 19.4 | 19.6 | 19.3 | 18.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s42 | 19.4 | 19.6 | 19.3 | 18.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s43 | 19.4 | 19.6 | 19.3 | 18.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s44 | 19.4 | 19.6 | 19.3 | 18.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s42 | 16.3 | 16.0 | 16.2 | 15.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s43 | 16.3 | 16.0 | 16.2 | 15.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s44 | 16.3 | 16.0 | 16.2 | 15.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s42 | 16.3 | 16.0 | 16.2 | 15.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s43 | 16.3 | 16.0 | 16.2 | 15.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s44 | 16.3 | 16.0 | 16.2 | 15.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s42 | 17.2 | 18.0 | 16.9 | 17.4 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s43 | 17.2 | 18.0 | 16.9 | 17.4 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s44 | 17.2 | 18.0 | 16.9 | 17.4 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s42 | 17.2 | 18.0 | 16.9 | 17.4 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s43 | 17.2 | 18.0 | 16.9 | 17.4 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s44 | 17.2 | 18.0 | 16.9 | 17.4 |
| t5 | 2wiki | fixed_M16_s42 | 10.1 | 10.0 | 9.6 | - |
| t5 | 2wiki | nested_M32__learned_s42 | 9.5 | 9.7 | 9.1 | 9.1 |
| t5 | 2wiki | nested_M32_s42 | 9.5 | 9.7 | 9.1 | 9.1 |
| t5 | hotpotqa | fixed_M16_s42 | 13.9 | 13.9 | 14.2 | - |
| t5 | hotpotqa | nested_M32__learned_s42 | 13.8 | 14.6 | 14.1 | 14.2 |
| t5 | hotpotqa | nested_M32_s42 | 13.8 | 14.6 | 14.1 | 14.2 |

## Retrieval (hit@1 / all-gold@2, %)

| Backbone | Dataset | Run | Random | BM25 | Reasoner before E2E | Reasoner after E2E |
|---|---|---|---|---|---|---|
| qwen | 2wiki | a3_fixed16_allqa_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 17.3 / 1.0 | 53.7 / 12.3 |
| qwen | 2wiki | a3_fixed16_lr5e-6_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 15.3 / 1.3 | 54.0 / 15.3 |
| qwen | 2wiki | a3_fixed16_lr5e-6_tau0.02_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 15.3 / 1.3 | 52.0 / 12.7 |
| qwen | 2wiki | a3_fixed16_tau0.02_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 15.3 / 1.3 | 67.3 / 21.3 |
| qwen | 2wiki | a3_head_ent0.1_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 25.7 / 1.0 | 69.3 / 21.0 |
| qwen | 2wiki | a3_head_ent0_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 25.7 / 1.0 | 71.7 / 25.3 |
| qwen | 2wiki | a3_head_tau0.02_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 25.7 / 1.0 | 69.7 / 20.3 |
| qwen | 2wiki | a3_head_tau0.1_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 25.7 / 1.0 | 70.3 / 22.0 |
| qwen | 2wiki | clara_official_CR16_s42 | 24.9 / 1.7 | - / - | - / - | 49.7 / 12.0 |
| qwen | 2wiki | fixed_M16_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 13.0 / 1.3 | 69.7 / 25.0 |
| qwen | 2wiki | nested_M32__learned_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 30.3 / 3.0 | 65.7 / 20.7 |
| qwen | 2wiki | nested_M32_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 30.3 / 3.0 | 66.7 / 23.0 |
| qwen | 2wiki | r2_fixed_M16_e6_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 15.3 / 1.3 | 64.0 / 21.3 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 27.0 / 1.7 | 70.3 / 24.0 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s43 | 24.9 / 1.7 | 58.3 / 12.0 | 27.0 / 1.7 | 70.3 / 21.7 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s44 | 24.9 / 1.7 | 58.3 / 12.0 | 27.0 / 1.7 | 67.0 / 23.3 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 27.0 / 1.7 | 69.3 / 23.0 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s43 | 24.9 / 1.7 | 58.3 / 12.0 | 27.0 / 1.7 | 71.7 / 25.7 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s44 | 24.9 / 1.7 | 58.3 / 12.0 | 27.0 / 1.7 | 69.3 / 22.7 |
| qwen | 2wiki | r2_nested_M32_all_e6_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 27.0 / 1.7 | 65.7 / 21.0 |
| qwen | 2wiki | r2_nested_M32_all_e6_s43 | 24.9 / 1.7 | 58.3 / 12.0 | 27.0 / 1.7 | 63.7 / 21.3 |
| qwen | 2wiki | r2_nested_M32_all_e6_s44 | 24.9 / 1.7 | 58.3 / 12.0 | 27.0 / 1.7 | 66.0 / 24.3 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 15.7 / 1.0 | 37.7 / 4.3 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s43 | 24.9 / 1.7 | 58.3 / 12.0 | 15.7 / 1.0 | 37.7 / 4.3 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s44 | 24.9 / 1.7 | 58.3 / 12.0 | 15.7 / 1.0 | 21.7 / 4.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 15.7 / 1.0 | 36.7 / 5.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s43 | 24.9 / 1.7 | 58.3 / 12.0 | 15.7 / 1.0 | 42.0 / 7.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s44 | 24.9 / 1.7 | 58.3 / 12.0 | 15.7 / 1.0 | 29.7 / 2.3 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 25.7 / 1.0 | 66.7 / 20.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s43 | 24.9 / 1.7 | 58.3 / 12.0 | 25.7 / 1.0 | 71.3 / 26.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s44 | 24.9 / 1.7 | 58.3 / 12.0 | 25.7 / 1.0 | 68.0 / 22.3 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 25.7 / 1.0 | 67.7 / 23.3 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s43 | 24.9 / 1.7 | 58.3 / 12.0 | 25.7 / 1.0 | 66.3 / 21.3 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s44 | 24.9 / 1.7 | 58.3 / 12.0 | 25.7 / 1.0 | 69.3 / 16.7 |
| qwen | hotpotqa | clara_official_CR16_s42 | 20.1 / 2.2 | - / - | - / - | 57.0 / 21.0 |
| qwen | hotpotqa | fixed_M16_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 47.7 / 10.3 | 63.0 / 22.7 |
| qwen | hotpotqa | nested_M32__learned_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 44.7 / 13.3 | 55.3 / 19.0 |
| qwen | hotpotqa | nested_M32_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 44.7 / 13.3 | 58.3 / 21.3 |
| qwen | hotpotqa | r2_fixed_M16_e6_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 37.3 / 7.3 | 52.7 / 15.0 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.0 | 57.3 / 19.3 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s43 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.0 | 61.7 / 22.0 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s44 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.0 | 56.3 / 17.3 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.0 | 57.3 / 20.3 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s43 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.0 | 55.0 / 18.7 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s44 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.0 | 59.3 / 19.0 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.0 | 57.0 / 20.3 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s43 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.0 | 60.7 / 17.7 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s44 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.0 | 55.7 / 16.3 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 36.7 / 8.3 | 50.0 / 12.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s43 | 20.1 / 2.2 | 68.7 / 20.7 | 36.7 / 8.3 | 51.3 / 14.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s44 | 20.1 / 2.2 | 68.7 / 20.7 | 36.7 / 8.3 | 50.3 / 13.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 36.7 / 8.3 | 40.3 / 9.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s43 | 20.1 / 2.2 | 68.7 / 20.7 | 36.7 / 8.3 | 52.3 / 13.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s44 | 20.1 / 2.2 | 68.7 / 20.7 | 36.7 / 8.3 | 53.7 / 15.3 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.3 | 53.3 / 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s43 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.3 | 55.3 / 18.3 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s44 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.3 | 59.3 / 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.3 | 57.0 / 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s43 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.3 | 60.3 / 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s44 | 20.1 / 2.2 | 68.7 / 20.7 | 39.0 / 10.3 | 62.3 / 20.7 |
| t5 | 2wiki | fixed_M16_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 39.0 / 8.0 | 54.7 / 14.3 |
| t5 | 2wiki | nested_M32__learned_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 42.7 / 11.7 | 53.0 / 16.3 |
| t5 | 2wiki | nested_M32_s42 | 24.9 / 1.7 | 58.3 / 12.0 | 42.7 / 11.7 | 55.3 / 18.3 |
| t5 | hotpotqa | fixed_M16_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 45.0 / 17.3 | 48.3 / 19.0 |
| t5 | hotpotqa | nested_M32__learned_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 42.7 / 16.0 | 45.0 / 17.3 |
| t5 | hotpotqa | nested_M32_s42 | 20.1 / 2.2 | 68.7 / 20.7 | 42.7 / 16.0 | 49.7 / 16.7 |

## End-to-end QA at a total budget of 64 memory vectors (F1)

| Backbone | Dataset | Run | uniform | top_heavy | score | learned | learned - uniform [95% CI] | learned - top_heavy [95% CI] | Raw text BM25 (F1 / tokens) |
|---|---|---|---|---|---|---|---|---|---|
| qwen | 2wiki | a3_fixed16_allqa_s42 | 36.8 | 36.8 | - | - | - | - | - / - |
| qwen | 2wiki | a3_fixed16_lr5e-6_s42 | 40.2 | 40.2 | - | - | - | - | - / - |
| qwen | 2wiki | a3_fixed16_lr5e-6_tau0.02_s42 | 40.9 | 40.9 | - | - | - | - | - / - |
| qwen | 2wiki | a3_fixed16_tau0.02_s42 | 39.9 | 39.9 | - | - | - | - | - / - |
| qwen | 2wiki | a3_head_ent0.1_s42 | 35.9 | 35.3 | - | 35.7 | -0.2 [-1.1, +0.8] | +0.5 [-0.4, +1.5] | - / - |
| qwen | 2wiki | a3_head_ent0_s42 | 36.4 | 36.4 | - | 34.6 | -1.8 [-3.6, -0.2] | -1.8 [-3.6, -0.2] | - / - |
| qwen | 2wiki | a3_head_tau0.02_s42 | 37.4 | 37.3 | - | 38.3 | +1.0 [-0.1, +2.3] | +1.0 [-0.8, +3.0] | - / - |
| qwen | 2wiki | a3_head_tau0.1_s42 | 36.5 | 36.4 | - | 35.7 | -0.8 [-1.8, -0.1] | -0.8 [-2.5, +0.8] | - / - |
| qwen | 2wiki | clara_official_CR16_s42 | 34.2 | - | - | - | - | - | - / - |
| qwen | 2wiki | fixed_M16_s42 | 31.4 | 31.4 | 31.4 | - | - | - | 23.5 / 490.0 |
| qwen | 2wiki | nested_M32__learned_s42 | 37.0 | 37.3 | 37.3 | 37.5 | +0.5 [-0.3, +1.5] | +0.2 [-1.2, +1.5] | 23.5 / 490.0 |
| qwen | 2wiki | nested_M32_s42 | 36.5 | 37.1 | 36.9 | - | - | - | 23.5 / 490.0 |
| qwen | 2wiki | r2_fixed_M16_e6_s42 | 37.7 | 37.7 | 37.7 | - | - | - | 23.5 / 490.0 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s42 | 38.3 | 38.9 | 38.9 | 38.6 | +0.3 [-1.0, +1.7] | -0.3 [-1.9, +1.3] | 23.5 / 490.0 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s43 | 38.3 | 37.4 | 37.5 | 38.3 | +0.0 [+0.0, +0.0] | +0.9 [-0.1, +2.2] | 23.5 / 490.0 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s44 | 39.1 | 39.9 | 39.7 | 39.1 | -0.0 [-1.4, +1.4] | -0.8 [-2.3, +0.6] | 23.5 / 490.0 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s42 | 37.4 | 37.9 | 37.9 | 37.4 | +0.0 [+0.0, +0.0] | -0.5 [-1.9, +0.8] | 23.5 / 490.0 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s43 | 41.2 | 40.2 | 40.4 | 40.6 | -0.6 [-1.8, +0.5] | +0.4 [-0.1, +0.9] | 23.5 / 490.0 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s44 | 40.4 | 40.2 | 40.0 | 40.4 | +0.0 [+0.0, +0.0] | +0.2 [-1.2, +1.6] | 23.5 / 490.0 |
| qwen | 2wiki | r2_nested_M32_all_e6_s42 | 34.5 | 35.8 | 35.6 | - | - | - | 23.5 / 490.0 |
| qwen | 2wiki | r2_nested_M32_all_e6_s43 | 38.5 | 36.7 | 36.7 | - | - | - | 23.5 / 490.0 |
| qwen | 2wiki | r2_nested_M32_all_e6_s44 | 37.4 | 37.0 | 37.1 | - | - | - | 23.5 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s42 | 38.0 | 38.2 | 38.5 | 38.3 | +0.2 [-0.7, +1.4] | +0.0 [-1.3, +1.4] | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s43 | 37.5 | 36.8 | 36.8 | 38.1 | +0.7 [+0.0, +1.7] | +1.3 [-0.4, +3.1] | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s44 | 38.4 | 38.4 | 38.0 | 38.2 | -0.2 [-0.5, +0.0] | -0.2 [-1.8, +1.3] | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s42 | 37.6 | 37.3 | 37.5 | - | - | - | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s43 | 40.5 | 41.2 | 40.9 | - | - | - | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s44 | 36.4 | 36.5 | 36.5 | - | - | - | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s42 | 38.1 | 37.7 | 37.5 | 37.4 | -0.8 [-2.3, +0.5] | -0.3 [-1.6, +0.8] | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s43 | 38.4 | 38.6 | 38.6 | 37.4 | -0.9 [-2.3, +0.1] | -1.2 [-2.7, +0.0] | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s44 | 37.3 | 38.2 | 38.1 | 38.1 | +0.8 [-0.4, +2.3] | -0.1 [-1.4, +1.3] | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s42 | 36.1 | 36.6 | 36.6 | - | - | - | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s43 | 40.6 | 40.0 | 40.0 | - | - | - | 23.6 / 490.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s44 | 39.2 | 39.5 | 39.4 | - | - | - | 23.6 / 490.0 |
| qwen | hotpotqa | clara_official_CR16_s42 | 18.3 | - | - | - | - | - | - / - |
| qwen | hotpotqa | fixed_M16_s42 | 21.4 | 21.4 | 21.4 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | nested_M32__learned_s42 | 21.3 | 20.9 | 21.1 | 20.7 | -0.6 [-1.5, +0.1] | -0.3 [-0.7, +0.2] | 21.7 / 527.9 |
| qwen | hotpotqa | nested_M32_s42 | 19.8 | 20.4 | 20.5 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | r2_fixed_M16_e6_s42 | 21.9 | 21.9 | 21.9 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s42 | 20.8 | 19.5 | 19.7 | 20.8 | +0.0 [+0.0, +0.0] | +1.3 [-0.3, +3.0] | 21.7 / 527.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s43 | 20.6 | 21.0 | 20.8 | 20.6 | +0.0 [+0.0, +0.0] | -0.4 [-1.4, +0.5] | 21.7 / 527.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s44 | 20.7 | 21.4 | 21.4 | 20.7 | +0.0 [+0.0, +0.0] | -0.7 [-2.6, +1.1] | 21.7 / 527.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s42 | 21.4 | 21.7 | 21.6 | 21.5 | +0.1 [-0.4, +0.6] | -0.2 [-1.7, +1.1] | 21.7 / 527.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s43 | 19.3 | 18.9 | 18.9 | 18.3 | -1.0 [-2.2, -0.1] | -0.6 [-2.0, +0.7] | 21.7 / 527.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s44 | 19.5 | 19.7 | 19.7 | 19.5 | +0.0 [+0.0, +0.0] | -0.2 [-1.4, +1.1] | 21.7 / 527.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s42 | 18.8 | 19.7 | 19.5 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s43 | 19.6 | 19.1 | 19.1 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s44 | 20.8 | 20.9 | 20.9 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s42 | 20.1 | 20.6 | 20.6 | 20.1 | +0.0 [+0.0, +0.0] | -0.5 [-1.4, +0.4] | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s43 | 20.5 | 20.9 | 20.9 | 20.9 | +0.4 [-1.0, +1.9] | +0.1 [-0.7, +1.0] | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s44 | 21.7 | 20.6 | 20.6 | 20.9 | -0.8 [-2.1, +0.5] | +0.3 [-0.6, +1.4] | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s42 | 19.5 | 17.7 | 17.8 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s43 | 19.3 | 19.8 | 19.9 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s44 | 21.5 | 20.8 | 20.9 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s42 | 20.7 | 21.4 | 21.4 | 21.6 | +0.8 [-0.2, +1.9] | +0.1 [-1.2, +1.2] | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s43 | 18.9 | 18.2 | 18.2 | 19.0 | +0.0 [-0.9, +1.0] | +0.8 [-0.2, +1.9] | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s44 | 21.6 | 22.3 | 22.0 | 22.4 | +0.8 [-0.8, +2.5] | +0.1 [-0.8, +1.0] | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s42 | 21.3 | 20.6 | 21.0 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s43 | 20.4 | 21.0 | 20.9 | - | - | - | 21.7 / 527.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s44 | 21.1 | 22.1 | 22.2 | - | - | - | 21.7 / 527.9 |
| t5 | 2wiki | fixed_M16_s42 | 37.7 | 37.7 | 37.7 | - | - | - | 23.5 / 494.9 |
| t5 | 2wiki | nested_M32__learned_s42 | 37.8 | 38.0 | 37.9 | 37.8 | +0.0 [+0.0, +0.0] | -0.1 [-0.4, +0.0] | 23.5 / 494.9 |
| t5 | 2wiki | nested_M32_s42 | 38.2 | 38.9 | 38.6 | - | - | - | 23.5 / 494.9 |
| t5 | hotpotqa | fixed_M16_s42 | 18.7 | 18.7 | 18.7 | - | - | - | 26.0 / 527.6 |
| t5 | hotpotqa | nested_M32__learned_s42 | 18.7 | 18.4 | 18.4 | 18.7 | +0.0 [+0.0, +0.0] | +0.3 [-0.3, +1.0] | 26.0 / 527.6 |
| t5 | hotpotqa | nested_M32_s42 | 18.2 | 18.4 | 18.4 | - | - | - | 26.0 / 527.6 |

## Learned budgets at 64 vectors: mean vectors per document

| Backbone | Dataset | Run | by rank slot | gold documents | other documents |
|---|---|---|---|---|---|
| qwen | 2wiki | a3_head_ent0.1_s42 | [21.4, 17.7, 12.7, 12.2] | 18.7 | 13.8 |
| qwen | 2wiki | a3_head_ent0_s42 | [11.9, 18.1, 12.8, 21.1] | 15.1 | 16.8 |
| qwen | 2wiki | a3_head_tau0.02_s42 | [15.9, 19.3, 14.4, 14.5] | 16.8 | 15.4 |
| qwen | 2wiki | a3_head_tau0.1_s42 | [16.2, 15.1, 19.2, 13.6] | 15.9 | 16.1 |
| qwen | 2wiki | nested_M32__learned_s42 | [14.6, 12.0, 29.4, 8.0] | 16.3 | 15.8 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s42 | [17.1, 16.7, 16.1, 14.1] | 17.5 | 14.7 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s43 | [16.0, 16.0, 16.0, 16.0] | 16.0 | 16.0 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s44 | [15.8, 14.7, 17.0, 16.5] | 15.1 | 16.7 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s42 | [16.0, 16.0, 16.0, 16.0] | 16.0 | 16.0 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s43 | [23.0, 20.3, 10.3, 10.4] | 19.1 | 13.4 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s44 | [16.0, 16.0, 16.0, 16.1] | 16.0 | 16.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s42 | [12.2, 12.0, 24.8, 15.0] | 16.8 | 15.6 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s43 | [15.7, 14.6, 16.0, 17.7] | 16.8 | 15.6 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s44 | [15.1, 15.1, 19.9, 13.9] | 16.3 | 15.9 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s42 | [14.5, 16.9, 16.6, 15.9] | 17.0 | 15.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s43 | [22.6, 15.8, 11.3, 14.3] | 18.2 | 14.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s44 | [18.9, 12.3, 19.1, 13.7] | 16.8 | 15.3 |
| qwen | hotpotqa | nested_M32__learned_s42 | [9.5, 21.8, 22.3, 10.4] | 14.9 | 16.6 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s42 | [16.0, 16.0, 16.0, 16.0] | 16.0 | 16.0 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s43 | [16.0, 16.0, 16.0, 16.0] | 16.0 | 16.0 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s44 | [16.0, 16.0, 16.0, 16.0] | 16.0 | 16.0 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s42 | [15.3, 15.5, 17.4, 15.8] | 15.6 | 16.2 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s43 | [24.6, 13.1, 8.0, 18.3] | 18.7 | 14.6 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s44 | [16.0, 16.0, 16.0, 16.0] | 16.0 | 16.0 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s42 | [16.0, 16.0, 16.0, 16.0] | 16.0 | 16.0 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s43 | [22.6, 18.3, 11.1, 11.9] | 18.5 | 14.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s44 | [16.2, 30.2, 9.5, 8.1] | 17.4 | 15.3 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s42 | [14.4, 14.7, 22.0, 12.9] | 16.3 | 15.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s43 | [27.3, 14.2, 9.6, 13.0] | 19.1 | 14.3 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s44 | [31.9, 13.0, 9.7, 9.4] | 19.5 | 14.0 |
| t5 | 2wiki | nested_M32__learned_s42 | [16.0, 16.0, 16.0, 16.0] | 16.0 | 16.0 |
| t5 | hotpotqa | nested_M32__learned_s42 | [16.0, 16.0, 16.0, 16.0] | 16.0 | 16.0 |

## Accuracy vs budget (F1)

| Backbone | Dataset | Run | Split | 16 | 32 | 64 | 128 |
|---|---|---|---|---|---|---|---|
| qwen | 2wiki | a3_fixed16_allqa_s42 | uniform | - | 35.0 | 36.8 | - |
| qwen | 2wiki | a3_fixed16_allqa_s42 | top_heavy | - | 35.9 | 36.8 | - |
| qwen | 2wiki | a3_fixed16_lr5e-6_s42 | uniform | - | 36.2 | 40.2 | - |
| qwen | 2wiki | a3_fixed16_lr5e-6_s42 | top_heavy | - | 38.7 | 40.2 | - |
| qwen | 2wiki | a3_fixed16_lr5e-6_tau0.02_s42 | uniform | - | 36.4 | 40.9 | - |
| qwen | 2wiki | a3_fixed16_lr5e-6_tau0.02_s42 | top_heavy | - | 39.2 | 40.9 | - |
| qwen | 2wiki | a3_fixed16_tau0.02_s42 | uniform | - | 36.3 | 39.9 | - |
| qwen | 2wiki | a3_fixed16_tau0.02_s42 | top_heavy | - | 40.0 | 39.9 | - |
| qwen | 2wiki | a3_head_ent0.1_s42 | uniform | - | 36.0 | 35.9 | - |
| qwen | 2wiki | a3_head_ent0.1_s42 | top_heavy | - | 35.9 | 35.3 | - |
| qwen | 2wiki | a3_head_ent0.1_s42 | learned | - | 35.9 | 35.7 | - |
| qwen | 2wiki | a3_head_ent0_s42 | uniform | - | 36.0 | 36.4 | - |
| qwen | 2wiki | a3_head_ent0_s42 | top_heavy | - | 35.4 | 36.4 | - |
| qwen | 2wiki | a3_head_ent0_s42 | learned | - | 36.0 | 34.6 | - |
| qwen | 2wiki | a3_head_tau0.02_s42 | uniform | - | 37.6 | 37.4 | - |
| qwen | 2wiki | a3_head_tau0.02_s42 | top_heavy | - | 38.1 | 37.3 | - |
| qwen | 2wiki | a3_head_tau0.02_s42 | learned | - | 38.2 | 38.3 | - |
| qwen | 2wiki | a3_head_tau0.1_s42 | uniform | - | 36.1 | 36.5 | - |
| qwen | 2wiki | a3_head_tau0.1_s42 | top_heavy | - | 35.9 | 36.4 | - |
| qwen | 2wiki | a3_head_tau0.1_s42 | learned | - | 36.1 | 35.7 | - |
| qwen | 2wiki | clara_official_CR16_s42 | uniform | - | - | 34.2 | - |
| qwen | 2wiki | fixed_M16_s42 | uniform | 30.4 | 32.8 | 31.4 | 31.4 |
| qwen | 2wiki | fixed_M16_s42 | top_heavy | 30.4 | 33.2 | 31.4 | 31.4 |
| qwen | 2wiki | nested_M32__learned_s42 | uniform | 37.5 | 37.2 | 37.0 | 38.1 |
| qwen | 2wiki | nested_M32__learned_s42 | top_heavy | 37.5 | 37.1 | 37.3 | 38.1 |
| qwen | 2wiki | nested_M32__learned_s42 | learned | 37.5 | 36.7 | 37.5 | 38.1 |
| qwen | 2wiki | nested_M32_s42 | uniform | 35.9 | 36.1 | 36.5 | 35.5 |
| qwen | 2wiki | nested_M32_s42 | top_heavy | 35.9 | 35.6 | 37.1 | 35.5 |
| qwen | 2wiki | r2_fixed_M16_e6_s42 | uniform | 36.3 | 36.5 | 37.7 | 37.7 |
| qwen | 2wiki | r2_fixed_M16_e6_s42 | top_heavy | 36.3 | 37.9 | 37.7 | 37.7 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s42 | uniform | 37.9 | 39.0 | 38.3 | 37.8 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s42 | top_heavy | 37.9 | 39.5 | 38.9 | 37.8 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s42 | learned | 37.9 | 39.0 | 38.6 | 37.8 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s43 | uniform | 36.5 | 38.4 | 38.3 | 38.8 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s43 | top_heavy | 36.5 | 37.8 | 37.4 | 38.8 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s43 | learned | 36.5 | 37.2 | 38.3 | 38.8 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s44 | uniform | 37.1 | 37.6 | 39.1 | 40.3 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s44 | top_heavy | 37.1 | 38.4 | 39.9 | 40.3 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s44 | learned | 37.1 | 37.6 | 39.1 | 40.3 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s42 | uniform | 35.8 | 36.2 | 37.4 | 37.3 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s42 | top_heavy | 35.8 | 38.0 | 37.9 | 37.3 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s42 | learned | 35.8 | 36.2 | 37.4 | 37.3 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s43 | uniform | 37.9 | 40.0 | 41.2 | 41.4 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s43 | top_heavy | 37.9 | 40.1 | 40.2 | 41.4 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s43 | learned | 37.9 | 40.0 | 40.6 | 41.4 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s44 | uniform | 37.6 | 40.3 | 40.4 | 40.4 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s44 | top_heavy | 37.6 | 40.4 | 40.2 | 40.4 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s44 | learned | 37.6 | 40.3 | 40.4 | 40.4 |
| qwen | 2wiki | r2_nested_M32_all_e6_s42 | uniform | 34.5 | 36.7 | 34.5 | 35.8 |
| qwen | 2wiki | r2_nested_M32_all_e6_s42 | top_heavy | 34.5 | 35.6 | 35.8 | 35.8 |
| qwen | 2wiki | r2_nested_M32_all_e6_s43 | uniform | 35.1 | 36.0 | 38.5 | 38.1 |
| qwen | 2wiki | r2_nested_M32_all_e6_s43 | top_heavy | 35.1 | 36.0 | 36.7 | 38.1 |
| qwen | 2wiki | r2_nested_M32_all_e6_s44 | uniform | 34.5 | 36.4 | 37.4 | 39.0 |
| qwen | 2wiki | r2_nested_M32_all_e6_s44 | top_heavy | 34.5 | 36.3 | 37.0 | 39.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s42 | uniform | 37.0 | 37.9 | 38.0 | 38.6 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s42 | top_heavy | 37.0 | 37.6 | 38.2 | 38.6 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s42 | learned | 37.0 | 37.7 | 38.3 | 38.6 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s43 | uniform | 37.7 | 37.8 | 37.5 | 37.8 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s43 | top_heavy | 37.7 | 37.0 | 36.8 | 37.8 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s43 | learned | 37.7 | 37.8 | 38.1 | 37.8 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s44 | uniform | 37.4 | 39.3 | 38.4 | 38.1 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s44 | top_heavy | 37.4 | 38.5 | 38.4 | 38.1 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s44 | learned | 37.4 | 39.3 | 38.2 | 38.1 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s42 | uniform | 37.4 | 40.0 | 37.6 | 37.9 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s42 | top_heavy | 37.4 | 38.3 | 37.3 | 37.9 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s43 | uniform | 38.9 | 40.6 | 40.5 | 40.9 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s43 | top_heavy | 38.9 | 39.6 | 41.2 | 40.9 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s44 | uniform | 37.4 | 37.9 | 36.4 | 38.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s44 | top_heavy | 37.4 | 38.4 | 36.5 | 38.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s42 | uniform | 37.7 | 39.4 | 38.1 | 37.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s42 | top_heavy | 37.7 | 39.3 | 37.7 | 37.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s42 | learned | 37.7 | 39.4 | 37.4 | 37.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s43 | uniform | 37.4 | 39.4 | 38.4 | 38.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s43 | top_heavy | 37.4 | 40.0 | 38.6 | 38.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s43 | learned | 37.4 | 39.4 | 37.4 | 38.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s44 | uniform | 37.2 | 37.4 | 37.3 | 37.9 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s44 | top_heavy | 37.2 | 36.7 | 38.2 | 37.9 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s44 | learned | 37.2 | 37.4 | 38.1 | 37.9 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s42 | uniform | 34.5 | 35.8 | 36.1 | 36.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s42 | top_heavy | 34.5 | 36.6 | 36.6 | 36.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s43 | uniform | 38.1 | 38.5 | 40.6 | 39.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s43 | top_heavy | 38.1 | 39.1 | 40.0 | 39.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s44 | uniform | 38.7 | 39.5 | 39.2 | 39.2 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s44 | top_heavy | 38.7 | 39.4 | 39.5 | 39.2 |
| qwen | hotpotqa | clara_official_CR16_s42 | uniform | - | - | 18.3 | - |
| qwen | hotpotqa | fixed_M16_s42 | uniform | 19.8 | 17.9 | 21.4 | 21.4 |
| qwen | hotpotqa | fixed_M16_s42 | top_heavy | 19.8 | 21.5 | 21.4 | 21.4 |
| qwen | hotpotqa | nested_M32__learned_s42 | uniform | 20.0 | 20.7 | 21.3 | 21.0 |
| qwen | hotpotqa | nested_M32__learned_s42 | top_heavy | 20.0 | 21.5 | 20.9 | 21.0 |
| qwen | hotpotqa | nested_M32__learned_s42 | learned | 20.0 | 20.7 | 20.7 | 21.0 |
| qwen | hotpotqa | nested_M32_s42 | uniform | 19.1 | 21.1 | 19.8 | 20.9 |
| qwen | hotpotqa | nested_M32_s42 | top_heavy | 19.1 | 21.0 | 20.4 | 20.9 |
| qwen | hotpotqa | r2_fixed_M16_e6_s42 | uniform | 20.6 | 22.3 | 21.9 | 21.9 |
| qwen | hotpotqa | r2_fixed_M16_e6_s42 | top_heavy | 20.6 | 21.7 | 21.9 | 21.9 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s42 | uniform | 20.7 | 21.8 | 20.8 | 20.3 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s42 | top_heavy | 20.7 | 21.1 | 19.5 | 20.3 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s42 | learned | 20.7 | 21.0 | 20.8 | 20.3 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s43 | uniform | 20.8 | 20.9 | 20.6 | 21.6 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s43 | top_heavy | 20.8 | 20.3 | 21.0 | 21.6 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s43 | learned | 20.8 | 19.3 | 20.6 | 21.6 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s44 | uniform | 21.1 | 22.5 | 20.7 | 22.6 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s44 | top_heavy | 21.1 | 21.4 | 21.4 | 22.6 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s44 | learned | 21.1 | 22.2 | 20.7 | 22.6 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s42 | uniform | 21.7 | 23.0 | 21.4 | 20.4 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s42 | top_heavy | 21.7 | 23.0 | 21.7 | 20.4 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s42 | learned | 21.7 | 22.7 | 21.5 | 20.4 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s43 | uniform | 19.0 | 19.9 | 19.3 | 20.5 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s43 | top_heavy | 19.0 | 20.3 | 18.9 | 20.5 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s43 | learned | 19.0 | 21.4 | 18.3 | 20.5 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s44 | uniform | 20.1 | 20.2 | 19.5 | 21.8 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s44 | top_heavy | 20.1 | 19.5 | 19.7 | 21.8 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s44 | learned | 20.1 | 20.1 | 19.5 | 21.8 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s42 | uniform | 20.3 | 19.2 | 18.8 | 21.1 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s42 | top_heavy | 20.3 | 18.5 | 19.7 | 21.1 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s43 | uniform | 20.7 | 20.4 | 19.6 | 20.8 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s43 | top_heavy | 20.7 | 18.5 | 19.1 | 20.8 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s44 | uniform | 20.6 | 20.6 | 20.8 | 20.8 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s44 | top_heavy | 20.6 | 21.0 | 20.9 | 20.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s42 | uniform | 19.5 | 19.4 | 20.1 | 19.4 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s42 | top_heavy | 19.5 | 19.6 | 20.6 | 19.4 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s42 | learned | 19.5 | 19.5 | 20.1 | 19.4 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s43 | uniform | 19.7 | 19.0 | 20.5 | 17.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s43 | top_heavy | 19.7 | 19.3 | 20.9 | 17.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s43 | learned | 19.7 | 18.4 | 20.9 | 17.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s44 | uniform | 20.1 | 20.3 | 21.7 | 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s44 | top_heavy | 20.1 | 20.1 | 20.6 | 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s44 | learned | 20.1 | 20.3 | 20.9 | 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s42 | uniform | 18.7 | 18.9 | 19.5 | 20.1 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s42 | top_heavy | 18.7 | 18.7 | 17.7 | 20.1 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s43 | uniform | 19.3 | 19.3 | 19.3 | 19.2 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s43 | top_heavy | 19.3 | 19.9 | 19.8 | 19.2 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s44 | uniform | 19.4 | 19.7 | 21.5 | 20.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s44 | top_heavy | 19.4 | 19.1 | 20.8 | 20.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s42 | uniform | 19.9 | 20.2 | 20.7 | 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s42 | top_heavy | 19.9 | 20.5 | 21.4 | 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s42 | learned | 19.9 | 20.1 | 21.6 | 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s43 | uniform | 17.7 | 18.2 | 18.9 | 20.0 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s43 | top_heavy | 17.7 | 18.3 | 18.2 | 20.0 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s43 | learned | 17.7 | 18.6 | 19.0 | 20.0 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s44 | uniform | 23.0 | 22.5 | 21.6 | 23.3 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s44 | top_heavy | 23.0 | 23.0 | 22.3 | 23.3 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s44 | learned | 23.0 | 22.5 | 22.4 | 23.3 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s42 | uniform | 20.4 | 19.4 | 21.3 | 21.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s42 | top_heavy | 20.4 | 20.1 | 20.6 | 21.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s43 | uniform | 19.3 | 20.3 | 20.4 | 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s43 | top_heavy | 19.3 | 20.9 | 21.0 | 20.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s44 | uniform | 19.4 | 20.0 | 21.1 | 22.6 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s44 | top_heavy | 19.4 | 20.0 | 22.1 | 22.6 |
| t5 | 2wiki | fixed_M16_s42 | uniform | 36.8 | 38.0 | 37.7 | 37.7 |
| t5 | 2wiki | fixed_M16_s42 | top_heavy | 36.8 | 38.2 | 37.7 | 37.7 |
| t5 | 2wiki | nested_M32__learned_s42 | uniform | 37.7 | 37.5 | 37.8 | 37.6 |
| t5 | 2wiki | nested_M32__learned_s42 | top_heavy | 37.7 | 38.2 | 38.0 | 37.6 |
| t5 | 2wiki | nested_M32__learned_s42 | learned | 37.7 | 38.4 | 37.8 | 37.6 |
| t5 | 2wiki | nested_M32_s42 | uniform | 37.8 | 38.0 | 38.2 | 38.7 |
| t5 | 2wiki | nested_M32_s42 | top_heavy | 37.8 | 37.6 | 38.9 | 38.7 |
| t5 | hotpotqa | fixed_M16_s42 | uniform | 20.2 | 19.0 | 18.7 | 18.7 |
| t5 | hotpotqa | fixed_M16_s42 | top_heavy | 20.2 | 19.3 | 18.7 | 18.7 |
| t5 | hotpotqa | nested_M32__learned_s42 | uniform | 18.3 | 18.3 | 18.7 | 17.5 |
| t5 | hotpotqa | nested_M32__learned_s42 | top_heavy | 18.3 | 18.4 | 18.4 | 17.5 |
| t5 | hotpotqa | nested_M32__learned_s42 | learned | 18.3 | 18.8 | 18.7 | 17.5 |
| t5 | hotpotqa | nested_M32_s42 | uniform | 18.4 | 18.3 | 18.2 | 18.5 |
| t5 | hotpotqa | nested_M32_s42 | top_heavy | 18.4 | 18.5 | 18.4 | 18.5 |

## Ours vs the original CLaRa code, paired on the same questions (64 vectors per question, F1)

| Backbone | Dataset | Ours (run: split) | Official CLaRa | Ours | Difference [95% CI] | P(not better) |
|---|---|---|---|---|---|---|
| qwen | 2wiki | a3_fixed16_allqa_s42: uniform@64 | 34.2 | 36.8 | +2.6 [-2.5, +7.6] | 0.163 |
| qwen | 2wiki | a3_fixed16_lr5e-6_s42: uniform@64 | 34.2 | 40.2 | +6.0 [+2.1, +10.1] | 0.002 |
| qwen | 2wiki | a3_fixed16_lr5e-6_tau0.02_s42: uniform@64 | 34.2 | 40.9 | +6.7 [+2.7, +10.7] | 0.001 |
| qwen | 2wiki | a3_fixed16_tau0.02_s42: uniform@64 | 34.2 | 39.9 | +5.7 [+1.0, +10.9] | 0.008 |
| qwen | 2wiki | a3_head_ent0.1_s42: top_heavy@64 | 34.2 | 35.3 | +1.1 [-3.9, +6.1] | 0.328 |
| qwen | 2wiki | a3_head_ent0_s42: top_heavy@64 | 34.2 | 36.4 | +2.2 [-2.8, +7.5] | 0.183 |
| qwen | 2wiki | a3_head_tau0.02_s42: top_heavy@64 | 34.2 | 37.3 | +3.1 [-2.1, +8.4] | 0.127 |
| qwen | 2wiki | a3_head_tau0.1_s42: top_heavy@64 | 34.2 | 36.4 | +2.2 [-2.3, +7.1] | 0.175 |
| qwen | 2wiki | fixed_M16_s42: uniform@64 | 34.2 | 31.4 | -2.8 [-8.3, +2.9] | 0.826 |
| qwen | 2wiki | nested_M32__learned_s42: learned@64 | 34.2 | 37.5 | +3.3 [-1.7, +8.6] | 0.088 |
| qwen | 2wiki | nested_M32_s42: top_heavy@64 | 34.2 | 37.1 | +2.9 [-2.0, +8.0] | 0.134 |
| qwen | 2wiki | r2_fixed_M16_e6_s42: uniform@64 | 34.2 | 37.7 | +3.5 [-1.2, +8.5] | 0.070 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1_s42: learned@64 | 34.2 | 38.6 | +4.4 [-0.3, +9.2] | 0.034 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_s42: learned@64 | 34.2 | 37.4 | +3.2 [-1.8, +8.3] | 0.113 |
| qwen | 2wiki | r2_nested_M32_all_e6_s42: top_heavy@64 | 34.2 | 35.8 | +1.6 [-3.6, +7.2] | 0.288 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned_s42: learned@64 | 34.2 | 38.3 | +4.1 [-0.9, +9.3] | 0.060 |
| qwen | 2wiki | r3_nested_M32_all_e6_it_s42: top_heavy@64 | 34.2 | 37.3 | +3.1 [-2.2, +8.4] | 0.121 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned_s42: learned@64 | 34.2 | 37.4 | +3.2 [-1.9, +8.1] | 0.102 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen_s42: top_heavy@64 | 34.2 | 36.6 | +2.4 [-2.5, +7.5] | 0.157 |
| qwen | hotpotqa | fixed_M16_s42: uniform@64 | 18.3 | 21.4 | +3.1 [-0.6, +7.1] | 0.051 |
| qwen | hotpotqa | nested_M32__learned_s42: learned@64 | 18.3 | 20.7 | +2.3 [-1.8, +6.3] | 0.123 |
| qwen | hotpotqa | nested_M32_s42: top_heavy@64 | 18.3 | 20.4 | +2.0 [-1.8, +5.8] | 0.138 |
| qwen | hotpotqa | r2_fixed_M16_e6_s42: uniform@64 | 18.3 | 21.9 | +3.6 [-0.2, +7.5] | 0.027 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1_s42: learned@64 | 18.3 | 20.8 | +2.5 [-1.3, +6.9] | 0.091 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_s42: learned@64 | 18.3 | 21.5 | +3.2 [-0.7, +7.3] | 0.053 |
| qwen | hotpotqa | r2_nested_M32_all_e6_s42: top_heavy@64 | 18.3 | 19.7 | +1.4 [-2.7, +6.1] | 0.263 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned_s42: learned@64 | 18.3 | 20.1 | +1.7 [-2.5, +6.0] | 0.194 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it_s42: top_heavy@64 | 18.3 | 17.7 | -0.6 [-4.7, +3.7] | 0.598 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned_s42: learned@64 | 18.3 | 21.6 | +3.2 [-0.7, +7.3] | 0.059 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen_s42: top_heavy@64 | 18.3 | 20.6 | +2.3 [-1.8, +6.8] | 0.140 |

## Mean +- std across seeds

| Backbone | Dataset | Config | Seeds | SCP F1 m=4 | SCP F1 m=16 | hit@1 after E2E | hit@1 gain from E2E | uniform@64 F1 | top_heavy@64 F1 | learned@64 F1 | learned gold / other vectors | top_heavy - uniform @32 | learned - uniform @32 | top_heavy - uniform @64 | learned - uniform @64 | memory gain (gold - none) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen | 2wiki | a3_fixed16_allqa | 1 | - | - | 53.7 | 36.3 | 36.8 | 36.8 | - | - | 0.8 | - | 0.0 | - | - |
| qwen | 2wiki | a3_fixed16_lr5e-6 | 1 | - | - | 54.0 | 38.7 | 40.2 | 40.2 | - | - | 2.5 | - | 0.0 | - | - |
| qwen | 2wiki | a3_fixed16_lr5e-6_tau0.02 | 1 | - | - | 52.0 | 36.7 | 40.9 | 40.9 | - | - | 2.7 | - | 0.0 | - | - |
| qwen | 2wiki | a3_fixed16_tau0.02 | 1 | - | - | 67.3 | 52.0 | 39.9 | 39.9 | - | - | 3.7 | - | 0.0 | - | - |
| qwen | 2wiki | a3_head_ent0 | 1 | - | - | 71.7 | 46.0 | 36.4 | 36.4 | 34.6 | 15.1 / 16.8 | -0.6 | 0.0 | 0.0 | -1.8 | - |
| qwen | 2wiki | a3_head_ent0.1 | 1 | - | - | 69.3 | 43.7 | 35.9 | 35.3 | 35.7 | 18.7 / 13.8 | -0.1 | -0.1 | -0.6 | -0.2 | - |
| qwen | 2wiki | a3_head_tau0.02 | 1 | - | - | 69.7 | 44.0 | 37.4 | 37.3 | 38.3 | 16.8 / 15.4 | 0.5 | 0.7 | -0.1 | 1.0 | - |
| qwen | 2wiki | a3_head_tau0.1 | 1 | - | - | 70.3 | 44.7 | 36.5 | 36.4 | 35.7 | 15.9 / 16.1 | -0.2 | 0.0 | -0.0 | -0.8 | - |
| qwen | 2wiki | clara_official_CR16 | 1 | - | - | 49.7 | - | 34.2 | - | - | - | - | - | - | - | - |
| qwen | 2wiki | fixed_M16 | 1 | 13.2 | 25.4 | 69.7 | 56.7 | 31.4 | 31.4 | - | - | 0.4 | - | 0.0 | - | +2.3 |
| qwen | 2wiki | nested_M32 | 1 | 20.5 | 22.1 | 66.7 | 36.3 | 36.5 | 37.1 | - | - | -0.5 | - | 0.6 | - | +2.5 |
| qwen | 2wiki | nested_M32__learned | 1 | 20.5 | 22.1 | 65.7 | 35.3 | 37.0 | 37.3 | 37.5 | 16.3 / 15.8 | -0.1 | -0.5 | 0.3 | 0.5 | +6.9 |
| qwen | 2wiki | r2_fixed_M16_e6 | 1 | 13.8 | 27.9 | 64.0 | 48.7 | 37.7 | 37.7 | - | - | 1.4 | - | 0.0 | - | +5.0 |
| qwen | 2wiki | r2_nested_M32_all_e6 | 3 | 21.6 +- 0.0 | 25.7 +- 0.0 | 65.1 +- 1.3 | 38.1 +- 1.3 | 36.8 +- 2.1 | 36.5 +- 0.6 | - | - | -0.4 +- 0.6 | - | -0.3 +- 1.6 | - | +3.7 +- 1.4 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned | 3 | 21.6 +- 0.0 | 25.7 +- 0.0 | 70.1 +- 1.3 | 43.1 +- 1.3 | 39.7 +- 2.0 | 39.4 +- 1.3 | 39.5 +- 1.8 | 17.0 / 15.1 | 0.7 +- 1.0 | 0.0 +- 0.0 | -0.2 +- 0.7 | -0.2 +- 0.3 | +5.2 +- 1.9 |
| qwen | 2wiki | r2_nested_M32_all_e6__learned_S1 | 3 | 21.6 +- 0.0 | 25.7 +- 0.0 | 69.2 +- 1.9 | 42.2 +- 1.9 | 38.6 +- 0.5 | 38.7 +- 1.3 | 38.7 +- 0.4 | 16.2 / 15.8 | 0.3 +- 0.7 | -0.4 +- 0.7 | 0.2 +- 0.9 | 0.1 +- 0.2 | +3.7 +- 1.8 |
| qwen | 2wiki | r3_nested_M32_all_e6_it | 3 | 11.2 +- 0.0 | 11.0 +- 0.0 | 36.1 +- 6.2 | 20.4 +- 6.2 | 38.2 +- 2.1 | 38.3 +- 2.5 | - | - | -0.8 +- 1.1 | - | 0.2 +- 0.6 | - | +5.8 +- 2.0 |
| qwen | 2wiki | r3_nested_M32_all_e6_it__learned | 3 | 11.2 +- 0.0 | 11.0 +- 0.0 | 32.3 +- 9.2 | 16.7 +- 9.2 | 38.0 +- 0.5 | 37.8 +- 0.9 | 38.2 +- 0.1 | 16.6 / 15.7 | -0.7 +- 0.3 | -0.1 +- 0.1 | -0.1 +- 0.5 | 0.2 +- 0.4 | +6.5 +- 0.7 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen | 3 | 19.3 +- 0.0 | 23.9 +- 0.0 | 67.8 +- 1.5 | 42.1 +- 1.5 | 38.7 +- 2.3 | 38.7 +- 1.8 | - | - | 0.4 +- 0.5 | - | 0.1 +- 0.6 | - | +4.9 +- 1.1 |
| qwen | 2wiki | r3_nested_M32_all_e6_itgen__learned | 3 | 19.3 +- 0.0 | 23.9 +- 0.0 | 68.7 +- 2.4 | 43.0 +- 2.4 | 37.9 +- 0.6 | 38.2 +- 0.5 | 37.6 +- 0.4 | 17.3 / 14.9 | -0.1 +- 0.7 | 0.0 +- 0.0 | 0.2 +- 0.7 | -0.3 +- 0.9 | +4.3 +- 2.1 |
| qwen | hotpotqa | clara_official_CR16 | 1 | - | - | 57.0 | - | 18.3 | - | - | - | - | - | - | - | - |
| qwen | hotpotqa | fixed_M16 | 1 | 13.0 | 18.8 | 63.0 | 15.3 | 21.4 | 21.4 | - | - | 3.6 | - | 0.0 | - | +6.7 |
| qwen | hotpotqa | nested_M32 | 1 | 16.5 | 16.4 | 58.3 | 13.7 | 19.8 | 20.4 | - | - | -0.1 | - | 0.6 | - | +4.2 |
| qwen | hotpotqa | nested_M32__learned | 1 | 16.5 | 16.4 | 55.3 | 10.7 | 21.3 | 20.9 | 20.7 | 14.9 / 16.6 | 0.8 | 0.0 | -0.3 | -0.6 | +4.5 |
| qwen | hotpotqa | r2_fixed_M16_e6 | 1 | 18.5 | 21.8 | 52.7 | 15.3 | 21.9 | 21.9 | - | - | -0.6 | - | 0.0 | - | +5.6 |
| qwen | hotpotqa | r2_nested_M32_all_e6 | 3 | 19.4 +- 0.0 | 19.3 +- 0.0 | 57.8 +- 2.6 | 18.8 +- 2.6 | 19.7 +- 1.1 | 19.9 +- 0.9 | - | - | -0.7 +- 1.2 | - | 0.2 +- 0.7 | - | +5.3 +- 1.5 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned | 3 | 19.4 +- 0.0 | 19.3 +- 0.0 | 57.2 +- 2.2 | 18.2 +- 2.2 | 20.1 +- 1.2 | 20.1 +- 1.5 | 19.8 +- 1.6 | 16.8 / 15.6 | -0.0 +- 0.6 | 0.4 +- 1.0 | 0.0 +- 0.4 | -0.3 +- 0.6 | +4.9 +- 0.3 |
| qwen | hotpotqa | r2_nested_M32_all_e6__learned_S1 | 3 | 19.4 +- 0.0 | 19.3 +- 0.0 | 58.4 +- 2.8 | 19.4 +- 2.8 | 20.7 +- 0.1 | 20.7 +- 1.0 | 20.7 +- 0.1 | 16.0 / 16.0 | -0.8 +- 0.3 | -0.9 +- 0.6 | -0.1 +- 1.1 | 0.0 +- 0.0 | +4.9 +- 0.8 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it | 3 | 16.3 +- 0.0 | 16.2 +- 0.0 | 48.8 +- 7.3 | 12.1 +- 7.3 | 20.1 +- 1.2 | 19.4 +- 1.6 | - | - | -0.1 +- 0.6 | - | -0.7 +- 1.1 | - | +4.0 +- 1.2 |
| qwen | hotpotqa | r3_nested_M32_all_e6_it__learned | 3 | 16.3 +- 0.0 | 16.2 +- 0.0 | 50.6 +- 0.7 | 13.9 +- 0.7 | 20.8 +- 0.8 | 20.7 +- 0.2 | 20.6 +- 0.5 | 17.3 / 15.4 | 0.1 +- 0.2 | -0.1 +- 0.4 | -0.1 +- 0.9 | -0.1 +- 0.6 | +4.8 +- 1.9 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen | 3 | 17.2 +- 0.0 | 16.9 +- 0.0 | 59.9 +- 2.7 | 20.9 +- 2.7 | 20.9 +- 0.5 | 21.2 +- 0.8 | - | - | 0.5 +- 0.3 | - | 0.3 +- 0.8 | - | +5.8 +- 0.7 |
| qwen | hotpotqa | r3_nested_M32_all_e6_itgen__learned | 3 | 17.2 +- 0.0 | 16.9 +- 0.0 | 56.0 +- 3.1 | 17.0 +- 3.1 | 20.4 +- 1.3 | 20.6 +- 2.2 | 21.0 +- 1.8 | 18.3 / 14.7 | 0.3 +- 0.2 | 0.1 +- 0.2 | 0.2 +- 0.9 | 0.6 +- 0.5 | +6.1 +- 1.0 |
| t5 | 2wiki | fixed_M16 | 1 | 10.1 | 9.6 | 54.7 | 15.7 | 37.7 | 37.7 | - | - | 0.2 | - | 0.0 | - | +1.3 |
| t5 | 2wiki | nested_M32 | 1 | 9.5 | 9.1 | 55.3 | 12.7 | 38.2 | 38.9 | - | - | -0.4 | - | 0.7 | - | +1.3 |
| t5 | 2wiki | nested_M32__learned | 1 | 9.5 | 9.1 | 53.0 | 10.3 | 37.8 | 38.0 | 37.8 | 16.0 / 16.0 | 0.7 | 0.9 | 0.1 | 0.0 | +2.0 |
| t5 | hotpotqa | fixed_M16 | 1 | 13.9 | 14.2 | 48.3 | 3.3 | 18.7 | 18.7 | - | - | 0.2 | - | 0.0 | - | -0.5 |
| t5 | hotpotqa | nested_M32 | 1 | 13.8 | 14.1 | 49.7 | 7.0 | 18.2 | 18.4 | - | - | 0.2 | - | 0.1 | - | +1.6 |
| t5 | hotpotqa | nested_M32__learned | 1 | 13.8 | 14.1 | 45.0 | 2.3 | 18.7 | 18.4 | 18.7 | 16.0 / 16.0 | 0.1 | 0.6 | -0.3 | 0.0 | +2.0 |
