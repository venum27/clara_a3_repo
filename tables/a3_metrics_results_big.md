# Extra metrics (results_big, 64 memory vectors per question)

Cells: F1 (%) ± 95% half-interval, (share of that run's question-seed pairs in the group).

## hotpotqa

Runs: official CLaRa = clara_official_CR16 [s42]; our CLaRa (fixed-16) = r2_fixed_M16_e6 [s42 (uniform@64)]; nested + budget head = r2_nested_M32_all_e6__learned [s42 (learned@64), s43 (learned@64), s44 (learned@64)]

| | official CLaRa | our CLaRa (fixed-16) | nested + budget head |
|---|---|---|---|
| EM | 11.1 ±1.1 | 11.5 ±1.1 | 11.7 ±0.7 |
| F1 | 17.5 ±1.2 | 19.8 ±1.2 | 19.2 ±0.7 |

| Question type | official CLaRa | our CLaRa (fixed-16) | nested + budget head |
|---|---|---|---|
| bridge | 10.5 ±1.0 (80%) | 13.5 ±1.1 (80%) | 12.6 ±0.6 (80%) |
| comparison | 46.0 ±3.8 (20%) | 45.4 ±3.8 (20%) | 46.7 ±2.2 (20%) |

| Answer type | official CLaRa | our CLaRa (fixed-16) | nested + budget head |
|---|---|---|---|
| yes/no | 58.7 ±7.2 (6%) | 55.3 ±7.3 (6%) | 56.6 ±4.2 (6%) |
| other | 14.9 ±1.1 (94%) | 17.5 ±1.2 (94%) | 16.9 ±0.7 (94%) |

| First gold passage | official CLaRa | our CLaRa (fixed-16) | nested + budget head |
|---|---|---|---|
| rank 1 | 18.7 ±1.7 (57%) | 23.3 ±1.8 (51%) | 21.1 ±1.0 (56%) |
| rank 2 | 18.8 ±2.7 (20%) | 19.2 ±2.8 (19%) | 17.5 ±1.6 (19%) |
| rank 3+ | 13.9 ±2.7 (16%) | 14.7 ±2.6 (18%) | 17.0 ±1.7 (16%) |
| not retrieved | 12.9 ±3.9 (8%) | 13.3 ±3.0 (12%) | 15.7 ±2.1 (9%) |

## 2wiki

Runs: a3_fixed16_allqa = a3_fixed16_allqa [s42 (uniform@64)]; a3_fixed16_lr5e-6 = a3_fixed16_lr5e-6 [s42 (uniform@64)]; a3_fixed16_lr5e-6_tau0.02 = a3_fixed16_lr5e-6_tau0.02 [s42 (uniform@64)]; a3_fixed16_tau0.02 = a3_fixed16_tau0.02 [s42 (uniform@64)]; a3_head_ent0.1 = a3_head_ent0.1 [s42 (learned@64)]; a3_head_ent0 = a3_head_ent0 [s42 (learned@64)]; a3_head_tau0.02 = a3_head_tau0.02 [s42 (learned@64)]; a3_head_tau0.1 = a3_head_tau0.1 [s42 (learned@64)]; official CLaRa = clara_official_CR16 [s42]; our CLaRa (fixed-16) = r2_fixed_M16_e6 [s42 (uniform@64)]; nested + budget head = r2_nested_M32_all_e6__learned [s42 (learned@64), s43 (learned@64), s44 (learned@64)]

| | a3_fixed16_allqa | a3_fixed16_lr5e-6 | a3_fixed16_lr5e-6_tau0.02 | a3_fixed16_tau0.02 | a3_head_ent0.1 | a3_head_ent0 | a3_head_tau0.02 | a3_head_tau0.1 | official CLaRa | our CLaRa (fixed-16) | nested + budget head |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EM | 30.6 ±1.6 | 29.5 ±1.6 | 29.5 ±1.6 | 32.7 ±1.7 | 30.0 ±1.6 | 30.2 ±1.6 | 30.7 ±1.7 | 31.0 ±1.7 | 29.0 ±1.6 | 31.2 ±1.7 | 31.1 ±1.0 |
| F1 | 35.4 ±1.6 | 33.4 ±1.6 | 33.3 ±1.6 | 37.9 ±1.6 | 34.8 ±1.6 | 35.1 ±1.6 | 36.0 ±1.6 | 35.8 ±1.6 | 31.9 ±1.6 | 35.7 ±1.6 | 36.2 ±0.9 |

| Question type | a3_fixed16_allqa | a3_fixed16_lr5e-6 | a3_fixed16_lr5e-6_tau0.02 | a3_fixed16_tau0.02 | a3_head_ent0.1 | a3_head_ent0 | a3_head_tau0.02 | a3_head_tau0.1 | official CLaRa | our CLaRa (fixed-16) | nested + budget head |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge_comparison | 55.5 ±3.7 (22%) | 56.1 ±3.7 (22%) | 56.3 ±3.7 (22%) | 57.0 ±3.7 (22%) | 58.0 ±3.7 (22%) | 57.2 ±3.7 (22%) | 55.9 ±3.7 (22%) | 58.5 ±3.7 (22%) | 57.7 ±3.7 (22%) | 57.1 ±3.7 (22%) | 57.7 ±2.1 (22%) |
| comparison | 58.8 ±3.6 (24%) | 59.6 ±3.6 (24%) | 59.4 ±3.6 (24%) | 60.8 ±3.6 (24%) | 53.5 ±3.6 (24%) | 55.0 ±3.6 (24%) | 56.1 ±3.6 (24%) | 57.2 ±3.6 (24%) | 59.6 ±3.6 (24%) | 58.0 ±3.6 (24%) | 58.1 ±2.1 (24%) |
| compositional | 14.3 ±1.8 (42%) | 10.3 ±1.6 (42%) | 10.1 ±1.5 (42%) | 18.8 ±2.0 (42%) | 15.5 ±1.8 (42%) | 15.5 ±1.9 (42%) | 17.2 ±1.9 (42%) | 15.2 ±1.8 (42%) | 7.3 ±1.3 (42%) | 16.0 ±1.9 (42%) | 15.7 ±1.1 (42%) |
| inference | 25.4 ±2.7 (12%) | 19.6 ±2.4 (12%) | 19.7 ±2.5 (12%) | 23.4 ±2.7 (12%) | 22.5 ±2.6 (12%) | 22.9 ±2.6 (12%) | 24.3 ±2.7 (12%) | 23.6 ±2.7 (12%) | 15.4 ±2.1 (12%) | 21.0 ±2.5 (12%) | 24.2 ±1.6 (12%) |

| Answer type | a3_fixed16_allqa | a3_fixed16_lr5e-6 | a3_fixed16_lr5e-6_tau0.02 | a3_fixed16_tau0.02 | a3_head_ent0.1 | a3_head_ent0 | a3_head_tau0.02 | a3_head_tau0.1 | official CLaRa | our CLaRa (fixed-16) | nested + budget head |
|---|---|---|---|---|---|---|---|---|---|---|---|
| yes/no | 72.5 ±4.9 (11%) | 72.5 ±4.9 (11%) | 72.2 ±4.9 (11%) | 72.5 ±4.9 (11%) | 72.5 ±4.9 (11%) | 72.5 ±4.9 (11%) | 72.2 ±4.9 (11%) | 72.5 ±4.9 (11%) | 73.1 ±4.8 (11%) | 72.5 ±4.9 (11%) | 72.5 ±2.8 (11%) |
| other | 30.9 ±1.6 (89%) | 28.6 ±1.6 (89%) | 28.6 ±1.6 (89%) | 33.7 ±1.7 (89%) | 30.3 ±1.6 (89%) | 30.5 ±1.6 (89%) | 31.6 ±1.6 (89%) | 31.4 ±1.7 (89%) | 26.9 ±1.6 (89%) | 31.3 ±1.7 (89%) | 31.8 ±1.0 (89%) |

| First gold passage | a3_fixed16_allqa | a3_fixed16_lr5e-6 | a3_fixed16_lr5e-6_tau0.02 | a3_fixed16_tau0.02 | a3_head_ent0.1 | a3_head_ent0 | a3_head_tau0.02 | a3_head_tau0.1 | official CLaRa | our CLaRa (fixed-16) | nested + budget head |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rank 1 | 34.5 ±2.1 (57%) | 27.5 ±2.0 (57%) | 27.5 ±2.0 (54%) | 35.1 ±1.9 (69%) | 35.2 ±1.9 (72%) | 35.0 ±1.9 (73%) | 36.0 ±1.9 (74%) | 35.6 ±1.9 (72%) | 33.0 ±2.2 (54%) | 34.9 ±2.0 (68%) | 36.2 ±1.1 (72%) |
| rank 2 | 38.4 ±4.1 (17%) | 36.0 ±4.1 (16%) | 37.4 ±4.1 (16%) | 41.1 ±4.2 (16%) | 34.6 ±4.1 (15%) | 35.5 ±4.3 (14%) | 37.0 ±4.5 (13%) | 36.1 ±4.2 (15%) | 31.7 ±3.8 (17%) | 37.4 ±3.9 (17%) | 36.5 ±2.4 (15%) |
| rank 3+ | 36.0 ±4.0 (16%) | 42.5 ±4.2 (16%) | 37.8 ±3.9 (18%) | 44.3 ±5.4 (10%) | 32.2 ±5.3 (9%) | 36.0 ±5.3 (9%) | 38.3 ±5.6 (9%) | 37.6 ±5.4 (9%) | 32.0 ±4.0 (16%) | 37.2 ±4.9 (11%) | 36.2 ±3.1 (9%) |
| not retrieved | 34.3 ±5.2 (10%) | 47.0 ±5.5 (10%) | 48.0 ±5.2 (12%) | 53.2 ±7.9 (5%) | 35.2 ±8.0 (4%) | 31.5 ±8.8 (3%) | 26.4 ±7.7 (4%) | 35.3 ±8.3 (4%) | 27.6 ±4.3 (13%) | 39.3 ±8.3 (4%) | 33.3 ±5.1 (3%) |

