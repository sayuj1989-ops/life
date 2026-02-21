# Experiment Registry

**Last Updated:** 2026-03-02
**Status:** Active

This registry tracks all computational experiments supporting the "Biological Countercurvature" manuscript.

## 1. Core Simulation Experiments

| Experiment ID | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP_01_PhaseDiagram** | `scripts/experiment_energy_phase_diagram.py` | Generate Figure 1: Energy Deficit Phase Diagram ($L$ vs $\chi_\kappa$). Identifies bifurcation point where demand ($L^4$) exceeds supply ($L^2$). | `outputs/thermodynamic_cost/energy_phase_diagram.csv`, `outputs/figures/energy_phase_diagram.png` | ✅ **Active** | Core result. Confirms $L_{crit} \approx 0.35$m. |
| **EXP_02_SpinalJetlag** | `scripts/experiment_spinal_jetlag.py` | Generate Figure 5: Microgravity & Jetlag predictions. Simulates circadian mismatch ($\phi$) and gravity loss ($g \to 0$). | `outputs/spinal_jetlag/jetlag_cycles.csv` | ✅ **Active** | Supports "Spinal Jetlag" hypothesis. Shows geometric drift when entrainment is lost. |
| **EXP_03_OptimizationFailure** | `scripts/experiment_optimization_failure.py` | Generate Figure 4 (Proxy): "Exploding Gradient" map. Sweeps $\chi_\kappa$ vs Sensory Noise $\sigma$. | `outputs/optimization_failure/exploding_gradient.csv` | ✅ **Active** | Models "generic" failure. Needs specific mutation mapping (see Gaps). |
| **EXP_04_DefectSensitivity** | `scripts/weekly_sim_defect_sensitivity.py` | Investigate "Basin of Attraction". Sweeps initial lateral defect vs $\chi_\kappa$. | `outputs/sim/2026-02-20/results.csv` | ✅ **Active** | Shows high growth drive amplifies small defects. |

## 2. Protein Structure Pipeline (AFCC)

| Component | Script Path | Purpose | Key Outputs | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AFCC_Pipeline** | `research/alphafold_countercurvature/scripts/run_afcc_daily.py` | Generate Figure 6: Protein Structure Integration. Fetches AFDB structures, computes Anisotropy/Disorder metrics. | `research/alphafold_countercurvature/data/processed/candidates.csv` | ✅ **Active** | Successfully ranks candidates (PIEZO2, COL1A1, etc.). |
| **AFCC_Report** | `research/alphafold_countercurvature/scripts/bolt_biofold_report.py` | Generate structured analysis reports. | `reports/afcc_latest.md` | ✅ **Active** | Summarizes protein metrics. |

## 3. Missing / Pending Experiments

| Experiment ID | Description | Gap | Action Required | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **EXP_MISSING_01** | **Cross-Species Scaling Validation** (Figure 3) | Manuscript claims "9 species: mouse to elephant" validation. **No script or data found in repo.** Only a toy `verify_bg.py` for Human/Mouse exists. | **CRITICAL:** Create `scripts/experiment_cross_species_scaling.py`. Gather data ($L, R, EI, g$) for 9 species. | 🚨 **High** |
| **EXP_MISSING_02** | **Specific Mutation Mapping** (Figure 4) | Manuscript claims "5 matrix protein variants simulated". Current code only does generic parameter sweeps. | **Important:** Create a mapping layer (e.g., `FBN1` $\to$ `EI *= 0.7`) in `experiment_optimization_failure.py`. | 🟠 **Medium** |
