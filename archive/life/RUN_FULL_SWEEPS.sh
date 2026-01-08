#!/bin/bash
# Run full parameter sweeps for publication-quality results
# 
# This script runs all experiments WITHOUT --quick flags to generate
# publication-quality data for the manuscript.
#
# Expected runtime: 40-70 minutes total
#
# Usage:
#   bash RUN_FULL_SWEEPS.sh
#   # or
#   chmod +x RUN_FULL_SWEEPS.sh && ./RUN_FULL_SWEEPS.sh

set -e  # Exit on error

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

echo "=========================================="
echo "Running Full Parameter Sweeps"
echo "=========================================="
echo ""
echo "This will run all experiments at full resolution."
echo "Expected total runtime: 40-70 minutes"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

echo ""
echo "=========================================="
echo "1. Spine modes vs gravity (5-10 min)"
echo "=========================================="
python3 -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity
echo "✅ Spine modes complete"

echo ""
echo "=========================================="
echo "2. Microgravity adaptation (10-15 min)"
echo "=========================================="
python3 -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation
echo "✅ Microgravity complete"

echo ""
echo "=========================================="
echo "3. Phase diagram + scoliosis (20-40 min)"
echo "=========================================="
python3 -m spinalmodes.experiments.countercurvature.experiment_phase_diagram
echo "✅ Phase diagram complete"

echo ""
echo "=========================================="
echo "4. Generate final figures (< 1 min)"
echo "=========================================="
python3 -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
echo "✅ Figures generated"

echo ""
echo "=========================================="
echo "5. Extract anchor numbers (< 1 min)"
echo "=========================================="
python3 scripts/extract_anchor_numbers.py
echo "✅ Numbers extracted"

echo ""
echo "=========================================="
echo "✅ ALL SWEEPS COMPLETE"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Review extracted numbers in output above"
echo "  2. Copy manuscript sentences into LaTeX file"
echo "  3. Update cover letter key claims with real numbers"
echo "  4. Final manuscript polish"
echo ""

