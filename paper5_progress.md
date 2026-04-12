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

## 2026-04-03
- Integrated DreamerV2 (TF2 implementation) as a submodule in `paper5_model/dreamerv2` to serve as a computational model of active inference's generative models and latent imagination. This aligns with the "Dream to Control" concept mentioned in the user prompt and fits the TF2 recommendation in the prompt.
- **Phase 1, Day 3:** Investigating the relation between Dreamer's latent space representations (world model, imagination) and active inference generalized coordinates.
