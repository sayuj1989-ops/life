# Paper 5: Progress Tracker

## Phase 1: Literature Review — Free-Energy Principle Foundations

* **Day 1**: Friston's free-energy principle — core papers (Friston 2010 Nat Rev Neurosci, Friston 2006 J Physiol Paris). Variational free energy, surprise minimisation, generative models, active inference. Focus on the mathematical formalism.



### Update: Day 1 Completed
* **Date**: 2024-05-24
* **Phase/Day**: Phase 1, Day 1 (FEP Foundations)
* **Key findings/mathematical insights**:
    *   FEP is fundamentally about minimising variational free energy, $F$, an upper bound on surprise (negative log-evidence).
    *   $F$ is defined using a generative model $p(y, x)$ and a recognition density $q(x)$ approximating the true posterior.
    *   Action and perception both minimise $F$: perception changes internal beliefs to match sensory data, action changes sensory data to match internal predictions.
    *   Precision ($\Pi$) acts as a gain on prediction errors. High precision means errors are trusted and heavily weight belief updates.
    *   Crucial insight for Paper 5: The delayed PID controller from Paper 2 can be viewed as an active inference system. Prediction errors map to control error signals. Precision weights map directly to the controller gains ($K_p$, $K_d$, $K_i$).
    *   The derivative gain gap can be formalised as a dynamic collapse in the precision assigned to generalised motion (velocity) errors, caused by a misspecified internal model during rapid adolescent growth.
* **Issues/open questions for Dr. Sayuj**:
    *   The literature extensively discusses active inference for action and perception, but the precise mathematical mapping from the Euler-Lagrange equations to delayed PID control needs to be derived. Does the Baltieri & Buckley (2019) paper provide the exact linear Gaussian form we need to adapt for the inverted pendulum model with delays?
* **Next session**: Execute Phase 1, Day 2: "Active inference and motor control". Review Friston et al. and Adams et al. on optimal motor control and the equilibrium-point hypothesis under FEP. Output to `paper5_literature/day2_active_inference_motor.md`.
