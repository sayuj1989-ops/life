# Research Schedule: Gravity as an Optimization Process

**Principal Investigator:** Jules
**Date:** 2026-10-27
**Status:** ACTIVE
**Theoretical Framework:** `docs/theory/formalism_01.md`
**Codebase Context:** `src/spinalmodes/countercurvature/pyelastica_bridge.py`, `scripts/experiment_minimal_elastica.py`

## Executive Summary

This 12-week research schedule tests the hypothesis that **Spinal Alignment is a Gradient Descent process minimizing a Counter-Curvature Energy potential ($U_{CC}$)**. We posit that Scoliosis is an **Optimization Failure**—specifically, a local minimum trap or exploding gradient caused by sensory noise or desynchronized gain scheduling ("Spinal Jetlag").

The schedule integrates computational modeling in PyElastica with wet-lab experimental design, focusing on the **Bio-Gravitational Number ($\mathcal{B}_g$)** and the **Vector-Scalar Mismatch** theory.

---

## Phase 1: Computational Proof-of-Concept (Weeks 1-4)
**Objective:** Operationalize the "Cost Function" and simulate "Optimization Failure" in PyElastica.

| Week | Focus | Task | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **01** | **The Cost Function ($U_{CC}$)** | **Implement `compute_U_CC()` in `SimulationResult` class (`pyelastica_bridge.py`).** <br> Calculate $U_{CC} = U_{elastic} + U_{grav} - W_{morpho}$. Verify convexity for simple rod shapes. | The organism minimizes Total Potential Energy minus Information Gain. Stability requires $\delta U_{CC} = 0$. |
| **02** | **The Bio-Gravitational Number** | **Implement `calculate_Bg()` and Species Sweep.** <br> Create a utility to calculate $\mathcal{B}_g = \frac{\chi_M \langle |\nabla I| \rangle}{\rho A g L^2}$. Run sweeps for Mouse ($L \approx 0.03m$) vs. Human ($L \approx 0.7m$) parameters to find the stability threshold ($\mathcal{B}_{g,crit} \approx 1$). | **Test B (Anisotropy Threshold):** Systems with $\mathcal{B}_g < 1$ (High Gravity / Low Gain) undergo Euler buckling (Scoliosis). |
| **03** | **The Gradient Descent Loop** | **Create `scripts/sim_gradient_descent.py`.** <br> Wrap the `CounterCurvatureRodSystem` in an outer optimization loop. Update stiffness gain $\chi_M$ iteratively: $\chi_M^{t+1} = \chi_M^t - \alpha \nabla U_{CC}$ (representing slow plastic growth). | Morphogenesis is a descent trajectory on the Free Energy landscape. |
| **04** | **Optimization Failure** | **Simulate "Exploding Gradient".** <br> Introduce Gaussian sensory noise $\eta \sim \mathcal{N}(0, \sigma)$ to the gradient update. Test if high Learning Rate ($\alpha$) + Noise leads to chaotic, high-entropy shapes (Scoliosis). | **H_2025_02_20_Active_Inference:** Loss of sensory precision (noise) prevents convergence to the global minimum, trapping the spine in a local curve. |

---

## Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)
**Objective:** Integrate Time ($t$) and the Circadian Clock as a Learning Rate Scheduler.

| Week | Focus | Task | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **05** | **The Clock Model** | **Implement `CircadianClock` in `src/spinalmodes/countercurvature/chronobiology.py`.** <br> Model a phase oscillator $\dot{\phi} = \omega + K \sin(\theta_{grav} - \phi)$. Output a gating factor $C(t) \in [0,1]$. | **H_2026_07_30_Spinal_Jetlag:** Gravity acts as the Zeitgeber ($\theta_{grav}$) for the spinal clock (BMAL1/CLOCK). |
| **06** | **Learning Rate Scheduling** | **Integrate Clock into `sim_gradient_descent.py`.** <br> Modulate the update step: $\Delta \chi_M = -\alpha \cdot C(t) \cdot \nabla U_{CC}$. Verify that "Night-only" remodeling is more stable than continuous remodeling. | **H_2026_02_05_Gain_Hysteresis:** Mechanical plasticity is temporally gated. Remodeling out of phase with the clock leads to error accumulation. |
| **07** | **Simulating Jetlag** | **Run `scripts/experiment_spinal_jetlag.py`.** <br> Force a phase shift $\Delta \phi$ between the Load Vector (Gravity) and the Clock. Measure "Geometric Error" accumulation over 30 simulation "days". | **Test U (Desynchronization Drift):** A phase mismatch ($\Delta \phi \neq 0$) breaks the "Learning Rate Schedule," causing "Kinked" growth. |
| **08** | **Vector-Scalar Mismatch** | **Simulate Microgravity ($g \to 0$).** <br> Set Gravity Vector to 0 (Vector Loss) but keep Scalar Growth Pressure high ($\chi_\kappa \gg 0$). Track $\mathcal{B}_g \to \infty$ and $\Phi_{VS} \to 0$. | **H_2026_06_24_Piezo_Duality:** Loss of Vector alignment ($\mathbf{\Lambda}$) while retaining Scalar drive leads to isotropic bloating and instability. |

---

## Phase 3: Experimental Validation Design (Weeks 9-12)
**Objective:** Translate computational predictions into falsifiable wet-lab protocols.

| Week | Focus | Task | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **09** | **Test T_Clock (Rescue)** | **Design `Protocol_01_Clock_Rescue`.** <br> Protocol for PER2::LUC vertebral explants in microgravity (Clinostat). Test if 24h Cyclic Strain restores BMAL1 amplitude. | **Test V (The Loading Rescue):** Mechanical entrainment ($\mathcal{E}_{mech}$) is required to maintain the "Learning Rate Scheduler." |
| **10** | **Test B_g (Scaling)** | **Design `Protocol_02_Allometry`.** <br> Protocol to measure Paraspinal PCSA vs. Vertebral BMC via MRI/DXA in adolescents. Calculate $\mathcal{B}_g$ for curve progressors vs. non-progressors. | **Test D (Critical Length Scale):** Scoliosis onset correlates with a drop in $\mathcal{B}_g$ below unity during the adolescent growth spurt. |
| **11** | **Microgravity Mismatch** | **Design `Protocol_03_Artificial_Vector`.** <br> Protocol for Zebrafish in Clinostat ($0g$) + Magnetic Tweezers (Artificial Vector). Test if restoring directional force rescues curvature. | **Test K (The Mismatch Rescue):** Providing a "Fake Vector" is sufficient to rescue the optimization process even without real gravity. |
| **12** | **Synthesis & Publication** | **Compile "Gravity Optimization" Manuscript.** <br> Synthesize Phase 1/2 simulations and Phase 3 protocols into the final paper structure defined in `manuscript/`. | Unification of Active Inference, Mechanics, and Chronobiology. |

---

## Risk Assessment

### Theoretical Bottlenecks
*   **The Cost Function Definition:** If $U_{CC}$ is too flat (low convexity), the Gradient Descent will be slow/stochastic.
    *   *Mitigation:* Introduce a "Momentum" term (Biological Memory/Epigenetics) to the optimizer to accelerate convergence.
*   **Parameter Space Explosion:** Phase 2 introduces $\omega, K, \phi_{lag}$.
    *   *Mitigation:* Fix $\omega$ to 24h and only sweep $K$ (Coupling Strength) to reduce dimensionality.

### Technical Risks (PyElastica)
*   **Instability at High Anisotropy:** PyElastica is known to be stiff for anisotropy ratios > 10.
    *   *Mitigation:* Use smaller timesteps ($dt < 10^{-6}$) and implicit damping for the "Microgravity" (Week 8) simulations.
*   **Integration Overhead:** Adding a Python optimization loop around the C++ optimized rod simulation may be slow.
    *   *Mitigation:* Run the optimization steps (growth) at a much slower frequency than the physics steps ($dt_{growth} = 10^5 \cdot dt_{physics}$).
