# Day 1: Friston's Free-Energy Principle Foundations

## Core Papers
1. Friston, K. J. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138. doi:10.1038/nrn2787
2. Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*, 100(1-3), 70-87. doi:10.1016/j.jphysparis.2006.10.001

## Variational Free Energy and Surprise Minimisation
The Free-Energy Principle (FEP) postulates that all self-organising biological systems must minimise their variational free energy to resist a natural tendency towards disorder (entropy). Variational free energy $F$ is an upper bound on surprise (negative log-evidence), meaning that by minimising $F$, an organism implicitly minimises the surprise of its sensory observations given its model of the world.

$$F \ge -\ln p(y | m)$$
where $y$ is sensory data and $m$ is the generative model.

## Generative Models and Active Inference
A generative model $p(y, x, v, \theta)$ captures the joint probability of sensory observations $y$, hidden states $x$, hidden causes $v$, and parameters $\theta$.
Under FEP, organisms maintain an internal model of the causal structure of their environment. They can minimise free energy in two ways:
1. **Perceptual Inference:** Updating their internal model (posterior beliefs) to better predict sensory inputs.
2. **Active Inference:** Changing the environment or their relationship to it (action) to make sensory inputs match their predictions.

## Connection to the Postural Control Model (Preview)
In the context of the Paper 2 PID model:
*   The "generative model" is the brain's internal representation of the spine/body's biomechanics (an inverted pendulum in gravity).
*   The system continually generates predictions about sensory states (proprioception).
*   Discrepancies between predicted and actual sensory states constitute "prediction errors," which the system aims to minimise through action (postural adjustments).
*   During adolescent growth spurts, rapid morphological changes cause the generative model to become miscalibrated (model misspecification), leading to a persistent increase in prediction error and a failure of the system to maintain the "upright" equilibrium state (a global free-energy minimum).
