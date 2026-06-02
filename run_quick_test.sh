#!/bin/bash
cd /home/sayuj/life
source .venv/bin/activate

time python3 scripts/experiments/experiment_bg_validation_jax.py \
    --phase all \
    --scales 1.0 \
    --seeds 3 \
    --chi-M-min 0.1 \
    --chi-M-max 50.0 \
    --n-chi-M 20 \
    --output results/bg_validation_jax_quick/
