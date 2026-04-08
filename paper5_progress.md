# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 2: Active Inference and Motor Control** - Completed (Date: 2026-04-02)

**Phase 1, Day 3: Generalised Coordinates of Motion in FEP** - Completed (Date: 2026-04-03)


## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006) on Day 1.
- Day 2: Active inference reframes motor control (Adams et al. 2013). Motor commands are descending proprioceptive predictions, and movement occurs via classical reflex arcs suppressing proprioceptive prediction errors.
- The equilibrium-point hypothesis aligns with active inference: descending signals specify an equilibrium state (a prediction).
- The derivative gain gap during rapid growth corresponds to a systematic mismatch between predictions and sensory feedback, leading to a down-weighting of the precision of velocity prediction errors. This precision drop is equivalent to the degradation of the derivative gain ($K_d$).

## Decisions / Issues
- The connection between precision of velocity prediction errors and $K_d$ is the critical mathematical bridge.
- Need to formalize how generalized coordinates of motion handle this precision weighting (upcoming Day 3).
- Day 3: Generalised coordinates of motion ($\tilde{x} = [x, x', x'', \dots]^T$) encode dynamic trajectories.
- Precision matrices weight the prediction errors at each derivative level.
- The precision on velocity prediction errors ($\Pi_1$) maps directly to the derivative gain ($K_d$) in PID control.
- The "derivative gain gap" from Paper 2 is reframed as a Bayesian "precision collapse" on velocity errors due to growth-induced model misspecification.


## Next Session Plan
- **Phase 1, Day 4:** PID control derived from free-energy minimisation. Review Baltieri & Buckley (2019) "PID Control as a Process of Active Inference with Linear Generative Models" to solidify the mathematical foundation before introducing delays and growth dynamics.