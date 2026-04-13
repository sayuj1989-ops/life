# Phase 3, Day 11: Formal Derivation Part A (Generative Model)

## The Postural Generative Model with Delay
Building on Baltieri & Buckley (2019), we define a linear Gaussian generative model in generalized coordinates of motion $\tilde{x} = [x, x', x'']^T$, where $x$ represents the trunk angle. The crucial addition is the explicit modeling of the proprioceptive delay $\tau$.

The true state of the plant (the spine/trunk) at time $t$ is $x(t)$.
The sensory observation $y$ arrives with a delay $\tau$:
$$y(t) = g(x(t-\tau)) + \omega_y$$

To minimize free energy, the generative model must predict the current sensory input based on its belief about the past state. Using a first-order Taylor series approximation (valid for small $\tau$ and smooth motion), the delayed state can be approximated using generalized coordinates:
$$x(t-\tau) \approx x(t) - \tau x'(t)$$

Therefore, the generative model's sensory prediction is:
$$ \mu_y = g(\mu_x - \tau \mu_{x'}) $$

Assuming a linear mapping $g(x) = x$, the prediction errors for position and velocity are:
$$ \varepsilon_{y,0} = y(t) - (\mu_x - \tau \mu_{x'}) $$
$$ \varepsilon_{y,1} = y'(t) - (\mu_{x'} - \tau \mu_{x''}) $$

## Free-Energy Minimization and PID Control
The variational free energy $F$ bounds the surprise. For a linear Gaussian model, it is proportional to the precision-weighted sum of squared prediction errors:
$$ F \approx \frac{1}{2} \tilde{\varepsilon}_y^T \Pi_y \tilde{\varepsilon}_y + \frac{1}{2} \tilde{\varepsilon}_x^T \Pi_x \tilde{\varepsilon}_x + \frac{1}{2} \tilde{\varepsilon}_v^T \Pi_v \tilde{\varepsilon}_v $$

Where:
- $\Pi_{y,0}$ is the precision of position observations.
- $\Pi_{y,1}$ is the precision of velocity observations.
- $\Pi_{v,0}$ is the precision of the high-level prior (the upright set-point).

Active inference minimizes $F$ with respect to action $a$ (muscle torque):
$$ \dot{a} = -\frac{\partial F}{\partial a} = -\frac{\partial \tilde{\varepsilon}_y}{\partial a}^T \Pi_y \tilde{\varepsilon}_y $$

As shown by Baltieri & Buckley (2019), this gradient descent yields a controller with terms homologous to PID.
Crucially, evaluating this with the delayed prediction error $\varepsilon_{y,0} = y - (\mu_x - \tau \mu_{x'})$ highlights the role of $\Pi_{y,1}$:
To stabilize a delayed system, the controller must heavily weight the velocity prediction error $\varepsilon_{y,1}$ (which maps to $K_d$) to anticipate the future state. If $\Pi_{y,1}$ drops, the system falls back to effectively pure proportional control on delayed information, which is mathematically guaranteed to go unstable (as shown in Paper 2).
