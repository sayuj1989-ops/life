# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 3: Generalised Coordinates of Motion in FEP** - Completed (Date: 2026-04-03)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006) on Day 1.
- Day 2: Active inference reframes motor control (Adams et al. 2013). Motor commands are descending proprioceptive predictions, and movement occurs via classical reflex arcs suppressing proprioceptive prediction errors.
- The equilibrium-point hypothesis aligns with active inference: descending signals specify an equilibrium state (a prediction).
- Day 3: Generalised coordinates of motion ($\tilde{x}$) allow the brain to represent trajectories (position, velocity, acceleration).
- The derivative gain $K_d$ maps mathematically to the precision ($\Pi_1$) assigned to the prediction errors on generalised velocity ($\epsilon_1$).
- The derivative gain gap during rapid growth corresponds to a systematic mismatch between predictions and sensory feedback, leading to a down-weighting of the precision of velocity prediction errors ($\Pi_1 \to 0$).

## Decisions / Issues
- The connection between precision of velocity prediction errors and $K_d$ is the critical mathematical bridge.
- The next step is to rigorously review the formal equivalence between PID control and active inference with linear generative models.

## Next Session Plan
- **Phase 1, Day 4:** PID control derived from free-energy minimisation. Review Baltieri & Buckley (2019) "PID Control as a Process of Active Inference with Linear Generative Models". This is a KEY paper. Summarise the derivation to form the foundation of Part A of our mathematical development.
