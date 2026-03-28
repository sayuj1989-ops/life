# Toy Models Plan

**Purpose:** To de-risk the complex Cosserat simulation and provide intuitive validation for "Metabolic Buckling" and "Active Countercurvature".

**Status:** ✅ Completed (2026-03-06)

## Toy Model A: 1D Thermostatic Column (Thermodynamic)

**Goal:** Demonstrate the "Energy Deficit Bifurcation" in a minimal system without complex geometry.

**Setup:**
- Consider a 1D column of height $L$.
- **Active Curvature Cost:** $C(L) \propto \chi_\kappa^2 L^3$ (Volume $\times$ Curvature Energy).
- **Metabolic Supply:** $S(L) \propto L^2$ (Surface Area / Flux Limit).
- **Deficit:** $D(L) = C(L) - S(L)$.

**Analysis:**
- Plot $D(L)$ vs $L$.
- Identify critical length $L_{crit}$ where $D(L) > 0$.
- Show that for $L < L_{crit}$, the column is stable (Surplus). For $L > L_{crit}$, it is unstable (Deficit).

**Implementation:**
- Script: `scripts/experiments/toy_model_thermostatic.py`
- **Output:** [`outputs/figures/toy_model_thermostatic.png`](../outputs/figures/toy_model_thermostatic.png)
- **Status:** ✅ **Implemented**

## Toy Model B: The "Active" Elastica (Mechanical)

**Goal:** Validate that *intrinsic curvature* can stabilize a column against gravity *without* infinite stiffness. Specifically, link Protein Anisotropy to $L_{crit}$.

**Setup:**
- Equations derived in `docs/theory/toy_model_anisotropy.md`.
- $L_{crit} \propto A^{-0.5}$ (Inverse square root of anisotropy).

**Simulations:**
1.  **Passive:** $\chi_\kappa = 0$. Show buckling under self-weight for large $L$.
2.  **Active:** $\chi_\kappa > 0$. Show stability for the same $L$.

**Implementation:**
- Script: `scripts/toy_model_anisotropy_link.py`
- **Output:** [`outputs/figures/toy_model_anisotropy_bifurcation.png`](../outputs/figures/toy_model_anisotropy_bifurcation.png)
- **Status:** ✅ **Implemented**

## Schedule

| Model | Owner | Effort | Status |
| :--- | :--- | :--- | :--- |
| **Toy A** | PI/Theory | 0.5 day | ✅ **Completed** |
| **Toy B** | Comp Bio | 1 day | ✅ **Completed** |
| **Toy C** | Comp Bio | 1 day | ✅ **Completed** (`toy_model_js_creature.py`) |
| **Toy D** | Comp Bio | 1 day | ✅ **Completed** (`toy_model_lenke_classes.py`) |
| **Toy E** | Comp Bio | 1 day | ✅ **Completed** (`toy_model_torsional_buckling.py`) |

---

## Toy Model D: Lenke Classifications (Spatial Deficit)

**Goal:** Demonstrate how the spatial distribution of the Energy Deficit dictates the resulting scoliotic curve shape, predicting specific Lenke classifications (types 1-6).

**Setup:**
- 1D differential equation solver simulating a simplified coupled Cosserat rod under axial load (gravity).
- **Deficit Localization:** Prescribe localized "Energy Deficit" profiles ($D(s)$) based on developmental biology (e.g., lower spine deficit vs. double thoracic deficit).
- **Buckling Modes:** Solve for the resulting spatial eigenmodes ($n=1, n=2, n=3$).

**Analysis:**
- Demonstrate that a lumbar-localized deficit triggers a single C-curve (Lenke Type 5).
- Demonstrate that a multi-region deficit (e.g., thoracic + lumbar) triggers a double S-curve (Lenke Type 3).
- Demonstrate that a complex tri-region deficit triggers a triple curve (Lenke Type 4).

**Implementation:**
- Script: `scripts/experiments/toy_model_lenke_classes.py`
- **Output:** [`outputs/figures/toy_model_lenke_classes.png`](../outputs/figures/toy_model_lenke_classes.png)
- **Status:** ✅ **Implemented**

---

## Part 2: Proposed Validation Experiments (Future)

To further de-risk the theory and provide robust validation, the following toy models and real experiments are proposed:

### Proposed Additional Toy Models

1.  **Torsional Buckling Model:**
    *   **Objective:** Demonstrate that information-coupled systems resist torsional loads better than passive Euler columns.
    *   **Method:** 1D Cosserat rod with an active twisting moment counteracting applied torque.
    *   **Success Metric:** $T_{crit}$ (critical torque) is significantly higher in the active model.
    *   **Expected Outcome:** Active model maintains stability up to $2\times$ the passive $T_{crit}$.
    *   **Stop Condition:** Analytical solution matches numerical simulation within 5% error.
    *   **Implementation:** Script: `scripts/experiments/toy_model_torsional_buckling.py`
    *   **Output:** [`figures/main/toy_model_torsional_buckling.png`](../figures/main/toy_model_torsional_buckling.png)
    *   **Status:** ✅ **Implemented**

2.  **Information-Coupled Thermostatic Column:**
    *   **Objective:** Extend Toy Model A to include a delayed feedback loop mimicking biological sensor lag.
    *   **Method:** 1D column with a PID controller regulating stiffness based on strain, with a defined time delay $\tau$.
    *   **Success Metric:** Identification of a critical delay $\tau_{crit}$ that induces oscillatory instability (hunting).
    *   **Expected Outcome:** System becomes unstable when $\tau$ exceeds the mechanical relaxation time.
    *   **Stop Condition:** Phase diagram maps stable vs. unstable regions across $(\tau, L)$ parameter space.
    *   **Implementation:** Script: `scripts/experiments/toy_model_thermostatic_delay.py`
    *   **Output:** [`figures/main/toy_model_thermostatic_delay.png`](../figures/main/toy_model_thermostatic_delay.png)
    *   **Status:** ✅ **Implemented**

3.  **Holographic Instability Lattice:**
    *   **Objective:** Verify the "Exploding Gradient" region using a minimal 2D lattice.
    *   **Method:** 2D spring-mass lattice where resting lengths update based on local stress gradients.
    *   **Success Metric:** Emergence of macroscopic curvature from isotropic initial conditions under high information-coupling ($\chi_\kappa$).
    *   **Expected Outcome:** Lattice reliably buckles into a defined curve when $\chi_\kappa > \chi_{crit}$.
    *   **Stop Condition:** Consistent buckling mode observed across 100 random noise seeds.
    *   **Implementation:** Script: `scripts/experiments/toy_model_holographic_lattice.py`
    *   **Output:** [`figures/main/toy_model_holographic_lattice.png`](../figures/main/toy_model_holographic_lattice.png)
    *   **Status:** ✅ **Implemented**

4.  **Growth Vector Mismatch Ablation Model (Negative Control):**
    *   **Objective:** Demonstrate that decoupling the growth vector from the gravitational scalar abolishes the protective effect of countercurvature.
    *   **Method:** 1D Cosserat simulation where the directional scalar tracking gravity is artificially held constant while physical mass increases.
    *   **Success Metric:** System buckling at length scales far shorter than normal physiological models.
    *   **Expected Outcome:** Immediate transition to Lenke-style scoliotic shapes at $L < L_{crit}$.
    *   **Stop Condition:** Robust phase change documented in 5 distinct parametric sweeps.
    *   **Implementation:** `scripts/experiments/toy_model_vector_mismatch.py`
    *   **Status:** ⚪ **Planned**

### Proposed Real Validation Experiments

1.  **PIEZO2 Conditional Knockout (Mouse Model):**
    *   **Objective:** Validate the role of proprioception in maintaining the straight spine against gravity.
    *   **Method:** Conditional knockout of PIEZO2 in spinal proprioceptors at P0. Assess spinal curvature at P30.
    *   **Success Metric:** Significant increase in Cobb angle ($>10^\circ$) compared to wild-type controls.
    *   **Expected Outcome:** Knockout mice develop progressive, gravity-dependent scoliosis.
    *   **Stop Condition:** Statistically significant difference ($p < 0.05$) observed in cohort of $N=10$ per group.

2.  **Microgravity Clinostat Assay (In Vitro):**
    *   **Objective:** Test the "Spinal Jetlag" hypothesis regarding vector-scalar mismatch.
    *   **Method:** Culture osteoblasts under cyclic compressive loading while rotating in a 3D clinostat (simulated microgravity).
    *   **Success Metric:** Quantification of extracellular matrix (ECM) alignment and osteogenic marker expression.
    *   **Expected Outcome:** Cells show normal proliferation (scalar pressure) but disorganized ECM alignment (missing gravity vector).
    *   **Stop Condition:** Assays completed for 3 distinct biological replicates with clear imaging data.

3.  **Circadian Desynchronization (In Vivo):**
    *   **Objective:** Directly test the impact of circadian rhythm disruption on spinal geometry.
    *   **Method:** Subject wild-type mice to chronic jetlag (12h phase shift every 3 days) from P10 to P40.
    *   **Success Metric:** Measurement of spinal curvature and vertebral wedging via micro-CT.
    *   **Expected Outcome:** Disrupted mice show increased variance in spinal alignment and minor wedging compared to controls.
    *   **Stop Condition:** Micro-CT analysis completed and data blinded for analysis.

4.  **HOX Gradient Manipulation (Zebrafish):**
    *   **Objective:** Confirm that the HOX positional code acts as the "target geometry" for the IEC.
    *   **Method:** Misexpress anterior HOX genes in the posterior somites using a heat-shock inducible promoter.
    *   **Success Metric:** Observation of ectopic structural curves or altered vertebral morphology.
    *   **Expected Outcome:** Altered HOX expression induces predictable changes in the resting curvature of the spine.
    *   **Stop Condition:** Consistent phenotype observed in $>50\%$ of treated embryos ($N=50$).

5.  **Clinical Cohort Mapping of Marfan FBN1 Variances (Epidemiological):**
    *   **Objective:** Validate the 'Optimization Failure' basin of attraction directly against Marfan prevalence rates.
    *   **Method:** Extract exact Marfan scoliosis prevalence rates from 3 major patient cohorts and correlate to FBN1 protein anisotropy defect metrics in the model.
    *   **Success Metric:** $R^2 > 0.8$ correlation between simulated instability range size and clinical prevalence.
    *   **Expected Outcome:** Higher structural uncertainty directly tracks clinical prevalence percentages in the Marfan cohorts.
    *   **Stop Condition:** 3 cohorts analyzed and standard errors plotted.
