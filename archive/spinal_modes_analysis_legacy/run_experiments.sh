#!/bin/bash
# Helper script to run countercurvature experiments
# Usage: ./run_experiments.sh [experiment_name]

set -e

# Set PYTHONPATH to include src directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Use python3 (macOS default)
PYTHON=.venv/bin/python3

# Get experiment name from argument, or run all
EXPERIMENT="${1:-all}"
MODE_FLAG=""
if [[ "${2:-}" == "quick" ]]; then
    MODE_FLAG="--quick"
fi

case "$EXPERIMENT" in
    spine|spine_modes)
        echo "🦴 Running spine modes vs gravity experiment..."
        $PYTHON -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity $MODE_FLAG
        ;;
    microgravity|micro)
        echo "🚀 Running microgravity adaptation experiment..."
        $PYTHON -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation $MODE_FLAG
        ;;
    plant|plant_growth)
        echo "🌱 Running plant upward growth experiment..."
        $PYTHON -m spinalmodes.experiments.countercurvature.experiment_plant_upward_growth
        ;;
    figure|fig)
        echo "📊 Generating countercurvature figure..."
        $PYTHON -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
        ;;
    phase|phase_diagram)
        echo "📊 Generating phase diagram..."
        $PYTHON -m spinalmodes.experiments.countercurvature.experiment_phase_diagram $MODE_FLAG
        ;;
    scoliosis|bifurcation)
        echo "🦴 Running scoliosis bifurcation experiment..."
        $PYTHON -m spinalmodes.experiments.countercurvature.experiment_scoliosis_bifurcation
        ;;
    all)
        echo "Running all countercurvature experiments..."
        echo ""
        echo "=== Spine Modes ==="
        $PYTHON -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity $MODE_FLAG
        echo ""
        echo "=== Microgravity ==="
        $PYTHON -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation $MODE_FLAG
        echo ""
        echo "=== Plant Growth ==="
        $PYTHON -m spinalmodes.experiments.countercurvature.experiment_plant_upward_growth
        echo ""
        echo "=== Generating Figure ==="
        $PYTHON -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
        ;;
    *)
        echo "Usage: $0 [spine|microgravity|plant|figure|phase|all]"
        echo ""
        echo "Examples:"
        echo "  $0 spine        # Run spine modes experiment"
        echo "  $0 microgravity # Run microgravity experiment"
        echo "  $0 plant        # Run plant growth experiment"
        echo "  $0 figure       # Generate publication figure"
        echo "  $0 phase        # Generate phase diagram"
        echo "  $0 scoliosis    # Run scoliosis bifurcation experiment"
        echo "  $0 all          # Run all experiments and generate figure"
        exit 1
        ;;
esac
