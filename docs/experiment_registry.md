# Experiment Registry

**Last Updated:** 2026-03-01
**Status:** Active

This registry tracks all computational experiments supporting the "Biological Countercurvature" manuscript.

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
| **EXP_08_SShapeEmergence** | `scripts/experiments/weekly_sim_s_shape_emergence.py` | Sweeps `chi_kappa` under growth + anisotropic stiffness. | `outputs/sim/2026-03-01/results.csv` | ✅ **Active** | Emergence of structural S-shape. |

## 2. Toy Models (Validation)

| Experiment ID | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TOY_01_Thermostatic** | `scripts/experiments/toy_model_thermostatic.py` | **Toy Model A:** 1D Thermostatic Column. Validates "Metabolic Buckling" concept without rod mechanics. | `outputs/figures/toy_model_thermostatic.png` | ✅ **Active/Validated** | Simple demonstration of $L^5$ vs $L^2$ scaling mismatch. |
| **TOY_02_Anisotropy** | `scripts/toy_model_anisotropy_link.py` | **Toy Model B:** Anisotropy-Stability Link. Validates $L_{crit} \propto A^{-0.5}$. | `outputs/figures/toy_model_anisotropy_bifurcation.png` | ✅ **Active/Validated** | Connects protein aspect ratio to spinal stability. |

## 3. Protein Structure Pipeline (AFCC)

| Component | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AFCC_Pipeline** | `research/alphafold_countercurvature/scripts/run_afcc_daily.py` | Generate Figure 6: Protein Structure Integration. Fetches AFDB structures, computes Anisotropy/Disorder metrics. | `research/alphafold_countercurvature/data/processed/candidates.csv` | ✅ **Active** | Successfully ranks candidates (PIEZO2, COL1A1, etc.). |
| **AFCC_Report** | `research/alphafold_countercurvature/scripts/bolt_biofold_report.py` | Generate structured analysis reports. | `reports/afcc_latest.md` | ✅ **Active** | Summarizes protein metrics. |

## 4. Missing / Pending Experiments

*All previously missing critical scripts and mapping procedures (Cross-Species Validation, Mutation Mapping) have now been successfully integrated into the active model logic.*
