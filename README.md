# Assignment 3 – Nested CLaRa: instruction tuning, the gap to the official code, ablations and a demo

Team Black Box Vectors · CS 613 Natural Language Processing, IIT Gandhinagar

Assignment 3 builds on our Assignment 2 code and trained models (nested memory tokens and a learned budget head for
CLaRa, https://github.com/venum27/clara_a2_repo). Every A3 file is a **new standalone file**: it imports nothing from
the A2 code, rebuilds the model exactly as `nclara/modeling.py` does, and reads and writes checkpoints in the A2
format, so A2's `train_e2e.py`, `evaluate.py` and `diagnose_memory.py` work on A3 checkpoints unchanged.

## Repository layout

| Folder | What it holds |
|---|---|
| `code/` | All A3 code: the new standalone files and `scripts/13`–`17`. To run it, copy the contents of `code/` into the A2 project folder (see below) |
| `runs/qwen/<dataset>/<run>/` | Per-run results of every A3 run: `results/` (eval.json, qa_predictions.json, diagnose.json), `results_big/`, and the settings and training logs of `scp/` and `e2e/` (`meta.json`, `train_log.json`); no model weights |
| `logs/` | Training and evaluation logs of all A3 runs |
| `tables/` | Summary tables (`a3_it_comparison.md`, `a3_ablations_2wiki.md`, `a3_ablations_2wiki_big.md`, ...) |
| `screenshots/` | `demo/` (deployment demo, cases A–D), `appendix/` (execution steps 1–10), `comparison/` (comparison with a standard text RAG) |
| `docs/` | Deployment section and reproduction appendix of the report (Word), and team members' write-ups |
| `analysis/` | Team members' analyses |

**The A3 code runs inside the A2 project.** It calls A2's `train_e2e.py`, `evaluate.py`, `diagnose_memory.py` and
`summarize.py`, reads A2's `data/` folder and starts from the trained A2 checkpoints. To reproduce: clone
https://github.com/venum27/clara_a2_repo, put the A2 checkpoints under `runs/`, copy the contents of this repository's
`code/` folder into it, and run the commands below from that folder.

The deployment demo and the comparison with a standard text RAG are part of this repository (see "Deployment
demo and comparison with a standard text RAG" below).

## What is new in Assignment 3

| | Experiment | Code |
|---|---|---|
| 1 | **Compression instruction tuning** – CLaRa's middle stage (between SCP and E2E), adapted to nested memory, in two variants: compressor + generator tuned, and generator only (compressor frozen) | `train_it_nested.py`, scripts 13 and 17 |
| 2 | **Why our pipeline beats the official code** – our CLaRa re-implementation (fixed-16) with the official E2E learning rate, the official straight-through temperature, both, and the official SCP target | `train_e2e_a3.py`, `train_scp_allqa.py`, scripts 14 and 15 |
| 3 | **Hyperparameter ablation of the budget head** – entropy bonus and straight-through temperature | script 14 |
| 4 | **Larger evaluation** of all ablations on 3,000 questions | script 16 |
| 5 | **Extra metrics without training** – F1 by question type, by answer type and by the rank of the first gold passage | `analyze_metrics.py` |
| 6 | **Correction to A2** – A2's straight-through top-k returns NaN at small temperatures; fixed in `train_e2e_a3.py` | `train_e2e_a3.py` |
| 7 | **Deployment demo** – a local Gradio app | `demo_app.py` |

## Files

| File | What it does |
|---|---|
| `train_it_nested.py` | Instruction tuning from an A2 nested SCP checkpoint: per training question the gold passages + BM25 distractors (4 in total, BM25 order); answer loss + 0.1 × MSE averaged over prefixes 4/8/16/32; `--train_compressor 0` tunes the generator only |
| `train_e2e_a3.py` | A2's E2E stage with a NaN-safe straight-through top-k (picked documents masked with −∞); identical to `train_e2e.py` at temperature 0.5 |
| `train_scp_allqa.py` | A2's SCP with the official target: the generator writes all QA pairs of a passage in one target (target limit 256 tokens); `--target perqa` reproduces A2's `train_scp.py` exactly |
| `summarize_ablations.py` | Ablation table with paired bootstrap differences against the A2 baselines (`--results results_big` for the 3,000-question set) |
| `compare_it.py` | Instruction tuning vs A2: answers, retrieval, memory diagnostic and compressor-only QA, averaged over seeds |
| `analyze_metrics.py` | Extra metrics from saved predictions (no GPU) |
| `demo_app.py` | Gradio demo: ranked candidates, the passages read, learned / uniform / top-heavy splits and their answers |
| `pack_a3.py` | Zips the A3 code, tables, run results and logs (no model weights) into `~/a3_share.zip` |
| `demo_app_compare.py` | The demo plus a standard text RAG row on every question, with ROUGE-L, containment, input size and time for every system |
| `compare_rag_systems.py` | Scores all systems on the held-out questions with EM, F1, ROUGE-1/2/L and containment, paired against a standard text RAG |
| `show_step_a3.py` | Prints the saved evidence of each step (logs and tables) for the execution screenshots |
| `scripts/13_it_nested.sh` | Instruction tuning (compressor + generator) → E2E (rule splits and budget head) → evaluation → memory diagnostic |
| `scripts/17_it_gen_only.sh` | The same with the compressor frozen |
| `scripts/14_e2e_ablations.sh` | The 7 E2E-only ablations on 2Wiki (two jobs side by side on one GPU) |
| `scripts/15_scp_allqa.sh` | Fixed-16 retrained with the official SCP target, then E2E and evaluation |
| `scripts/16_big_eval_a3.sh` | Re-evaluates the ablation runs on 3,000 questions (no retraining) |

Scripts 13 and 17 train the E2E stage with A2's `train_e2e.py` (exact at temperature 0.5, which they use); scripts 14 and 15 use `train_e2e_a3.py`, which is also correct at the official temperature 0.02. `show_step_a3.py` is shared separately (it is not inside `a3_share.zip`).

## Requirements

Same environment as Assignment 2 (Python 3.10, PyTorch 2.4, PEFT 0.20; our A3 runs used Transformers 4.46.3 – A2
used 4.43.4). A3 starts from the trained A2 checkpoints, which are not in the GitHub repository:
`runs/qwen/<dataset>/r2_nested_M32_all_e6_s42/scp` (nested compressor) and `runs/qwen/<dataset>/r2_fixed_M16_e6_s42/scp`
(fixed-16), produced by A2's `scripts/07_round2.sh`. Data: A2's `data/` folder (including `<dataset>_evalbig.json`).

## How to run

From the project folder, in this order. Every script runs in the background, writes to `logs/`, skips steps that
have already finished (so an interrupted run is simply started again) and keeps running after logout.

```
./scripts/00_check_gpus.sh                               # which GPU is free
GPUS=1 SEEDS=42,43,44 bash scripts/13_it_nested.sh       # instruction tuning, compressor + generator
SEEDS=42,43,44 bash scripts/17_it_gen_only.sh            # instruction tuning, generator only
bash scripts/14_e2e_ablations.sh                         # 7 E2E ablations (2Wiki, seed 42)
bash scripts/15_scp_allqa.sh                             # official SCP target (2Wiki, seed 42)
bash scripts/16_big_eval_a3.sh                           # ablations on 3,000 questions
```

Tables (seconds, no GPU):

```
python3 compare_it.py --seeds 42,43,44                           # runs/a3_it_comparison.md
python3 summarize_ablations.py --dataset 2wiki                   # runs/a3_ablations_2wiki.md
python3 summarize_ablations.py --dataset 2wiki --results results_big   # runs/a3_ablations_2wiki_big.md
python3 analyze_metrics.py                                       # runs/a3_metrics_results_big.md
python3 pack_a3.py                                               # ~/a3_share.zip
python3 show_step_a3.py 2                                        # evidence of step 2 (python3 show_step_a3.py lists all)
```

Approximate times on one shared L40S: instruction tuning about 18 min per dataset (about 10 min generator only); each
E2E + evaluation + memory diagnostic 30–40 min; SCP with the official target about 50 min (6 epochs); each
3,000-question evaluation 25–90 min, depending on how busy the GPU is. Each job needs a few GB of GPU memory
(a 3,000-question evaluation about 10 GB). If a job stops with a CUDA out-of-memory error on the shared GPU, start the
same script again, on the other GPU if needed (`GPU=1` or `GPUS=1`).

The training files and `demo_app.py` have a `--tiny` option that runs on a tiny random model on the CPU (plumbing tests only).

## Deployment demo and comparison with a standard text RAG

The demo (`code/demo_app.py`) runs the full pipeline for one held-out question on the GPU server and is opened from a laptop through an SSH tunnel; `code/demo_app_compare.py` adds a standard text RAG to every question. Screenshots: `screenshots/demo/` and `screenshots/comparison/`; the write-up is in `docs/A3_deployment_section_and_appendix.docx`.

### The systems compared

All use Qwen2.5-0.5B-Instruct, the same held-out questions (300 per dataset) and 4 retrieved passages per question.

| System | Retrieval | What the generator reads |
|---|---|---|
| **Standard text RAG** | BM25 top 4 | the 4 passages as raw text (about 500 tokens); base model with no training |
| Official CLaRa code | its trained retriever | 16 memory vectors per passage (64 in total) |
| Our CLaRa re-implementation (fixed-16) | trained query reasoner | 16 memory vectors per passage (64) |
| Ours: nested memory + learned budget head | trained query reasoner | 64 memory vectors split by the learned head |

### Results: compressed memory vs standard text RAG

300 questions per dataset; the nested model is averaged over 3 seeds. Scores in %. ROUGE is computed exactly like the
`rouge-score` package (F-measure, no stemming; checked on 31,200 answer pairs).

| Dataset | System | Input | EM | F1 | ROUGE-2 | ROUGE-L | Containment | Answer words |
|---|---|---|---|---|---|---|---|---|
| 2Wiki | Standard text RAG | 490 tokens | 15.7 | 23.5 | 17.6 | 23.5 | 33.7 | 8.1 |
| 2Wiki | Official CLaRa code | 64 vectors | 32.3 | 34.2 | 22.4 | 34.3 | 32.3 | 2.4 |
| 2Wiki | Ours: nested + budget head | 64 vectors | **34.9** | **39.5** | **23.8** | **39.6** | **36.3** | 2.5 |
| HotpotQA | Standard text RAG | 528 tokens | 8.7 | **21.7** | **11.6** | **21.6** | **27.3** | 8.1 |
| HotpotQA | Official CLaRa code | 64 vectors | 11.7 | 18.3 | 7.2 | 18.5 | 12.7 | 2.6 |
| HotpotQA | Ours: nested + budget head | 64 vectors | **12.1** | 19.8 | 7.2 | 20.0 | 13.8 | 2.3 |

Paired against the text RAG over the same questions (95% intervals): on 2Wiki our system gains **+16.0 F1
[+10.4, +21.5]** and **+16.1 ROUGE-L [+10.8, +21.6]** while reading about 8× less input; on HotpotQA F1 and ROUGE-L
differ by less than the noise (−1.9 [−6.6, +2.6] and −1.6 [−6.4, +3.3]), and our EM is 3.4 points higher.

The different metrics tell a consistent story about answer length. The untrained text RAG writes long answers
(about 8 words against our 2.4), so it does better on the lenient metrics – containment and ROUGE-2 – and worse on
exact match. Note that our generator was trained on 1,000 training questions while the text RAG is zero-shot, so
part of the gap reflects task training and answer format, not only compression. `tables/a3_rag_comparison.md` has
all systems, ROUGE-1 and the paired differences; run `compare_rag_systems.py` on the server to add the A3 model
(instruction tuning of the generator).

### Running the demo

On the GPU server, in a separate environment (Gradio 6 needs `huggingface_hub` 1.x, which Transformers 4.46 does not
support, so the versions are pinned):

```
python3 -m venv ~/demo_env --system-site-packages
~/demo_env/bin/pip install "gradio==4.44.1" "fastapi==0.112.2" "huggingface_hub<1.0" rank_bm25
CUDA_VISIBLE_DEVICES=1 ~/demo_env/bin/python demo_app_compare.py
```

On the laptop: `ssh -L 7860:localhost:7860 <user>@<server>` and open http://localhost:7860.
Options: `--run runs/qwen/<dataset>/<run>` (a trained run folder with `e2e/`; default
`runs/qwen/2wiki/r2_nested_M32_all_e6__learned_s42`), `--dataset hotpotqa`, `--port`, `--share`, and `--tiny`
(a tiny random model on the CPU, for testing). The demo expects the project layout: `data/<dataset>_eval.json` and
the trained runs under `runs/`. One question takes 0.1–0.8 s per system on an L40S.

### Reproducing the comparison

From the project folder (needs the saved `qa_predictions.json` of the runs; no GPU, a few seconds):

```
python3 compare_rag_systems.py                          # runs/a3_rag_comparison.md
python3 compare_rag_systems.py --runs_dir results/runs  # on the A2 repo's saved results
```

The text-RAG answers come from the raw-text baseline that A2's `evaluate.py` saves with every evaluation
(`preds["raw_bm25"]`); they are identical across all runs, as the base model is deterministic.

## Results

All tables are in `runs/` (and in `tables/` of the shared zip). Main findings (Qwen2.5-0.5B, 64 memory vectors):

1. **Tuning the compressor during instruction tuning breaks retrieval.** On 2Wiki the trained query reasoner's hit@1
   falls from about 68 to about 34 (3 seeds), because the same memory vectors are read by the generator and compared
   by the retriever; before E2E the tuned compressor ranks 2Wiki passages below chance (hit@1 15.7 vs about 25), and in
   one seed (2Wiki, seed 44, rule splits) training ended with hit@4 at 54.6%, also below chance.
2. **Tuning only the generator keeps retrieval at the A2 level** and gives small gains: HotpotQA F1 +1.2 and EM +1.6 to
   +2.6 (3 seeds); on 2Wiki the changes are within noise.
3. **The 10× higher E2E learning rate is the main reason our pipeline beats the official code** (3,000 questions):
   with the official learning rate our fixed-16 model loses 2.4 F1 [−3.8, −1.0] of the 3.8-point gap and its
   retrieval falls to the official level. The official temperature 0.02 is better than ours (+2.1 F1 [+1.0, +3.2]);
   the official SCP target makes no difference (−0.3 [−1.7, +1.1]).
4. **The learned budget split still matches the uniform split**: learned − uniform stays within ±0.8 F1 in the 3-seed
   comparisons and within ±0.3 on 3,000 questions (the larger single-seed gaps on 300 questions, −1.8 and +1.0,
   vanish on 3,000), and no entropy-bonus or temperature setting changes F1 by more than 0.6. The training logs show
   why: with the entropy bonus the head's split entropy stays at about 2.56, the maximum for 13 splits, so it never
   prefers any split.

## Notes

- `train_e2e_a3.py` was checked against A2's `train_e2e.py` on the same seed at temperature 0.5: identical training
  logs and weights equal up to floating-point rounding. With temperature 0.02, A2's code picks the same document
  twice and returns NaN (silently with rule splits, a crash with the budget head); the fixed version trains normally.
- `train_scp_allqa.py --target perqa` reproduced A2's `train_scp.py` exactly in our CPU test (same seed, identical weights); the official all-QA targets average
  91 tokens (maximum 164), so A2's 96-token target limit would have cut many of them.
- With the compressor frozen, the query reasoner starts from the A2 weights; its before-E2E hit@1 (39.0 on HotpotQA,
  25.7 vs A2's 27.0 on 2Wiki) differs only by numerical noise from the newer Transformers version.
