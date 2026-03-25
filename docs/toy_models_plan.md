# Toy Models & Experiments Plan
**Target:** Simplify and de-risk the "Biological Countercurvature" hypothesis for interdisciplinary reviewers.

## Existing Validation Models (Active)

### 1. TOY_01: Thermostatic Column (Metabolic Buckling)
- **Objective:** Demonstrate how a scaling mismatch between demand ($L^5$) and supply ($L^2$) predictably drives instability.
- **Method:** 1D column with thermodynamic constraints `scripts/experiments/toy_model_thermostatic.py`.
- **Status:** Validated. Output at `outputs/figures/toy_model_thermostatic.png`.

### 2. TOY_02: Anisotropy-Stability Link
- **Objective:** Show how protein-level structural geometry translates to macro-stability without full PyElastica simulation.
- **Method:** Bifurcation threshold mapping ($L_{crit} \propto A^{-0.5}$) via `scripts/toy_model_anisotropy_link.py`.
- **Status:** Validated. Output at `outputs/figures/toy_model_anisotropy_bifurcation.png`.

### 3. TOY_05: Torsional Buckling
- **Objective:** Prove that axial torque resistance requires active energy, connecting geometry to metabolism.
- **Method:** `scripts/experiments/toy_model_torsional_buckling.py`.
- **Status:** Validated. Output at `outputs/figures/toy_model_torsional_buckling.png`.

## Proposed Experiments (Next Steps)

### EXP_NEW_01: Falsification via High Capacity (Athletic Cohort Proxy)
- **Objective:** If the Energy Deficit hypothesis is true, simulating an artificially high $S_{supply}$ (e.g. modelling high baseline muscle mass) during the PHV window should completely abolish the buckling instability.
- **Method:** Modify `scripts/experiment_phv_timing.py` to add a third trace representing $P_{demand}$ relative to $S_{supply\_enhanced} = 1.5 \times S_{supply}$.
- **Success Metric:** The new $R_{eff}$ curve never crosses $R_{crit}$.
- **Expected Outcome:** Validates that capacity ($S$), not just raw growth velocity ($dL/dt$), is the protective factor.
- **Stop Condition:** Successful demonstration of an un-buckled system.

### EXP_NEW_02: Ablation of Regional Stiffness (Lenke Failure Mode)
- **Objective:** Prove that the 6 Lenke curves only emerge because of regional physiological constraints (e.g., rib cage stiffness).
- **Method:** Run `scripts/experiment_lenke_classes.py` with the $EI_{base}$ (rib cage buttressing) explicitly removed / flattened to 1.0.
- **Success Metric:** The system should collapse into generic, undifferentiated sine-wave modes rather than the localized clinical Lenke patterns.
- **Expected Outcome:** Highlights that standard mechanics without regional biological context cannot predict AIS phenotypes.
- **Stop Condition:** Production of the comparative plots (with vs. without regional stiffness).

### EXP_NEW_03: ALSPAC Negative Control (Low Growth Rate)
- **Objective:** Verify that poor metabolic supply ($S$) alone does not trigger scoliosis unless accompanied by rapid growth ($dL/dt$).
- **Method:** Simulate the ALSPAC low BMI cohort using `scripts/experiment_phv_timing.py`, pairing a low $S_{supply}$ with an artificially depressed $k_{growth}$ (representing generalized stunting/undernutrition).
- **Success Metric:** The model does not buckle; the $R_{eff}$ never exceeds $R_{crit}$.
- **Expected Outcome:** Shows that the defect is fundamentally driven by *velocity mismatch* rather than absolute weakness, predicting why not all malnourished children develop AIS.
- **Stop Condition:** Generation of the non-buckling phase trace.
