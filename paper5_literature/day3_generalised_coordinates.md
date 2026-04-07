# Day 3: Generalised Coordinates of Motion and PID Control in Active Inference

**Date**: 2026-04-03
**Focus**: Literature Review of Baltieri & Buckley (2019) and Friston's formalism.

## Summary of Findings

1. **Friston's Generalised Coordinates of Motion**:
   Active inference employs generalised coordinates of motion ($\tilde{x} = [x, x', x'', \dots]^T$) to represent a state not just by its position, but by its velocity, acceleration, and higher-order derivatives. This allows the generative model to anticipate trajectories and enables smooth movement without ad-hoc temporal delays.

2. **PID Control as Active Inference**:
   Baltieri & Buckley (2019) explicitly mapped the classical PID (Proportional-Integral-Derivative) control mechanism to active inference using linear generative models.
   - Proportional control ($K_p$) corresponds to the precision on position prediction errors ($\Pi_x$).
   - Derivative control ($K_d$) corresponds to the precision on velocity prediction errors ($\Pi_{x'}$ or $\Pi_v$).
   - Integral control ($K_i$) maps to the adaptation of prior expectations over longer timescales.

## Innovative Integration (The Dreamer Bridge)
Building on the 'Dream to Control' (Dreamer) reinforcement learning architecture by Hafner et al., the brain's generative model acts as a latent world model. The "Derivative Gain Gap" (the age-related or growth-spurt related drop in $K_d$ seen in AIS) can thus be reinterpreted as a failure of the world model's capacity to accurately forecast or trust its own latent velocity predictions ($\Pi_v \to 0$).

## References
- Friston, K. J. (2008). Hierarchical models in the brain. *PLoS Comput Biol*, 4(11), e1000211.
- Baltieri, M., & Buckley, C. L. (2019). PID control as a process of active inference with linear generative models. *Entropy*, 21(3), 257.
- Hafner, D., et al. (2019). Dream to control: Learning behaviors by latent imagination. *arXiv preprint arXiv:1912.01603*.
