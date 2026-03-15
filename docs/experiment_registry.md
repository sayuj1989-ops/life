# Experiment Registry

**Last Updated:** 2026-03-15
**Status:** Active

This registry tracks all computational experiments supporting the "Biological Countercurvature" manuscript.

## 1. Core Simulation Experiments

| Experiment ID | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP_CORE_01** | `scripts/experiments/experiment_minimal_elastica.py` | **Primary Simulation.** Runs the full Cosserat rod model with IEC coupling. Maps anisotropy/growth to curvature ($L$ vs $\chi_\kappa$, $A$). | `outputs/minimal_experiment_results_v2.csv` | ✅ **Validated** | Generates core S-curve results. |
| **EXP_01a_DeficitWindow** | `scripts/experiments/experiment_energy_deficit_window.py` | Generate Figure 2 (Line Plot): Energy Deficit Window ($L$ vs Cost). Shows $P \sim L^2$ vs $S \sim L^{0.5}$ crossover. | `outputs/thermodynamic_cost/energy_deficit_window.csv` | ✅ **Validated** | Confirms $L_{crit} \approx 0.35$m. |
| **EXP_01b_PhaseDiagram** | `scripts/experiment_energy_phase_diagram.py` | Generate Figure 2 (Heatmap): Bifurcation Diagram ($L$ vs $\chi_\kappa$). Shows instability region. | `outputs/figures/energy_phase_diagram.png` | ⚠️ **Plot Missing** | Script exists, but unified plot requires generation. |
| **EXP_02_SpinalJetlag** | `scripts/experiment_spinal_jetlag.py` | Generate Figure 5: Microgravity & Jetlag predictions. Simulates circadian mismatch ($\phi$) and gravity loss ($g \to 0$). | `outputs/spinal_jetlag/jetlag_cycles.csv` | ✅ **Validated** | Supports "Spinal Jetlag" hypothesis. |
| **EXP_03_OptimizationFailure** | `scripts/experiment_optimization_failure.py` | Generate Figure 4 (Proxy): "Exploding Gradient" map. Sweeps $\chi_\kappa$ vs Sensory Noise $\sigma$. | `outputs/optimization_failure/exploding_gradient.csv` | ✅ **Validated** | Models "generic" failure. |
| **EXP_04_DefectSensitivity** | `scripts/weekly_sim_defect_sensitivity.py` | Investigate "Basin of Attraction". Sweeps initial lateral defect vs $\chi_\kappa$. | `outputs/sim/2026-02-20/results.csv` | ✅ **Validated** | Shows high growth drive amplifies small defects. |
| **EXP_05_Proteins** | `scripts/experiments/experiment_thermodynamic_cost_proteins.py` | Generate Table 2: Assigns metabolic cost terms to specific proteins (e.g., PPARGC1A). | `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv` | ✅ **Validated** | Validated against manuscript Table 2. |
| **EXP_06_CrossSpecies** | `scripts/experiment_cross_species_scaling.py` | Generate Figure 3: Validates cross-species scaling across 9 species to compute $B_g$. | `outputs/thermodynamic_cost/cross_species_scaling.csv` | ✅ **Validated** | Confirms the human "Allometric Trap". |
| **EXP_07_MutationMap** | `scripts/experiment_optimization_failure.py` | Generate Figure 4 specific mutations: Maps `FBN1` etc. to simulation parameters. | Console/CSV output with `--run-mutations`. | ✅ **Validated** | Integrated within Optimization Failure script. |

## 2. Toy Models & Sanity Checks
*See `docs/toy_models_plan.md` for the full framework strategy.*

| Experiment ID | Script Path | Purpose | Key Outputs | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Toy A: Thermostatic Column** | `scripts/experiments/toy_model_thermostatic.py` | 1D Metabolic Buckling confirmation. | Critical length derivation. | ✅ **Validated** |
| **Toy B: Anisotropy Link** | `scripts/toy_model_anisotropy_link.py` | Relate protein anisotropy to structural stability. | $L_{crit} \propto A^{-0.5}$ plot. | ✅ **Validated** |
| **Toy D: Lenke Classes** | `scripts/experiments/toy_model_lenke_classes.py` | Predict scoliotic curves based on deficit localization. | Spatial deficit $D(s)$. | ✅ **Validated** |
| **Toy E: Torsional Buckling** | `scripts/experiments/toy_model_torsional_buckling.py` | Demonstrate Info-coupled active models resist torque. | Critical Torque $T_{crit}$. | ✅ **Validated** |
