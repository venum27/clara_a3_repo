#!/usr/bin/env bash
# Assignment 3: re-evaluate the ablation runs on the 3,000-question set (no retraining), so their differences can be
# judged with ~±1.5 F1 intervals instead of ~±5. Same evaluation as A2's larger set (data/<dataset>_evalbig.json,
# results_big), but only at 64 memory vectors -- the budget the ablation table uses; F1 at 64 does not depend on
# which other budgets are evaluated. Two jobs side by side on one GPU; the official-code group goes first.
# The table is rebuilt after every run, so it can be read while the rest is still running.
#   bash scripts/16_big_eval_a3.sh            2Wiki on GPU 0
#   GPU=1 bash scripts/16_big_eval_a3.sh
# Progress: tail -n 3 logs/a3_big_eval_2wiki_q1.log      Table: cat runs/a3_ablations_2wiki_big.md
set -euo pipefail
trap '' HUP    # like nohup: the background jobs keep running after you log out
cd "$(dirname "$0")/.."
PY=${PY:-python3}; GPU=${GPU:-0}; DS=${DS:-2wiki}; SEED=${SEED:-42}
DATA=${DATA_DIR:-data}; RUNS=${RUNS_DIR:-runs}; EXTRA=${EXTRA:-}
export CUDA_VISIBLE_DEVICES=$GPU TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}
mkdir -p logs
[ -f "$DATA/${DS}_evalbig.json" ] || { echo "missing $DATA/${DS}_evalbig.json (made in A2 by make_big_eval.py)"; exit 1; }
QUEUE1="a3_fixed16_lr5e-6 a3_fixed16_lr5e-6_tau0.02 a3_head_ent0 a3_head_ent0.1"
QUEUE2="a3_fixed16_tau0.02 a3_fixed16_allqa a3_head_tau0.02 a3_head_tau0.1"

for q in 1 2; do
    if [ $q -eq 1 ]; then list=$QUEUE1; else list=$QUEUE2; fi
    log=logs/a3_big_eval_${DS}_q$q.log
    (
        for name in $list; do
            run=$RUNS/qwen/$DS/${name}_s$SEED
            if [ ! -f "$run/e2e/meta.json" ]; then echo "skip $run (not trained)"; continue; fi
            if [ ! -f "$run/results_big/eval.json" ]; then
                echo "== evaluate $run on 3,000 questions ($(date))"
                $PY evaluate.py --run_dir "$run" --dataset "$DS" --data_dir "$DATA" --seed "$SEED" --amp bf16 \
                    --eval_name evalbig --out_name results_big --sections retrieval,qa --totals 64 \
                    --policies uniform --no_raw $EXTRA
            fi
            $PY summarize_ablations.py --runs_dir "$RUNS" --dataset "$DS" --seed "$SEED" --results results_big
        done
        echo "== queue $q done ($(date))"
    ) >> "$log" 2>&1 &
    echo "GPU $GPU, queue $q: $log"
done
echo "running in the background. Table (updated after every run): cat $RUNS/a3_ablations_${DS}_big.md"
