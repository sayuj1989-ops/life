# Experiment Registry

**Last Updated:** 2026-03-27
**Status:** Active

This registry tracks all computational experiments supporting the "Biological Countercurvature" manuscript, focusing on the *Spine* journal validation metrics.

## 1. Core Simulation Experiments

| Experiment ID | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP_CORE_01** | `scripts/experiments/experiment_minimal_elastica.py` | **Primary Simulation.** Runs the full Cosserat rod model with IEC coupling. Maps anisotropy/growth to curvature ($L$ vs $\chi_\kappa$, $A$). | `outputs/minimal_experiment_results_v2.csv` | ✅ **Active** | Validated. Generates core S-curve results. |
| **EXP_01a_DeficitWindow** | `scripts/experiments/experiment_energy_deficit_window.py` | Generate Figure 2 (Line Plot): Energy Deficit Window ($L$ vs Cost). Shows $P \sim L^2$ vs $S \sim L^{0.5}$ crossover. | `outputs/thermodynamic_cost/energy_deficit_window.csv` | ✅ **Active** | Confirms $L_{crit} \approx 0.35$m. |
| **EXP_01b_PhaseDiagram** | `scripts/experiment_energy_phase_diagram.py` | Generate Figure 2 (Heatmap): Bifurcation Diagram ($L$ vs $\chi_\kappa$). Shows instability region. | `outputs/figures/energy_phase_diagram.png` | ✅ **Active** | Visualizes the "Energy Cliff". |
| **EXP_02_SpinalJetlag** | `scripts/experiment_spinal_jetlag.py` | Generate Figure 5: Microgravity & Jetlag predictions. Simulates circadian mismatch ($\phi$) and gravity loss ($g \to 0$). | `outputs/spinal_jetlag/jetlag_cycles.csv` | ✅ **Active** | Supports "Spinal Jetlag" hypothesis. |
| **EXP_03_OptimizationFailure** | `scripts/experiment_optimization_failure.py` | Generate Figure 4 (Proxy): "Exploding Gradient" map. Sweeps $\chi_\kappa$ vs Sensory Noise $\sigma$. | `outputs/optimization_failure/exploding_gradient.csv` | ✅ **Active** | Models "generic" failure. |
| **EXP_04_DefectSensitivity** | `scripts/weekly_sim_defect_sensitivity.py` | Investigate "Basin of Attraction". Sweeps initial lateral defect vs $\chi_\kappa$. | `outputs/sim/2026-02-20/results.csv` | ✅ **Active** | Shows high growth drive amplifies small defects. |
| **EXP_05_Proteins** | `scripts/experiments/experiment_thermodynamic_cost_proteins.py` | Generate Table 2: Assigns metabolic cost terms to specific proteins (e.g., PPARGC1A). | `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv` | ✅ **Active** | Validated against manuscript Table 2. |
| **EXP_06_CrossSpecies** | `scripts/experiment_cross_species_scaling.py` | Generate Figure 3: Validates cross-species scaling. Uses `data/species_parameters.csv` (`Mass_kg`, `Length_m`, `EI_Nm2`) to compute $B_g$ and cross-species scaling curves. | `outputs/thermodynamic_cost/cross_species_scaling.csv` | ✅ **Active** | Added. |
| **EXP_07_MutationMap** | `scripts/experiment_optimization_failure.py` | Generate Figure 4 specific mutations: Maps `FBN1` etc. to simulation parameters. | Console/CSV output with `--run-mutations`. | ✅ **Active** | Integrated within Optimization Failure script. |
| **EXP_08_SShapeEmergence** | `scripts/sim_active_curvature_sweep.py` | Sweeps `chi_kappa` under growth + anisotropic stiffness. | `outputs/sim/2026-03-01/results.csv` | ✅ **Active** | Emergence of structural S-shape. |
| **EXP_09_AnisotropyRescue**| `scripts/experiment_anisotropy_rescue.py` | Validates vector constraints via anisotropy sweeps. | `outputs/thermodynamic_cost/anisotropy_rescue.csv` | ✅ **Active** | Generates Figure 4 (Therapeutic Rescue). |
| **EXP_10_SpineSonification**| `scripts/experiment_spine_sonification.py`| Maps buckling instability parameters to audio frequencies. | `outputs/sim/*_spine_sonification/buckling_sonification.wav`| ✅ **Active** | Public engagement/supplementary material. |
| **EXP_11_LocomotorResonance**| `scripts/experiment_locomotor_resonance.py`| Generates Locomotor Resonance peak plots. Tests "Locomotor Resonance Catastrophe" by applying oscillating vertical acceleration to mimic human walking (1.5-2.5 Hz). | `outputs/locomotor_resonance/locomotor_resonance_peak.png` | ✅ **Active** | Out-of-the-box enhancement testing resonance. |

## 2. Toy Models (Validation)

| Experiment ID | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TOY_01_Thermostatic** | `scripts/experiments/toy_model_thermostatic.py` | **Toy Model A:** 1D Thermostatic Column. Validates "Metabolic Buckling" concept without rod mechanics. | `outputs/figures/toy_model_thermostatic.png` | ✅ **Active/Validated** | Simple demonstration of $L^5$ vs $L^2$ scaling mismatch. |
| **TOY_02_Anisotropy** | `scripts/toy_model_anisotropy_link.py` | **Toy Model B:** Anisotropy-Stability Link. Validates $L_{crit} \propto A^{-0.5}$. | `outputs/figures/toy_model_anisotropy_bifurcation.png` | ✅ **Active/Validated** | Connects protein aspect ratio to spinal stability. |
| **TOY_03_JSCreature** | `scripts/experiments/toy_model_js_creature.py` | **Toy Model C:** Secondary 2D minimal representation for biomechanics reviewers. | `outputs/js_creature_toy_model` | ✅ **Active** | Potential visual addition for robustness. |
| **TOY_04_Lenke** | `scripts/experiments/toy_model_lenke_classes.py` | **Toy Model D:** Lenke Classifications. Spatial deficit distribution | `outputs/figures/toy_model_lenke_classes.png` | ✅ **Active** | Predicts scoliotic curve shape. |
| **TOY_05_Torsional** | `scripts/experiments/toy_model_torsional_buckling.py` | **Toy Model E:** Torsional Buckling Model. | `outputs/figures/toy_model_torsional_buckling.png` | ✅ **Active** | Demonstrates active torque resistance. |

## 3. Protein Structure Pipeline (AFCC)

| Component | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AFCC_Pipeline** | `research/alphafold_countercurvature/scripts/run_afcc_daily.py` | Generate Figure 6: Protein Structure Integration. Fetches AFDB structures, computes Anisotropy/Disorder metrics. | `research/alphafold_countercurvature/data/processed/candidates.csv` | ✅ **Active** | Successfully ranks candidates (PIEZO2, COL1A1, etc.). |
| **AFCC_Report** | `research/alphafold_countercurvature/scripts/bolt_biofold_report.py` | Generate structured analysis reports. | `reports/afcc_latest.md` | ✅ **Active** | Summarizes protein metrics. |

## 4. Clinical Validation Data Tracking (Phase 2)

| Dataset/Analysis | Target Application | Purpose | Expected Output | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CLIN_01_PHV** | `experiment_phv_timing.py`  | Map model Instability Window against Peak Height Velocity clinical growth charts. | Overlay plot (Simulated Deficit vs PHV Age) | ✅ **Completed** | Required for Spine clinical relevance. |
| **CLIN_02_ALSPAC** | Literature comparison | Validate prior energy deficit using low BMI at age 10 predicting AIS at age 15. | Text/Supplementary Data | ⚪ **Planned** | Cross-check core hypothesis. |
| **CLIN_03_Marfan** | `experiment_optimization_failure.py` | Map ~63% scoliosis prevalence in Marfan to FBN1 anisotropy metrics. | FBN1 Anisotropy Mapping | ✅ **Active** | Leverages existing script logic. |
| **CLIN_04_SexRatio** | Literature comparison | Map stiffness and growth rate parameter variations to the 7:1 female-to-male clinical ratio. | Text/Plot | ⚪ **Planned** | Crucial for epidemiological alignment. |

## 5. Missing / Pending Experiments

*All previously missing critical core scripts (Cross-Species Validation, Mutation Mapping) are active. Focus is entirely on executing Phase 2 Clinical Validation tasks (CLIN_01 - CLIN_04).*
