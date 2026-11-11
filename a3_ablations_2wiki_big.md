# E2E-only ablations: 2wiki, seed 42, 64 memory vectors, 3,000 evaluation questions (results_big)

One seed: differences smaller than about 2 F1 are within the seed-to-seed spread measured in Assignment 2. Difference = run minus baseline, paired over the same questions, with 95% interval.

## Why our pipeline beats the official code: our CLaRa re-implementation (fixed-16) with official choices

| Setting | Run | F1 | EM | hit@1 | learned - uniform | F1 difference |
|---|---|---|---|---|---|---|
| ours: E2E lr 5e-5, ST temperature 0.5 | r2_fixed_M16_e6 | 35.7 | 31.2 | 67.6 | - | baseline |
| E2E lr 5e-6 (official) | a3_fixed16_lr5e-6 | 33.4 | 29.5 | 57.1 | - | -2.4 [-3.8, -1.0] |
| ST temperature 0.02 (official) | a3_fixed16_tau0.02 | 37.9 | 32.7 | 68.9 | - | +2.1 [+1.0, +3.2] |
| both (official E2E settings) | a3_fixed16_lr5e-6_tau0.02 | 33.3 | 29.5 | 54.4 | - | -2.4 [-3.9, -1.0] |
| SCP target: all QA pairs in one target (official) | a3_fixed16_allqa | 35.4 | 30.6 | 57.0 | - | -0.3 [-1.7, +1.1] |
| official CLaRa code (reference) | clara_official_CR16 | 31.9 | 29.0 | 54.3 | - | -3.8 [-5.4, -2.3] |

## Hyperparameters of our method (nested memory + learned budget head)

| Setting | Run | F1 | EM | hit@1 | learned - uniform | F1 difference |
|---|---|---|---|---|---|---|
| ours: entropy bonus 0.02, ST temperature 0.5 | r2_nested_M32_all_e6__learned | 35.4 | 30.7 | 71.6 | +0.0 | baseline |
| entropy bonus beta = 0 | a3_head_ent0 | 35.1 | 30.2 | 73.1 | -0.3 | -0.3 [-1.2, +0.6] |
| entropy bonus beta = 0.1 | a3_head_ent0.1 | 34.8 | 30.0 | 71.9 | +0.1 | -0.5 [-1.4, +0.4] |
| ST temperature 0.1 | a3_head_tau0.1 | 35.8 | 31.0 | 71.8 | -0.1 | +0.5 [-0.4, +1.4] |
| ST temperature 0.02 | a3_head_tau0.02 | 36.0 | 30.7 | 74.1 | -0.0 | +0.6 [-0.3, +1.6] |

