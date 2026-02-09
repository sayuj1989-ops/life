# Research Schedule: Gravity as an Optimization Process

## Summary

This research schedule operationalizes the hypothesis that spinal alignment is a "Gradient Descent" optimization process where the organism minimizes the **Total Potential Energy** ($U_{CC}$) against the gravitational field. The schedule is designed to test the stability boundary defined by the **Bio-Gravitational Number** ($\mathcal{B}_g$) and the failure modes associated with "**Spinal Jetlag**" (circadian desynchronization of the learning rate).

**Core Framework:**
*   **Cost Function ($U_{CC}$):** Total Potential Energy (Gravity + Elasticity - Information). The system seeks to minimize $U_{CC} = E_g + E_{el} - U_{info}$.
*   **The Gradient:** Mechanosensory error (PIEZO2) between the current shape and the genetic "Reference Metric" ($\kappa_{rest}$).
*   **The Optimizer:** The system updates shape via Differential Growth (Slow timescale) and Muscle Tone (Fast timescale).
*   **The Learning Rate Scheduler:** The Circadian Clock (BMAL1) modulates the sensitivity of the tissue to mechanical signals ($\alpha(t)$), gating the optimizer's updates to specific phases of the gravitational load cycle.
*   **The Failure Mode:** Scoliosis is a "Local Minimum" (stable deformity) or an "Exploding Gradient" (oscillatory divergence) caused by sensory noise, feedback delays, or desynchronization.

---

## Phase 1: Computational Proof-of-Concept (Weeks 1-4)

**Objective:** Establish the baseline simulation environment in `src/spinalmodes/countercurvature/pyelastica_bridge.py`, explicitly defining the cost function and demonstrating optimization failure (Scoliosis).

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **1** | The Cost Function ($U_{CC}$) | Implement a utility in `pyelastica_bridge.py` to calculate the components of $U_{CC}$: Gravitational Potential ($E_g$) vs. Elastic Strain Energy ($E_{el}$) vs. Information Work. Map the energy landscape for a simple 1D rod. | Minimizing $U_{CC}$ leads to a stable, straight spine in 1g. The system naturally finds the global minimum when $\mathcal{B}_g > 1$. |
| **2** | The Gradient (Error Signal) | Implement an iterative "Gradient Descent" loop. Update `rod.rest_kappa` in `CounterCurvatureRodSystem` based on the error between current curvature and genetic target: $\Delta \kappa_{rest} \propto -\alpha (\kappa_{curr} - \kappa_{target})$. | Local mechanosensory feedback (Gradient) is sufficient to correct global posture errors without a central controller, provided the learning rate $\alpha$ is within stability bounds. |
| **3** | The Bio-Gravitational Number ($\mathcal{B}_g$) | Perform a parameter sweep of the `CounterCurvatureParams` in `pyelastica_bridge.py`. Calculate $\mathcal{B}_g = \frac{\chi_M \langle |\nabla I| \rangle}{\rho A g L^2}$ for simulation values. Identify the critical $\mathcal{B}_g$. | There exists a critical $\mathcal{B}_g \approx 1$ where the optimizer fails to converge, leading to buckling (Local Minimum). Species with low $\mathcal{B}_g$ are susceptible to optimization failure. |
| **4** | Optimization Failure (Exploding Gradient) | Simulate "Exploding Gradient" by increasing the feedback gain (learning rate $\alpha$) or introducing delay/noise in the `ActiveMuscleTorques` update loop. Generate phase plots of Curvature vs. Time. | High sensory noise or delays cause the optimization step size to exceed the stability limit, resulting in oscillatory divergence (Scoliosis) rather than convergence. |

---

## Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)

**Objective:** Integrate the Circadian Clock as a time-dependent "Learning Rate Scheduler" to test the "Spinal Jetlag" hypothesis. What happens if the clock desynchronizes from the gravity vector?

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **5** | The Learning Rate Scheduler | Implement a time-dependent scalar for `ActiveMuscleTorques` and growth updates: $\alpha(t) = \alpha_{base} (1 + A \cos(\omega t + \phi))$. Ensure $\omega$ matches the loading cycle frequency. | Synchronizing the "Learning Rate" (sensitivity) with the "Batch Load" (daily gravity cycle) minimizes energy expenditure and maximizes correction efficiency. |
| **6** | Desynchronization (The Jetlag) | Run simulations where the clock phase $\phi$ is shifted relative to the gravity load cycle (simulating "Shift Work" or "Jetlag"). Vary phase shift $\Delta \phi$ from 0 to $\pi$. | A phase mismatch ($\Delta \phi \neq 0$) causes the optimizer to update shape based on "stale" or irrelevant gradients, increasing the steady-state error (Cobb angle) and driving instability. |
| **7** | Vector-Scalar Mismatch | Simulate **Microgravity**: Set gravity vector $\mathbf{g}=0$ but maintain high Scalar "swelling pressure". Implement `beta_H` parameter in `coupling.py` to model hydration-induced stiffness loss. Calculate $\Phi_{VS} = |\mathbf{S}_{vec}| / S_{scalar}$. | Loss of the vector component ($\mathbf{g}$) while maintaining scalar pressure ($\Phi_{VS} \to 0$) leads to "Directionless Growth" (spherical expansion) and loss of curvature definition. |
| **8** | The Stabilizer (Torsional Coupling) | Revisit `stiffness_anisotropy` in `CounterCurvatureRodSystem`. Test if high Torsional Coupling (`chi_tau`) dampens the circadian oscillations and stabilizes the gradient descent. | Structural coupling (Torsion) acts as a passive damper (Regularization term) that stabilizes the aggressive active optimization of the circadian clock. |

---

## Phase 3: Experimental Validation Design (Weeks 9-12)

**Objective:** Outline specific wet-lab experiments to validate the computational predictions, translating `pyelastica` results into biological protocols.

| Week | Focus | Task | Hypothesis |
| :--- | :--- | :--- | :--- |
| **9** | Species Comparative Analysis | Design a comparative study to calculate $\mathcal{B}_g$ for: Human (AIS), Mouse, Zebrafish, and Whale using literature data (Muscle PCSA vs Bone Length). | Species with $\mathcal{B}_g \approx 1$ (Humans) are uniquely susceptible to "Optimization Failure" compared to high $\mathcal{B}_g$ species (Mice), explaining the rarity of spontaneous scoliosis in quadrupeds. |
| **10** | Experimental Design: "Test T_Clock" | Design the "Desynchronization Drift" protocol: Raise zebrafish in arhythmic (strobe) vs. rhythmic (12:12) light. Measure spinal straightness and `ActiveMuscleTorques` proxies (calcium imaging). | Disruption of the central clock (Learning Rate Scheduler) leads to higher variance in spinal alignment (higher Loss Function value) due to uncoordinated optimization steps. |
| **11** | Experimental Design: "Test U" | Design the "Loading Rescue" protocol: Apply cyclic mechanical stretch to organoids at specific circadian phases (PER2::LUC bioluminescence) to simulate "re-entrainment". | Mechanical loading is only anabolic (corrective) if applied during the "sensitive" phase of the local clock; loading during the "refractory" phase is ineffective or damaging. |
| **12** | Synthesis & Manuscript | Integrate Phase 1/2 simulation data and Phase 3 experimental designs into `manuscript/sections/theory.tex`. Finalize `formalism_01.md` with new definitions. | The "Gravity as Optimization" framework successfully unifies mechanical buckling and biological growth theories, offering a novel therapeutic target (Chronotherapy). |

---

## Risk Assessment

### 1. Theoretical Bottlenecks
*   **Non-Convex Cost Function:** The Total Potential Energy landscape ($U_{CC}$) might be non-convex, meaning "Gradient Descent" could get stuck in local minima (deformities) even with a perfect optimizer.
    *   *Mitigation:* Use `pyelastica` to map the full energy landscape and identify "Basins of Attraction" for healthy vs. scoliotic spines. Use "Simulated Annealing" (stochastic noise) to test robustness.
*   **Definition of Information Energy:** The term $-U_{info}$ in the cost function is abstract.
    *   *Mitigation:* Operationalize it strictly as the deviation from `kappa_rest` in the code, avoiding information-theoretic ambiguity.

### 2. Computational Risks
*   **Timescale Separation:** Simulating circadian days ($10^5$ seconds) with mechanical timesteps ($10^{-4}$ seconds) is computationally prohibitive.
    *   *Mitigation:* Use "Time-Homogenization" or a dual-scale approach in `pyelastica_bridge.py`, assuming mechanical equilibrium is reached instantly relative to growth. Run short "bursts" of mechanical simulation to calculate gradients.

### 3. Experimental Risks
*   **Measuring $\mathcal{B}_g$ In Vivo:** Estimating "Information Gradient" strength in living tissue is difficult.
    *   *Mitigation:* Use proxies like Muscle/Bone cross-sectional area ratios and `ActiveMuscleTorques` generated in simulations as a baseline.
*   **Vector-Scalar Mismatch Fidelity:** It is hard to decouple gravity from pressure in 1g.
    *   *Mitigation:* Use "Neutral Buoyancy" or "Clinostat" experiments with added osmotic pressure agents (e.g., PEG) to simulate high scalar/low vector environments.
