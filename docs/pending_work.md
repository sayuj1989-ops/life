# Pending Work

This document tracks immediate, actionable tasks required to advance the research project.

## Priority 1: High (Next 7 Days)
- [ ] **Verify "Defect Sensitivity" Results:** Locate or re-run `scripts/weekly_sim_defect_sensitivity.py` and confirm output in `outputs/sim/`.
- [ ] **Generate "Defect Sensitivity" Plots:** Ensure `plot_defect_cobb.png` and `plot_defect_slat.png` are created and look correct.
- [ ] **Implement "Toy Model A":** Create `scripts/experiments/toy_model_metabolic_spring.py` to simulate energy-limited collapse.
- [ ] **Update Protein Table:** Add "Energy Supply (Gamma_m)" scaling details to `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv`.

## Priority 2: Medium (Next 30 Days)
- [ ] **Run "Energy Phase Diagram":** Implement `scripts/experiments/experiment_energy_phase_diagram.py` to map (Growth Rate vs. Energy Supply).
- [ ] **Synthesize "Protein Cost Landscape":** Write a report (`reports/protein_cost_landscape.md`) linking anisotropy to ATP cost.
- [ ] **Draft Figure 2 (Defect Sensitivity):** Create a high-quality figure for the manuscript using simulation data.
- [ ] **Draft Figure 3 (Energy Deficit):** Visualize the $L^3$ vs $L^2$ scaling mismatch and the "window".

## Priority 3: Low (Backlog)
- [ ] **Explore "Spinal Jetlag":** Continue refining the circadian mismatch simulation (`scripts/experiment_spinal_jetlag.py`).
- [ ] **Code Cleanup:** Refactor `src/spinalmodes` for better modularity and documentation.
- [ ] **Web Dashboard:** Update the project website/dashboard with latest results.
- [ ] **Literature Review:** Update `manuscript/references.bib` with 2025/2026 papers.

## Manuscript Tasks
- [ ] **Abstract:** Polish the abstract in `manuscript/nature_final.md` to be punchier.
- [ ] **Methods:** Verify all parameters in "Methods" section match the actual code.
- [ ] **Discussion:** Add a paragraph on "Sexual Dimorphism" based on new metabolic depth calculations.
