# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 2: Active Inference and Motor Control** - Completed (Date: 2026-04-01)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006).
- Mapped the concept of surprise minimization to the "derivative gain gap": rapid growth causes a persistent increase in sensory surprise because the physical body changes faster than the generative model updates.
- Identified that motor commands in active inference are predictions of proprioceptive states; when these predictions are misspecified during growth, both perception and action fail to minimize free energy, potentially leading to a local minimum (asymmetric posture).
- Analyzed Adams et al. (2013) on motor control as active inference.
- Showed how active inference subsumes the Equilibrium-Point Hypothesis: moving the body is a process of changing descending predictions, which spinal reflexes automatically fulfill.
- Precision weighting is critical: to move, the system must confidently believe its predictions. If precision collapses during the derivative gain gap, the system might update its model to accept abnormal posture rather than correcting it.

## Decisions / Issues
- The role of generalized coordinates of motion (velocity, acceleration) needs to be mapped to the PID controller's specific terms (especially $K_d$). This is the next theoretical step.

## Next Session Plan
- **Phase 1, Day 3:** Generalized coordinates of motion in FEP. How Friston's formalism encodes velocity, acceleration, and jerk, and how precision on generalized motion relates to derivative control.
