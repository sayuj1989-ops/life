# Paper 5 Progress Log

**Date**: 2024-05-24
**Phase/Day Completed**: Day 1 / Literature Review & Math Mapping

**Key Findings / Mathematical Insights**:
- Integrated Hafner et al. (2019) "Dream to Control" into the predictive processing framework.
- Mapped latent imagination and learned world models to active inference.
- Formalized the mapping of Paper 2's PID controller to Friston's active inference: $K_p$ to sensory precision on position, $K_d$ to sensory precision on velocity, $K_i$ to prior precision on persistent causes, and $\tau$ to sensory delay.

**Issues / Questions for Dr. Sayuj K.S.** (hellodr@drsayuj.info):
- Should we explicitly simulate the Dreamer latent space alongside the active inference SPM-style generative models in `paper5_model/`?

**Next Session's Plan**:
- Implement the baseline predictive processing simulation in `paper5_model/` using the established active inference mappings.

**Date**: 2024-05-25
**Phase/Day Completed**: Day 2 / Baseline Predictive Processing Simulation

**Key Findings / Mathematical Insights**:
- Implemented the baseline predictive processing simulation in `paper5_model/baseline_predictive_processing.py`.
- Demonstrated that the PID controller maps to Friston's active inference formalism for a linear generative model (Baltieri & Buckley, 2019).
- PID gains effectively control the simulated plant by parameterizing the precision of the sensory and prior distributions, governing the update dynamics in the face of delayed observations ($\tau$).

**Issues / Questions for Dr. Sayuj K.S.** (hellodr@drsayuj.info):
- How does the "Derivative Gain Trap" interact with the Dreamer framework's value estimation in a delayed environment?

**Next Session's Plan**:
- Investigate the "Spinal Sleep Spindles" hypothesis and simulate the "Derivative Gain Trap".
