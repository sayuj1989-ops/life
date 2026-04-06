# Phase 1, Day 2: Active Inference and Motor Control

## Core Papers Reviewed
- Adams, R. A., Shipp, S., & Friston, K. J. (2013). Predictions not commands: active inference in the motor system. *Brain Structure and Function*, 218(3), 611-643. DOI: [10.1007/s00429-012-0475-5](https://doi.org/10.1007/s00429-012-0475-5)
- Hafner, D., Lillicrap, T., Ba, J., & Norouzi, M. (2019). Dream to Control: Learning Behaviors by Latent Imagination. *arXiv preprint arXiv:1912.01603*.

## Active Inference in the Motor System
According to Adams et al. (2013), the motor system does not issue optimal motor commands. Instead, descending motor pathways convey **predictions** of proprioceptive states.
1. **Proprioceptive Prediction Errors:** Motor behavior is elicited by prior expectations of trajectories. When the actual proprioceptive state (e.g., muscle stretch) differs from the descending prediction, a proprioceptive prediction error is generated.
2. **Peripheral Reflex Arcs:** The spinal reflex arcs resolve these prediction errors not by updating the internal model (perception), but by acting on the environment (muscle contraction) to make the sensory state match the prediction.
3. **Equilibrium-Point Hypothesis:** This elegantly fulfills the equilibrium-point hypothesis, framing motor control purely as active inference where action minimizes free energy at the periphery.

## Latent Imagination and Generative Models (Dreamer)
To model the brain's generative models within this active inference framework, we integrate the **Dream to Control (Dreamer)** architecture by Hafner et al. (2019).
1. **Latent Space Dynamics:** Dreamer learns a world model from past experiences to predict future states within a compact latent space. This aligns with active inference, where the brain maintains a generative model of hidden states $\vartheta$.
2. **Latent Imagination:** Dreamer learns long-horizon behaviors by backpropagating value estimates through trajectories imagined purely in this latent space. This conceptualizes how the central nervous system anticipates and plans optimal postural adjustments or motor trajectories before they are executed.
3. **Implementation Note:** For computational modelling of this generative framework, we will rely on the newer implementation of Dreamer in **TensorFlow 2**, as it is substantially simpler and faster while replicating the original results.

## Relevance to Paper 5: The Derivative Gain Gap
- **Misaligned Predictions:** During adolescent growth spurts, the physical properties of the spine (mass, length) scale rapidly. If the generative model (or "world model" in Dreamer terms) fails to update its latent dynamics quickly enough, it issues proprioceptive predictions based on an outdated body schema.
- **Action Fails to Resolve Error:** The peripheral reflex arcs contract muscles to fulfill these misspecified predictions. However, because the plant dynamics (equations of motion) have changed, this leads to persistent asymmetry and a derivative gain gap.
- **Latent Imagination Breakdown:** The agent's ability to plan postural corrections via latent imagination is compromised because the imagined trajectories in the latent space diverge from actual biomechanical outcomes, trapping the system in a suboptimal free-energy minimum.
