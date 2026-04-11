# Day 3: Generalised Coordinates of Motion in FEP

## Core Concept: Generalised Coordinates of Motion
In Friston's formulation of the Free-Energy Principle (FEP) for continuous-time systems (e.g., DEM: Dynamic Expectation Maximization, Friston et al. 2008, DOI: 10.1016/j.neuroimage.2008.02.054), states are represented not just by their current value, but by their path or trajectory.

A state $\tilde{x} = (x, x', x'', \ldots)^T$ is represented in "generalised coordinates of motion", combining the position ($x$), velocity ($x'$), acceleration ($x''$), jerk ($x'''$), and higher-order temporal derivatives.

## Precision Weighting on Generalised Motion
In a generative model predicting a sensory trajectory $\tilde{y}$ from hidden states $\tilde{x}$, the prediction error is evaluated at each order of motion:
- Position error: $\varepsilon_0 = y - g(x)$
- Velocity error: $\varepsilon_1 = y' - g'(x)$
- Acceleration error: $\varepsilon_2 = y'' - g''(x)$

The precision matrix $\Pi$ weights these errors in the free-energy functional. In active inference, the system minimizes precision-weighted prediction errors.
The precision $\pi_i$ assigned to the $i$-th order derivative defines how heavily the system penalizes prediction errors at that order.

## Relationship to Derivative Control
In classical PID control, the derivative term $K_d \frac{de}{dt}$ scales the control response based on the rate of change of the error.
Within the FEP formalism, penalizing velocity prediction errors ($\varepsilon_1$) acts analogously to a derivative control term.
Specifically, if the precision on velocity $\pi_1$ is high, the system will strongly correct deviations in the expected rate of change—mirroring a high derivative gain $K_d$.

If $\pi_1$ is low (precision collapse), the system essentially ignores velocity prediction errors, relying only on position error ($\varepsilon_0$ with precision $\pi_0 \leftrightarrow K_p$). This corresponds exactly to the "derivative gain gap" in our scoliosis model, where the degradation of $K_d$ is framed as a down-weighting of velocity prediction precision due to rapid bodily changes and proprioceptive delay.

## Conclusion
The generalised coordinates framework provides the formal justification for mapping the PID control terms ($K_p, K_d$) to sensory precisions ($\pi_0, \pi_1$) in active inference.
