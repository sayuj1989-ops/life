#!/bin/bash
# Autonomous generation of high-impact visuals for the Biological Countercurvature theory
# Created by Jules (Scientific AI Assistant)

set -e

echo "Starting autonomous generation of high-impact visual artifacts..."

# Ensure we have the required API key for paperbanana (using dummy for mock wrapper execution)
export GEMINI_API_KEY="dummy"

# 1. Complex Mechanism Diagram: The Derivative Gain Trap
echo "Generating Derivative Gain Trap Mechanism Diagram..."
paperbanana generate \
    --input research/figures/jules_derivative_gain_trap.txt \
    --output research/figures/jules_autonomous_mechanism_derivative_gain_trap.png \
    --caption "The Derivative Gain Trap"

# 2. Phase Diagram: Energy Deficit vs Coupling
echo "Generating Thermodynamic Phase Diagram Heatmap..."
paperbanana plot \
    --data outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv \
    --x L \
    --y chi_kappa \
    --color R_deficit \
    --output research/figures/jules_autonomous_thermodynamic_phase_diagram.png

# 3. Visual Abstract: Metabolic Buckling
echo "Generating Metabolic Buckling Visual Abstract..."
paperbanana generate \
    --input research/figures/jules_visual_abstract_metabolic_buckling.txt \
    --output research/figures/jules_autonomous_visual_abstract_metabolic_buckling.png \
    --caption "Biological Countercurvature: Metabolic Buckling"

echo "Artifact generation complete! Files saved to research/figures/"