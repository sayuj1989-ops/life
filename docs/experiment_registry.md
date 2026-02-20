# Experiment Registry

This registry tracks all computational experiments, simulations, and data analysis pipelines in the project.

**Status Legend:**
- ✅ **Done**: Completed, results available.
- 🟡 **Active**: Currently running or in active development.
- 🔴 **Stalled**: Encountered errors or issues.
- ⚪ **Planned**: Scheduled but not started.

## 1. Core Simulation: Cosserat Rod (PyElastica)

These experiments simulate the mechanics of the spine under growth, gravity, and information coupling.

| ID | Name | Script / Command | Status | Key Findings / Outcome | Output Path |
|:---|:-----|:-----------------|:-------|:-----------------------|:------------|
| SIM_001 | **Defect Sensitivity Sweep** | `scripts/weekly_sim_defect_sensitivity.py` | 🟡 Active | Investigates amplification of small lateral defects (0.02-0.5) under high growth (chi=15.0). *Results pending verification.* | `outputs/sim/2026-02-20/` |
| SIM_002 | **Energy Deficit Bifurcation** | `scripts/weekly_sim_energy_deficit_bifurcation.py` | ✅ Done | Mapped the "Energy Deficit Window" (L > 0.35m) where metabolic demand exceeds supply. | `outputs/sim/energy_deficit_bifurcation.csv` |
| SIM_003 | **Optimization Failure** | `scripts/experiment_optimization_failure.py` | ✅ Done | Demonstrated "Exploding Gradient" failure mode when sensory noise increases. | `outputs/optimization_failure/` |
| SIM_004 | **Spinal Jetlag** | `scripts/experiment_spinal_jetlag.py` | 🟡 Active | Models circadian desynchrony; tests effect of phase lag on growth coupling. | `outputs/spinal_jetlag/` |
| SIM_005 | **Anisotropy Rescue** | `scripts/weekly_sim_anisotropy_rescue.py` | ✅ Done | High anisotropy (R=3) stabilizes moderate growth (10.0) but fails at high growth (15.0+). | `outputs/sim/2026-02-19/` |
| SIM_006 | **Focal Anisotropy Defect** | `scripts/weekly_sim_focal_anisotropy_defect.py` | ✅ Done | Basal defects (0.2-0.3) are more destabilizing than apical ones. | `outputs/sim/2026-02-18/` |
| SIM_007 | **Growth Instability** | `scripts/weekly_sim_growth_instability.py` | ✅ Done | S-shape instability emerges at chi > 14.0. | `outputs/sim/2026-02-16/` |
| SIM_008 | **Torsion High Anisotropy** | `scripts/weekly_sim_torsion_high_anisotropy.py` | ✅ Done | High anisotropy (R=10) remains unstable with torsion coupling. | `outputs/sim/2026-02-11/` |
| SIM_009 | **Gravity-Anisotropy Interaction** | `scripts/weekly_sim_gravity_anisotropy.py` | ✅ Done | High gravity (2g) + high anisotropy maintained stability in vertical setup. | `outputs/sim/2026-08-01/` |

## 2. Thermodynamic Analysis

These experiments quantify the metabolic cost of maintaining the spinal structure.

| ID | Name | Script / Command | Status | Key Findings / Outcome | Output Path |
|:---|:-----|:-----------------|:-------|:-----------------------|:------------|
| THERMO_001 | **Protein Cost Landscape** | `scripts/experiments/experiment_thermodynamic_cost_proteins.py` | ✅ Done | Quantified Anisotropy x Residues for 23 proteins. Vimentin (7.47) and PIEZO2 (4.44) are most expensive. | `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv` |
| THERMO_002 | **Energy Deficit Window** | `scripts/experiment_energy_deficit_window.py` | ✅ Done | Calculated crossover point L_crit ≈ 0.35m where P_counter > S_proprio. | `outputs/figures/energy_deficit_window.png` |

## 3. Structural Biology (AlphaFold)

These pipelines fetch and analyze protein structures to feed into the thermodynamic model.

| ID | Name | Script / Command | Status | Key Findings / Outcome | Output Path |
|:---|:-----|:-----------------|:-------|:-----------------------|:------------|
| AFCC_001 | **Daily Refresh Pipeline** | `scripts/data_management/afcc_daily_refresh.py` | ✅ Done | Automates candidate selection, UniProt mapping, structure fetching, and metrics. | `outputs/afcc/YYYY-MM-DD/` |
| AFCC_002 | **Bolt BioFold Analysis** | `scripts/data_management/bolt_biofold_analysis.py` | ✅ Done | Generates PAE heatmaps and focused structural metrics. | `outputs/bolt_biofold/` |
| AFCC_003 | **Structure Hypothesis Generator** | `scripts/structure_hypothesis_generator.py` | ✅ Done | Clusters proteins by Anisotropy vs. Disorder to suggest mechanical roles. | `reports/structure_clusters/` |

## 4. Historical / Superseded Simulations

Older simulations retained for reference. See `docs/simulations_status.md` for full details.

- **Weekly Sim 01-15**: Basic parameter sweeps (chi_kappa, chi_M, chi_E). Established baseline S-shape behavior.
- **Torsion Series**: Investigated coupling between planar curvature and torsion.

## 5. Planned / Proposed

| ID | Name | Objective | Status | Priority |
|:---|:-----|:----------|:-------|:---------|
| PLAN_001 | **Toy Model A: 1D Metabolic Spring** | Verify "Collapse" dynamics in a simplified energy-limited system. | ⚪ Planned | High |
| PLAN_002 | **Toy Model B: Supply Chain** | Model the lag between transport (supply) and growth rate (demand). | ⚪ Planned | Medium |
| PLAN_003 | **Falsification: The Anisotropic Filter** | Test if high anisotropy actually filters high-frequency noise (as claimed). | ⚪ Planned | High |
