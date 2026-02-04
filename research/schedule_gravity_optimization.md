# Research Schedule: Gravity as an Optimization Process
**Principal Investigator:** Jules
**Date:** 2026-10-28
**Status:** ACTIVE
**Theoretical Framework:** `formalism_01.md`
**Codebase Context:** `pyelastica_bridge.py`, `experiment_minimal_elastica.py`

## Executive Summary

This 12-week research schedule is designed to test the **"Gravity as an Optimization Process"** hypothesis, which posits that spinal alignment is the result of a biological Gradient Descent algorithm minimizing a Counter-Curvature Energy potential ($U_{CC}$). We frame Scoliosis not as a random deformity, but as an **Optimization Failure** (e.g., local minimum trap, exploding gradient) driven by sensory noise or gain scheduling errors ("Spinal Jetlag").

The schedule is divided into three phases:
1.  **Computational Proof-of-Concept:** Formalizing the Cost Function and Optimizer in PyElastica.
2.  **The "Spinal Jetlag" Simulation:** Integrating Circadian dynamics as a Learning Rate Scheduler.
3.  **Experimental Validation Design:** Translating computational predictions into falsifiable wet-lab protocols.

---

## Phase 1: Computational Proof-of-Concept (Weeks 1-4)
**Objective:** Operationalize the "Cost Function" $U_{CC}$ and simulate "Optimization Failure".

| Week | Focus | Task | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **01** | **The Cost Function ($U_{CC}$)** | **Implement `compute_U_CC()` in `pyelastica_bridge.py`.** <br> Calculate Total Potential Energy = Elastic Energy ($U_E$) + Gravitational Energy ($U_G$) - Morphogenetic Work ($W_{bio}$). | The organism minimizes $U_{CC} = \int (U_E + U_G - \mathbf{M}_{bio} \cdot \Delta\kappa) ds$. Stability requires $\delta U_{CC} = 0$. |
| **02** | **The Bio-Gravitational Number** | **Implement `calculate_Bg()` utility.** <br> Calculate $\mathcal{B}_g = \frac{\chi_M \langle |\nabla I| \rangle}{\rho A g L^2}$ for the current rod setup. Run a sweep to find the critical $\mathcal{B}_{g,crit}$ where $U_{CC}$ loses convexity. | **Test B (Anisotropy Threshold):** Systems with $\mathcal{B}_g < 1$ cannot optimize against gravity, leading to buckling (Scoliosis). |
| **03** | **The Gradient Descent Loop** | **Create `optimize_spine.py`.** <br> Instead of a static run, wrap the simulation in a loop where $\chi_M$ (Gain) and $\kappa_{rest}$ (Target) are updated iteratively: $\chi_M^{t+1} = \chi_M^t - \alpha \nabla U_{CC}$. | Morphogenesis is a slow gradient descent process. Development is the trajectory through the energy landscape. |
| **04** | **Optimization Failure** | **Simulate "Exploding Gradient".** <br> Introduce sensory noise $\eta$ into the gradient update. Test if high Learning Rate ($\alpha$) + Noise leads to chaotic spinal shapes (Scoliosis) instead of straightness. | **H_2025_02_20_Active_Inference:** High noise forces the system into local minima ("Geometric Hallucinations"). |

---

## Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)
**Objective:** Integrate Time ($t$) and the Circadian Clock as a Learning Rate Scheduler.

| Week | Focus | Task | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **05** | **The Clock Model** | **Implement `CircadianClock` class.** <br> A simple phase oscillator $\dot{\phi} = \omega + K \sin(\theta_{grav} - \phi)$. Output a time-dependent scalar $C(t) \in [0,1]$. | **H_2026_07_30_Spinal_Jetlag:** Gravity acts as the Zeitgeber ($\theta_{grav}$) for the spinal clock. |
| **06** | **Learning Rate Scheduling** | **Modulate $\alpha$ with $C(t)$.** <br> Update the optimizer: $\chi_M^{t+1} = \chi_M^t - \alpha \cdot C(t) \cdot \nabla U_{CC}$. The organism only "learns" (remodels) when the clock is active (Night/Day specific). | **H_2026_02_05_Gain_Hysteresis:** Mechanical plasticity is gated by the circadian cycle. Remodeling requires temporal synchronization. |
| **07** | **Simulating Jetlag** | **Run `experiment_spinal_jetlag.py`.** <br> Desynchronize the external gravity vector phase from the internal clock phase. Observe if this leads to "Kinked" growth trajectories. | **Test U (Desynchronization Drift):** Phase mismatch between load and repair cycles causes accumulation of geometric errors. |
| **08** | **Vector-Scalar Mismatch** | **Simulate Microgravity ($g=0$).** <br> Set Vector signal (Gravity) to 0, but keep Scalar signal (Pressure/Growth) high. Monitor $\mathcal{B}_g$ and $U_{CC}$ evolution. | **H_2026_06_24_Piezo_Duality:** Loss of Vector alignment while retaining Scalar growth leads to "Frustrated Repair" and isotropic bloating. |

---

## Phase 3: Experimental Validation Design (Weeks 9-12)
**Objective:** Translate simulations into wet-lab protocols.

| Week | Focus | Task | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **09** | **Test T_Clock** | **Design `Protocol_01_Clock_Rescue`.** <br> Define experiment to test if Cyclic Loading rescues BMAL1 amplitude in microgravity (using PER2::LUC explants). | **Test V (The Loading Rescue):** Mechanical strain is required to maintain clock amplitude ($\mathcal{E}_{mech} > 1$). |
| **10** | **Test B_g (Scaling)** | **Design `Protocol_02_Scaling_Law`.** <br> Protocol to measure Paraspinal PCSA / Vertebral BMC ratio across species (Mouse, Human, Giraffe) to validate $\mathcal{B}_g$ constancy. | **Test D (Critical Length Scale):** Biological structures maintain $\mathcal{B}_g \approx \text{const}$ across scales; deviation predicts risk. |
| **11** | **Microgravity Rescue** | **Design `Protocol_03_Artificial_Vector`.** <br> Protocol using Magnetic Tweezers to apply "Fake Gravity" (Vector force) to specific sensors (cilia/nuclei) in $0g$ cultures. | **Test K (The Mismatch Rescue):** Artificial restoration of the Vector component should rescue the optimization process even in $0g$. |
| **12** | **Synthesis** | **Compile "Gravity Optimization" Manuscript.** <br> Synthesize simulation results (Phases 1-2) and experimental designs (Phase 3) into a single coherent framework. | Final integration of `formalism_01.md` with simulation data. |

---

## Risk Assessment

### Theoretical Bottlenecks
*   **Definition of $U_{CC}$**: The "Reference Metric" ($\kappa_{rest}$) is currently assumed to be a straight line. If the genetic target is intrinsically curved (e.g., thoracic kyphosis), the cost function becomes non-convex.
    *   *Mitigation*: Start with 2D planar assumption before moving to 3D torsion.
*   **Time Scale Separation**: Differential Growth happens over months; Muscle Tone happens over milliseconds. Simulating both in one loop is computationally expensive.
    *   *Mitigation*: Use "Effective Development Time" where 1 step = 1 day, abstracting fast muscle dynamics into the Stiffness Gain $\chi_M$.

### Technical Risks
*   **PyElastica Stability**: High stiffness anisotropy ratios (>10) often cause numerical instability in Cosserat rod formulations.
    *   *Mitigation*: Use `damping` parameters carefully and validate against analytical Euler-Bernoulli solutions for small deflections.
*   **Clock Coupling**: The mathematical form of the coupling between the Clock $C(t)$ and the Optimizer is hypothetical.
    *   *Mitigation*: Test three different coupling functions (Linear, Sigmoidal, Gated) to check for robustness of the "Jetlag" phenomenon.
