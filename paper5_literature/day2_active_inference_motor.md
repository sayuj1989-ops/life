# Phase 1, Day 2: Active Inference and Motor Control

## Core Papers Reviewed
- Adams, R. A., Shipp, S., & Friston, K. J. (2013). Predictions not commands: active inference in the motor system. *Brain Structure and Function*, 218(3), 611-643. DOI: [10.1007/s00429-012-0475-5](https://doi.org/10.1007/s00429-012-0475-5)
- Friston, K. J., Mattout, J., & Kilner, J. (2011). Action understanding and active inference. *Biological Cybernetics*, 104(1-2), 137-160. DOI: [10.1007/s00422-011-0424-z](https://doi.org/10.1007/s00422-011-0424-z)
- Perrinet, L. U., Adams, R. A., & Friston, K. J. (2014). Active inference, eye movements and oculomotor delays. *Biological Cybernetics*, 108(6), 777-801. DOI: [10.1007/s00422-014-0620-8](https://doi.org/10.1007/s00422-014-0620-8)
- Priorelli, M., et al. (2023). Modeling Motor Control in Continuous Time Active Inference: A Survey. *IEEE Transactions on Cognitive and Developmental Systems*, 16, 485-500.

## Key Concepts for the Postural Model

### 1. Motor Commands as Proprioceptive Predictions
In classical optimal control (including the PID framework of Paper 2), the brain computes a target trajectory and issues explicit motor commands (forces or torques) to drive the muscles. In active inference, the motor cortex does not send movement commands. Instead, it sends **proprioceptive predictions**—descending signals specifying the expected state of the body (e.g., muscle lengths and velocities).

### 2. The Equilibrium-Point Hypothesis Reimagined
This aligns with the equilibrium-point hypothesis (Feldman, 1986) but reframes it dynamically:
- The descending prediction acts as a moving equilibrium point.
- The prediction error (the difference between the current sensed posture and the predicted posture) is resolved not by updating the brain's model (which would be perception), but by peripheral reflexes moving the muscles to make the prediction come true (action).
- The spinal reflex arc is essentially a prediction error minimization circuit.

### 3. Delays in Active Inference
Perrinet et al. (2014) explicitly deal with visuo-oculomotor delays, highlighting that an agent must predict the *present* state based on *past* delayed sensory signals.
- In the scoliosis model, the proprioceptive delay $\tau \approx 200ms$ means the generative model must project forward in time.
- During rapid growth, if the physical plant's parameters (mass, length) change, the forward model's prediction of current velocity (the derivative term) becomes inaccurate.

### 4. Precision and Classical Gains
Adams et al. (2013) note that in active inference, classical feedback gains correspond to **precisions**.
- A high precision on sensory prediction errors means the system reacts strongly to deviations (high gain).
- In the PID model, the derivative gain $K_d$ is specifically the precision assigned to errors on the *rate of change* of posture.
- If predictions of velocity become systematically wrong (due to growth-induced model misspecification), optimal Bayesian updating demands that the system lower its precision on these predictions. This precision collapse *is* the derivative gain gap.

## Synthesis for Paper 5
The transition from Paper 2 to Paper 5 requires mapping:
- Motor control $u(t)$ $\rightarrow$ Reflex arc minimizing proprioceptive prediction error.
- Target angle $\theta_0$ $\rightarrow$ High-level proprioceptive prior.
- Feedback delay $\tau$ $\rightarrow$ Temporal horizon of the generative model.
- Gain $K_d$ $\rightarrow$ Precision on generalized velocity $\pi_v$.

When the generative model fails to update its plant parameters (growth), the mismatch primarily impacts the predicted generalized velocity. The system's optimal response is precision attenuation on velocity, leaving the system under-damped and susceptible to transient instabilities.
