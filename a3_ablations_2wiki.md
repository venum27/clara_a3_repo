# E2E-only ablations: 2wiki, seed 42, 64 memory vectors, 300 evaluation questions

One seed: differences smaller than about 2 F1 are within the seed-to-seed spread measured in Assignment 2. Difference = run minus baseline, paired over the same questions, with 95% interval.

## Why our pipeline beats the official code: our CLaRa re-implementation (fixed-16) with official choices

| Setting | Run | F1 | EM | hit@1 | learned - uniform | F1 difference |
|---|---|---|---|---|---|---|
| ours: E2E lr 5e-5, ST temperature 0.5 | r2_fixed_M16_e6 | 37.7 | 34.0 | 64.0 | - | baseline |
| E2E lr 5e-6 (official) | a3_fixed16_lr5e-6 | 40.2 | 37.3 | 54.0 | - | +2.6 [-2.2, +7.0] |
| ST temperature 0.02 (official) | a3_fixed16_tau0.02 | 39.9 | 36.3 | 67.3 | - | +2.2 [-1.1, +5.6] |
| both (official E2E settings) | a3_fixed16_lr5e-6_tau0.02 | 40.9 | 38.3 | 52.0 | - | +3.2 [-1.4, +7.8] |
| SCP target: all QA pairs in one target (official) | a3_fixed16_allqa | 36.8 | 34.3 | 53.7 | - | -0.9 [-5.4, +3.6] |
| official CLaRa code (reference) | clara_official_CR16 | 34.2 | 32.3 | 49.7 | - | -3.5 [-8.5, +1.5] |

## Hyperparameters of our method (nested memory + learned budget head)

| Setting | Run | F1 | EM | hit@1 | learned - uniform | F1 difference |
|---|---|---|---|---|---|---|
| ours: entropy bonus 0.02, ST temperature 0.5 | r2_nested_M32_all_e6__learned | 37.4 | 33.0 | 69.3 | +0.0 | baseline |
| entropy bonus beta = 0 | a3_head_ent0 | 34.6 | 31.0 | 71.7 | -1.8 | -2.8 [-5.6, +0.0] |
| entropy bonus beta = 0.1 | a3_head_ent0.1 | 35.7 | 32.0 | 69.3 | -0.2 | -1.6 [-4.5, +1.3] |
| ST temperature 0.1 | a3_head_tau0.1 | 35.7 | 32.3 | 70.3 | -0.8 | -1.7 [-5.0, +1.4] |
| ST temperature 0.02 | a3_head_tau0.02 | 38.3 | 34.0 | 69.7 | +1.0 | +1.0 [-2.5, +4.4] |

