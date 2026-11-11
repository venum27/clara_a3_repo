#!/usr/bin/env bash
# Assignment 3: nested CLaRa WITH compression instruction tuning (CLaRa's middle stage, added between nested SCP and
# end-to-end training). For each dataset, in the background on its own GPU (HotpotQA on the first GPU in GPUS, 2Wiki
# on the second):
#   1. train_it_nested.py   tunes the Assignment 2 nested compressor (r2_nested_M32_all_e6_s42) and generator
#   2. train_e2e.py         rule splits (<name>_s<seed>) and the learned budget head (<name>__learned_s<seed>)
#   3. evaluate.py + diagnose_memory.py on the 300 evaluation questions, then summarize.py
# Finished steps are skipped, so after an interruption simply start it again.
#   bash scripts/13_it_nested.sh              both datasets, seeds 42,43,44
#   SEEDS=42 bash scripts/13_it_nested.sh     one seed first (about a third of the time)
#   GPUS=1 bash scripts/13_it_nested.sh       both datasets on GPU 1
# Progress: tail -n 5 logs/it_nested_2wiki.log
set -euo pipefail
trap '' HUP    # like nohup: the background jobs keep running after you log out
cd "$(dirname "$0")/.."
PY=${PY:-python3}; GPUS=${GPUS:-0,1}; SEEDS=${SEEDS:-42,43,44}; DATASETS=${DATASETS:-hotpotqa,2wiki}
NAME=${NAME:-r3_nested_M32_all_e6_it}; DATA=${DATA_DIR:-data}; RUNS=${RUNS_DIR:-runs}; EXTRA=${EXTRA:-}
export TOKENIZERS_PARALLELISM=false PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}
mkdir -p logs
IFS=, read -ra G <<< "$GPUS"
i=0
for ds in ${DATASETS//,/ }; do
    gpu=${G[$(( i < ${#G[@]} ? i : ${#G[@]} - 1 ))]}; i=$((i + 1))
    log=logs/it_nested_${ds}.log
    (
        export CUDA_VISIBLE_DEVICES=$gpu
        echo "== $ds on GPU $gpu, seeds $SEEDS ($(date))"
        $PY train_it_nested.py --dataset "$ds" --seeds "$SEEDS" --name "$NAME" --data_dir "$DATA" \
            --runs_dir "$RUNS" --amp bf16 $EXTRA
        for s in ${SEEDS//,/ }; do
            for v in "" "__learned"; do
                run=$RUNS/qwen/$ds/${NAME}${v}_s$s
                alloc=""
                if [ -n "$v" ]; then alloc="--train_alloc learned --train_totals 32,64"; fi
                if [ ! -f "$run/e2e/meta.json" ]; then
                    echo "== E2E $run ($(date))"
                    $PY train_e2e.py --run_dir "$run" --dataset "$ds" --data_dir "$DATA" --seed "$s" --amp bf16 \
                        $alloc $EXTRA
                fi
                if [ ! -f "$run/results/eval.json" ]; then
                    echo "== evaluate $run ($(date))"
                    $PY evaluate.py --run_dir "$run" --dataset "$ds" --data_dir "$DATA" --seed "$s" --amp bf16 $EXTRA
                fi
                if [ ! -f "$run/results/diagnose.json" ]; then
                    echo "== memory diagnostic $run ($(date))"
                    $PY diagnose_memory.py --run_dir "$run" --data_dir "$DATA" --runs_dir "$RUNS" --amp bf16 $EXTRA
                fi
            done
        done
        $PY summarize.py --runs_dir "$RUNS"
        echo "== $ds done ($(date))"
    ) >> "$log" 2>&1 &
    echo "GPU $gpu: $ds -> $log"
done
echo "running in the background. Progress: tail -n 5 logs/it_nested_<dataset>.log"
