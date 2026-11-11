#!/usr/bin/env bash
# Assignment 3: E2E-only ablations on one dataset (seed 42), two jobs side by side on one GPU.
#   Why our pipeline beats the official code -- our CLaRa re-implementation (fixed-16) with official E2E values:
#     a3_fixed16_lr5e-6, a3_fixed16_tau0.02, a3_fixed16_lr5e-6_tau0.02      (ours: lr 5e-5, tau 0.5)
#   Hyperparameters of our method (nested memory + budget head):
#     a3_head_ent0, a3_head_ent0.1 (entropy bonus beta)  a3_head_tau0.1, a3_head_tau0.02 (ST temperature)
#                                                                            (ours: beta 0.02, tau 0.5)
# Each run copies the Assignment 2 compressor (no SCP retraining), trains E2E with ONE setting changed and is
# scored on the 300 evaluation questions (retrieval + QA at 32 and 64 vectors). Finished steps are skipped.
# E2E uses train_e2e_a3.py: identical to train_e2e.py at our temperature (checked), but its straight-through
# top-k stays finite at the official temperature 0.02, where train_e2e.py produces NaN.
#   bash scripts/14_e2e_ablations.sh                   2Wiki on GPU 0
#   GPU=1 DS=hotpotqa bash scripts/14_e2e_ablations.sh
# Progress: tail -n 5 logs/a3_ablations_2wiki_q1.log      Table: python3 summarize_ablations.py
set -euo pipefail
trap '' HUP    # like nohup: the background jobs keep running after you log out
cd "$(dirname "$0")/.."
PY=${PY:-python3}; GPU=${GPU:-0}; DS=${DS:-2wiki}; SEED=${SEED:-42}
DATA=${DATA_DIR:-data}; RUNS=${RUNS_DIR:-runs}; EXTRA=${EXTRA:-}
export CUDA_VISIBLE_DEVICES=$GPU TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}
mkdir -p logs
HEAD="--train_alloc learned --train_totals 32,64"
#    run name                    | compressor taken from  | E2E arguments
RUNS_LIST=(
    "a3_fixed16_lr5e-6           |r2_fixed_M16_e6        |--train_alloc uniform --lr 5e-6"
    "a3_head_ent0                |r2_nested_M32_all_e6   |$HEAD --entropy_coef 0"
    "a3_fixed16_tau0.02          |r2_fixed_M16_e6        |--train_alloc uniform --tau 0.02"
    "a3_head_ent0.1              |r2_nested_M32_all_e6   |$HEAD --entropy_coef 0.1"
    "a3_fixed16_lr5e-6_tau0.02   |r2_fixed_M16_e6        |--train_alloc uniform --lr 5e-6 --tau 0.02"
    "a3_head_tau0.1              |r2_nested_M32_all_e6   |$HEAD --tau 0.1"
    "a3_head_tau0.02             |r2_nested_M32_all_e6   |$HEAD --tau 0.02"
)

run_one() {
    local name src e2e run
    IFS='|' read -r name src e2e <<< "$1"
    name=$(echo $name); src=$(echo $src)
    run=$RUNS/qwen/$DS/${name}_s$SEED
    if [ ! -f "$run/scp/meta.json" ]; then
        local from=$RUNS/qwen/$DS/${src}_s42/scp
        [ -f "$from/meta.json" ] || { echo "missing $from"; return 1; }
        mkdir -p "$run"; rm -rf "$run/scp"; cp -r "$from" "$run/scp"
    fi
    if [ ! -f "$run/e2e/meta.json" ]; then
        echo "== E2E $run: $e2e ($(date))"
        $PY train_e2e_a3.py --run_dir "$run" --dataset "$DS" --data_dir "$DATA" --seed "$SEED" --amp bf16 $e2e $EXTRA
    fi
    if [ ! -f "$run/results/eval.json" ]; then
        echo "== evaluate $run ($(date))"
        $PY evaluate.py --run_dir "$run" --dataset "$DS" --data_dir "$DATA" --seed "$SEED" --amp bf16 \
            --sections retrieval,qa --totals 32,64 --policies uniform,top_heavy --no_raw $EXTRA
    fi
}

for q in 0 1; do
    log=logs/a3_ablations_${DS}_q$((q + 1)).log
    (
        for i in "${!RUNS_LIST[@]}"; do
            if [ $((i % 2)) -eq $q ]; then run_one "${RUNS_LIST[$i]}"; fi
        done
        $PY summarize_ablations.py --runs_dir "$RUNS" --dataset "$DS" --seed "$SEED"
        echo "== queue $((q + 1)) done ($(date))"
    ) >> "$log" 2>&1 &
    echo "GPU $GPU, queue $((q + 1)): $log"
done
echo "running in the background. Table when both queues are done: python3 summarize_ablations.py --dataset $DS"
