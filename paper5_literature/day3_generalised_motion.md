# Phase 1, Day 3: Generalised coordinates of motion in FEP

## Core Concept: Generalised Coordinates
Friston's active inference formulation uses a state-space approach that represents not just the value of a variable, but its instantaneous velocity, acceleration, jerk, and higher-order derivatives. A "generalised state" $\tilde{x}$ is defined as the tuple $(x, x', x'', x''', \dots)$.
This allows continuous-time dynamics to be cast as a gradient descent on a single quantity (free energy) because temporal transitions are explicitly encoded in the state itself. By the shift operator $D$, we can represent temporal changes $\partial \tilde{x} / \partial t = D\tilde{x}$.

## The Importance of Precision on Velocity
In active inference, the generative model specifies expected trajectories. If we observe a trajectory, the prediction errors are not just on position ($e_x$), but on velocity ($e_{x'}$), acceleration ($e_{x''}$), and so on.
Each level of these generalized errors is weighted by its *precision* (inverse variance or uncertainty).
Let $\Pi_0$ be precision on position, $\Pi_1$ be precision on velocity.
The free energy $F$ contains terms like $e_x^T \Pi_0 e_x + e_{x'}^T \Pi_1 e_{x'}$.

## Connection to Derivative Control (PID)
In PID control, the derivative term ($K_d$) scales the control output based on the rate of change of the error.
In active inference, the precision on velocity ($\Pi_1$) determines how much the system updates its states and drives action to correct velocity errors.
When $\Pi_1$ is high, the system strongly corrects velocity deviations (high effective $K_d$).
When $\Pi_1$ collapses, the system ignores velocity prediction errors, meaning it only corrects based on position (equivalent to losing the $K_d$ term).

## Relevance to Paper 2's Derivative Gain Gap
During adolescent growth spurts, rapid morphological changes mean the brain's internal model of body dynamics becomes structurally misspecified (predictions of acceleration/velocity based on motor commands are consistently wrong due to changing mass/inertia).
Because the predictions are systematically poor, Bayesian inference dictates that the *precision* assigned to these predictions must drop (the brain learns that its velocity estimates are unreliable).
This precision drop mathematically mimics the degradation of derivative gain $K_d$ that Paper 2 empirically modelled as leading to postural instability (scoliosis).

## Literature Cited
- Buckley, C. L., et al. (2017). "The free energy principle for action and perception: A mathematical review." *Journal of Mathematical Psychology*. https://doi.org/10.1016/j.jmp.2017.09.004
- Friston, K. J., et al. (2010). "Action and behavior: a free-energy formulation." *Biological Cybernetics*. https://doi.org/10.1007/s00422-010-0364-z
- Baltieri, M., & Buckley, C. L. (2019). "PID Control as a Process of Active Inference with Linear Generative Models." *Entropy*, 21(3), 257. https://doi.org/10.3390/e21030257
