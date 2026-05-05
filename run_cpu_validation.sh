#!/bin/bash
cd /home/sayuj/life
source .venv/bin/activate

# Create output directory
mkdir -p results/bg_validation

# Run full protocol with PyElastica (6 hours, accurate physics)
nohup python3 scripts/experiments/experiment_bg_critical_point_validation.py \
    --phase all \
    --scales 0.5 1.0 2.0 \
    --seeds 8 \
    --chi-M-min 0.1 \
    --chi-M-max 50.0 \
    --n-chi-M 30 \
    --output results/bg_validation/ \
    > results/bg_validation/run.log 2>&1 &

echo "=========================================="
echo "CPU PyElastica validation started!"
echo "=========================================="
echo "Expected time: ~6 hours (720 simulations)"
echo "Progress: tail -f results/bg_validation/run.log"
echo "Process ID: $!"
echo ""
echo "Check if running:"
echo "  ps aux | grep experiment_bg_critical_point"
echo ""
echo "Results will be at:"
echo "  results/bg_validation/bg_validation_results.csv"
