# Experiment Registry

**Last Updated:** 2026-04-08
**Status:** Active

This registry tracks all computational experiments supporting the "Biological Countercurvature" manuscript, focusing on the *Spine* journal validation metrics.

## 1. Core Simulation Experiments

| Experiment ID | Script Path | Purpose | Key Outputs | Status | Notes | Reproducibility | Missing Assets |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP_CORE_01** | `scripts/experiments/experiment_minimal_elastica.py` | Runs the full Cosserat rod model with IEC coupling. | `outputs/minimal_experiment_results_v2.csv` | ✅ **Active** | Validated. Generates core S-curve results. | ✅ High | None |
| **EXP_01a_DeficitWindow** | `scripts/experiments/experiment_energy_deficit_window.py` | Generate Figure 2: Energy Deficit Window ($L$ vs Cost). | `outputs/thermodynamic_cost/energy_deficit_window.csv` | ✅ **Active** | Confirms $L_{crit} \approx 0.35$m. | ✅ High | None |
| **EXP_01b_PhaseDiagram** | `scripts/experiment_energy_phase_diagram.py` | Generate Figure 2: Bifurcation Diagram ($L$ vs $\chi_\kappa$). | `outputs/figures/energy_phase_diagram.png` | ✅ **Active** | Visualizes the "Energy Cliff". | 🟡 Check | `scripts/experiment_energy_phase_diagram.py` script missing |
| **EXP_02_SpinalJetlag** | `scripts/experiment_spinal_jetlag.py` | Generate Figure 5: Microgravity & Jetlag predictions. | `outputs/spinal_jetlag/jetlag_cycles.csv` | ✅ **Active** | Supports "Spinal Jetlag" hypothesis. | 🟡 Check | `scripts/experiment_spinal_jetlag.py` script missing |
| **EXP_03_OptimizationFailure** | `scripts/experiment_optimization_failure.py` | Generate Figure 4: "Exploding Gradient" map. | `outputs/optimization_failure/exploding_gradient.csv` | ✅ **Active** | Models "generic" failure. | 🟡 Check | `scripts/experiment_optimization_failure.py` script missing |
| **EXP_06_CrossSpecies** | `scripts/experiment_cross_species_scaling.py` | Generate Figure 3: Validates cross-species scaling. | `outputs/thermodynamic_cost/cross_species_scaling.csv` | ✅ **Active** | Validated scaling bounds. | 🟡 Check | `scripts/experiment_cross_species_scaling.py` missing |
| **EXP_07_MutationMap** | `scripts/experiment_optimization_failure.py` | Generate Figure 4 specific mutations: Maps `FBN1`. | Console/CSV output. | ✅ **Active** | Integrated within Optimization script. | 🔴 Low | Dependent script missing |

*(Note: Some scripts referenced in older documentation appear to be renamed or missing in the current repository snapshot, e.g., `experiment_optimization_failure.py` -> potentially `experiment_life_thermodynamic_attractor.py` or `experiment_instability_wedge_elastica.py`. They are flagged above as needing check.)*

## 2. Toy Models (Validation)

| Experiment ID | Script Path | Purpose | Key Outputs | Status | Reproducibility |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TOY_01_Thermostatic** | `scripts/experiments/toy_model_thermostatic.py` | **Toy Model A:** 1D Thermostatic Column ($L^5$ vs $L^2$). | `outputs/figures/toy_model_thermostatic.png` | ✅ **Active** | ✅ High |
| **TOY_02_Anisotropy** | `scripts/experiments/toy_model_anisotropy_link.py` | **Toy Model B:** Anisotropy-Stability Link. | `outputs/figures/toy_model_anisotropy_bifurcation.png` | ✅ **Active** | 🟡 Path check |
| **TOY_03_JSCreature** | `scripts/experiments/toy_model_js_creature.py` | **Toy Model C:** Secondary 2D minimal representation. | `outputs/js_creature_toy_model` | ✅ **Active** | ✅ High |
| **TOY_04_Lenke** | `scripts/experiments/toy_model_lenke_classes.py` | **Toy Model D:** Lenke Classifications. Spatial deficits. | `outputs/figures/toy_model_lenke_classes.png` | ✅ **Active** | ✅ High |
| **TOY_05_Torsional** | `scripts/experiments/toy_model_torsional_buckling.py` | **Toy Model E:** Torsional Buckling Model. | `outputs/figures/toy_model_torsional_buckling.png` | ✅ **Active** | ✅ High |

## 3. Missing/Pending Analysis

To complete Phase 2 Clinical Validation, the following analyses are required but not yet implemented:

| Dataset/Analysis | Target Application | Purpose | Expected Output | Status |
| :--- | :--- | :--- | :--- | :--- |
| **CLIN_01_PHV** | `scripts/experiment_phv_timing.py` (Pending) | Map model Instability Window against PHV growth charts. | Overlay plot | 🔴 **Pending** |
| **CLIN_02_ALSPAC** | Literature comparison | Validate prior energy deficit using low BMI. | Text integration | ⚪ **Planned** |
