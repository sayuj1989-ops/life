# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 1: FEP Foundations** - Completed (Date: 2026-04-01)
**Phase 1, Day 2: Active Inference and Motor Control** - Completed (Date: 2026-04-05)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006).
- Mapped the concept of surprise minimization to the "derivative gain gap": rapid growth causes a persistent increase in sensory surprise because the physical body changes faster than the generative model updates.
- Identified that motor commands in active inference are predictions of proprioceptive states; when these predictions are misspecified during growth, both perception and action fail to minimize free energy, potentially leading to a local minimum (asymmetric posture).
- Reviewed Adams et al. (2013) and Perrinet et al. (2014) on active inference in motor control.
- Established that classical feedback gains correspond to precision weighting on prediction errors. Specifically, the PID derivative gain $K_d$ maps to the precision on generalized velocity ($\pi_v$).
- Concluded that the "derivative gain gap" is a precision collapse: when growth-induced model misspecification makes velocity predictions unreliable, optimal Bayesian updating down-weights their precision.

## Decisions / Issues
- Need to formally map the PID components to the generative model (upcoming in Part A derivation).
- Mapped key PID components for the paper: $K_d \rightarrow \pi_v$, $u(t) \rightarrow$ reflex arc, $\tau \rightarrow$ temporal horizon.

## Next Session Plan
- **Phase 1, Day 3:** Generalised coordinates of motion in FEP — Friston's formalism for encoding velocity, acceleration, jerk etc. as "generalised motion." How precision on generalised motion relates to derivative control.
