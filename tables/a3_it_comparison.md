# Instruction tuning (A3) vs Assignment 2, seed(s) 42, 43, 44

Same nested compressor family, Qwen2.5-0.5B, 300 evaluation questions per dataset. With one seed, differences under about 2 F1 are within the seed-to-seed spread measured in A2.

## hotpotqa

**End-to-end answers** (F1 at a total of 32 / 64 / 128 memory vectors; budget-head runs use their learned split)

| Run | seeds | F1 @32 | F1 @64 | F1 @128 | EM @64 | learned - uniform @64 |
|---|---|---|---|---|---|---|
| A2, rule splits | 3 | 20.0 | 19.7 | 20.9 | 12.2 | - |
| A2, budget head | 3 | 21.4 | 19.8 | 20.9 | 12.1 | -0.3 |
| A3 tuned, rule splits | 3 | 19.3 | 20.1 | 20.1 | 13.6 | - |
| A3 tuned, budget head | 3 | 19.4 | 20.6 | 19.3 | 14.1 | -0.1 |
| A3 tuned generator only, rule splits | 3 | 19.9 | 20.9 | 21.7 | 13.8 | - |
| A3 tuned generator only, budget head | 3 | 20.4 | 21.0 | 21.3 | 14.7 | +0.6 |

**Retrieval** (%; after E2E = the trained query reasoner; before E2E = the copy of the compressor it starts from, which shows whether the compressor's memories still support retrieval)

| Run | hit@1 | hit@2 | all-gold@2 | hit@1 before E2E |
|---|---|---|---|---|
| A2, rule splits | 57.8 | 75.3 | 18.1 | 39.0 |
| A2, budget head | 57.2 | 74.4 | 19.3 | 39.0 |
| A3 tuned, rule splits | 48.8 | 67.6 | 12.9 | 36.7 |
| A3 tuned, budget head | 50.6 | 69.8 | 13.7 | 36.7 |
| A3 tuned generator only, rule splits | 59.9 | 76.4 | 20.7 | 39.0 |
| A3 tuned generator only, budget head | 56.0 | 75.4 | 19.9 | 39.0 |

**Memory diagnostic** (F1 answering with: no memory / another question's memory / gold passages cut to 4 vectors / gold passages complete; gain = gold complete - no memory)

| Run | no memory | wrong memory | gold (4) | gold (all) | memory gain |
|---|---|---|---|---|---|
| A2, rule splits | 17.7 | 14.2 | 21.9 | 23.0 | +5.3 |
| A2, budget head | 17.5 | 14.9 | 20.8 | 22.4 | +4.9 |
| A3 tuned, rule splits | 18.4 | 15.3 | 22.1 | 22.4 | +4.0 |
| A3 tuned, budget head | 17.8 | 15.6 | 22.2 | 22.7 | +4.8 |
| A3 tuned generator only, rule splits | 18.1 | 15.6 | 22.7 | 23.9 | +5.8 |
| A3 tuned generator only, budget head | 17.4 | 15.8 | 22.2 | 23.5 | +6.1 |

**Compressor-only QA** (F1 on held-out synthetic questions, first m memory vectors; shows whether nesting survives instruction tuning)

| Run | m=4 | m=8 | m=16 | m=32 |
|---|---|---|---|---|
| A2, rule splits | 19.4 | 19.6 | 19.3 | 18.9 |
| A2, budget head | 19.4 | 19.6 | 19.3 | 18.9 |
| A3 tuned, rule splits | 16.3 | 16.0 | 16.2 | 15.8 |
| A3 tuned, budget head | 16.3 | 16.0 | 16.2 | 15.8 |
| A3 tuned generator only, rule splits | 17.2 | 18.0 | 16.9 | 17.4 |
| A3 tuned generator only, budget head | 17.2 | 18.0 | 16.9 | 17.4 |

## 2wiki

**End-to-end answers** (F1 at a total of 32 / 64 / 128 memory vectors; budget-head runs use their learned split)

| Run | seeds | F1 @32 | F1 @64 | F1 @128 | EM @64 | learned - uniform @64 |
|---|---|---|---|---|---|---|
| A2, rule splits | 3 | 36.4 | 36.8 | 37.6 | 33.3 | - |
| A2, budget head | 3 | 38.8 | 39.5 | 39.7 | 34.9 | -0.2 |
| A3 tuned, rule splits | 3 | 39.5 | 38.2 | 39.2 | 34.2 | - |
| A3 tuned, budget head | 3 | 38.3 | 38.2 | 38.2 | 34.3 | +0.2 |
| A3 tuned generator only, rule splits | 3 | 37.9 | 38.7 | 38.4 | 34.9 | - |
| A3 tuned generator only, budget head | 3 | 38.7 | 37.6 | 38.1 | 34.2 | -0.3 |

**Retrieval** (%; after E2E = the trained query reasoner; before E2E = the copy of the compressor it starts from, which shows whether the compressor's memories still support retrieval)

| Run | hit@1 | hit@2 | all-gold@2 | hit@1 before E2E |
|---|---|---|---|---|
| A2, rule splits | 65.1 | 85.0 | 22.2 | 27.0 |
| A2, budget head | 70.1 | 86.8 | 23.8 | 27.0 |
| A3 tuned, rule splits | 36.1 | 57.0 | 5.0 | 15.7 |
| A3 tuned, budget head | 32.3 | 55.9 | 4.2 | 15.7 |
| A3 tuned generator only, rule splits | 67.8 | 84.0 | 20.4 | 25.7 |
| A3 tuned generator only, budget head | 68.7 | 85.4 | 23.0 | 25.7 |

**Memory diagnostic** (F1 answering with: no memory / another question's memory / gold passages cut to 4 vectors / gold passages complete; gain = gold complete - no memory)

| Run | no memory | wrong memory | gold (4) | gold (all) | memory gain |
|---|---|---|---|---|---|
| A2, rule splits | 35.0 | 33.5 | 36.7 | 38.7 | +3.7 |
| A2, budget head | 35.3 | 33.5 | 37.9 | 40.5 | +5.2 |
| A3 tuned, rule splits | 34.8 | 33.5 | 39.8 | 40.6 | +5.8 |
| A3 tuned, budget head | 34.3 | 33.1 | 38.7 | 40.7 | +6.5 |
| A3 tuned generator only, rule splits | 36.3 | 33.4 | 38.8 | 41.3 | +4.9 |
| A3 tuned generator only, budget head | 35.7 | 32.8 | 38.6 | 40.0 | +4.3 |

**Compressor-only QA** (F1 on held-out synthetic questions, first m memory vectors; shows whether nesting survives instruction tuning)

| Run | m=4 | m=8 | m=16 | m=32 |
|---|---|---|---|---|
| A2, rule splits | 21.6 | 23.8 | 25.7 | 26.6 |
| A2, budget head | 21.6 | 23.8 | 25.7 | 26.6 |
| A3 tuned, rule splits | 11.2 | 11.2 | 11.0 | 11.2 |
| A3 tuned, budget head | 11.2 | 11.2 | 11.0 | 11.2 |
| A3 tuned generator only, rule splits | 19.3 | 20.8 | 23.9 | 23.8 |
| A3 tuned generator only, budget head | 19.3 | 20.8 | 23.9 | 23.8 |

