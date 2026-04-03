# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 2: Active Inference and Motor Control** - Completed (Date: 2026-04-03)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006) and active inference for motor control (Adams et al. 2013).
- Mapped the concept of surprise minimization to the "derivative gain gap": rapid growth causes a persistent increase in sensory surprise because the physical body changes faster than the generative model updates.
- Identified that motor commands in active inference are predictions of proprioceptive states; when these predictions are misspecified during growth, both perception and action fail to minimize free energy, potentially leading to a local minimum (asymmetric posture).
- Analyzed Adams et al. (2013) which argues that motor control does not rely on efference copies, but instead fulfills proprioceptive predictions. This naturally aligns with the equilibrium-point hypothesis, where descending signals set sensory expectations (equilibrium states) rather than specifying muscle forces.

## Decisions / Issues
- Need to formally map the PID components to the generative model (upcoming in Part A derivation).
- The transition from equilibrium-point hypothesis to generalized coordinates of motion is key for explaining the derivative gain gap.

## Next Session Plan
- **Phase 1, Day 3:** Generalised coordinates of motion in FEP. Focus on Friston's formalism for encoding velocity and acceleration, and how precision on generalized motion relates to derivative control.
