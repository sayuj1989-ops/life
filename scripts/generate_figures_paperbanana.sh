#!/bin/bash
# Commands generated for PaperBanana Visualization Pipeline
# This script contains the exact paperbanana CLI commands needed to generate
# the 3 high-impact visual artifacts supporting the Biological Countercurvature theory.
# Requires GEMINI_API_KEY environment variable to be set.

# 1. Complex Mechanism Diagram: The Mechanogenetic Demand-Supply Gap
paperbanana generate --input research/figures/iec_demand_supply_mechanism.txt --caption "Mechanogenetic Demand-Supply Gap"

# 2. Key Result Plot: Thermodynamic Stability Phase Diagram
paperbanana plot --data outputs/thermodynamic_cost/phase_diagram_energy_deficit_for_plot.csv --intent "Plot a heatmap mapping L (Spinal Length) to the X-axis, chi_kappa (Coupling Strength) to the Y-axis, and R_deficit (Energy Deficit Ratio) as the color intensity. Use the viridis colormap and draw a red dashed line at the R=1 instability limit if applicable."

# 3. Visual Abstract Diagram: Biological Countercurvature of Spacetime
paperbanana generate --input research/figures/biological_countercurvature_abstract.txt --caption "Visual Abstract: Biological Countercurvature"
