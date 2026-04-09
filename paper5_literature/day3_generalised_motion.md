# Phase 1, Day 3: Generalised coordinates of motion in FEP

## 1. Generalised Motion Concept
Karl Friston's formalism of active inference uses "generalized coordinates of motion" to handle dynamics natively. Instead of just modeling a state $x(t)$, the generative model represents a state and all its higher-order temporal derivatives: $\tilde{x} = (x, x', x'', \dots)$. This allows the brain to model trajectories rather than just static points.

- Sensory states $\tilde{y} = (y, y', y'', \dots)$
- Hidden states $\tilde{x} = (x, x', x'', \dots)$
- Hidden causes $\tilde{v} = (v, v', v'', \dots)$

## 2. The D-Operator
A key element of generalized coordinates is the shift operator, $D$, which simply shifts the elements of the vector one position to the left (taking the derivative): $D \tilde{x} = (x', x'', \dots)$.
The generative model predicts $\tilde{y}$ based on $\tilde{x}$ and $\tilde{v}$, and free-energy minimization involves reducing prediction errors on all these levels of motion simultaneously.

## 3. Link to Derivative Control ($K_d$)
In a standard PID controller, the derivative term $K_d \frac{d}{dt} e(t)$ corrects for the rate of change of the error.
In active inference with generalized coordinates, prediction errors are evaluated not just on the position (0th order), but on the velocity (1st order), acceleration (2nd order), etc.

Precision matrices $\Pi$ weight the importance of each order of prediction error.
- The precision on the 0th order (position) error $\Pi_0$ corresponds functionally to the proportional gain $K_p$.
- The precision on the 1st order (velocity) error $\Pi_1$ corresponds to the derivative gain $K_d$.

When the body grows rapidly, the internal model of its dynamics becomes outdated (the mapping from states to velocity/acceleration is misspecified). The brain detects that its velocity predictions are consistently wrong, leading to an increase in the variance of the 1st-order prediction errors.

Because precision is inverse variance ($\Pi = \Sigma^{-1}$), the precision on velocity ($\Pi_1$) drops. This means the system stops trusting its velocity predictions and stops acting vigorously on them — effectively reducing the derivative gain $K_d$. This is the FEP equivalent of the "derivative gain gap."
