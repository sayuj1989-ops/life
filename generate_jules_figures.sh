#!/bin/bash
paperbanana generate --input research/figures/mechanism_desc.txt --output research/figures/generated_mechanism.png || true
paperbanana generate --input research/figures/abstract_desc.txt --output research/figures/generated_abstract.png || true
paperbanana plot --data outputs/thermodynamic_cost/energy_deficit_window.csv --intent "Plot Energy Deficit Window: P_counter vs S_proprio showing crossover at L_crit = 0.35m" --output research/figures/generated_phase_diagram.png || true
