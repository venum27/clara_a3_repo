#!/usr/bin/env bash
# Assignment 3: the third difference from the official CLaRa code -- the SCP target.
# Our fixed-16 model (CLaRa re-implementation) retrained with the official SCP target (all QA pairs of a passage in
# one target) and otherwise exactly the settings of r2_fixed_M16_e6_s42 (6 epochs, lr 1e-4, seed 42), then E2E with
# our usual settings and the same evaluation as the other ablations. Run: a3_fixed16_allqa_s42.
# Finished steps are skipped, so after an interruption simply start it again.
#   bash scripts/15_scp_allqa.sh               2Wiki on GPU 0
#   GPU=1 bash scripts/15_scp_allqa.sh
# Progress: tail -n 5 logs/a3_scp_allqa_2wiki.log      Table: python3 summarize_ablations.py --dataset 2wiki
set -euo pipefail
trap '' HUP    # like nohup: the background job keeps running after you log out
cd "$(dirname "$0")/.."
PY=${PY:-python3}; GPU=${GPU:-0}; DS=${DS:-2wiki}; SEED=${SEED:-42}
DATA=${DATA_DIR:-data}; RUNS=${RUNS_DIR:-runs}; EXTRA=${EXTRA:-}
export CUDA_VISIBLE_DEVICES=$GPU TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}
mkdir -p logs
run=$RUNS/qwen/$DS/a3_fixed16_allqa_s$SEED
log=logs/a3_scp_allqa_${DS}.log
(
    if [ ! -f "$run/scp/meta.json" ]; then
        echo "== SCP with all-QA target $run ($(date))"
        $PY train_scp_allqa.py --dataset "$DS" --data_dir "$DATA" --run_dir "$run" --mode fixed --max_mem 16 \
            --epochs 6 --seed "$SEED" --amp bf16 $EXTRA
    fi
    if [ ! -f "$run/e2e/meta.json" ]; then
        echo "== E2E $run ($(date))"
        $PY train_e2e_a3.py --run_dir "$run" --dataset "$DS" --data_dir "$DATA" --seed "$SEED" --amp bf16 \
            --train_alloc uniform $EXTRA
    fi
    if [ ! -f "$run/results/eval.json" ]; then
        echo "== evaluate $run ($(date))"
        $PY evaluate.py --run_dir "$run" --dataset "$DS" --data_dir "$DATA" --seed "$SEED" --amp bf16 \
            --sections retrieval,qa --totals 32,64 --policies uniform,top_heavy --no_raw $EXTRA
    fi
    $PY summarize_ablations.py --runs_dir "$RUNS" --dataset "$DS" --seed "$SEED"
    echo "== done ($(date))"
) >> "$log" 2>&1 &
echo "GPU $GPU: $DS -> $log"
