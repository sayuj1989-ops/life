# Research Schedule: Gravity as an Optimization Process

**Date:** 2026-02-25
**PI:** Jules (Theoretical Biology & Biomechanics)
**Objective:** Validate the "Gravity as Gradient Descent" hypothesis for spinal morphogenesis over a 12-week timeline.

## Summary

This research plan operationalizes the theory that the spine is an "Active Optimizing Structure" minimizing a potential energy cost function ($U_{CC}$) defined by gravity, elasticity, and information. We will deploy computational simulations using PyElastica to test failure modes ("Scoliosis as Local Minimum") and design experimental validations for the "Spinal Jetlag" and "Vector-Scalar Mismatch" hypotheses.

---

## Phase 1: Computational Proof-of-Concept (Weeks 1-4)
**Focus:** Defining the Cost Function ($U_{CC}$) and simulating "Optimization Failure".

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **1** | **The Cost Function ($U_{CC}$)** | **Implement `compute_U_CC` in `pyelastica_bridge.py`.** Formalize the energy terms: $U_{grav}$ (Gravity), $U_{elastic}$ (Strain), and $U_{info}$ (Alignment Benefit). Verify that a straight spine in 1g minimizes $U_{CC}$ when $\mathcal{B}_g > 1$. | The organism minimizes $U_{CC} = U_{grav} + U_{elastic} - U_{info}$. A failure to minimize this (high residual energy) corresponds to deformity. |
| **2** | **The Bio-Gravitational Number ($\mathcal{B}_g$)** | **Implement `calculate_Bg` utility.** Create a script to sweep $\chi_M$ (morphomechanical stiffness) and $L$ (length) to map the $\mathcal{B}_g$ phase space. Identify the critical value $\mathcal{B}_{crit} \approx 1$ where gravity overwhelms the biological moment. | Scoliosis onset occurs when $\mathcal{B}_g < 1$, i.e., when the biological counter-moment ($\chi_M \nabla I$) is insufficient to oppose the gravitational moment ($\rho A g L^2$). |
| **3** | **Optimization Failure (The Exploding Gradient)** | **Refine `experiment_optimization_failure.py`.** Simulate the "Exploding Gradient" scenario: High Gain ($\chi_\kappa \gg 1$) combined with Sensory Noise ($\sigma_{noise} > 0$). Run Monte Carlo simulations to detect stochastic buckling events. | High sensory gain (required for rapid growth) makes the system brittle. Sensory noise induces a "searching" behavior that gets trapped in a local minimum (S-curve). |
| **4** | **The Developmental Loop** | **Implement `simulate_growth.py`.** Create a wrapper around `pyelastica_bridge.py` that updates intrinsic curvature $\kappa_{rest}$ over "developmental time" (weeks) based on residual stress, simulating the "Slow Optimizer". | Differential growth is the primary optimizer. If the growth update rule is too slow relative to perturbation frequency ($\mathcal{D}_{morph} \gg 1$), errors accumulate. |

---

## Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)
**Focus:** Integrating Time-Dependent Learning Rate (Circadian Clock) and Vector-Scalar Mismatch.

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **5** | **The Clock Model** | **Implement `CircadianParams` logic in `pyelastica_bridge.py`.** Model the "Learning Rate" $\eta(t)$ as a function of BMAL1 expression: $\eta(t) = \eta_0 (1 + A \cos(\omega t + \phi))$. Ensure stiffness $\chi_M$ oscillates. | The spine is only "plastic" (learns geometry) during specific circadian phases (e.g., night/sleep). Mismatch between load and plasticity leads to maladaptation. |
| **6** | **Spinal Jetlag (Desynchronization)** | **Run `experiment_spinal_jetlag.py`.** Simulate a phase shift $\Delta\phi$ between the gravitational load cycle (upright/supine) and the circadian clock (plasticity window). | **Spinal Jetlag:** If mechanical loading peaks when the tissue is "soft" (high learning rate), the spine learns the wrong shape. $\Delta\phi \neq 0$ drives curvature. |
| **7** | **Vector-Scalar Mismatch (Microgravity)** | **Simulate Microgravity ($g \to 0$).** Set Gravity Vector to zero but maintain Scalar Drive (Pressure/Growth). Implement the "Confused Sensor" model where $\Phi_{VS} \to 0$. | In the absence of a Vector signal (Gravity), the Scalar signal (Growth) becomes isotropic. The spine loses its "direction" and buckles under internal growth stress. |
| **8** | **The "Rescue" Simulation** | **Simulate Pharmacological Rescue.** Test if "rebooting" the clock (resetting phase $\phi$) or artificially boosting Vector signal (magnetic tweezers proxy) can escape the local minimum. | Resynchronizing the clock with the load cycle (e.g., via Melatonin or Nobiletin) can halt curve progression by realigning the "Learning Window". |

---

## Phase 3: Experimental Validation Design (Weeks 9-12)
**Focus:** Designing Wet-Lab experiments to validate computational predictions.

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **9** | **Experiment Design: "Test T_Clock"** | **Protocol for Zebrafish Clock Disruption.** Design an experiment using *per2::luc* zebrafish larvae. Conditions: (1) Normal Light/Dark, (2) Constant Light (Arrhythmic), (3) Shifted Cycle (Jetlag). Measure Spinal Curvature (Cobb Angle). | Arrhythmic or phase-shifted larvae will develop spinal curvature deviations significantly higher than controls, validating the "Spinal Jetlag" hypothesis. |
| **10** | **Experiment Design: "The Pressure Chamber"** | **Protocol for Vector-Scalar Mismatch.** Design a setup using a hyperbaric chamber (High Scalar) vs. a Clinostat (Zero Vector). Compare bone/notochord morphology. | High pressure (Scalar) without gravity (Vector) will result in "bloated" vertebrae with low aspect ratio, whereas Gravity + Pressure yields elongation. |
| **11** | **Data Pipeline & Integration** | **Develop `analyze_experimental_data.py`.** Create a pipeline to ingest experimental data (images/CSV) and map them to $\mathcal{B}_g$ and $\Phi_{VS}$ parameter space for model validation. | Experimental results should map to the "Unstable Region" of the computationally derived phase diagram. |
| **12** | **Synthesis & Manuscript** | **Draft "Gravity as Optimization" Manuscript.** Compile simulation results (Phase 1 & 2) and experimental designs (Phase 3) into a cohesive paper. | The theoretical framework unifies "Scoliosis," "Microgravity Adaptation," and "Developmental Stability" under a single energy minimization principle. |

---

## Risk Assessment & Mitigation

1.  **Theoretical Risk:** *The "Cost Function" might be ill-defined for biological growth.*
    *   *Mitigation:* We explicitly separate "Elastic Energy" (Passive) from "Informational Energy" (Active). We will use `compute_U_CC` to track the ratio, ensuring the active term $\chi_M$ behaves physically (as a generalized stiffness).

2.  **Computational Risk:** *PyElastica simulations might be too slow for "Developmental Time" (Weeks).*
    *   *Mitigation:* Use the "Quasi-Static" assumption. We do not simulate every second of growth. We step `t_growth` in discrete intervals (e.g., 1 day), running a short relaxation simulation (10s) at each step to find equilibrium.

3.  **Experimental Risk:** *Zebrafish clocks might be too robust to disrupt easily.*
    *   *Mitigation:* Use *Cry1/2* double knockouts or pharmacological clock inhibitors (e.g., KL001) if light cycles alone are insufficient.

4.  **Integration Risk:** *Mapping "Scalar Pressure" to PyElastica forces.*
    *   *Mitigation:* We model Scalar Pressure as an isotropic expansion term in the reference metric (Growth Tensor $\mathbf{\Omega}$), while Vector Gravity remains an external force density.
