# Research Schedule: Gravity as a Gradient Descent Optimization Process

**Principal Investigator:** Jules (AI)
**Date:** 2026-05-22
**Project:** The "Thermodynamic Standing Wave" & Spinal Buckling
**Objective:** Validate the hypothesis that spinal alignment is a Gradient Descent Optimization process minimized by the Bio-Gravitational Number ($\mathcal{B}_g$) and modulated by circadian rhythms ("Spinal Jetlag").

---

## **Phase 1: Computational Proof-of-Concept (Weeks 1-4)**
**Goal:** Establish the baseline model where scoliosis is an "Optimization Failure" (Local Minimum).

| Week | Focus | Task | Hypothesis | Risk |
|---|---|---|---|---|
| **1** | **Cost Function Definition** | Define $U_{total} = U_{elastic} + U_{grav} - U_{info}$ in `formalism_01.md`. Implement `compute_cost_landscape(curvature, gravity)` in `pyelastica_bridge.py`. | The healthy spine minimizes $U_{total}$ at zero curvature (Global Minimum). | **High:** Cost landscape might be too flat (insufficient gradient). |
| **2** | **The Bio-Gravitational Number ($\mathcal{B}_g$)** | Calculate $\mathcal{B}_g = \frac{F_{gravity}}{F_{elastic}}$ for 9 species in `scripts/calculate_bio_gravity.py`. Correlate with Scoliosis prevalence. | High $\mathcal{B}_g$ implies higher susceptibility to local minima (buckling). | **Medium:** Data availability for all species. |
| **3** | **Gradient Descent Simulation** | Implement a `GradientDescentOptimizer` class in `pyelastica_bridge.py` that iteratively updates `rest_kappa` based on $\nabla U$. | The system converges to straightness *unless* learning rate $\eta$ is too high (instability). | **Low:** Numerical stability of the optimizer. |
| **4** | **Simulating Failure (Scoliosis)** | Introduce "Sensory Noise" (Gaussian jitter to $\nabla U$). Run simulations where optimization gets trapped in a local minimum. | Sensory noise > Threshold causes the optimizer to settle on a curved state (Scoliosis). | **Medium:** Tuning noise parameters to be biologically realistic. |

---

## **Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)**
**Goal:** Integrate time-dependent learning rates to simulate circadian desynchronization.

| Week | Focus | Task | Hypothesis | Risk |
|---|---|---|---|---|
| **5** | **Circadian Learning Rate** | Implement `learning_rate(t) = \eta_0 * (1 + A * cos(\omega t + \phi))` in the optimizer. | Growth/Correction only occurs effectively during "High Sensitivity" windows (Night?). | **Medium:** Determining the correct phase $\phi$ relative to activity. |
| **6** | **Vector-Scalar Mismatch (Microgravity)** | Simulate a scenario: High Growth Pressure (Scalar) but Zero Gravity (Vector). | Without the gravity vector to orient the gradient, the optimizer performs a "Random Walk" (Disorientation). | **High:** Defining "Scalar" pressure in the model explicitly. |
| **7** | **The "Jetlag" Condition** | Introduce a phase shift $\Delta \phi$ between the clock and the mechanical load cycle. | Mismatch ($\Delta \phi \neq 0$) reduces convergence speed, leading to accumulated error (progressive curve). | **Low:** Straightforward math implementation. |
| **8** | **Rescue via "Melatonin"** | Simulate a "Drug" that re-synchronizes the clock ($\Delta \phi \to 0$) or dampens the noise. | Re-synchronization restores the Global Minimum convergence. | **Medium:** Modeling the "drug" effect mechanism mechanistically. |

---

## **Phase 3: Experimental Validation Design (Weeks 9-12)**
**Goal:** Design wet-lab experiments to validate computational predictions.

| Week | Focus | Task | Hypothesis | Risk |
|---|---|---|---|---|
| **9** | **Experiment T_Clock Design** | Design a protocol for `C2C12` myoblasts under cyclic strain with/without BMAL1 knockdown. | BMAL1-deficient cells will fail to align with the strain vector (Loss of Optimization). | **High:** Experimental complexity (cyclic strain bioreactor). |
| **10** | **The "Gravity-Blind" Assay** | Propose an experiment: 3D Clinostat rotation (simulated microgravity) + Pressure. | Cells will proliferate but lose directional organization (Isotropic expansion). | **Medium:** Access to Clinostat hardware. |
| **11** | **Genetic Target Validation** | Select top 3 candidates (from `candidates_master.csv`) for CRISPR interference in the model. | Knockdown of `PIEZO2` (Sensor) or `LBX1` (Integrator) flattening the Cost Landscape. | **Low:** Candidates already identified. |
| **12** | **Manuscript Integration** | Synthesize findings into "Gravity as an Optimization Process" section of the Nature manuscript. | The "Optimization Failure" model unifies genetic and biomechanical theories. | **Low:** Writing task. |

---

## **Risk Assessment & Mitigation**

1.  **Theoretical Bottleneck:** The **Bio-Gravitational Number ($\mathcal{B}_g$)** might not show a clear threshold for scoliosis across species.
    *   *Mitigation:* Refine $\mathcal{B}_g$ to include "Slenderness Ratio" or "Growth Rate" ($\mathcal{B}_{g}^*$).
2.  **Simulation Artifacts:** The `GradientDescentOptimizer` might diverge numerically rather than biologically.
    *   *Mitigation:* Use adaptive step sizes (e.g., Adam optimizer analogue) and strict bounds on `rest_kappa`.
3.  **Experimental Feasibility:** "Spinal Jetlag" is hard to test in vivo.
    *   *Mitigation:* Focus on the *in vitro* "Clock-Strain" experiment (Week 9) as a proxy for the whole spine.
