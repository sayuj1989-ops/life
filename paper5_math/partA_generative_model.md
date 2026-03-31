# Day 11: Formal Derivation Part A - PID as Active Inference

## 1. The Generative Model

We define a linear Gaussian generative model $p(y, x, v)$ for the postural control system, building on Baltieri & Buckley (2019) but explicitly incorporating delayed observations.

Let the hidden states (e.g., trunk angle) be $x \in \mathbb{R}$. The system evolves in continuous time. We use generalised coordinates of motion $\tilde{x} = [x, x', x'', \dots]^T$.

The generative model specifies the joint probability of sensory observations $y$ and hidden states $\tilde{x}$, parameterised by hidden causes $v$ (e.g., persistent gravitational torque).

$$ p(\tilde{y}, \tilde{x}, v) = p(\tilde{y} | \tilde{x}) p(\tilde{x} | v) p(v) $$

### 1.1 Sensory Likelihood (with Delay)
The observations $y(t)$ are a delayed mapping of the true states $x(t - \tau)$ plus sensory noise $\omega_y$:
$$ y(t) = g(x(t - \tau)) + \omega_y $$
For a linear system, $g(x) = C x$. In generalised coordinates:
$$ \tilde{y} = C \tilde{x}_\tau + \tilde{\omega}_y $$
where $\tilde{x}_\tau$ is the delayed state. The noise $\tilde{\omega}_y$ is drawn from a Gaussian distribution with precision matrix $\Pi_y$.

### 1.2 State Dynamics (Priors)
The state evolves according to a linear function $f$, driven by hidden causes $v$ and state noise $\omega_x$:
$$ \tilde{x}' = f(\tilde{x}, v) + \tilde{\omega}_x $$
$$ \tilde{x}' = A \tilde{x} + B v + \tilde{\omega}_x $$
The noise $\tilde{\omega}_x$ has precision $\Pi_x$.

## 2. Variational Free Energy Minimisation

The system seeks to minimise variational free energy $F$, which bounds the surprise of the observations. Under the Laplace assumption (Gaussian densities), $F$ is a function of the prediction errors $\tilde{\varepsilon}$:

$$ F \approx \frac{1}{2} \tilde{\varepsilon}_y^T \Pi_y \tilde{\varepsilon}_y + \frac{1}{2} \tilde{\varepsilon}_x^T \Pi_x \tilde{\varepsilon}_x $$

where the prediction errors are:
*   **Sensory Error:** $\tilde{\varepsilon}_y = \tilde{y} - C \tilde{\mu}_{x,\tau}$  (where $\mu_x$ is the brain's estimate of the state)
*   **State/Dynamics Error:** $\tilde{\varepsilon}_x = D\tilde{\mu}_x - f(\tilde{\mu}_x, v)$ (where $D$ is the derivative operator)

## 3. Active Inference and PID Control

Action $a$ (muscle torque) minimises free energy by changing the sensory input $\tilde{y}$ to match the predictions. This is the reflex arc.
$$ \dot{a} = -\frac{\partial F}{\partial a} = -\frac{\partial F}{\partial \tilde{y}} \frac{\partial \tilde{y}}{\partial a} $$

If we expand this for the first two orders of motion (position $y$ and velocity $y'$), and assume the desired state (set-point) is $r=0$:
$$ a(t) \propto \Pi_{y,0} (y(t) - r) + \Pi_{y,1} (y'(t) - r') + \Pi_v \int (y(\sigma) - r) d\sigma $$

This is exactly the PID control law:
*   $K_p \leftrightarrow \Pi_{y,0}$ (Precision on position error)
*   $K_d \leftrightarrow \Pi_{y,1}$ (Precision on velocity error)
*   $K_i \leftrightarrow \Pi_v$ (Precision on the slowly varying prior/bias $v$)

**Crucially for Paper 5:** The derivative gain $K_d$ is mathematically equivalent to the sensory precision on the velocity prediction error, $\Pi_{y,1}$.
