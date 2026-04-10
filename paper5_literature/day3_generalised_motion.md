# Phase 1, Day 3: Generalised Coordinates of Motion in the Free-Energy Principle

## 1. The Concept of Generalised Motion
In continuous-time active inference, systems do not just represent their current state at an infinitesimal point in time; they represent the local trajectory of states. Karl Friston mathematically formalises this using **generalised coordinates of motion**, denoted by the tilde notation:
$$ \tilde{x} = \begin{bmatrix} x \\ x' \\ x'' \\ x''' \\ \vdots \end{bmatrix} $$
Where:
- $x$ is the state (position/value).
- $x'$ is the first derivative (velocity).
- $x''$ is the second derivative (acceleration).
- $x'''$ is the third derivative (jerk), and so on.

By maintaining a probability distribution over these generalised coordinates, the brain's generative model implicitly predicts the immediate future through local Taylor series expansions.

## 2. Prediction Errors on Generalised Coordinates
Sensory evidence and internal states are evaluated not just at the 0-th order, but across all orders of motion. The system computes a vector of prediction errors $\tilde{\epsilon}$:
- **$\epsilon_0$**: Prediction error on position (current state mismatch).
- **$\epsilon_1$**: Prediction error on velocity (rate of change mismatch).
- **$\epsilon_2$**: Prediction error on acceleration, etc.

The update of internal states $\tilde{\mu}$ (the brain's "best guess" or posterior mean) is driven by these hierarchical prediction errors, scaled by their expected **precisions** (inverse variances), often denoted by matrices $\tilde{\Pi}$.

## 3. How Generalised Motion Relates to Derivative Control
In classical control theory (specifically PID control), the controller issues commands based on:
- **Proportional (P)** error: difference between target and actual position.
- **Derivative (D)** error: difference between target and actual velocity.
- **Integral (I)** error: accumulated past errors.

Under the active inference formulation, the **proportional gain ($K_p$)** maps naturally to the precision-weighted prediction error on the 0-th order state ($\Pi_0 \epsilon_0$).
Crucially, the **derivative gain ($K_d$)** maps to the precision-weighted prediction error on the 1st-order state—generalised velocity ($\Pi_1 \epsilon_1$).

### The Bridging Insight for Paper 5
If $K_d$ is equivalent to the precision of velocity prediction errors ($\Pi_1$), then the "derivative gain gap" modeled in Paper 2 (which triggers transient instability during the adolescent growth spurt) must correspond to a **collapse in the precision of velocity predictions** ($\Pi_1 \to 0$).
When the body grows too fast (>6 cm/yr), the generative model's mapping between motor commands and actual kinematic velocities becomes miscalibrated. The Bayesian brain correctly detects this uncertainty and down-weights the velocity prediction errors (reducing $\Pi_1$). As $\Pi_1$ drops, the "effective $K_d$" drops, removing the damping required to stabilize the delayed proprioceptive feedback loop.

## 4. Summary
Generalised coordinates of motion provide the necessary mathematical vocabulary to bridge Friston's predictive processing with classical PID control. The degradation of derivative control in scoliosis is formally identical to precision collapse on 1st-order generalised motion within a Bayesian filtering framework.
