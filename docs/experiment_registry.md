# Experiment Registry

**Last Updated:** 2026-03-05
**Maintainer:** Comp Bio Team

This registry tracks all computational experiments, simulations, and data analysis scripts for the "Biological Countercurvature" project.

## 1. Core Simulations (Physics & Mechanics)

| Experiment Name | Script Path | Description | Status | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Energy Deficit Window** | `scripts/experiment_energy_deficit_window.py` | Simulates metabolic demand ($L^2$) vs proprioceptive supply ($L^\alpha$) to find $L_{crit}$. | ✅ **Active** | None | `outputs/thermodynamic_cost/energy_deficit.csv` |
| **Peristaltic Spine** | `scripts/experiment_peristaltic_spine.py` | Models traveling stiffness waves to explore "Phase Frustration" dynamics. | ✅ **Active** | None | `outputs/peristaltic_spine/` |
| **Optimization Failure** | `scripts/experiment_optimization_failure.py` | Maps the "Exploding Gradient" region in ($\chi_\kappa, \sigma$) space. | 🟡 **Partial** (Mutation map pending) | None | `outputs/optimization_failure/exploding_gradient.csv` |
| **Weekly Bifurcation** | `scripts/weekly_sim_energy_deficit_bifurcation.py` | 2D parameter sweep ($\chi_\kappa$ vs $L$) for the Energy Deficit Window. | ✅ **Active** | None | `outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv` |
| **Anisotropy Sweep** | `scripts/sim_anisotropy_sweep_v2.py` | Sweeps stiffness anisotropy (1.0–10.0) under high active growth. | ✅ **Active** | None | `outputs/sim/anisotropy_sweep/` |
| **Taper Sweep** | `scripts/sim_taper_sweep.py` | Sweeps geometric taper ratio (0.5–1.5) to test stability. | ✅ **Active** | None | `outputs/sim/taper_sweep/` |

## 2. Data Analysis & Validation

| Experiment Name | Script Path | Description | Status | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cross-Species Scaling** | `scripts/analysis/cross_species_scaling.py` | Validates "Allometric Trap" ($L^4$ demand vs $L^{3}$ supply) across 9 species. | ✅ **Completed** | `data/species_parameters.csv` | `outputs/figures/cross_species_scaling.png` |
| **Bolt BioFold Analysis** | `scripts/bolt_biofold_analysis.py` | Metrics analysis for key proteins (PIEZO2, COL1A1). | ✅ **Completed** | AFDB PDBs | `outputs/bolt_biofold/report.md` |

## 3. Toy Models (Theory Validation)

| Experiment Name | Script Path | Description | Status | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Thermostatic Column** | `scripts/experiments/toy_model_thermostatic.py` | 1D thermodynamic model showing energy deficit bifurcation. | ✅ **Completed** | None | `outputs/figures/toy_model_thermostatic.png` |
| **Anisotropy Link** | `scripts/toy_model_anisotropy_link.py` | Minimal mechanical model linking anisotropy to stability. | ✅ **Completed** | None | `outputs/figures/toy_model_anisotropy_bifurcation.png` |
