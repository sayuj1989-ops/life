# Day 4: PID Control Derived from Free-Energy Minimisation

## Key Paper
Baltieri, M., & Buckley, C. L. (2019). *PID Control as a Process of Active Inference with Linear Generative Models*. Entropy. DOI: 10.3390/e21030257 (Preprint: 10.20944/preprints201902.0246.v1)

## Core Insight
Baltieri & Buckley formally prove that classic Proportional-Integral-Derivative (PID) control can be derived exactly from the free-energy minimization framework (Active Inference) by specifying a specific linear Gaussian generative model.

## The Mapping
1. **Proportional Gain ($K_p$) $\leftrightarrow$ Precision of Position Sensory Error ($\Sigma_y^{-1}$ or $\Pi_y$):**
   The proportional term corresponds to the prediction error on the sensory data ($y - \mu$), scaled by the sensory precision. When confidence in current sensory data is high, $K_p$ is high.

2. **Derivative Gain ($K_d$) $\leftrightarrow$ Precision of Velocity/Generalised Motion:**
   The derivative term corresponds to the prediction error on the *rate of change* (first order of generalised motion, $y' - \mu'$). In Baltieri & Buckley, this arises from the sensory precision on the velocity component. High precision on velocity error leads to a strong dampening response (high $K_d$).

3. **Integral Gain ($K_i$) $\leftrightarrow$ Prior Precision / Inference on Hidden Causes ($w$):**
   The integral term emerges from the system inferring a slow-changing or constant hidden cause (like a constant gravitational bias or load). It corresponds to updating the belief about this hidden cause ($\mu_w$) driven by persistent prediction errors.

## Bridging to the Derivative Gain Gap (Paper 2)
In Paper 2, the "derivative gain gap" was modeled as an ad hoc, empirical degradation of $K_d$ during rapid growth due to proprioceptive delay.

Under the active inference framing (via Baltieri & Buckley):
- Rapid growth implies the body's true dynamics ($A, B$ matrices in the plant) change faster than the generative model can adapt.
- Because of the proprioceptive delay ($\tau$), the velocity predictions ($\mu'$) become systematically misaligned with the delayed sensory velocity ($y'$).
- The system correctly detects this systematic error and, to minimize variational free energy, reduces the precision ($\Pi_{y'}$) assigned to velocity sensory inputs.
- Because $K_d \propto \Pi_{y'}$, the optimal derivative gain drops.
- Therefore, the derivative gain gap is not an engineering failure, but a mathematically optimal (Bayesian) precision collapse in response to model misspecification during rapid morphological change.
