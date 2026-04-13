# Phase 1, Day 4: PID control derived from free-energy minimisation

## Core Paper
**Baltieri, M., & Buckley, C. L. (2019). PID Control as a Process of Active Inference with Linear Generative Models. Entropy, 21(3), 257.**

## Summary of Baltieri & Buckley (2019)
Baltieri and Buckley provide a formal proof that Proportional-Integral-Derivative (PID) control can be derived as a process of active inference, assuming a linear generative model and a specific precision structure over generalized coordinates of motion.

### The Generative Model
The system uses a generative model in generalized coordinates (up to order 2: position, velocity, acceleration).
- Hidden state $\tilde{x} = [x, x', x'']$
- Sensory observations $\tilde{y} = [y, y', y'']$
- Target (prior) $\tilde{v} = [\mu, \mu', \mu'']$

### The Mapping
Baltieri and Buckley demonstrate the following equivalences:
1. **Proportional Gain ($K_p$):** Maps to the precision on position prediction errors ($\Pi_{y,0}$) multiplied by the inverse mapping from states to sensors.
2. **Derivative Gain ($K_d$):** Maps to the precision on velocity prediction errors ($\Pi_{y,1}$). High $K_d$ means the system heavily penalizes deviations from the predicted velocity.
3. **Integral Gain ($K_i$):** Maps to the precision on the higher-level prior ($\Pi_{v,0}$) or the inverse learning rate on the causes $v$, effectively accumulating steady-state error.

## Implications for Paper 5
This paper provides the foundational proof we need: PID *is* Active Inference under linear Gaussian assumptions.
Our novel contribution in Paper 5 will be extending this to include:
1. **Delayed Observations ($\tau$):** Baltieri & Buckley do not explicitly model the proprioceptive delay $\tau$, which is central to the derivative gain gap in Paper 2. We must show how $\tau$ necessitates temporal prediction in the generative model.
2. **Time-Varying Plant Parameters (Growth):** We must model growth velocity as a continuous change in the true mapping from action to generalized states (the physical plant).
3. **Precision Collapse Dynamics:** When the plant changes faster than the model can update, the variance of velocity prediction errors increases, leading to a dynamic reduction in $\Pi_{y,1}$ (and therefore, a transient drop in effective $K_d$).

## Next Steps
We have established the mapping between PID parameters and precisions on generalized motion.
Phase 2 (Days 7-10) will bridge this to the developmental and clinical context of Adolescent Idiopathic Scoliosis (AIS).
Phase 3 will then derive the mathematical extensions (delay, growth, precision collapse) on top of the Baltieri & Buckley foundation.
