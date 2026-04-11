# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 4: PID control derived from free-energy minimisation** - Completed (Date: 2026-04-04)

## Key Findings
- Day 4: Reviewed Baltieri & Buckley (2019) (DOI: 10.3390/e21030257). It proves PID control is exactly active inference under a linear Gaussian generative model. $K_p$ maps to sensory precision on position, $K_d$ to sensory precision on velocity, and $K_i$ to inference on constant hidden causes. This provides the mathematical bedrock for Paper 5.
- Day 3: Formalised Friston's generalised coordinates of motion (DEM framework). Position error $\epsilon_0$ maps to proportional gain $K_p$, while velocity prediction error $\epsilon_1$ maps to derivative gain $K_d$. Precision $\pi_1$ determines the effective $K_d$.
- Reviewed core FEP papers (Friston 2010, Friston 2006) on Day 1.
- Day 2: Active inference reframes motor control (Adams et al. 2013). Motor commands are descending proprioceptive predictions, and movement occurs via classical reflex arcs suppressing proprioceptive prediction errors.
- The equilibrium-point hypothesis aligns with active inference: descending signals specify an equilibrium state (a prediction).
- The derivative gain gap during rapid growth corresponds to a systematic mismatch between predictions and sensory feedback, leading to a down-weighting of the precision of velocity prediction errors. This precision drop is equivalent to the degradation of the derivative gain ($K_d$).

## Decisions / Issues
- The degradation of $K_d$ in Paper 2 is perfectly explained as a Bayesian precision collapse ($\pi_1 \rightarrow 0$) due to model misspecification during rapid adolescent growth.

## Next Session Plan
- **Phase 1, Day 5:** Predictive Processing and body representation. Review how PP explains proprioception, body schema, interoception, and precision weighting in postural control.