# Research Schedule: Gravity as an Optimization Process

**Principal Investigator:** Jules
**Date:** 2026-10-28
**Status:** ACTIVE
**Theoretical Framework:** `formalism_01.md`
**Codebase Context:** `pyelastica_bridge.py`, `experiment_minimal_elastica.py`

## Executive Summary

This 12-week research schedule operationalizes the **"Gravity as an Optimization Process"** framework. We postulate that spinal alignment emerges from a biological Gradient Descent algorithm where the organism minimizes a Counter-Curvature Energy potential ($U_{CC}$). In this view, Scoliosis is identified as an **Optimization Failure**—specifically, a "Local Minimum" trap or "Exploding Gradient" driven by sensory noise or gain scheduling errors ("Spinal Jetlag").

The schedule progresses through three phases:
1.  **Computational Proof-of-Concept:** Defining the Cost Function and simulating failure modes in PyElastica.
2.  **The "Spinal Jetlag" Simulation:** Integrating Circadian dynamics to modulate the optimization Learning Rate.
3.  **Experimental Validation Design:** Developing wet-lab protocols to falsify the "Clock-Gravity" coupling.

---

## Phase 1: Computational Proof-of-Concept (Weeks 1-4)
**Objective:** Formalize the Cost Function $U_{CC}$ and simulate "Optimization Failure" due to noise.

| Week | Focus | Task | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **01** | **The Cost Function ($U_{CC}$)** | **Implement `compute_U_CC()` in `pyelastica_bridge.py`.**<br>Calculate Total Potential Energy = Elastic Energy ($U_E$) + Gravitational Energy ($U_G$) - Morphogenetic Work ($W_{bio}$). Establish the global minimum at vertical straightness. | The organism minimizes $U_{CC} = \int (U_E + U_G - \mathbf{M}_{bio} \cdot \Delta\kappa) ds$. Stability requires $\delta U_{CC} = 0$. |
| **02** | **The Bio-Gravitational Number** | **Implement `calculate_Bg()` and sweep parameters.**<br>Calculate $\mathcal{B}_g = \frac{\chi_M \langle |\nabla I| \rangle}{\rho A g L^2}$ for various conditions (e.g., Human vs. Mouse, Earth vs. Mars). Identify the critical $\mathcal{B}_{g,crit}$ where convexity is lost. | **Test B (Anisotropy Threshold):** Systems with $\mathcal{B}_g < 1$ cannot optimize against gravity, leading to buckling (Scoliosis). |
| **03** | **The Gradient Descent Loop** | **Create `optimize_spine.py`.**<br>Wrap the static simulation in an iterative loop. Update the active gain $\chi_M$ via gradient descent: $\chi_M^{t+1} = \chi_M^t - \alpha \nabla U_{CC}$, representing slow tissue remodeling. | Morphogenesis is a slow gradient descent process. Development is the trajectory through the energy landscape. |
| **04** | **Optimization Failure** | **Simulate "Exploding Gradient".**<br>Introduce sensory noise $\eta$ into the update rule. Test if high Learning Rate ($\alpha$) combined with noise leads to chaotic, high-energy shapes (Scoliosis) instead of convergence. | **H_2025_02_20_Active_Inference:** High noise forces the system into local minima ("Geometric Hallucinations"). |

---

## Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)
**Objective:** Integrate Time ($t$) and the Circadian Clock as a Learning Rate Scheduler.

| Week | Focus | Task | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **05** | **The Clock Model** | **Implement `CircadianClock` class.**<br>Model a simple phase oscillator $\dot{\phi} = \omega + K \sin(\theta_{grav} - \phi)$. Output a time-dependent scalar $C(t) \in [0,1]$ representing clock amplitude. | **H_2026_07_30_Spinal_Jetlag:** Gravity acts as the Zeitgeber ($\theta_{grav}$) for the spinal clock. |
| **06** | **Learning Rate Scheduling** | **Modulate $\alpha$ with $C(t)$.**<br>Update the optimizer: $\chi_M^{t+1} = \chi_M^t - \alpha \cdot C(t) \cdot \nabla U_{CC}$. Ensure remodeling only occurs when $C(t)$ is high (permissive window). | **H_2026_02_05_Gain_Hysteresis:** Mechanical plasticity is gated by the circadian cycle. Remodeling requires temporal synchronization. |
| **07** | **Simulating Jetlag** | **Run `experiment_spinal_jetlag.py`.**<br>Desynchronize the external gravity vector phase from the internal clock phase. Observe if this phase mismatch leads to "Kinked" growth trajectories due to remodeling during "forbidden" zones. | **Test U (Desynchronization Drift):** Phase mismatch between load and repair cycles causes accumulation of geometric errors. |
| **08** | **Vector-Scalar Mismatch** | **Simulate Microgravity ($g=0$).**<br>Set the Vector signal (Gravity) to 0 while maintaining high Scalar signals (Pressure/Growth). Monitor $\mathcal{B}_g \to 0$ and the resulting isotropic bloating vs. directional elongation. | **H_2026_06_24_Piezo_Duality:** Loss of Vector alignment while retaining Scalar growth leads to "Frustrated Repair" and shape instability. |

---

## Phase 3: Experimental Validation Design (Weeks 9-12)
**Objective:** Translate computational predictions into falsifiable wet-lab protocols.

| Week | Focus | Task | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **09** | **Test T_Clock** | **Design `Protocol_01_Clock_Rescue`.**<br>Define an experiment using PER2::LUC vertebral explants. Test if applying cyclic mechanical loading restores BMAL1 amplitude in microgravity conditions. | **Test V (The Loading Rescue):** Mechanical strain is required to maintain clock amplitude ($\mathcal{E}_{mech} > 1$). |
| **10** | **Test B_g (Scaling)** | **Design `Protocol_02_Scaling_Law`.**<br>Outline a comparative anatomy study measuring Paraspinal PCSA / Vertebral BMC ratio across species (Mouse, Human, Giraffe) to validate $\mathcal{B}_g$ constancy. | **Test D (Critical Length Scale):** Biological structures maintain $\mathcal{B}_g \approx \text{const}$ across scales; deviation predicts risk. |
| **11** | **Microgravity Rescue** | **Design `Protocol_03_Artificial_Vector`.**<br>Propose using Magnetic Tweezers to apply "Fake Gravity" (Vector force) to specific mechanosensors (cilia/nuclei) in $0g$ cultures to rescue the optimization process. | **Test K (The Mismatch Rescue):** Artificial restoration of the Vector component should rescue the optimization process even in $0g$. |
| **12** | **Synthesis** | **Compile "Gravity Optimization" Manuscript.**<br>Synthesize simulation results (Phases 1-2) and experimental designs (Phase 3) into the final manuscript, linking $U_{CC}$ minimization to Active Inference. | Final integration of `formalism_01.md` with simulation data. |

---

## Risk Assessment

### Theoretical Bottlenecks
*   **Definition of $U_{CC}$**: The "Reference Metric" ($\kappa_{rest}$) is currently assumed to be a straight line. If the genetic target is intrinsically curved (e.g., thoracic kyphosis), the cost function becomes non-convex, potentially invalidating the simple gradient descent model.
    *   *Mitigation*: Begin with 2D planar assumptions. Introduce "Target Kyphosis" as a fixed bias term in $U_{CC}$ only after validating the straight-spine model.
*   **Time Scale Separation**: Differential Growth ($10^6$ s) and Muscle Tone ($10^{-2}$ s) operate on vastly different scales. Naive integration will be computationally intractable.
    *   *Mitigation*: Use "Effective Development Time" where 1 simulation step = 1 circadian day, abstracting fast muscle dynamics into the Stiffness Gain $\chi_M$ (Mean Field Approximation).

### Technical Risks
*   **PyElastica Stability**: High stiffness anisotropy ratios ($\mathcal{B}_g \gg 1$) often cause numerical instability in Cosserat rod formulations due to shear locking.
    *   *Mitigation*: Implement rigorous damping and validate against analytical Euler-Bernoulli solutions for small deflections. Limit anisotropy to biologically relevant ranges ($<20$).
*   **Clock Coupling**: The mathematical form of the coupling between the Clock $C(t)$ and the Optimizer is hypothetical.
    *   *Mitigation*: Test three different coupling functions (Linear, Sigmoidal, Gated) to demonstrate that the "Jetlag" phenomenon is a robust topological feature, not an artifact of a specific function choice.
