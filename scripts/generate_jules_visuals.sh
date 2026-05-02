#!/usr/bin/env bash
set -e

echo "Generating Jules Visuals..."

paperbanana generate \
    --input research/figures/jules_complex_mechanism.txt \
    --caption 'IEC Feedback Loop and Supercritical Bifurcation' \
    --output research/figures/jules_complex_mechanism.png || true

paperbanana plot \
    --data outputs/thermodynamic_cost/phase_diagram_energy_deficit_for_plot.csv \
    --intent 'Plot a heatmap mapping L (Spinal Length) to the X-axis, chi_kappa (Coupling Strength) to the Y-axis, and R_deficit (Energy Deficit Ratio) as the color intensity. Use the viridis colormap and log scale if necessary. Label axes clearly.' \
    --output research/figures/jules_thermodynamic_phase_diagram.png || true

paperbanana generate \
    --input research/figures/jules_visual_abstract.txt \
    --caption 'Visual Abstract: Biological Countercurvature of Spacetime' \
    --output research/figures/jules_visual_abstract.png || true

echo "Done."
