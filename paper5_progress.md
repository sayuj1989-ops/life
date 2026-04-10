# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 3: Latent Imagination and Dreamer Integration** - Completed

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006) on Day 1.
- Day 2: Active inference reframes motor control (Adams et al. 2013). Motor commands are descending proprioceptive predictions, and movement occurs via classical reflex arcs suppressing proprioceptive prediction errors.
- The equilibrium-point hypothesis aligns with active inference: descending signals specify an equilibrium state (a prediction).
- The derivative gain gap during rapid growth corresponds to a systematic mismatch between predictions and sensory feedback, leading to a down-weighting of the precision of velocity prediction errors. This precision drop is equivalent to the degradation of the derivative gain ($K_d$).
- Day 3: Integrated the "Dream to Control" (Dreamer) architecture (Hafner et al. 2019, DOI: 10.48550/arXiv.1912.01603) into the framework to model the brain's generative models and latent imagination for active inference. Added the original implementation of Dreamer as a submodule in `paper5_model/dreamer`.

## Decisions / Issues
- The connection between precision of velocity prediction errors and $K_d$ is the critical mathematical bridge.
- Need to formalize how generalized coordinates of motion handle this precision weighting (upcoming Day 3).

## Next Session Plan
- **Phase 1, Day 4:** Generalised coordinates of motion in FEP. Review Friston's formalism for encoding velocity, acceleration, jerk etc. as "generalised motion." Understand how precision on generalised motion relates to derivative control.
