# Experiment Registry

**Last Updated:** 2026-03-19
**Status:** Active

This registry tracks all computational experiments supporting the "Biological Countercurvature" manuscript.

## 1. Core Simulation Experiments

| Experiment ID | Script Path | Purpose | Setup / Parameters | Key Outputs / Metrics | Status & Reproducibility | Notes (Missing Items) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP_CORE_01** | `scripts/experiments/experiment_minimal_elastica.py` | **Primary Simulation.** Runs full Cosserat rod with IEC coupling. Maps anisotropy/growth to curvature. | Cosserat rod + IEC coupling. Sweeps $\chi_\kappa$, $A$ | $L$ vs $\chi_\kappa, A$ (`minimal_experiment_results_v2.csv`) | ✅ **Tracked in `outputs/`** | Validated. Generates core S-curve results. |
| **EXP_01a_DeficitWindow** | `scripts/experiments/experiment_energy_deficit_window.py` | Figure 2: Energy Deficit Window ($L$ vs Cost crossover). | Defines $P \sim L^2$ vs $S \sim L^{0.5}$ | Cost crossover bounds (`energy_deficit_window.csv`) | ✅ **Tracked in `outputs/`** | Confirms $L_{crit} \approx 0.35$m. |
| **EXP_01b_PhaseDiagram** | `scripts/experiment_energy_phase_diagram.py` | Figure 2: Bifurcation Diagram ($L$ vs $\chi_\kappa$). Shows instability region. | Parameter sweep mapping $L$ vs $\chi_\kappa$ | Heatmap arrays (`outputs/figures/energy_phase_diagram.png`) | ⚠️ **Output plot missing** | **MISSING:** The unified plot figure is currently absent and needs generation. |
| **EXP_02_SpinalJetlag** | `scripts/experiment_spinal_jetlag.py` | Figure 5: Microgravity & Jetlag predictions. | Simulates circadian mismatch ($\phi$) and gravity loss ($g \to 0$) | Jetlag cycles metrics (`jetlag_cycles.csv`) | ✅ **Tracked in `outputs/`** | Supports "Spinal Jetlag" hypothesis. |
| **EXP_03_OptimizationFailure** | `scripts/experiment_optimization_failure.py` | Figure 4: "Exploding Gradient" map & mutation map. | Sweeps $\chi_\kappa$ vs Sensory Noise $\sigma$ | Map $\chi_\kappa$ vs $\sigma$ (`exploding_gradient.csv`) | ✅ **Tracked in `outputs/`** | Models generic failure and specific mutations. |
| **EXP_04_DefectSensitivity** | `scripts/weekly_sim_defect_sensitivity.py` | Investigate "Basin of Attraction" and defect amplification. | Sweeps initial lateral defect vs $\chi_\kappa$ | Curve dev metrics (`outputs/sim/2026-02-20/results.csv`) | ✅ **Tracked in `outputs/`** | Shows high growth drive amplifies small defects. |
| **EXP_05_Proteins** | `scripts/experiments/experiment_thermodynamic_cost_proteins.py` | Table 2: Assigns metabolic cost terms to specific proteins. | Maps protein interactions to metabolic costs | Tables (`thermodynamic_cost_proteins.csv`) | ✅ **Tracked in `outputs/`** | Validated against manuscript Table 2. |
| **EXP_06_CrossSpecies** | `scripts/experiment_cross_species_scaling.py` | Figure 3: Validates cross-species scaling of metabolic need. | Loads `data/species_parameters.csv` (`Mass_kg`, `Length_m`, `EI_Nm2`) | $B_g$ vs Mass (`cross_species_scaling.csv`) | ✅ **Tracked in `outputs/`** | Validates Passive vs Active scaling curves. |
| **EXP_08_SShapeEmergence** | `scripts/sim_active_curvature_sweep.py` | Sweeps active parameters under growth + anisotropy. | Sweeps `chi_kappa` under growth | S-shape metrics (`outputs/sim/2026-03-01/results.csv`) | ✅ **Tracked in `outputs/`** | Tracks emergence of structural S-shape. |
| **EXP_09_AnisotropyRescue**| `scripts/experiment_anisotropy_rescue.py` | Figure 4 (Rescue): Validates vector constraints via anisotropy sweeps. | Anisotropy sweep against critical buckling | Anisotropy constraints (`anisotropy_rescue.csv`) | ✅ **Tracked in `outputs/`** | Models therapeutic rescues via anisotropy. |
| **EXP_10_SpineSonification**| `scripts/experiment_spine_sonification.py`| Maps buckling instability to audio. | Audio mapping variables | `.wav` (`outputs/sim/*_spine_sonification/buckling_sonification.wav`)| ✅ **Tracked in `outputs/`** | Public engagement material. |
| **EXP_11_LocomotorResonance**| `scripts/experiment_locomotor_resonance.py`| Locomotor Resonance peak plots. | Applies oscillating vertical acceleration (1.5-2.5 Hz) | Resonance peak maps (`locomotor_resonance_peak.png`) | ✅ **Tracked in `outputs/`** | Tests "Locomotor Resonance Catastrophe". |
| **EXP_12_AFCCPipeline** | `scripts/afcc_daily_refresh.py` | AlphaFold Mechanotransduction structure metrics. | Protein structure data parsing & calculations | Ranked output (`candidates.csv`) | ✅ **Active in `reports/`** | Ranks PIEZO2, COL1A1 etc. |

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

## 4. Missing / Pending Experiments

*All previously missing critical scripts and mapping procedures (Cross-Species Validation, Mutation Mapping) have now been successfully integrated into the active model logic.*
