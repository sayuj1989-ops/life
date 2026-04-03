# Experiment Registry

**Last Updated:** 2026-04-03
**Status:** Active

This registry tracks all computational experiments supporting the "Biological Countercurvature" manuscript, focusing on the *Spine* journal validation metrics.

## 1. Core Simulation Experiments

| Experiment ID | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP_CORE_01** | `scripts/experiments/experiment_minimal_elastica.py` | Runs full Cosserat rod model with IEC coupling. Maps anisotropy/growth to curvature. | `outputs/minimal_experiment_results_v2.csv` | ✅ **Active** | Validated. Generates core S-curve results. |
| **EXP_01a_DeficitWindow** | `scripts/experiments/experiment_energy_deficit_window.py` | Energy Deficit Window ($L$ vs Cost). Shows $P \sim L^2$ vs $S \sim L^{0.5}$ crossover. | `outputs/thermodynamic_cost/energy_deficit_window.csv` | ✅ **Active** | Confirms $L_{crit} \approx 0.35$m. |
| **EXP_01b_PhaseDiagram** | `scripts/experiment_energy_phase_diagram.py` | Bifurcation Diagram ($L$ vs $\chi_\kappa$). Shows instability region. | `outputs/figures/energy_phase_diagram.png` | ✅ **Active** | Visualizes the "Energy Cliff". |
| **EXP_02_SpinalJetlag** | `scripts/experiment_spinal_jetlag.py` | Microgravity & Jetlag predictions. Simulates circadian mismatch ($\phi$) and gravity loss. | `outputs/spinal_jetlag/jetlag_cycles.csv` | ✅ **Active** | Supports "Spinal Jetlag" hypothesis. |
| **EXP_03_OptimizationFailure** | `scripts/experiment_optimization_failure.py` | "Exploding Gradient" map. Sweeps $\chi_\kappa$ vs Sensory Noise $\sigma$. | `outputs/optimization_failure/exploding_gradient.csv` | ✅ **Active** | Models "generic" failure. |
| **EXP_04_DefectSensitivity** | `scripts/weekly_sim_defect_sensitivity.py` | Sweeps initial lateral defect vs $\chi_\kappa$. | `outputs/sim/2026-02-20/results.csv` | ✅ **Active** | Shows high growth drive amplifies small defects. |
| **EXP_05_Proteins** | `scripts/experiments/experiment_thermodynamic_cost_proteins.py` | Assigns metabolic cost terms to specific proteins. | `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv` | ✅ **Active** | Validated against manuscript Table 2. |
| **EXP_06_CrossSpecies** | `scripts/experiment_cross_species_scaling.py` | Validates cross-species scaling using $B_g$ against mass/length data. | `outputs/thermodynamic_cost/cross_species_scaling.csv` | ✅ **Active** | Completed. |
| **EXP_07_MutationMap** | `scripts/experiment_optimization_failure.py` | Maps `FBN1` etc. to simulation parameters. | Console/CSV output | ✅ **Active** | Integrated within Optimization Failure script. |
| **EXP_08_SShapeEmergence** | `scripts/sim_active_curvature_sweep.py` | Sweeps `chi_kappa` under growth + anisotropic stiffness. | `outputs/sim/2026-03-01/results.csv` | ✅ **Active** | Emergence of structural S-shape. |
| **EXP_09_AnisotropyRescue**| `scripts/experiment_anisotropy_rescue.py` | Validates vector constraints via anisotropy sweeps. | `outputs/thermodynamic_cost/anisotropy_rescue.csv` | ✅ **Active** | Generates Figure 4 (Therapeutic Rescue). |

## 2. Toy Models (Validation)

| Experiment ID | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TOY_01_Thermostatic** | `scripts/experiments/toy_model_thermostatic.py` | **Toy Model A:** 1D Thermostatic Column. | `outputs/figures/toy_model_thermostatic.png` | ✅ **Validated** | Demonstrates $L^5$ vs $L^2$ scaling mismatch. |
| **TOY_02_Anisotropy** | `scripts/toy_model_anisotropy_link.py` | **Toy Model B:** Anisotropy-Stability Link ($L_{crit} \propto A^{-0.5}$). | `outputs/figures/toy_model_anisotropy_bifurcation.png` | ✅ **Validated** | Connects aspect ratio to stability. |
| **TOY_03_JSCreature** | `scripts/experiments/toy_model_js_creature.py` | **Toy Model C:** 2D minimal representation. | `outputs/js_creature_toy_model` | ✅ **Validated** | Secondary biomechanics robust check. |
| **TOY_04_Lenke** | `scripts/experiments/toy_model_lenke_classes.py` | **Toy Model D:** Lenke Classifications (Spatial deficit distribution). | `outputs/figures/toy_model_lenke_classes.png` | ✅ **Validated** | Predicts scoliotic curve shape. |
| **TOY_05_Torsional** | `scripts/experiments/toy_model_torsional_buckling.py` | **Toy Model E:** Torsional Buckling Model. | `outputs/figures/toy_model_torsional_buckling.png` | ✅ **Validated** | Demonstrates active torque resistance. |

## 3. Protein Structure Pipeline (AFCC)

| Component | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AFCC_Pipeline** | `research/alphafold_countercurvature/scripts/run_afcc_daily.py` | Fetches AFDB structures, computes Anisotropy/Disorder metrics. | `data/processed/candidates.csv` | ✅ **Active** | Successfully ranks candidates. |

## 4. Clinical Validation Data Tracking (Phase 2)

| Dataset/Analysis | Target Application | Purpose | Expected Output | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CLIN_01_PHV** | `experiment_phv_timing.py` (Pending) | Map model Instability Window against Peak Height Velocity clinical growth charts. | Overlay plot | 🔴 **Pending** | Required for Spine clinical relevance. |
| **CLIN_02_ALSPAC** | Literature comparison | Validate prior energy deficit using low BMI at age 10 predicting AIS at age 15. | Text/Supplementary Data | ⚪ **Planned** | Cross-check core hypothesis. |
| **CLIN_03_Marfan** | `experiment_optimization_failure.py` | Map ~63% scoliosis prevalence in Marfan to FBN1 anisotropy metrics. | FBN1 Anisotropy Mapping | ✅ **Active** | Leverages existing script logic. |
| **CLIN_04_SexRatio** | Literature comparison | Map stiffness and growth rate parameter variations to the 7:1 female-to-male clinical ratio. | Text/Plot | ⚪ **Planned** | Crucial for epidemiological alignment. |
