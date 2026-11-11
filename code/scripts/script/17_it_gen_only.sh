#!/usr/bin/env bash
# Assignment 3 follow-up: instruction tuning with the COMPRESSOR FROZEN (only the generator is tuned).
# Full instruction tuning (13_it_nested.sh) made the memory more useful to the generator on 2Wiki but retrieval
# collapsed, because the compressor -- whose memories the retriever compares -- was retrained for generation only.
# Here the compressor and memory tokens stay exactly as in A2 (so the cached document memories, and the query reasoner
# copied from them, are unchanged) and only the generator learns to read compressed passages for the real task.
# Same pipeline otherwise: tuning -> E2E (rule splits and budget head) -> evaluation -> memory diagnostic, both
# datasets, runs r3_nested_M32_all_e6_itgen[__learned]_s<seed>. Finished steps are skipped.
#   bash scripts/17_it_gen_only.sh              both datasets, seed 42, HotpotQA on GPU 0 and 2Wiki on GPU 1
#   GPUS=1 bash scripts/17_it_gen_only.sh       both datasets on GPU 1
# Progress: tail -n 5 logs/it_gen_2wiki.log      Comparison: python3 compare_it.py
set -euo pipefail
trap '' HUP    # like nohup: the background jobs keep running after you log out
cd "$(dirname "$0")/.."
PY=${PY:-python3}; GPUS=${GPUS:-0,1}; SEEDS=${SEEDS:-42}; DATASETS=${DATASETS:-hotpotqa,2wiki}
NAME=${NAME:-r3_nested_M32_all_e6_itgen}; DATA=${DATA_DIR:-data}; RUNS=${RUNS_DIR:-runs}; EXTRA=${EXTRA:-}
export TOKENIZERS_PARALLELISM=false PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}
mkdir -p logs
IFS=, read -ra G <<< "$GPUS"
i=0
for ds in ${DATASETS//,/ }; do
    gpu=${G[$(( i < ${#G[@]} ? i : ${#G[@]} - 1 ))]}; i=$((i + 1))
    log=logs/it_gen_${ds}.log
    (
        export CUDA_VISIBLE_DEVICES=$gpu
        echo "== $ds on GPU $gpu, seeds $SEEDS ($(date))"
        $PY train_it_nested.py --dataset "$ds" --seeds "$SEEDS" --name "$NAME" --data_dir "$DATA" \
            --runs_dir "$RUNS" --amp bf16 --train_compressor 0 $EXTRA
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
echo "running in the background. Progress: tail -n 5 logs/it_gen_<dataset>.log"
