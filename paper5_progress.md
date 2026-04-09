# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 2: Active Inference and Motor Control** - Completed (Date: 2026-04-02)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006) on Day 1.
- Day 2: Active inference reframes motor control (Adams et al. 2013). Motor commands are descending proprioceptive predictions, and movement occurs via classical reflex arcs suppressing proprioceptive prediction errors.
- The equilibrium-point hypothesis aligns with active inference: descending signals specify an equilibrium state (a prediction).
- The derivative gain gap during rapid growth corresponds to a systematic mismatch between predictions and sensory feedback, leading to a down-weighting of the precision of velocity prediction errors. This precision drop is equivalent to the degradation of the derivative gain ($K_d$).

## Decisions / Issues
- The connection between precision of velocity prediction errors and $K_d$ is the critical mathematical bridge.
- Need to formalize how generalized coordinates of motion handle this precision weighting (upcoming Day 3).

## Next Session Plan
- **Phase 1, Day 3:** Generalised coordinates of motion in FEP. Review Friston's formalism for encoding velocity, acceleration, jerk etc. as "generalised motion." Understand how precision on generalised motion relates to derivative control.


**Phase 1, Day 3: Generalised coordinates of motion** - Completed (Date: 2026-04-03)

## Key Findings
- Generalised coordinates of motion ($\tilde{x} = (x, x', x'', \dots)$) are Friston's way of encoding trajectories.
- Prediction errors exist for each order of motion, weighted by precision matrices.
- The precision on the 1st-order (velocity) prediction error corresponds directly to the derivative gain ($K_d$) in a PID controller.
- Misspecified internal models during rapid growth cause systemic velocity prediction errors, leading the brain to downweight velocity precision. This precision collapse *is* the derivative gain gap.

## Next Session Plan
- **Phase 1, Day 4:** PID control derived from free-energy minimisation. Review Baltieri & Buckley (2019).
