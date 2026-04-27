#!/bin/bash

# Visual Abstract Generation
paperbanana generate -i research/figures/jules_visual_abstract.txt -c "Visual Abstract of Biological Countercurvature" -o research/figures/visual_abstract.png

# Concept Mechanism Generation
paperbanana generate -i research/figures/jules_mechanism_diagram.txt -c "Derivative Gain Trap Mechanism" -o research/figures/derivative_gain_trap.png

# Statistical Plot Generation
paperbanana plot -d outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv --intent "Plot a heatmap mapping Spinal Length L (m) to the X-axis, Coupling Strength \chi_\kappa to the Y-axis, and log deficit ratio P/S as color intensity" -o research/figures/energy_deficit_phase_diagram.png
