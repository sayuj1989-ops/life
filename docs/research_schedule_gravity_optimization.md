# Research Schedule: Gravity as an Optimization Process

## Summary

This 12-week research schedule operationalizes the "Gravity as an Optimization Process" hypothesis, framing spinal morphogenesis as a Gradient Descent algorithm minimizing a Counter-Curvature Energy function ($U_{CC}$). The schedule is divided into three 4-week phases: computational proof-of-concept (Phase 1), circadian dynamics (Phase 2), and experimental validation design (Phase 3). It integrates key theoretical constructs like the Bio-Gravitational Number ($\mathcal{B}_g$) and Vector-Scalar Mismatch ($\Phi_{VS}$).

## Phase 1: Computational Proof-of-Concept (Weeks 1-4)

**Objective**: Explicitly define the Cost Function ($U_{CC}$) in PyElastica and simulate "Optimization Failure" (Scoliosis) as a local minimum trap.

| Week | Focus | Task | Hypothesis | Tone |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **The Cost Function ($U_{CC}$)** | Implement `compute_U_CC()` (already in `pyelastica_bridge.py`) and validate it against analytical solutions for a simple beam. Visualize the energy landscape for variable $\kappa_{rest}$. | The organism minimizes $U_{CC} = U_{gravity} + U_{elastic} - U_{info}$. Scoliosis is a high-energy state relative to the global minimum but a local attractor. | Rigorous, Foundational. Verify energy conservation. |
| **2** | **The Gradient Descent Optimizer** | Implement an "Outer Loop" wrapper around PyElastica simulations that updates $\kappa_{rest}$ based on the "Spinal Learning Rate" $\eta_{spine}$ (Formalism 2.26). | The spine "learns" its shape by descending the gradient of sensed stress. $\frac{d\kappa}{dt} = -\eta \nabla U$. | Algorithmic, Evolutionary. Treat the spine as a neural network weight. |
| **3** | **The Bio-Gravitational Number ($\mathcal{B}_g$)** | Parameter sweep of $\mathcal{B}_g$ (Formalism 2.3). Vary $\chi_M$ (Stiffness) vs. Gravity ($g$). Identify the critical threshold $\mathcal{B}_{crit}$ for buckling. | Below a critical $\mathcal{B}_g$, the global minimum vanishes, and the system bifurcates into stable scoliotic wells. | Quantitative, Analytical. Determine the phase boundary. |
| **4** | **Optimization Failure (Exploding Gradient)** | Simulate "Sensory Noise" (Vestibular vs. Proprioceptive). Inject noise into the gradient calculation of the Optimizer. | High sensory gain ($\chi_\kappa$) with noise leads to "Exploding Gradients," causing the spine to overshoot and lock into deformity. | Diagnostic, Critical. Identification of failure modes. |

## Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)

**Objective**: Integrate time-dependent "Learning Rate" (Circadian Clock) and simulate desynchronization between the biological clock and the gravitational vector.

| Week | Focus | Task | Hypothesis | Tone |
| :--- | :--- | :--- | :--- | :--- |
| **5** | **The Circadian Clock ($T_{clock}$)** | Utilize `CircadianModulationCallback` in `pyelastica_bridge.py`. Modulation of $\chi_\kappa$ (curvature sensitivity) with period $T_{clock} = 24h$. | The spine's sensitivity to error signals oscillates. "Learning" only happens during the active phase. | Rhythmic, Dynamic. Validate temporal modulation. |
| **6** | **Spinal Jetlag (Phase Mismatch)** | Sweep the phase difference $\phi$ between the Load Cycle (Gravity) and the Sensitivity Cycle (Clock). | Mismatch ($\phi \approx \pi$) leads to "Anti-Learning": the spine consolidates deformations during the wrong phase. | Chronobiological, Disruptive. Simulate "Night Shift" spine. |
| **7** | **Frequency Detuning (The Bastien Number)** | Simulate a mismatch in frequency ($\omega_{clock} \neq \omega_{load}$). Test the resonance condition $\omega_{load} \approx 2\omega_{natural}$. | Resonance between metabolic oscillations and mechanical loading drives rapid curvature progression (Parametric Excitation). | Resonance-focused, Vibrational. |
| **8** | **The Sleep-Walking Spine (Microgravity)** | Simulate $g \to 0$ during the "Sleep" phase vs. "Wake" phase. Compare "Sleeping in Space" vs. "Active in Space". | Loss of gravitational zeitgeber during the sensitive window allows random drift (Brownian motion of curvature). | Space-faring, Speculative but grounded. |

## Phase 3: Experimental Validation Design (Weeks 9-12)

**Objective**: Design wet-lab experiments and calculate dimensionless numbers to validate computational predictions.

| Week | Focus | Task | Hypothesis | Tone |
| :--- | :--- | :--- | :--- | :--- |
| **9** | **Vector-Scalar Mismatch ($\Phi_{VS}$)** | **Simulation**: Set $g=0$ (Vector=0) but maintain high $S_{scalar}$ (Pressure). Compare to $g=9.8$ control. <br> **Design**: Protocol for hyper-osmotic loading of zebrafish in clinostat. | High Scalar/Low Vector ($\Phi_{VS} \to 0$) triggers "Geometric Hallucination" (growth without direction). | Comparative, Physiological. Define the "Confused" state. |
| **10** | **Calculating $\mathcal{B}_g$ Across Species** | Write `scripts/calculate_Bg_species.py`. Aggregate data (Length, Stiffness, Density) for Human, Whale, Mouse, Giraffe. | Humans are the only species near the instability threshold ($\mathcal{B}_g \approx 1$). Others are Deeply Stable ($\mathcal{B}_g \gg 1$). | Allometric, Evolutionary. The "Anthropic Principle" of Scoliosis. |
| **11** | **Designing "Test T_Clock"** | **Protocol Design**: Design an experiment using PER2::LUC vertebral explants under cyclic loading at variable phases. Define required sample sizes and loading regimes. | Mechanical loading entrains the spinal clock. Phase shifting load desynchronizes the clock (Jetlag). | Experimental, Methodological. Prepare for wet-lab. |
| **12** | **Synthesis & Manuscript** | Compile results into "Gravity as Optimization" manuscript. Generate Phase Diagrams ($B_g$ vs. $\Phi_{VS}$). | The framework unifies Scoliosis, Spaceflight adaptation, and Allometry under a single optimization problem. | Conclusive, Holistic. Submission ready. |

## Risk Assessment & Theoretical Bottlenecks

1.  **Gradient Definition**: Defining the "gradient" $\nabla U$ in a high-dimensional shape space (Cosserat rod) is non-trivial. *Mitigation*: Restrict optimization to a low-dimensional latent space (e.g., Curvature Modes $k_1, k_2$).
2.  **Time-Scale Separation**: Morphogenesis ($T \sim \text{Years}$) vs. Elastic Relaxation ($T \sim \text{Seconds}$) requires efficient multi-scale coupling. *Mitigation*: Use "Quasi-Static" assumption where the rod equilibrates instantly between growth steps.
3.  **Parameter Identification**: Determining realistic values for $\chi_M$ and $\eta_{spine}$ for humans vs. mice is difficult. *Mitigation*: Use dimensionless ratios ($\mathcal{B}_g$) rather than absolute values.
4.  **PyElastica Stability**: Extreme parameter sweeps (e.g., negative stiffness or high growth rates) may cause numerical instability. *Mitigation*: Implement robust damping and adaptive time-stepping in `pyelastica_bridge.py`.

## References
- `src/spinalmodes/countercurvature/pyelastica_bridge.py`: Existing simulation core.
- `docs/theory/formalism_01.md`: Theoretical definitions of $\mathcal{B}_g$, $\Phi_{VS}$, $\eta_{spine}$.
