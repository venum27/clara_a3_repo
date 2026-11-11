# Compressed-memory RAG vs standard text RAG (Qwen2.5-0.5B, 300 questions per dataset)

Scores in %. Multi-seed systems are averaged per question over their seeds. Differences are paired against the standard text RAG over the same questions, with bootstrap 95% intervals. ROUGE as in the rouge-score package (F-measure, no stemming).

## hotpotqa

| System | seeds | Input per question | EM | F1 | ROUGE-1 | ROUGE-2 | ROUGE-L | Containment | answer words |
|---|---|---|---|---|---|---|---|---|---|
| Standard text RAG (BM25 top-4 raw text, untrained) | 1 | 528 text tokens | 8.7 | 21.7 | 21.7 | 11.6 | 21.6 | 27.3 | 8.1 |
| Official CLaRa code (16 vectors x 4) | 1 | 64 memory vectors | 11.7 | 18.3 | 18.5 | 7.2 | 18.5 | 12.7 | 2.6 |
| Our CLaRa re-implementation (fixed-16) | 1 | 64 memory vectors | 13.0 | 21.9 | 22.2 | 7.1 | 22.2 | 14.7 | 2.4 |
| A2: nested memory + budget head | 3 | 64 memory vectors | 12.1 | 19.8 | 20.1 | 7.2 | 20.0 | 13.8 | 2.3 |
| A3: + instruction tuning (generator only) | 3 | 64 memory vectors | 14.7 | 21.0 | 21.3 | 8.6 | 21.2 | 16.3 | 2.3 |

Difference against the standard text RAG (paired, 95% interval):

| System | F1 | ROUGE-L | EM |
|---|---|---|---|
| Official CLaRa code (16 vectors x 4) | -3.3 [-8.2, +1.6] | -3.1 [-8.2, +2.0] | +3.0 [-1.7, +7.7] |
| Our CLaRa re-implementation (fixed-16) | +0.2 [-4.9, +5.5] | +0.6 [-4.9, +5.7] | +4.3 [-0.7, +9.7] |
| A2: nested memory + budget head | -1.9 [-6.6, +2.6] | -1.6 [-6.4, +3.3] | +3.4 [-1.1, +8.1] |
| A3: + instruction tuning (generator only) | -0.7 [-5.5, +4.1] | -0.4 [-5.2, +4.4] | +6.0 [+1.1, +10.9] |

## 2wiki

| System | seeds | Input per question | EM | F1 | ROUGE-1 | ROUGE-2 | ROUGE-L | Containment | answer words |
|---|---|---|---|---|---|---|---|---|---|
| Standard text RAG (BM25 top-4 raw text, untrained) | 1 | 490 text tokens | 15.7 | 23.5 | 23.5 | 17.6 | 23.5 | 33.7 | 8.1 |
| Official CLaRa code (16 vectors x 4) | 1 | 64 memory vectors | 32.3 | 34.2 | 34.3 | 22.4 | 34.3 | 32.3 | 2.4 |
| Our CLaRa re-implementation (fixed-16) | 1 | 64 memory vectors | 34.0 | 37.7 | 37.9 | 22.4 | 37.9 | 34.3 | 2.4 |
| A2: nested memory + budget head | 3 | 64 memory vectors | 34.9 | 39.5 | 39.6 | 23.8 | 39.6 | 36.3 | 2.5 |
| A3: + instruction tuning (generator only) | 3 | 64 memory vectors | 34.2 | 37.6 | 37.7 | 22.6 | 37.7 | 35.1 | 2.5 |

Difference against the standard text RAG (paired, 95% interval):

| System | F1 | ROUGE-L | EM |
|---|---|---|---|
| Official CLaRa code (16 vectors x 4) | +10.7 [+4.9, +16.6] | +10.8 [+4.8, +16.7] | +16.7 [+10.3, +23.0] |
| Our CLaRa re-implementation (fixed-16) | +14.2 [+8.4, +20.0] | +14.3 [+8.5, +20.5] | +18.3 [+12.0, +24.7] |
| A2: nested memory + budget head | +16.0 [+10.5, +21.7] | +16.1 [+10.8, +21.6] | +19.2 [+13.4, +25.0] |
| A3: + instruction tuning (generator only) | +14.2 [+8.6, +19.7] | +14.2 [+8.7, +20.0] | +18.6 [+12.7, +24.6] |

