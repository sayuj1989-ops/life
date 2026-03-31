# Mathematical Development: Mapping Friston to Dreamer to PID

This document establishes the formal derivation connecting Friston's active inference to the Dreamer architecture, and subsequently linking it to the PID postural controller developed in Papers 2 and 3.

## 1. Friston's Active Inference (Continuous Time)

In active inference, an agent minimizes free energy $F$, which bounds the surprise of observations $y$. The dynamics of internal states $\mu$ are driven by prediction errors:

$$ \dot{\mu} = \mu' - \frac{\partial F}{\partial \mu} $$

Assuming Gaussian densities, the free energy relies on the precision-weighted prediction errors. Let $\varepsilon_y = y - g(\mu)$ be the sensory prediction error, with precision matrix $\Pi_y$.

$$ F \approx \frac{1}{2} \varepsilon_y^T \Pi_y \varepsilon_y + \frac{1}{2} \varepsilon_\mu^T \Pi_\mu \varepsilon_\mu - \frac{1}{2} \ln |\Pi_y \Pi_\mu| $$

## 2. Dreamer's Latent Objective

Dreamer models the world using a recurrent state-space model (RSSM). The variational lower bound (ELBO) maximized by Dreamer is analogous to negative free energy. The transition model $p(s_t | s_{t-1}, a_{t-1})$ corresponds to the empirical prior (dynamics), and the observation model $p(o_t | s_t)$ corresponds to the generative model mapping states to sensory inputs.

## 3. The PID - Active Inference Bridge

The core theoretical contribution of Paper 5 is mapping the classical PID gains ($K_p$, $K_i$, $K_d$) to parameters within the active inference scheme.

We define the error signal $e(t) = \theta_{ref} - \theta(t)$, where $\theta(t)$ is the spinal angle.

In an active inference framework, sensory precision $\Pi_y$ dictates the gain on sensory prediction errors. A high $\Pi_y$ means the system heavily penalizes deviations from the predicted sensory state (the reference state, assuming strong top-down priors).

### Derivation: Proportional Gain as Sensory Precision

The restorative force (or torque) in active inference is proportional to the gradient of Free Energy with respect to action:
$$ a = -\frac{\partial F}{\partial a} = - \frac{\partial \varepsilon_y}{\partial a} \Pi_y \varepsilon_y $$

If we assume a simple mapping where action directly affects sensory input (e.g., $y \approx a$), the restoring action is proportional to $\Pi_y \varepsilon_y$.
In classical control, the proportional response is $K_p \cdot e(t)$.

Therefore, we establish the identity:
$$ K_p \propto \Pi_y $$

**Conclusion:** The proportional stiffness of the spine ($K_p$) is formally equivalent to the precision of sensory (proprioceptive) prediction errors in a predictive processing framework.

### The Derivative Gain Gap (Revisited)

Paper 2 established that a temporal lag ($\tau$) degrades the effective derivative gain $K_d$, leading to instability (scoliosis onset). In the active inference formulation, $K_d$ maps to the precision on the *first derivative* of sensory states (or the velocity prediction error). A breakdown in $K_d$ is mathematically equivalent to a loss of precision on velocity priors, causing the agent to rely excessively on position errors (high $K_p$), leading to oscillatory dynamics and structural buckling.
