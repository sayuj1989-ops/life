# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 2: Active Inference and Motor Control** - Completed (Date: 2026-04-06)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006).
- Mapped the concept of surprise minimization to the "derivative gain gap": rapid growth causes a persistent increase in sensory surprise because the physical body changes faster than the generative model updates.
- Identified that motor commands in active inference are predictions of proprioceptive states; when these predictions are misspecified during growth, both perception and action fail to minimize free energy, potentially leading to a local minimum (asymmetric posture).
- Reviewed Adams et al. (2013) on "Predictions not commands", conceptualizing the equilibrium-point hypothesis as active inference resolving proprioceptive prediction errors at peripheral reflex arcs.
- Integrated the Dream to Control (Dreamer) framework (Hafner et al., 2019) to model the brain's generative models and latent imagination, explicitly noting the use of the newer TensorFlow 2 implementation for code integration.

## Decisions / Issues
- Need to formally map the PID components to the generative model (upcoming in Part A derivation).

## Next Session Plan
- **Phase 2, Day 3:** Bridging Material. Focus on Baltieri & Buckley (2019) and framing PID as Active Inference.
