# Nested CLaRa – Assignment 3

**CS 613: Natural Language Processing, IIT Gandhinagar – Assignment 3 (final)**
Team Black Box Vectors: Venugopala Rao Mallipuram, Atragada Venkata Naga Sai Ganesh, Dasari Lohith, Manemoni Sumanjali,
Rayan Talukder, Sidda Divya, Swami Aryanathan, Vyomika Vasireddy

## Overview

In Assignment 1 we reproduced CLaRa (He et al., 2025) at a small scale with Qwen2.5-0.5B and FLAN-T5-base. In
Assignment 2 we extended it with nested memory tokens and a learned budget head that splits a fixed number of memory
vectors across the retrieved documents. The A2 code and results are in
[clara_a2_repo](https://github.com/venum27/clara_a2_repo).

For Assignment 3 we followed up on the open questions from A2:

1. **Compression instruction tuning.** Official CLaRa has a middle training stage between SCP and E2E that we had
   skipped. We added it to our nested pipeline in two versions: tuning both the compressor and the generator, and
   tuning only the generator.
2. **Why our pipeline beats the official code.** A2 found that our re-implementation scores 2–4 F1 above the official
   CLaRa code but never tested why. We switched our model to the official learning rate, the official temperature
   and the official SCP target, one at a time.
3. **Hyperparameter ablation** of the budget head (entropy bonus and temperature).
4. **A larger evaluation** of the ablations on 3,000 questions per dataset, since the 300-question set was too small
   to separate 2–3 F1 differences.
5. **A bug fix.** A2's straight-through top-k gives NaN at small temperatures (it picks the same document twice), so the
   official temperature 0.02 could not be tested. `train_e2e_a3.py` fixes this.
6. **Extra metrics** without retraining (F1 by question type, answer type and gold-passage rank).
7. **A deployment demo** and a comparison with a standard text RAG using more metrics (ROUGE, containment).

## Repository structure

```
code/          A3 code (new standalone Python files) and code/scripts/ with the run scripts 13–17
runs/          per-run results: eval.json, qa_predictions.json, diagnose.json, train logs (no model weights)
logs/          training and evaluation logs
tables/        summary tables of all experiments
screenshots/   demo/ (deployment demo), appendix/ (execution steps 1–10), comparison/ (vs standard text RAG)
docs/          deployment section and reproduction appendix of the report
analysis/      analyses by team members
```

The A3 code is not a separate project – it runs inside the A2 project. It reuses A2's `train_e2e.py`,
`evaluate.py`, `diagnose_memory.py` and `summarize.py`, A2's `data/` folder and the trained A2 checkpoints. None of the
new files import anything from the A2 code, and they save checkpoints in the same format as A2.

## Setup

1. Clone [clara_a2_repo](https://github.com/venum27/clara_a2_repo) and set it up as described there.
2. Put the trained A2 checkpoints under `runs/` (we start from `r2_nested_M32_all_e6_s42` and `r2_fixed_M16_e6_s42`).
   They are not on GitHub because of their size.
3. Copy everything inside this repo's `code/` folder into the A2 project folder.

We ran everything on our lab server (2× NVIDIA L40S) with Python 3.10, PyTorch 2.4, PEFT 0.20 and Transformers 4.46.3.

## Running the experiments

From the A2 project folder. The scripts run in the background, write their logs to `logs/` and skip any step that has
already finished, so an interrupted run can simply be started again.

```
./scripts/00_check_gpus.sh                            # check which GPU is free
GPUS=1 SEEDS=42,43,44 bash scripts/13_it_nested.sh    # instruction tuning (compressor + generator)
SEEDS=42,43,44 bash scripts/17_it_gen_only.sh         # instruction tuning (generator only)
bash scripts/14_e2e_ablations.sh                      # 7 E2E ablations on 2Wiki
bash scripts/15_scp_allqa.sh                          # official SCP target
bash scripts/16_big_eval_a3.sh                        # ablations on 3,000 questions
```

The tables are built from the saved results in a few seconds (no GPU):

```
python3 compare_it.py --seeds 42,43,44                                 # instruction tuning vs A2
python3 summarize_ablations.py --dataset 2wiki --results results_big   # ablations (3,000 questions)
python3 compare_rag_systems.py                                         # comparison with a standard text RAG
python3 analyze_metrics.py                                             # extra metrics
python3 show_step_a3.py 2                                              # print the evidence of one step
```

On a shared L40S, instruction tuning took about 18 minutes per dataset (about 10 minutes for the generator-only
version), each E2E training with evaluation 30–40 minutes, SCP with the official target about 45 minutes, and each
3,000-question evaluation 25–90 minutes depending on how busy the GPU was.

## Results

All numbers are for Qwen2.5-0.5B with 64 memory vectors per question. The full tables are in `tables/`.

**Instruction tuning** (3 seeds, 300 questions per dataset)

- Tuning the compressor during instruction tuning breaks retrieval: on 2Wiki, hit@1 drops from about 68 to about 34.
  The compressor's memory vectors are used both by the generator and by the retriever, and tuning them only for
  answering ruins them for retrieval. In one seed, retrieval ended up below random.
- Tuning only the generator keeps retrieval at the A2 level and gives small gains on HotpotQA (F1 +1.2, EM +1.6 to
  +2.6). On 2Wiki the changes are within noise.

**Why we beat the official code** (3,000 questions, 2Wiki)

- The main reason is our 10× higher E2E learning rate. With the official learning rate, our model loses 2.4 F1
  [−3.8, −1.0] of the 3.8 F1 gap and its retrieval drops to the official level.
- The official temperature (0.02) is actually better than ours: +2.1 F1 [+1.0, +3.2]. This only works after the NaN fix.
- The official SCP target makes no difference (−0.3 [−1.7, +1.1]).

**Budget head**

The learned split still performs the same as the uniform split (within ±0.8 F1 over 3 seeds, within ±0.3 on 3,000
questions), and changing the entropy bonus or the temperature does not change this. The training logs explain why: the
head's split entropy stays at about 2.56, which is the maximum for 13 possible splits, so the head never learns to
prefer any split.

**Comparison with a standard text RAG** (300 questions per dataset)

For the deployment part we compared our system with a standard RAG pipeline: the same Qwen2.5-0.5B model without any
training, reading BM25's top-4 passages as plain text. Besides EM and F1 we report ROUGE-2, ROUGE-L (computed like the
`rouge-score` package) and containment (does the answer contain the gold answer).

| Dataset | System | Input | EM | F1 | ROUGE-2 | ROUGE-L | Containment | Answer words |
|---|---|---|---|---|---|---|---|---|
| 2Wiki | Standard text RAG | 490 tokens | 15.7 | 23.5 | 17.6 | 23.5 | 33.7 | 8.1 |
| 2Wiki | Official CLaRa code | 64 vectors | 32.3 | 34.2 | 22.4 | 34.3 | 32.3 | 2.4 |
| 2Wiki | Ours (A2, nested + budget head) | 64 vectors | 34.9 | 39.5 | 23.8 | 39.6 | 36.3 | 2.5 |
| 2Wiki | Ours (A3, generator tuned) | 64 vectors | 34.2 | 37.6 | 22.6 | 37.7 | 35.1 | 2.5 |
| HotpotQA | Standard text RAG | 528 tokens | 8.7 | 21.7 | 11.6 | 21.6 | 27.3 | 8.1 |
| HotpotQA | Official CLaRa code | 64 vectors | 11.7 | 18.3 | 7.2 | 18.5 | 12.7 | 2.6 |
| HotpotQA | Ours (A2, nested + budget head) | 64 vectors | 12.1 | 19.8 | 7.2 | 20.0 | 13.8 | 2.3 |
| HotpotQA | Ours (A3, generator tuned) | 64 vectors | 14.7 | 21.0 | 8.6 | 21.2 | 16.3 | 2.3 |

On 2Wiki our models are clearly better than the text RAG (+14 to +16 F1, all significant) while reading about 8 times
less input. On HotpotQA the F1 and ROUGE-L differences are within noise, but our A3 model has a significantly higher
exact match (EM +6.0 [+1.1, +10.9]). The text RAG gives long answers (8 words on average against our 2–3), which is why
it does better on the lenient metrics (containment, ROUGE-2) and worse on exact match. Keep in mind that our generator
was trained on 1,000 training questions, while the text RAG is used zero-shot.

## Deployment demo

The demo is a small Gradio app that runs on the lab server and is opened from a laptop through an SSH tunnel.
`demo_app.py` shows, for one held-out question, the ranked candidate passages, the 4 passages the generator reads,
how the memory budget is split (learned, uniform and top-heavy) and the answer for each split. `demo_app_compare.py`
adds the standard text RAG next to it, with EM, F1, ROUGE-L, input size and time for every system. Screenshots are in
`screenshots/demo/` and `screenshots/comparison/`.

We installed Gradio in a separate environment so the training setup stays untouched. The versions are pinned because
Gradio 6 needs `huggingface_hub` 1.x, which does not work with our Transformers version.

```
python3 -m venv ~/demo_env --system-site-packages
~/demo_env/bin/pip install "gradio==4.44.1" "fastapi==0.112.2" "huggingface_hub<1.0" rank_bm25
CUDA_VISIBLE_DEVICES=1 ~/demo_env/bin/python demo_app_compare.py
```

Then on the laptop: `ssh -L 7860:localhost:7860 <user>@<server>` and open http://localhost:7860. By default the demo
loads our A2 budget-head model on 2Wiki; `--run runs/qwen/<dataset>/<run>` loads another trained run. One question
takes well under a second per system.

## Notes

- We checked `train_e2e_a3.py` against A2's `train_e2e.py` with the same seed at temperature 0.5: the training logs
  are identical and the weights agree up to floating-point rounding.
- With the official SCP target, a passage's QA pairs together are 91 tokens on average (164 at most). A2's 96-token
  target limit would have cut many of them, so `train_scp_allqa.py` uses 256.
- Our A3 runs used Transformers 4.46.3, while A2 used 4.43.4. This explains a tiny difference in one before-training
  retrieval number (2Wiki hit@1 25.7 vs 27.0 with the same frozen compressor).
- Every training script and both demos have a `--tiny` option that runs on a tiny random model on the CPU, which we
  used to test the code before the real runs.
