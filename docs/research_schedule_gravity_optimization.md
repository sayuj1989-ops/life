# Research Schedule: Gravity as an Optimization Process

## Summary

This research schedule operationalizes the hypothesis that spinal alignment is a "Gradient Descent" optimization process where the organism minimizes the Total Potential Energy ($U_{CC}$) against the gravitational field. The schedule is designed to test the stability boundary defined by the Bio-Gravitational Number ($\mathcal{B}_g$) and the failure modes associated with "Spinal Jetlag" (circadian desynchronization of the learning rate).

**Core Framework:**
*   **Cost Function ($U_{CC}$):** Total Potential Energy (Gravity + Elasticity - Information).
*   **Gradient:** Mechanosensory error (PIEZO2) between current shape and genetic reference metric.
*   **Optimizer:** Differential Growth (Slow) and Muscle Tone (Fast).
*   **Learning Rate Scheduler:** Circadian Clock (BMAL1) modulates tissue sensitivity ($\alpha$).
*   **Failure Mode:** Scoliosis as a "Local Minimum" or "Exploding Gradient".

## Phase 1: Computational Proof-of-Concept (Weeks 1-4)

**Objective:** Establish the baseline simulation environment in `pyelastica_bridge.py`, explicitly defining the cost function and demonstrating optimization failure.

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **1** | The Cost Function ($U_{CC}$) | Implement `compute_U_CC` in `pyelastica_bridge.py`. Calculate potential energy of gravity vs. elastic energy of the rod. | Minimizing $U_{CC}$ leads to a stable, straight spine in 1g. |
| **2** | The Gradient (Error Signal) | Implement a "Gradient Descent" step where `rest_kappa` is updated based on `kappa_error = kappa_current - kappa_target`. | Local mechanosensory feedback is sufficient to correct global posture errors. |
| **3** | The Optimizer (Muscle Tone) | Implement `ActiveMuscleTorques` as a function of the error signal: $\mathbf{M}_{bio} = -\eta \cdot \nabla U_{CC}$. Tune $\eta$ (learning rate). | Fast-acting muscle tone acts as a "momentum" term in the optimization, smoothing out high-frequency noise. |
| **4** | Optimization Failure (Scoliosis) | Simulate "Exploding Gradient" by increasing feedback delay or noise in `kappa_error`. Parameter sweep $\mathcal{B}_g < 1$. | Scoliosis emerges when the optimization step size (gain) exceeds the stability limit of the physical system. |

## Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)

**Objective:** Integrate the Circadian Clock as a time-dependent "Learning Rate Scheduler" to test the "Spinal Jetlag" hypothesis.

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **5** | The Learning Rate Scheduler | Modulate the feedback gain $\alpha(t)$ in `pyelastica_bridge.py` with a circadian function: $\alpha(t) = \alpha_0 (1 + A \cos(\omega t + \phi))$. | Synchronized oscillation of sensitivity ($\alpha$) and load ($g$) minimizes energy expenditure. |
| **6** | Vector-Scalar Mismatch ($\Phi_{VS}$) | Simulate Microgravity: Set $\mathbf{g} = 0$ (Vector loss) but maintain $S_{scalar}$ (swelling pressure). Track $\chi_M$ decay. | Loss of the vector component ($\Phi_{VS} \to 0$) causes the optimizer to lose direction, leading to "random walk" drift. |
| **7** | Desynchronization (Jetlag) | Introduce a phase shift $\Delta \phi$ between the load cycle (activity) and the sensitivity cycle (clock). Run for $t=30$ days. | A phase mismatch ($\Delta \phi \neq 0$) increases the steady-state error (Cobb angle) despite normal average load. |
| **8** | The Loading Rescue (Test V) | Simulate "Artificial Gravity" rescue: Apply periodic external forcing frequency-matched to the internal clock. | Resonant loading restores the optimization trajectory even in the absence of constant 1g. |

## Phase 3: Experimental Validation Design (Weeks 9-12)

**Objective:** Design wet-lab experiments to validate computational predictions, focusing on $\mathcal{B}_g$ and clock genes.

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **9** | Experimental Design: Test T_Clock | Design protocol for "The Desynchronization Drift": Raise zebrafish in strobe light (arhythmic) vs. 12:12 LD. Measure spinal straightness. | Arhythmic circadian clocks lead to higher variance in spinal curvature (higher "loss"). |
| **10** | Experimental Design: Test U | Design protocol for "The Loading Rescue": Apply cyclic mechanical stretch to organoids with/without clock sync. Measure $Col1a1$ expression. | Mechanical loading is only anabolic if applied during the "sensitive" phase of the circadian cycle. |
| **11** | The Bio-Gravitational Number ($\mathcal{B}_g$) | Calculate $\mathcal{B}_g$ for: Human (AIS), Mouse, Zebrafish, and Whale. Compile literature data on muscle PCSA and bone length. | Species with $\mathcal{B}_g$ closer to 1 (slender columns) are more susceptible to optimization failure (scoliosis). |
| **12** | Synthesis & Manuscript | Integrate simulation results (Phase 1 & 2) with experimental designs (Phase 3) into the `manuscript/` draft. Finalize `formalism_01.md`. | The "Gravity as Optimization" framework unifies mechanical and biological timescales of spinal deformity. |

## Risk Assessment

1.  **Parameter Estimation for $\chi_M$:**
    *   *Risk:* The value of the morphomechanical coupling constant is difficult to estimate from literature.
    *   *Mitigation:* Use Phase 1 to "reverse engineer" $\chi_M$ by fitting the model to known stability boundaries of the human spine.

2.  **Computational Cost:**
    *   *Risk:* Simulating circadian timescales (days) with mechanical timesteps (milliseconds) is computationally prohibitive in PyElastica.
    *   *Mitigation:* Use "Time-Homogenization" or dual-scale modeling. Assume mechanical equilibrium is reached instantly relative to growth/clock timescales.

3.  **Theoretical Complexity:**
    *   *Risk:* The definition of "Information" in the Cost Function remains abstract.
    *   *Mitigation:* Operationalize "Information" strictly as the deviation from the genetic `kappa_rest`, avoiding information-theoretic ambiguities.
