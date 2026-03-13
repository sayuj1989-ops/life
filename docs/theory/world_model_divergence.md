# Latent Imagination of the Spine: World Model Divergence

## Formalization
In the Biological Counter-Curvature framework, spinal control is modeled as an active inference process (analogous to Dreamer RL agents). The nervous system maintains a latent state prediction $z_t$ of postural alignment based on an internal gravity model $g_{internal}$.

The reward function minimizes metabolic energy cost, penalized by the Energy Deficit Proxy:
$R(z_t, u_t) = - \alpha E_{deficit}(u_t) - \beta D_{KL}(P(z_t|g_{internal}) || P(z_t|g_{true}))$

During the adolescent growth spurt, rapid physical changes cause $P(z_t|g_{true})$ to diverge faster than the learning rate of $g_{internal}$. The accumulating divergence (Sensory Prediction Error) manifests physically as the scoliotic curvature (Cobb angle).

## Falsifiable Tests
1. **Test: Proprioceptive Lag Quantification**
   - **Data Needed:** Serial fMRI and force-plate posturography of adolescents tracking proprioceptive response times across peak height velocity (PHV).
   - **Refutation:** If scoliotic patients show identical or faster predictive model updating (no lag) compared to healthy controls across the growth spurt, the world model divergence hypothesis is falsified.
2. **Test: VR-Induced Model Reset**
   - **Data Needed:** Intervention trial using Virtual Reality to systematically perturb visual-vestibular gravity references, forcing rapid recalibration of $g_{internal}$.
   - **Refutation:** If aggressive, forced recalibration of the internal gravity model during the onset window fails to alter the progression rate of early AIS, the hypothesis is falsified.

## References
- Hafner, D., et al. (2019). "Dream to Control: Learning Behaviors by Latent Imagination." *arXiv*.
- Franklin, D. W., & Wolpert, M. D. (2011). "Computational mechanisms of sensorimotor control." *Neuron*, 72(3).
