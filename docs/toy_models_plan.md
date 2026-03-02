# Toy Models Plan

**Purpose:** To de-risk the complex Cosserat simulation and provide intuitive validation for "Metabolic Buckling" and "Active Countercurvature".

**Status:** ✅ Completed (2026-05-25)

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

---

## Part 2: Proposed Validation Experiments (Future)

To further de-risk the theory and provide robust validation, the following toy models and real experiments are proposed:

### Additional Toy Models (Implemented)

1.  **Torsional Buckling Model:**
    *   **Objective:** Demonstrate that information-coupled systems resist torsional loads better than passive Euler columns.
    *   **Method:** 1D Cosserat rod with an active twisting moment counteracting applied torque.
    *   **Implementation:** Script: `scripts/experiments/toy_model_torsional_buckling.py`
    *   **Output:** [`outputs/figures/toy_model_torsional_buckling.png`](../outputs/figures/toy_model_torsional_buckling.png)
    *   **Status:** ✅ **Implemented**

2.  **Information-Coupled Thermostatic Column:**
    *   **Objective:** Extend Toy Model A to include a delayed feedback loop mimicking biological sensor lag.
    *   **Method:** 1D column with a PID controller regulating stiffness based on strain, with a defined time delay $\tau$.
    *   **Implementation:** Script: `scripts/experiments/toy_model_delayed_thermostatic.py`
    *   **Output:** [`outputs/figures/toy_model_delayed_thermostatic.png`](../outputs/figures/toy_model_delayed_thermostatic.png)
    *   **Status:** ✅ **Implemented**

3.  **Holographic Instability Lattice:**
    *   **Objective:** Verify the "Exploding Gradient" region using a minimal 2D lattice.
    *   **Method:** 2D spring-mass lattice where resting lengths update based on local stress gradients.
    *   **Implementation:** Script: `scripts/experiments/toy_model_holographic_lattice.py`
    *   **Output:** [`outputs/figures/toy_model_holographic_lattice.png`](../outputs/figures/toy_model_holographic_lattice.png)
    *   **Status:** ✅ **Implemented**

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
