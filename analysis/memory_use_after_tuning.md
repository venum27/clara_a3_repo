# Memory Use After Instruction Tuning

## 1. Objective

This analysis checks whether the generator continues to use compressed document memory after A3 instruction tuning, and whether its use of memory changes relative to the A2 system.

The analysis uses two complementary diagnostics:

1. **Generator memory diagnostic:** compare answer F1 when the generator receives no memory, memory from an unrelated question, gold supporting passages compressed into memory, or the complete gold memory.
2. **Compressor-only QA:** evaluate whether the compressed memory itself retains information that supports answering held-out synthetic questions when only the first \(m\) memory vectors are available.

These diagnostics answer related but different questions. The first measures the generator's benefit from relevant memory under controlled memory conditions. The second measures the answer-bearing quality of the compressor's representations.

## 2. Data and comparison

The comparison uses the Qwen2.5-0.5B nested CLaRa runs on HotpotQA and 2WikiMultiHopQA. The instruction-tuning comparison uses 300 held-out evaluation questions per dataset and three seeds (42, 43 and 44).

The following variants are compared:

- **A2:** the original nested CLaRa system, with rule-based splits or the learned budget head.
- **A3 joint instruction tuning (`it`):** instruction tuning updates both the compressor and generator.
- **A3 generator-only instruction tuning (`itgen`):** the compressor is frozen during the instruction-tuning stage and only the generator is tuned.

The reported values below are the three-seed summaries in `tables/a3_it_comparison.md`. F1 values are percentages.

## 3. Generator memory diagnostic

For each run, the generator is evaluated under four memory conditions:

- **No memory:** the generator receives no compressed document memory.
- **Wrong memory (all):** the generator receives memory from another question.
- **Gold memory (4):** the generator receives the gold supporting passages with four memory vectors.
- **Gold memory (all):** the generator receives the complete gold memory.

The **memory gain** is defined as:

\[
\text{Memory gain} = \text{F1}_{\text{gold memory (all)}} -
                      \text{F1}_{\text{no memory}}.
\]

A positive memory gain means that providing the complete gold memory improves answer F1 over answering without memory. The wrong-memory condition is a control for whether unrelated memory helps or harms the answer.

### 3.1 HotpotQA

| Variant | No memory | Wrong memory (all) | Gold memory (4) | Gold memory (all) | Memory gain |
|---|---:|---:|---:|---:|---:|
| A2, rule splits | 17.7 | 14.2 | 21.9 | 23.0 | +5.3 |
| A2, budget head | 17.5 | 14.9 | 20.8 | 22.4 | +4.9 |
| A3 joint IT, rule splits | 18.4 | 15.3 | 22.1 | 22.4 | +4.0 |
| A3 joint IT, budget head | 17.8 | 15.6 | 22.2 | 22.7 | +4.8 |
| A3 generator-only IT, rule splits | 18.1 | 15.6 | 22.7 | 23.9 | +5.8 |
| A3 generator-only IT, budget head | 17.4 | 15.8 | 22.2 | 23.5 | +6.1 |

For generator-only instruction tuning, the memory gain is +5.8 F1 with rule splits and +6.1 F1 with the budget head. These are respectively 0.5 and 1.2 F1 points above the corresponding A2 values (+5.3 and +4.9).

The wrong-memory condition is below the no-memory condition for every variant. For example, A3 generator-only IT with rule splits scores 18.1 F1 without memory and 15.6 with unrelated memory. This is consistent with the generator responding to the content of the memory rather than benefiting from the presence of arbitrary memory vectors.

### 3.2 2WikiMultiHopQA

| Variant | No memory | Wrong memory (all) | Gold memory (4) | Gold memory (all) | Memory gain |
|---|---:|---:|---:|---:|---:|
| A2, rule splits | 35.0 | 33.5 | 36.7 | 38.7 | +3.7 |
| A2, budget head | 35.3 | 33.5 | 37.9 | 40.5 | +5.2 |
| A3 joint IT, rule splits | 34.8 | 33.5 | 39.8 | 40.6 | +5.8 |
| A3 joint IT, budget head | 34.3 | 33.1 | 38.7 | 40.7 | +6.5 |
| A3 generator-only IT, rule splits | 36.3 | 33.4 | 38.8 | 41.3 | +4.9 |
| A3 generator-only IT, budget head | 35.7 | 32.8 | 38.6 | 40.0 | +4.3 |

For generator-only instruction tuning, the memory gain is +4.9 F1 with rule splits and +4.3 F1 with the budget head. Compared with A2, this is +1.2 F1 points for rule splits and -0.9 for the budget-head variant. Therefore, the result does not show a consistent increase in memory gain across both split strategies.

Again, unrelated memory scores below the no-memory condition for all variants. With generator-only IT, the scores are 36.3 versus 33.4 for rule splits, and 35.7 versus 32.8 for the budget head. Gold memory produces the strongest scores in both cases.

### 3.3 Interpretation

The memory diagnostic shows that the generator continues to use relevant compressed memory after generator-only instruction tuning:

- Gold memory improves F1 over the no-memory condition on both datasets.
- Unrelated memory performs worse than no memory, suggesting that the model is sensitive to whether the supplied memory is relevant.
- Generator-only instruction tuning preserves or modestly changes the measured memory gain. The change is not uniformly positive: it increases for both HotpotQA variants and for 2Wiki rule splits, but decreases for the 2Wiki budget-head variant.

Thus, the results support the conclusion that **generator-only instruction tuning does not remove the generator's dependence on useful compressed memory**. They do not support the stronger claim that instruction tuning always makes the generator use memory more than A2.

The joint compressor-and-generator variant also retains a positive gold-memory gain, but this should not be interpreted as evidence that its retrieval representation remains healthy. The retrieval results show a substantial degradation for this variant, especially on 2Wiki. The memory diagnostic supplies gold passages directly and therefore does not test whether the retriever can find those passages.

## 4. Compressor-only QA

Compressor-only QA measures F1 on held-out synthetic questions using the first \(m\) memory vectors. It is used as a diagnostic of how much answer-relevant information is retained in the compressed representations at different prefix lengths.

### 4.1 HotpotQA

| Variant | \(m=4\) | \(m=8\) | \(m=16\) | \(m=32\) |
|---|---:|---:|---:|---:|
| A2 | 19.4 | 19.6 | 19.3 | 18.9 |
| A3 joint IT | 16.3 | 16.0 | 16.2 | 15.8 |
| A3 generator-only IT | 17.2 | 18.0 | 16.9 | 17.4 |

### 4.2 2WikiMultiHopQA

| Variant | \(m=4\) | \(m=8\) | \(m=16\) | \(m=32\) |
|---|---:|---:|---:|---:|
| A2 | 21.6 | 23.8 | 25.7 | 26.6 |
| A3 joint IT | 11.2 | 11.2 | 11.0 | 11.2 |
| A3 generator-only IT | 19.3 | 20.8 | 23.9 | 23.8 |

### 4.3 Interpretation

Compressor-only QA is lower after both A3 instruction-tuning variants than in A2. The decline is particularly large for joint instruction tuning on 2WikiMultiHopQA, where the scores are approximately 11.0–11.2 across all prefix lengths, compared with 21.6–26.6 for A2.

Generator-only instruction tuning performs better than joint instruction tuning on this diagnostic. On 2Wiki, its scores increase with prefix length from 19.3 at \(m=4\) to 23.8 at \(m=32\), although they remain below the A2 values. On HotpotQA, generator-only scores are also above the joint-IT scores at every listed prefix length, but below A2.

This distinction is important: freezing the compressor during the instruction-tuning stage avoids the severe degradation associated with jointly tuning it, but the post-training compressor-only QA scores do not fully return to A2 levels. The results therefore suggest that generator-only tuning is the safer of the two instruction-tuning variants for preserving memory quality, not that the compressed representations are completely unchanged.

## 5. Relation to retrieval results

The retrieval measurements provide a separate check. In the three-seed instruction-tuning comparison:

- On HotpotQA, A2 hit@1 is 57.8% with rule splits and 57.2% with the budget head. A3 generator-only IT obtains 59.9% and 56.0%, respectively.
- On 2WikiMultiHopQA, A2 hit@1 is 65.1% with rule splits and 70.1% with the budget head. A3 generator-only IT obtains 67.8% and 68.7%, respectively.
- By contrast, joint compressor-and-generator instruction tuning reduces 2Wiki hit@1 to 36.1% with rule splits and 32.3% with the budget head, compared with the A2 values above.

These retrieval results agree with the broader A3 finding: tuning only the generator during instruction tuning avoids the large retrieval collapse observed when the compressor is also updated. The memory diagnostic and retrieval metrics should nevertheless be interpreted separately: the former supplies gold memory to test the generator, while the latter tests whether the query reasoner can retrieve supporting documents.

## 6. Conclusion

The A3 memory diagnostics show that the generator continues to benefit from relevant compressed memory after instruction tuning. For generator-only instruction tuning, gold memory improves F1 over the no-memory condition on both HotpotQA and 2WikiMultiHopQA, while unrelated memory lowers F1. The measured memory gain is comparable to A2, with modest increases in some settings and a decrease in the 2Wiki budget-head setting; therefore, the results do not establish a universal increase in memory use.

The compressor-only QA results add an important qualification. Jointly tuning the compressor and generator causes a large reduction in compressed-memory answer quality, especially on 2Wiki. Generator-only instruction tuning avoids most of this severe drop, although its compressor-only QA scores remain below A2. Taken together with the retrieval results, the evidence supports generator-only instruction tuning as the safer variant: it retains useful memory for generation and avoids the major retrieval degradation caused by updating the compressor during instruction tuning.

## 7. Files and reproducibility

The following files in `a3_share.zip` support this analysis:

- `tables/a3_it_comparison.md` — three-seed summary of end-to-end QA, retrieval, generator memory diagnostics and compressor-only QA.
- `tables/results_summary.md` — per-run summaries across A2 and A3 runs.
- `tables/diagnose_summary.md` — consolidated memory-diagnostic output.
- `logs/it_gen_hotpotqa.log` and `logs/it_gen_2wiki.log` — generator-only instruction-tuning and evaluation logs.
- `runs/qwen/<dataset>/r3_nested_M32_all_e6_itgen_s<seed>/results/diagnose.json` — per-run memory-diagnostic results.
- `runs/qwen/<dataset>/r3_nested_M32_all_e6_itgen__learned_s<seed>/results/diagnose.json` — per-run budget-head memory-diagnostic results.
- The corresponding `results/eval.json`, `results/summary.md` and `results/qa_predictions.json` files contain the evaluation metrics, summaries and per-question predictions.

The evaluation and diagnostic tables used here are based on the 300-question instruction-tuning comparison. The 3,000-question ablation results are not substituted for these memory-diagnostic measurements.
