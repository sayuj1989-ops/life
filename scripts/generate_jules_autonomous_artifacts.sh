#!/bin/bash
# Autonomous generation script to generate high-impact visuals using PaperBanana CLI

export PATH="/home/jules/self_created_tools/bin:$PATH"

echo "=== Autonomous PaperBanana Generation ==="

CMD1="paperbanana generate --input research/figures/jules_synthesized_mechanism.txt --caption 'Mechanogenetic Demand-Supply Gap' --output research/figures/jules_synthesized_mechanism.png"
CMD2="paperbanana plot --data outputs/thermodynamic_cost/phase_diagram_energy_deficit_for_plot.csv --intent 'Plot a heatmap mapping L (Spinal Length) to the X-axis, chi_kappa (Coupling Strength) to the Y-axis, and R_deficit (Energy Deficit Ratio) as the color intensity. Use the viridis colormap. Use default fonts.' --output research/figures/jules_synthesized_phase_diagram.png"
CMD3="paperbanana generate --input research/figures/jules_synthesized_visual_abstract.txt --caption 'Visual Abstract: Biological Countercurvature' --output research/figures/jules_synthesized_visual_abstract.png"

echo "Executing command 1: $CMD1"
eval $CMD1

echo "Executing command 2: $CMD2"
eval $CMD2

echo "Executing command 3: $CMD3"
eval $CMD3

echo "=== Complete ==="
