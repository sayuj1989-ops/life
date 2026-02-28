# Experiment Registry

**Last Updated:** 2026-02-28
**Status:** Active

## Core Simulation Experiments

| Experiment ID | Script Path | Dataset/Sim Setup | Outputs/Metrics | Status | Reproducibility Status | Missing Elements |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Minimal Cosserat** | `scripts/experiments/experiment_minimal_elastica.py` | IEC-coupled Cosserat rod under gravity. | `outputs/minimal_experiment_results_v2.csv` | ✅ Completed | Highly Reproducible | None |
| **Deficit Window** | `scripts/experiments/experiment_energy_deficit_window.py` | Param sweep evaluating P_counter vs S_proprio | `energy_deficit_window.csv`, `energy_deficit_window.png` | ✅ Completed | Highly Reproducible | Formal logging missing |
| **Phase Diagram** | `scripts/experiment_energy_phase_diagram.py` | 2D sweep: Length vs Curvature cost | `energy_phase_data.csv`, `energy_phase_diagram.png` | ✅ Completed | Highly Reproducible | None |
| **Spinal Jetlag** | `scripts/experiment_spinal_jetlag.py` | Modulated time-varying noise via circadian proxy | `outputs/spinal_jetlag/jetlag_cycles.csv` | ✅ Completed | Reproducible | Needs high-res plot script |
| **Optimization Failure** | `scripts/experiment_optimization_failure.py` | Digital twin gene map sweeping noise and stiffness | `outputs/optimization_failure/exploding_gradient.csv` | ✅ Completed | Reproducible | Final figure assembly |
| **Cross-Species** | `scripts/experiment_cross_species_scaling.py` | Bg number derivation from 10 species dataset | `cross_species_scaling.csv`, `cross_species_scaling.png` | ✅ Completed | Reproducible | Validation against text numbers |
| **Anisotropy Rescue** | `scripts/experiment_anisotropy_rescue.py` | Rescue stability via increased structural anisotropy | `anisotropy_rescue.csv`, `anisotropy_rescue.png` | ✅ Completed | Reproducible | None |

## Missing or Incomplete Experiments
*   **Protein Elastica:** `scripts/experiments/experiment_protein_elastica.py` | Missing outputs: `protein_elastica_results.csv` | Action: Run to generate basic output array.
*   **Instability Wedge:** `scripts/experiments/experiment_instability_wedge_elastica.py` | Missing outputs: `phase_diagram_elastica.csv` | Action: Execute parameter sweep.
*   **Protein Physics:** `scripts/experiments/experiment_protein_physics.py` | Missing outputs: `experiment_results.csv` | Action: Run to validate protein cost theory.
