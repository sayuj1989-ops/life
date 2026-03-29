# Phase 1, Day 1: Free-Energy Principle Foundations

## Objective
Establish the core mathematical formalism of Friston's free-energy principle (FEP) as the foundation for the "Predictive Processing Bridge" mapping to PID postural control.

## Key Concepts and Definitions
1. **Generative Model ($p(y, x, v, \theta)$)**:
   The brain maintains an internal model of the world and body to predict sensory inputs.
   - $y$: Sensory observations (e.g., proprioceptive and vestibular feedback).
   - $x$: Hidden states (e.g., current trunk angle, angular velocity).
   - $v$: Hidden causes (e.g., gravitational torque, biomechanical parameters like growth velocity).
   - $\theta$: Model parameters (e.g., slowly changing constants).

2. **Variational Free Energy ($\mathcal{F}$)**:
   An upper bound on sensory surprise (negative log-evidence, $-\ln p(y)$). Biological systems minimize $\mathcal{F}$ to maintain their structural and functional integrity.
   $$ \mathcal{F} \ge -\ln p(y) $$
   It is defined as complexity minus accuracy:
   $$ \mathcal{F} = D_{KL}[q(x,v,\theta) || p(x,v,\theta)] - E_{q}[\ln p(y | x,v,\theta)] $$
   Where $q$ is the approximate posterior distribution (the brain's "best guess" or conscious experience in predictive processing frameworks).

3. **Active Inference**:
   The process of minimizing variational free energy. It can be achieved in two ways:
   - **Perceptual Inference**: Updating the internal model ($q$) to better predict sensations.
   - **Active Inference (Motor Control)**: Performing actions to change sensory input ($y$) to match the model's predictions.

4. **Prediction Error ($\varepsilon$)**:
   The discrepancy between predicted and actual sensory input. In linear Gaussian models, free-energy minimization reduces to prediction error minimization weighted by precision ($\Pi$, inverse variance).
   $$ \mathcal{F} \approx \frac{1}{2} \varepsilon^T \Pi \varepsilon + \dots $$

## Insights for Paper 5
- The proportional gain ($K_p$) in the PID model corresponds to precision-weighted prediction errors on position (states).
- The derivative gain ($K_d$) corresponds to precision-weighted prediction errors on generalized motion (velocity).
- A breakdown in $K_d$ during rapid growth (the "Derivative Gain Gap") maps precisely to a collapse in the precision assigned to velocity predictions due to model misspecification.

## References
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127–138. DOI: 10.1038/nrn2787
- Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*, 100(1–3), 70–87. DOI: 10.1016/j.jphysparis.2006.10.001
