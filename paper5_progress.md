# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 3: Generalised coordinates of motion in FEP** - Completed (Date: 2026-04-03)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006) on Day 1.
- Day 2: Active inference reframes motor control (Adams et al. 2013). Motor commands are descending proprioceptive predictions, and movement occurs via classical reflex arcs suppressing proprioceptive prediction errors.
- The equilibrium-point hypothesis aligns with active inference: descending signals specify an equilibrium state (a prediction).
- The derivative gain gap during rapid growth corresponds to a systematic mismatch between predictions and sensory feedback, leading to a down-weighting of the precision of velocity prediction errors. This precision drop is equivalent to the degradation of the derivative gain ($K_d$).
- Day 3: Explored generalized coordinates of motion ($x, x', x'' \dots$). Precision on velocity errors ($\Pi_1$) is the active inference analogue to derivative gain ($K_d$). When morphological changes cause systemic prediction errors, Bayesian updating reduces $\Pi_1$, triggering the "derivative gain gap".


## Decisions / Issues
- Day 3 completed successfully.
- The mapping between PID control terms and precision parameters is now theoretically grounded.

## Next Session Plan
- **Phase 1, Day 4:** PID control derived from free-energy minimisation. Review Baltieri & Buckley (2019) thoroughly. Understand how PID is formally mapped to active inference with linear generative models.
