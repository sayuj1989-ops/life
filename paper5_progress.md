# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 3: Latent Imagination and Generative Models (Dreamer)** - Completed (Date: 2026-04-13)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006) on Day 1.
- Day 2: Active inference reframes motor control (Adams et al. 2013). Motor commands are descending proprioceptive predictions, and movement occurs via classical reflex arcs suppressing proprioceptive prediction errors.
- The equilibrium-point hypothesis aligns with active inference: descending signals specify an equilibrium state (a prediction).
- The derivative gain gap during rapid growth corresponds to a systematic mismatch between predictions and sensory feedback, leading to a down-weighting of the precision of velocity prediction errors. This precision drop is equivalent to the degradation of the derivative gain ($K_d$).
- Day 3: Integrated "Dream to Control" (Hafner et al., 2019) to model the brain's generative models and latent imagination within the active inference framework. Dreamer's world model learns from past experience to predict future states in a latent space, which conceptually mirrors FEP descending predictions. A mismatch between the world model and physical body (due to rapid growth) degrades the agent's latent imagination of stable trajectories, mathematically bridging the derivative gain drop.

## Decisions / Issues
- The connection between precision of velocity prediction errors and $K_d$ is the critical mathematical bridge.
- The Dreamer TF1 repository was cloned to `paper5_model/dreamer` for use in Phase 3 simulations.
- Need to formalize how generalized coordinates of motion handle this precision weighting, potentially integrating Baltieri & Buckley (2019).

## Next Session Plan
- **Phase 1, Day 4:** Generalised coordinates of motion in FEP. Review Friston's formalism for encoding velocity, acceleration, jerk etc. as "generalised motion." Formally connect precision on generalised motion to derivative control (PID), drawing on Baltieri & Buckley (2019).
