#!/bin/bash
# Generate high-impact visual artifacts for the Biological Countercurvature theory
mkdir -p research/figures/

paperbanana generate -i jules_mechanism_derivative_gain_trap.txt -c "Derivative Gain Trap" -o research/figures/jules_autonomous_mechanism_derivative_gain_trap.png
paperbanana generate -i jules_visual_abstract_metabolic_buckling.txt -c "Biological Countercurvature Visual Abstract" -o research/figures/jules_autonomous_visual_abstract_metabolic_buckling.png
paperbanana plot -d outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv --x chi_kappa --y L --color R_deficit -o research/figures/jules_autonomous_thermodynamic_phase_diagram.png
