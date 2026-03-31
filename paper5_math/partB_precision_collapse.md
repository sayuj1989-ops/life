# Day 12: Formal Derivation Part B - The Derivative Gain Gap as Precision Collapse

## 1. The Non-Stationary Plant (Growth)
In Paper 2, the adolescent growth spurt is modelled as a rapid increase in trunk length $L$ and mass $m$.
Let the plant's parameters be $\theta_{plant}(t) = [m(t), L(t)]$. The rate of change is $v_{growth} = \dot{\theta}_{plant}$.

The brain's generative model relies on an internal estimate of these parameters, $\theta_{model}$.

## 2. Model Misspecification and Prediction Error
The true dynamics of the spine (the pendulum) depend on $\theta_{plant}$. For example, the gravitational torque is proportional to $m L$.
$$ x_{true}'' = f_{biomech}(x, x', \theta_{plant}) $$

The generative model predicts the dynamics using $\theta_{model}$:
$$ \mu_x'' = f_{model}(\mu_x, \mu_x', \theta_{model}) $$

During a rapid growth spurt, $v_{growth}$ exceeds the Bayesian learning rate of the model:
$$ \theta_{model}(t) \neq \theta_{plant}(t) $$

This misspecification means the model's predictions about the acceleration ($x''$) and velocity ($x'$) of the spine are systematically biased.
Consequently, the variance of the sensory prediction errors on velocity ($\varepsilon_{y'} = y' - \mu_y'$) increases.

## 3. Precision Updating (The Collapse)
In hierarchical predictive processing, precisions $\Pi$ are not fixed; they are themselves parameters (hyperparameters) that are optimised to minimise free energy.
If the variance of a prediction error signal increases consistently over time, the optimal Bayesian inference is to down-weight its precision.

Let $\sigma_{y'}^2$ be the empirical variance of the velocity prediction errors. The optimal precision $\Pi_{y'}$ is the inverse variance:
$$ \Pi_{y'}^* = \frac{1}{\sigma_{y'}^2 + \lambda} $$
where $\lambda$ is a baseline noise term.

Since $\sigma_{y'}^2$ scales with the degree of model misspecification, which in turn scales with growth velocity $v_{growth}$ and proprioceptive delay $\tau$:
$$ \sigma_{y'}^2 \approx k(v_{growth} \cdot \tau) $$

Therefore, the precision on velocity prediction errors becomes:
$$ \Pi_{y'}^* \propto \frac{1}{v_{growth} \cdot \tau + \lambda} $$

## 4. Equivalence to the Derivative Gain Gap
From Part A, we established $K_d \leftrightarrow \Pi_{y'}$.
Therefore:
$$ K_{d, effective} \propto \frac{1}{v_{growth} \cdot \tau + \lambda} $$

This is the formal derivation of the central mechanism of Paper 2: **The transient degradation of derivative gain ($K_d$) during adolescence is mathematically equivalent to the optimal Bayesian down-weighting of sensory precision on velocity prediction errors due to growth-induced model misspecification.**
