# Day 3: Generalised Coordinates of Motion in FEP

## Core Formalism
1. Friston, K. (2008). Hierarchical models in the brain. *PLoS computational biology*, 4(11), e1000211. doi:10.1371/journal.pcbi.1000211
2. Buckley, C. L., Kim, C. S., McGregor, S., & Seth, A. K. (2017). The free energy principle for action and perception: A mathematical review. *Journal of Mathematical Psychology*, 81, 55-79. doi:10.1016/j.jmp.2017.09.004

## Generalised Coordinates of Motion
In Friston's formulation, dynamic systems are typically modelled in generalised coordinates of motion, $\tilde{x} = [x, x', x'', \dots]^T$. This allows the generative model to capture not just states (e.g., position), but their temporal derivatives (velocity, acceleration, jerk, etc.).
The evolution of the state is given by an ordinary differential equation (ODE) mapped to a continuous time representation.
The dynamics can be written in a unified form using the differential operator $D$: $D\tilde{x} = f(\tilde{x}, v, \theta) + \omega$, where $\omega$ is a smooth random fluctuation.

## Precision on Generalised Motion and Derivative Control
A key insight for Paper 5 is that sensory prediction errors ($\varepsilon$) are also encoded in generalised coordinates: $\tilde{\varepsilon} = \tilde{y} - g(\tilde{x}, v, \theta)$.
The precision matrix $\Pi$ weights these errors in the free-energy functional.
Specifically, precision on the first derivative of the sensory signal (velocity) governs how aggressively the system minimises velocity prediction errors.
In classical control theory, this is exactly the role of derivative gain ($K_d$).
A high precision on $\varepsilon'$ (velocity error) maps to a high $K_d$ — the system aggressively resists changes in velocity (damping).
A low precision on $\varepsilon'$ maps to a low $K_d$ — the system is underdamped and oscillates or drifts.

## The Connection
Paper 2 defined the "derivative gain gap" as an ad-hoc, phenomenological reduction in $K_d$ during rapid adolescent growth.
In the active inference framework, this is formalised as a drop in $\Pi_{y'}$, the sensory precision assigned to velocity prediction errors.
Why does $\Pi_{y'}$ drop? Because the generative model $g(\dots)$ is misspecified. It assumes body parameters (mass, length, inertia) that are outdated because the plant is growing too fast. The brain detects that its velocity predictions are systematically wrong (high variance in $\omega'$), and optimally down-weights them to avoid acting on noise.
