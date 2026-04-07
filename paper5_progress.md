# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 2: Active Inference and Motor Control** - Completed (Date: 2026-04-02)
**Phase 1, Day 3: Generalised Coordinates and Precision** - Completed (Date: 2026-04-07)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006) on Day 1.
- Day 2: Active inference reframes motor control (Adams et al. 2013). Motor commands are descending proprioceptive predictions, and movement occurs via classical reflex arcs suppressing proprioceptive prediction errors.
- The equilibrium-point hypothesis aligns with active inference: descending signals specify an equilibrium state (a prediction).
- The derivative gain gap during rapid growth corresponds to a systematic mismatch between predictions and sensory feedback, leading to a down-weighting of the precision of velocity prediction errors. This precision drop is equivalent to the degradation of the derivative gain ($K_d$).

## Decisions / Issues
- Phase 1, Day 3: Explored Friston's generalised coordinates of motion. Using Baltieri & Buckley (2019), formalized that the precision of velocity prediction errors ($\Pi_1$) is mathematically equivalent to the derivative gain ($K_d$).
- The connection between precision of velocity prediction errors and $K_d$ is the critical mathematical bridge.

## Next Session Plan
- **Phase 1, Day 4:** Active Inference and RL. Review Hafner's Dreamer (Dream to Control) as a conceptual implementation of active inference using latent imagination for long-horizon planning. Consider TensorFlow 2 implementation for future computational models.
