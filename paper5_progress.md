# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 3: Generalised coordinates of motion in FEP** - Completed (Date: 2026-04-03)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006) on Day 1.
- Day 2: Active inference reframes motor control (Adams et al. 2013). Motor commands are descending proprioceptive predictions, and movement occurs via classical reflex arcs suppressing proprioceptive prediction errors.
- The equilibrium-point hypothesis aligns with active inference: descending signals specify an equilibrium state (a prediction).
- The derivative gain gap during rapid growth corresponds to a systematic mismatch between predictions and sensory feedback, leading to a down-weighting of the precision of velocity prediction errors. This precision drop is equivalent to the degradation of the derivative gain ($K_d$).
- Day 3: Friston's formalism uses "generalised coordinates of motion" to track state, velocity, acceleration, etc., enabling the generative model to capture smooth temporal trajectories.
- The precision assigned to the velocity prediction error mathematically corresponds to the Derivative gain ($K_d$) in a PID controller.
- The derivative gain gap during rapid growth maps to a precision collapse on generalised motion.

## Decisions / Issues
- The connection between precision of velocity prediction errors and $K_d$ is the critical mathematical bridge.
- The derivative gain gap is now formally framed as a precision collapse on generalised motion.
- Need to review Baltieri & Buckley (2019) to extract the exact linear Gaussian generative model equations that yield the PID mapping.

## Next Session Plan
- **Phase 1, Day 4:** PID control derived from free-energy minimisation. Search for any existing work formally showing PID as a special case of active inference. Review Baltieri & Buckley (2019) "PID Control as a Process of Active Inference with Linear Generative Models" thoroughly.
