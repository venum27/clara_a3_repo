# Linking the official-code gap to A2's Table 3

**Contribution:** Atragada Venkata Naga Sai Ganesh (24110060)
**Source:** A2 report, *"Not All Documents Deserve Equal Space: Adaptive Memory Budgets for CLaRa"*, §5.1 (Table 3) and §9.2 ("Comparison with the official code (H6)").

## The gap we're explaining

At the same total memory budget (B = 64), our method (nested Salient Compressor
Pretraining + learned budget head) beat the official CLaRa implementation by:

- **+1.8 F1 on HotpotQA**
- **+4.2 F1 on 2WikiMultihopQA**

(both differences statistically significant, on the larger 3,000-question/9,000
question-seed-pair evaluation reported in §9.2).

The question H6 raises is *why*: is the gain coming from our novelty (nesting,
the learned budget head), or from something else entirely? A2's own fixed-rate
re-implementation — which has **neither** nesting **nor** a budget head, and
simply assigns a uniform 16-vector split like the official code — closed
almost the same gap on its own (on the order of +3.8 / +2.3 F1, per §9.2). That
is the finding this file documents: most of the advantage is not coming from
adaptive budgeting. It's coming from how the two pipelines are trained. A2's
Table 3 is the table that spells out exactly what differs.

## Table 3 — Official CLaRa code vs. A2's re-implementation

| | Official code | Our re-implementation |
|---|---|---|
| Stages | SCP, instruction tuning, E2E | SCP, E2E |
| SCP QA target | All QA pairs of a passage, written by the generator | One question in, its answer out |
| Retrieval score | Cosine, flattened memory | Same |
| ST temperature | 0.02 | 0.5 |
| E2E learning rate | 5 × 10⁻⁶ | 5 × 10⁻⁵ |
| Backbones | Decoder-only | Decoder-only and encoder–decoder |

*(Reproduced from A2 report, Table 3, §5.1 "Running the official CLaRa code".)*

## Which differences plausibly explain the gain

Reading the table against what we know changes final-stage performance most:

1. **E2E learning rate (5 × 10⁻⁶ → 5 × 10⁻⁵, a 10× increase).** This is the
   single largest, most mechanically plausible driver. A higher E2E learning
   rate lets the query reasoner and generator adapt faster to the frozen,
   cached memory representations in the final training stage — exactly the
   stage where our method's retrieval improvements showed up (hit@1 rising
   18–19 points on HotpotQA and 38–43 points on 2Wiki once the query reasoner
   trains properly; A2 Table 8).
2. **Dropping instruction tuning as a separate stage.** The official code runs
   SCP → instruction tuning → E2E as three stages; our pipeline collapses this
   to SCP → E2E. Removing a stage changes what the model has already converged
   to before E2E begins, which can interact with the learning-rate change
   above.
3. **SCP QA target (all QA pairs per passage vs. one question in/out).**
   Changes how much synthetic supervision per passage the compressor sees
   during Salient Compressor Pretraining, which affects what the memory
   vectors encode before E2E ever starts.
4. **ST (straight-through) temperature (0.02 → 0.5).** A much softer top-k
   selection changes the gradient signal reaching the retriever during E2E;
   this is a secondary candidate alongside the learning-rate change.
5. **Retrieval score formula and backbone coverage** are listed as the same or
   as an added capability (decoder-only **and** encoder–decoder) rather than a
   change in optimization behavior, so they are unlikely to explain the F1 gap
   itself.

## Bottom line for A3

The official-code comparison (H6) is supported, but the source of the
advantage is the corrected training recipe (largely the 10× E2E learning rate,
plus the collapsed-stage schedule), not the adaptive memory budget that is the
paper's actual novelty. A2 states this directly: the fixed-rate
re-implementation — with no nesting and no budget head — recovers almost the
same gain on its own. **Isolating how much of the +1.8 / +4.2 F1 is
attributable to the learning-rate/schedule changes in Table 3, versus any
residual contribution from nesting or the budget head, has not been done and
remains an open thread** — this is also flagged in the Mentor Feedback section
of the A3 report as unfinished work for the "novelty" track.
