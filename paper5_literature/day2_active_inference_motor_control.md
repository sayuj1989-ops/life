# Phase 1, Day 2: Active Inference and Motor Control

## Core Papers Reviewed
- Adams, R. A., Shipp, S., & Friston, K. J. (2013). Predictions not commands: active inference in the motor system. *Brain Structure and Function*, 218(3), 611-643. DOI: [10.1007/s00429-012-0475-5](https://doi.org/10.1007/s00429-012-0475-5)
- Hafner, D., Lillicrap, T., Ba, J., & Norouzi, M. (2019). Dream to Control: Learning Behaviors by Latent Imagination. *arXiv preprint arXiv:1912.01603*.
- Friston, K. J. (2011). What is optimal about motor control? *Neuron*, 72(3), 488-498. DOI: [10.1016/j.neuron.2011.10.018](https://doi.org/10.1016/j.neuron.2011.10.018)

## The Equilibrium-Point Hypothesis as Active Inference

### 1. Predictions, Not Commands
Classical optimal control theory assumes the brain computes a forward model to issue specific motor commands (e.g., muscle activations) that minimize a cost function. Active inference, as detailed by Adams et al., reframes motor control entirely:
- The brain does not issue motor commands.
- Instead, the cortex issues *predictions* about the proprioceptive consequences of a desired movement.
- These descending proprioceptive predictions act as setpoints for peripheral reflex arcs.
- The spinal cord and muscles simply execute reflexes to minimize the resulting prediction error between the desired proprioceptive state and the actual sensory feedback.

### 2. Motor Control as Sensory Suppression
Because action acts to fulfill sensory predictions, the agent must selectively ignore or attenuate the actual sensory input to allow the predicted state to drive the movement. This is known as sensory attenuation.
- In the context of active inference, this means reducing the precision (confidence) of sensory prediction errors.
- If precision is too high, the system is overly sensitive to current states and cannot move; if too low, it cannot effectively minimize error.

### 3. Relevance to the Dreamer Architecture
The Dreamer agent (Hafner et al., 2019) learns long-horizon behaviors by backpropagating value estimates through trajectories imagined in the compact latent space of a learned world model.
- Dreamer learns a world model from past experience that predicts into the future.
- It learns action and value models in its compact latent space. The value model optimizes Bellman consistency of imagined trajectories.
- The action model maximizes value estimates by propagating their analytic gradients back through imagined trajectories.
- When interacting with the environment, it executes the action model.
- This represents a computational parallel to active inference: the agent uses a generative model (the "world model") to predict future states (imagined trajectories) and selects actions that fulfill these predictions.

## Relevance to Paper 5: The Derivative Gain Gap
For the scoliosis model:
- The "Derivative Gain Gap" represents a mismatch where the physical body (plant) grows and changes rapidly, while the generative model (the brain's internal model) updates too slowly.
- During rapid growth, descending proprioceptive predictions become misspecified. The setpoints for the spinal reflex arcs are based on an outdated body schema.
- This creates persistent proprioceptive prediction errors.
- To maintain stability, the system might reduce the precision of these errors (sensory attenuation), leading to impaired postural control.
- Alternatively, the system may adapt by finding a new, asymmetric equilibrium point where the prediction error is minimized locally, manifesting as scoliotic curvature.
- The computational framework of Dreamer, specifically its reliance on an accurate learned world model to generate actions, underscores the critical vulnerability when this model becomes disjointed from reality, as hypothesized in the adolescent spine.
