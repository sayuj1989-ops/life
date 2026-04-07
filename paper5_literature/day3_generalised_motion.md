# Phase 1, Day 3: Generalised Coordinates of Motion in the Free-Energy Principle

## Core Concepts

1. **Generalised Coordinates of Motion ($\tilde{x}$)**:
   In Karl Friston's formalism of the Free-Energy Principle (FEP), dynamic systems are represented using *generalised coordinates of motion*. Instead of just tracking the current state $x$, the system tracks the state and its higher-order temporal derivatives:
   $\tilde{x} = [x, x', x'', \dots]^T$
   This means the generative model explicitly encodes position, velocity, acceleration, jerk, and so on.

2. **Temporal Correlations**:
   This approach allows the agent's generative model to capture smooth temporal trajectories. By predicting not just where an object is, but where it is going and how its velocity is changing, the system can anticipate the future and compensate for sensorimotor delays (like the proprioceptive delay $\tau$).

3. **Generalised Prediction Errors ($\tilde{\varepsilon}$)**:
   Sensory input $\tilde{y}$ is also treated in generalised coordinates. The prediction error is therefore a vector spanning multiple derivative orders:
   $\tilde{\varepsilon} = \tilde{y} - g(\tilde{x})$
   This implies the brain evaluates separate prediction errors for position ($\varepsilon_0$), velocity ($\varepsilon_1$), and so on.

## The Bridge to PID Control (Baltieri & Buckley, 2019)

1. **Precision Weighting ($\Pi$)**:
   In active inference, each prediction error is weighted by its expected *precision* (inverse variance). Precision acts as a gain factor, determining how much influence a prediction error has on belief updating (perception) or motor action.

2. **Mapping to Controller Gains**:
   When active inference is applied to motor control with linear generative models (as demonstrated by Baltieri & Buckley, 2019):
   - The precision assigned to the **position prediction error** ($\Pi_0$) mathematically corresponds to the **Proportional gain ($K_p$)**.
   - The precision assigned to the **velocity prediction error** ($\Pi_1$) mathematically corresponds to the **Derivative gain ($K_d$)**.
   - The precision assigned to persistent biases or prior hidden causes mathematically corresponds to the **Integral gain ($K_i$)**.

3. **The Derivative Gain Gap as Precision Collapse**:
   Our Paper 2 hypothesis of the "Derivative Gain Gap" (degradation of $K_d$ during rapid adolescent growth) can now be rigorously mapped into the FEP.
   - Rapid biomechanical growth causes systematic mismatch in the generative model for velocity/acceleration.
   - The system detects high uncertainty in its velocity predictions and responds by optimally *down-weighting the precision of velocity prediction errors* ($\Pi_1$).
   - This precision collapse on generalised motion is the exact mathematical equivalent of the degradation of the effective derivative gain ($K_d$).

## Next Steps

- Formally review Baltieri & Buckley (2019) to extract the exact linear Gaussian generative model equations that yield the PID mapping.
- Understand how time-delay ($\tau$) interacts with generalised motion in this framework.
