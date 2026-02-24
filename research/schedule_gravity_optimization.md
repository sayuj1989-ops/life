# Research Schedule: Gravity as an Optimization Process

**Date:** 2026-03-10
**PI:** Jules (Theoretical Biology & Biomechanics)
**Objective:** Validate the "Gravity as Gradient Descent" hypothesis for spinal morphogenesis over a 12-week timeline. This schedule focuses on computational proof-of-concept, the "Spinal Jetlag" hypothesis, and experimental validation design.

## Summary

This research plan operationalizes the theory that the spine is an "Active Optimizing Structure" minimizing a potential energy cost function ($U_{CC}$) defined by gravity, elasticity, and information. We deploy PyElastica simulations to test failure modes ("Scoliosis as Local Minimum") and design experimental validations for the "Spinal Jetlag" and "Vector-Scalar Mismatch" hypotheses.

---

## Phase 1: Computational Proof-of-Concept (Weeks 1-4)
**Focus:** Defining the Cost Function ($U_{CC}$) and simulating "Optimization Failure" (Scoliosis).

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **1** | **The Cost Function ($U_{CC}$)** | **Implement/Refine `compute_U_CC` in `pyelastica_bridge.py`.** Formalize the energy terms: $U_{grav}$ (Gravity), $U_{elastic}$ (Strain), and $U_{info}$ (Alignment Benefit). Verify that a straight spine in 1g minimizes $U_{CC}$ when $\mathcal{B}_g > 1$. | The organism minimizes $U_{CC} = U_{grav} + U_{elastic} - U_{info}$. A failure to minimize this (high residual energy) corresponds to deformity. |
| **2** | **The Bio-Gravitational Number ($\mathcal{B}_g$)** | **Calculate $\mathcal{B}_g$ for Mouse, Human, Giraffe, Whale.** Implement `calculate_Bg.py` to sweep parameters ($\chi_M$, $L$, $\rho$) across species. Identify the critical value $\mathcal{B}_{crit} \approx 1$ where gravity overwhelms the biological moment. | Humans operate near the instability threshold ($\mathcal{B}_g \approx 1$), making us uniquely susceptible to scoliosis compared to quadrupeds (high $\mathcal{B}_g$) or aquatic mammals (buoyancy support). |
| **3** | **Optimization Failure (The Exploding Gradient)** | **Execute `experiment_optimization_failure.py`.** Simulate the "Exploding Gradient" scenario: High Gain ($\chi_\kappa \gg 1$) combined with Sensory Noise ($\sigma_{noise} > 0$). Run Monte Carlo simulations to detect stochastic buckling events. | High sensory gain (required for rapid growth) makes the system brittle. Sensory noise induces a "searching" behavior that gets trapped in a local minimum (S-curve). |
| **4** | **Vector-Scalar Mismatch** | **Simulate "Scalar Overload" in Microgravity.** Run a simulation with high Scalar drive (Growth Pressure) but Zero Vector signal (Gravity = 0). Implement the "Confused Sensor" model where $\Phi_{VS} \to 0$. | In the absence of a Vector signal (Gravity), the Scalar signal (Growth) becomes isotropic. The spine loses its "direction" and buckles under internal growth stress (Euler buckling from internal pressure). |

---

## Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)
**Focus:** Integrating Time-Dependent Learning Rate (Circadian Clock) and Vector-Scalar Mismatch.

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **5** | **The Clock Model** | **Implement/Refine `CircadianParams` logic in `pyelastica_bridge.py`.** Model the "Learning Rate" $\eta(t)$ as a function of BMAL1 expression: $\eta(t) = \eta_0 (1 + A \cos(\omega t + \phi))$. Ensure stiffness $\chi_M$ oscillates. | The spine is only "plastic" (learns geometry) during specific circadian phases (e.g., night/sleep). Mismatch between load and plasticity leads to maladaptation. |
| **6** | **Spinal Jetlag (Desynchronization)** | **Run `experiment_spinal_jetlag.py`.** Simulate a phase shift $\Delta\phi$ between the gravitational load cycle (upright/supine) and the circadian clock (plasticity window). Test $\Delta\phi = 0, \pi/2, \pi$. | **Spinal Jetlag:** If mechanical loading peaks when the tissue is "soft" (high learning rate), the spine learns the wrong shape. Anti-phase loading ($\Delta\phi = \pi$) drives curvature. |
| **7** | **The "Rescue" Simulation** | **Simulate Chronobiological Intervention.** Test if "rebooting" the clock (resetting phase $\phi$) or artificially boosting Vector signal (magnetic tweezers proxy) can escape the local minimum. | Resynchronizing the clock with the load cycle (e.g., via Melatonin or Nobiletin) can halt curve progression by realigning the "Learning Window". |
| **8** | **Multi-Cycle Drift (Long-Term)** | **Simulate 2 Weeks of Adaptation.** Run a multi-cycle simulation (14 days) to observe the accumulation of small daily errors (integral wind-up) under "Jetlagged" vs "Entrained" conditions. | Small, uncorrected errors from daily "Jetlag" accumulate over weeks into macroscopic deformity, mirroring the slow progression of adolescent scoliosis. |

---

## Phase 3: Experimental Validation Design (Weeks 9-12)
**Focus:** Designing Wet-Lab experiments to validate computational predictions.

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **9** | **Exp Design: "Test T_Clock"** | **Protocol for Zebrafish Clock Disruption.** Design an experiment using *per2::luc* zebrafish larvae. Conditions: (1) Normal Light/Dark, (2) Constant Light (Arrhythmic), (3) Shifted Cycle (Jetlag). Measure Spinal Curvature (Cobb Angle). | Arrhythmic or phase-shifted larvae will develop spinal curvature deviations significantly higher than controls, validating the "Spinal Jetlag" hypothesis. |
| **10** | **Exp Design: "The Pressure Chamber"** | **Protocol for Vector-Scalar Mismatch.** Design a setup using a hyperbaric chamber (High Scalar) vs. a Clinostat (Zero Vector). Compare bone/notochord morphology. | High pressure (Scalar) without gravity (Vector) will result in "bloated" vertebrae with low aspect ratio, whereas Gravity + Pressure yields elongation. |
| **11** | **Exp Design: "Phantom Limbs"** | **Protocol for Proprioceptive Delay.** Design an experiment to alter feedback delay $\tau$ (e.g., focal cooling of dorsal root ganglia in rats). Test if increased $\tau$ induces scoliosis in otherwise stable spines. | Increasing neural delay $\tau$ beyond a critical threshold ($\tau_{crit}$) destabilizes the feedback loop, creating "Phantom Limbs" instability even in non-rapidly growing animals. |
| **12** | **Synthesis & Validation** | **Compile "Gravity as Optimization" Manuscript.** Synthesize simulation data (Phase 1 & 2) and experimental designs (Phase 3) into a cohesive paper. Generate final figures correlating $\mathcal{B}_g$ with Cobb Angle. | The framework unifies "Scoliosis," "Microgravity Adaptation," and "Developmental Stability" under a single energy minimization principle, explaining AIS etiology. |

---

## Risk Assessment & Mitigation

1.  **Theoretical Risk:** *The "Bio-Gravitational Number" ($\mathcal{B}_g$) might oversimplify complex anisotropy.*
    *   *Mitigation:* We explicitly calculate $\mathcal{B}_g$ using tensor stiffness components ($\chi_M$ matrix) rather than scalar approximations. We will validate against Finite Element Models (FEM) if analytical drift is high.

2.  **Computational Risk:** *PyElastica simulations might be unstable with high active forces.*
    *   *Mitigation:* Use "Quasi-Static" relaxation steps rather than full dynamics for long-term growth. We implement adaptive time-stepping (`dt`) in `pyelastica_bridge.py` to handle stiff active forces.

3.  **Experimental Risk:** *Zebrafish clocks might be too robust to disrupt easily.*
    *   *Mitigation:* Use *Cry1/2* double knockouts or pharmacological clock inhibitors (e.g., KL001) if light cycles alone are insufficient.

4.  **Integration Risk:** *Mapping "Scalar Pressure" to PyElastica forces.*
    *   *Mitigation:* We model Scalar Pressure as an isotropic expansion term in the reference metric (Growth Tensor $\mathbf{\Omega}$), while Vector Gravity remains an external force density.
