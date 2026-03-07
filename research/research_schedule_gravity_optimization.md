# Gravity as an Optimization Process: 12-Week Research Schedule

## Summary
This document outlines a rigorous 12-week research schedule to test and validate the "Gradient Descent" hypothesis of spinal alignment. In this theoretical framework, spinal geometry is viewed as the solution to a continuous optimization process where the organism seeks to minimize a thermodynamic cost function, the Counter-Curvature Energy ($U_{CC}$). This cost function represents the sum of gravitational potential and elastic strain, mitigated by the informational alignment driven by mechanosensory feedback.

Our hypothesis states that the learning rate of this optimization (Spinal Jetlag) is gated by the circadian clock, and failure modes—such as adolescent idiopathic scoliosis—arise from either an "exploding gradient" (excessive learning rate vs. sensory noise) or desynchronization from the gravity vector. By leveraging computational modeling (`pyelastica_bridge.py`) and formalizing new dimensionless groups like the Bio-Gravitational Number ($\mathcal{B}_g$), we aim to validate this active inference model of biological geometry.

## 12-Week Schedule

### Phase 1: Computational Proof-of-Concept (Weeks 1-4)
**Focus:** Defining the Cost Function ($U_{CC}$) explicitly and simulating "Optimization Failure" (Scoliosis).

| Week | Focus | Task | Hypothesis / Theory Tested |
| :--- | :--- | :--- | :--- |
| **1** | The Cost Function ($U_{CC}$) | Implement and validate `compute_U_CC` inside `src/spinalmodes/countercurvature/pyelastica_bridge.py`. Run a PyElastica parameter sweep comparing stable S-curves against scoliotic phenotypes. | **Hypothesis:** The healthy spine exists at the global minimum of $U_{CC} = U_{grav} + U_{elastic} - U_{info}$. Scoliosis represents a trapped local minimum or energetic divergence. |
| **2** | Optimization Failure (Scoliosis) | Create `scripts/experiment_exploding_gradient.py`. Introduce targeted sensory noise to the `InfoField1D` and sweep the geometric coupling constant ($\chi_\kappa$) to trigger divergent buckling. | **Exploding Gradient:** When the learning rate ($\chi_\kappa$) is disproportionately high relative to mechanosensory noise (e.g., PIEZO2 dysfunction), the gradient descent algorithm overcorrects and explodes into structural instability (scoliosis). |
| **3** | The Bio-Gravitational Number ($\mathcal{B}_g$) | Write `scripts/experiment_Bg_scaling.py` to calculate and map the dimensionless $\mathcal{B}_g$ space across simulated murine, zebrafish, and human spinal parameters. | **Stability Criterion:** Based on `formalism_01.md` (Eq 2.3), stable counter-curvature requires $\mathcal{B}_g \approx 1$. If $\mathcal{B}_g \ll 1$, passive gravitational collapse occurs; if $\mathcal{B}_g \gg 1$, active hallucination occurs. |
| **4** | Vector-Scalar Mismatch (Microgravity) | Modify `CounterCurvatureRodSystem` in `pyelastica_bridge.py` to set the vector field (`gravity = 0.0`) while maintaining the scalar `active_curvature` drive. Run simulations to observe emergent geometry. | **Mismatch Hypothesis:** In microgravity, the organism loses the vector reference but maintains scalar pressure signals (high $\Phi_{VS}$ mismatch in `formalism_01.md`), causing the optimization process to hallucinate non-functional curvature. |

### Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)
**Focus:** Integrating a time-dependent "Learning Rate" (Circadian Clock) into the model and observing the consequences of phase desynchronization.

| Week | Focus | Task | Hypothesis / Theory Tested |
| :--- | :--- | :--- | :--- |
| **5** | Circadian Integration | Refine `CircadianParams` and `CircadianModulationCallback` in `pyelastica_bridge.py`. Validate that $\chi_\kappa(t)$ oscillates smoothly with period $T$ and amplitude $A$. | **Time-Dependent Learning Rate:** The tissue's sensitivity to mechanical error signals (learning rate) is intrinsically gated by the BMAL1 clock to coincide with peak daily loading. |
| **6** | Jetlag Simulation (Desynchronization) | Develop `scripts/experiment_spinal_jetlag.py`. Simulate a phase shift ($\phi$) between the external gravity load cycle and the internal $\chi_\kappa(t)$ oscillation. | **Desynchronization Failure:** When the clock desynchronizes from the gravity vector ($\phi \approx \pi$), the optimization updates occur during low signal-to-noise periods, causing progressive accumulation of geometric error. |
| **7** | Frequency Modulation and Rescue | Extend the jetlag script to test whether increasing the basal stiffness ($\chi_E$) or altering the frequency ($f_{load}$) can rescue the structural instability caused by phase mismatch. | **Entrainment Window:** There exists a critical frequency band for $f_{load}$ where the mechanical antenna (e.g., primary cilia) can re-entrain a drifting biological clock. |
| **8** | Phase Diagram Generation | Generate a comprehensive $(A, \phi)$ phase space diagram plotting final Cobb Angle versus the degree of circadian mismatch, mapping the 'Safe Zone'. | **Critical Phase Boundary:** There exists a critical phase lag $\phi_{crit}$ beyond which the spinal alignment algorithm inevitably diverges into scoliosis. |

### Phase 3: Experimental Validation Design (Weeks 9-12)
**Focus:** Outlining specific wet-lab experiments to falsify or validate the computational predictions generated in Phases 1 & 2.

| Week | Focus | Task | Hypothesis / Theory Tested |
| :--- | :--- | :--- | :--- |
| **9** | "Test T_Clock" Protocol Design | Draft the experimental protocol to culture PER2::LUC reporter mouse intervertebral disc explants under a programmable bioreactor applying cyclic compression. | **Circadian Validation:** Applying mechanical loading in anti-phase to the endogenous PER2::LUC clock will dampen the bioluminescent amplitude and suppress downstream alignment genes (*Col1a1*). |
| **10** | Vector-Scalar In Vivo Validation | Design a clinostat (simulated microgravity) experiment for zebrafish larvae. Introduce targeted focal pressure (e.g., optical or magnetic tweezers) to stimulate PIEZO2 independently of global gravity. | **Geometric Hallucination:** Providing localized scalar stress without a uniform gravitational vector will drive the spontaneous formation of scoliotic curves predicted by the Week 4 simulations. |
| **11** | Cross-Species $\mathcal{B}_g$ Verification | Synthesize literature datasets of spinal slenderness, bone density, and muscle mass across mammalian species to explicitly calculate their $\mathcal{B}_g$ during rapid growth phases. | **Scaling Universality:** Despite massive differences in length $L$, the Bio-Gravitational Number $\mathcal{B}_g$ must remain conserved near 1 for all upright or actively swimming vertebrates to prevent mechanical buckling. |
| **12** | Synthesis and Dissemination | Compile the PyElastica simulation outputs, phase diagrams, and wet-lab protocols into a structured pre-print draft targeting a high-impact biophysics or biomechanics journal. | **Unified Framework:** Gravity is not merely a passive load, but the active, continuous training signal that optimizes biological geometry via a gradient descent process. |

## Risk Assessment (Theoretical Bottlenecks)

1. **Quantification of Information Energy ($U_{info}$):** Converting genetic/informational states into Joule-equivalent terms is conceptually difficult.
   - *Mitigation:* We will rely strictly on the relative ratio ($U_{info} / U_{elastic}$) defined in `compute_U_CC` rather than absolute thermodynamic values, ensuring the optimization behaves correctly regardless of arbitrary scaling.
2. **Separating Vector vs. Scalar Sensation In Vivo:** The physiological difficulty of mechanically decoupling directional gravity sensing (vector) from bulk tissue compression (scalar).
   - *Mitigation:* The simulated microgravity clinostat model (Phase 3, Week 10) combined with targeted PIEZO2 agonists/antagonists is specifically designed to isolate these variables.
3. **PyElastica Numerical Instability:** Long-duration temporal simulations of slow biological growth (weeks/months) require extremely small time steps ($dt$) in PyElastica, which may lead to exploding gradients purely from numerical artifacts.
   - *Mitigation:* We will employ quasi-static time scaling and strictly monitor energy conservation (`rotational_energy`, `translational_energy`) using the callbacks implemented in `pyelastica_bridge.py`.
