# Phase 3, Day 12: Formal Derivation Part B (Precision Collapse)

## Modeling the Plant and Growth
Let the true physical plant (the trunk) be modeled as an inverted pendulum with parameters $\theta_p = \{m, l, I\}$ (mass, length, inertia).
The mapping from action $a$ (muscle torque) to body motion $x''$ depends on these parameters: $x'' = f_{plant}(x, a, \theta_p)$.
During the adolescent growth spurt, these parameters change continuously over time. Let $v_g$ be the growth velocity. Thus, $\dot{\theta}_p = h(v_g)$.

## The Generative Model's Parameter Update
The brain maintains an internal estimate of these parameters, $\theta_m$. It updates them via a slower learning process (hyperparameter learning in FEP) with a learning rate $\eta$:
$$ \dot{\theta}_m = -\eta \frac{\partial F}{\partial \theta_m} $$

**The Core Misspecification:** If the physical growth rate exceeds the biological learning rate ($|\dot{\theta}_p| > |\dot{\theta}_m|$), the model becomes systematically misspecified: $\Delta\theta = \theta_p - \theta_m \neq 0$.

## Deriving the Precision Dynamics ($\dot{\Pi}_{y,1}$)
Because the internal model uses the wrong inertia and lever arms ($\theta_m$), its predictions about the sensory consequences of its own motor commands are wrong. Specifically, the predicted velocity $\mu_{x'}$ deviates from the true sensory velocity $y'$.
This creates a persistent, non-zero prediction error on the first generalized coordinate: $\varepsilon_{y,1} = y' - \mu_{x'}$.

In active inference, precisions ($\Pi$) are not fixed; they are also optimized to minimize free energy. The precision $\Pi_{y,1}$ is the inverse of the estimated variance of the velocity sensory channel, $\Sigma_{y,1}$.
The optimal estimate for the variance tracks the squared prediction errors:
$$ \dot{\Sigma}_{y,1} = \kappa (\varepsilon_{y,1}^2 - \Sigma_{y,1}) $$
where $\kappa$ is the precision updating rate.

Because the persistent model misspecification ($\Delta\theta$) drives $\varepsilon_{y,1}^2$ consistently higher, the estimated variance $\Sigma_{y,1}$ increases.
Since $\Pi_{y,1} = 1 / \Sigma_{y,1}$, the precision *collapses*:
$$ \Pi_{y,1}(t) \propto \frac{1}{\varepsilon_{y,1}(t)^2} $$

## Connecting Back to $K_d$
From Day 11, we know the effective derivative gain $K_d$ maps to $\Pi_{y,1}$.
Therefore, the dynamic collapse of $\Pi_{y,1}$ due to unlearnable plant changes perfectly derives the phenomenological "Derivative Gain Degradation" curve we posited in Paper 2.
We have now proven the "Derivative Gain Gap" is a mathematically inevitable consequence of Free-Energy Minimization when $\dot{\theta}_p > \dot{\theta}_m$ and $\tau > 0$.
