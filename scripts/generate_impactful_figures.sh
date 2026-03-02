#!/usr/bin/env bash

# generate_impactful_figures.sh
#
# Helper script to generate high-impact visual artifacts for the "Biological Countercurvature" theory
# using the paperbanana CLI tool.
#
# Note: Ensure you have your Gemini API key set and paperbanana installed.
#
# Usage:
#   export GEMINI_API_KEY="your-api-key"
#   ./scripts/generate_impactful_figures.sh

set -e

echo "=== Generating High-Impact Visual Artifacts with PaperBanana ==="

if [[ -z "${GEMINI_API_KEY}" ]]; then
    echo "Error: GEMINI_API_KEY is not set."
    echo "Please set it via: export GEMINI_API_KEY='your-api-key'"
    exit 1
fi

# Generate: The Mechanogenetic Demand-Supply Gap Mechanism
echo "[1/3] Generating Mechanogenetic Demand-Supply Gap Mechanism diagram..."
paperbanana generate \
    --input research/figures/demand_supply_gap_mechanism.txt \
    --caption "Mechanogenetic Demand-Supply Gap Mechanism" \
    --output research/figures/demand_supply_gap_mechanism.png

# Plot: Thermodynamic Stability Phase Diagram
echo "[2/3] Plotting Thermodynamic Stability Phase Diagram..."
paperbanana plot \
    --input outputs/thermodynamic_cost/phase_diagram_energy_deficit_for_plot.csv \
    --prompt "Use seaborn to plot a heatmap mapping L to X, chi_kappa to Y, and R_deficit to Color (Viridis). Use default fonts." \
    --output research/figures/thermodynamic_instability_heatmap.png

# Generate: Visual Abstract (Biological Countercurvature of Spacetime)
echo "[3/3] Generating Visual Abstract..."
paperbanana generate \
    --input research/figures/biological_countercurvature_spacetime_abstract.txt \
    --caption "Visual Abstract: Biological Countercurvature of Spacetime" \
    --output research/figures/biological_countercurvature_spacetime_abstract.png

echo "Done! The new figures have been saved to research/figures/"
