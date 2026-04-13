# Phase 1, Day 3: Latent Imagination and Generative Models in Active Inference

## Source Materials
- Hafner, D., Lillicrap, T., Ba, J., & Norouzi, M. (2019). Dream to Control: Learning Behaviors by Latent Imagination. arXiv preprint arXiv:1912.01603. DOI: 10.48550/arXiv.1912.01603

## Synthesis: Dreamer as a Framework for Predictive Processing
The 'Dream to Control' (Dreamer) architecture provides a concrete computational implementation of latent imagination that conceptually bridges reinforcement learning and active inference. Dreamer learns a world model from past experience, which functions analogously to the brain's generative models in the Free Energy Principle (FEP).

### Key Concept Alignments
1. **World Model as Generative Model:** Dreamer's world model predicts future states into a compact latent space, similar to how descending predictions in active inference specify expected sensory trajectories.
2. **Latent Imagination:** Dreamer backpropagates value estimates through trajectories imagined purely in the latent space. In active inference, this is akin to evaluating expected free energy over future policies or counterfactual processing.
3. **Action Model and Equilibrium Points:** While Dreamer maximizes value estimates via analytic gradients propagated back through imagined trajectories, active inference fulfills predictions by suppressing prediction errors via peripheral reflex arcs. Both architectures rely on the world model/generative model to simulate outcomes and select optimal motor commands.

### Relevance to the Derivative Gain Gap
In the context of the derivative gain gap and rapid adolescent growth (the scoliosis model):
- The internal world model must accurately capture "generalized motion" (position, velocity, acceleration) to imagine realistic postural trajectories.
- When the body undergoes a sudden growth spurt, the internal world model becomes outdated. The transition model fails to accurately predict sensory outcomes from actions due to altered physical biomechanics.
- This mismatch leads to an attenuation of precision on the velocity prediction errors. In PID control terms, this manifests as a degraded derivative gain ($K_d$).
- By integrating the Dreamer architecture, we have a computational framework to model this breakdown: when the latent imagination diverges from environment dynamics, the agent cannot synthesize long-horizon stabilization behaviors, leading to postural collapse.

## Implementation Notes
- The original Dreamer TF1 repository has been cloned to `paper5_model/dreamer`.
- Phase 3 will involve leveraging this architecture to simulate the divergence between a learned world model (pre-growth spine) and actual environment dynamics (elongated spine).
