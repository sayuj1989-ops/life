# Phase 1, Day 2: Active Inference and Motor Control

## Core Concepts
Active inference frames motor control not as computing commands to achieve goals, but as fulfilling proprioceptive predictions. The brain maintains a generative model of the world (including the body) and minimizes free energy (prediction error) through two pathways:
1. **Perceptual Inference:** Updating internal beliefs (the generative model) to match sensory inputs.
2. **Active Inference:** Moving the body to change sensory inputs to match predictions.

## Key Papers
- **Adams, Shipp, & Friston (2013). Predictions not commands: active inference in the motor system.**
  - Argues against traditional optimal motor control and inverse models.
  - Proposes that motor commands are actually descending proprioceptive predictions.
  - Movement occurs when classical reflex arcs act to suppress proprioceptive prediction errors.
- **Friston (2011). What is optimal about motor control?**
  - Discusses how optimal control is a special case of active inference. Value/reward is recast as prior expectations about the states an organism expects to inhabit.

## Relevance to the "Derivative Gain Gap" (Paper 2)
In Paper 2, the human trunk is modelled as an inverted pendulum with a PID controller. The active inference framework reframes this:
- The "set point" or target posture is a high-level prior (expectation).
- Motor commands are descending predictions of the proprioceptive state of being upright.
- Proprioceptive prediction errors drive reflexes to correct posture.
- The **equilibrium-point hypothesis** aligns nicely here: descending signals specify an equilibrium state (a prediction), and spinal reflexes generate forces to reach it.

### The "Gap" Mechanism in FEP terms
If the physical body grows rapidly (velocity of growth > 6 cm/yr), the mapping from proprioceptive signals to physical states (e.g., muscle lengths, joint angles) changes. The generative model's predictions become systematically mismatched with actual sensory feedback.
- Because the predictions are constantly wrong, the precision (confidence) of those predictions is down-weighted.
- In Friston's formalism, precision weighting of prediction errors on generalized motion corresponds to the derivative gain ($K_d$).
- A drop in precision on velocity prediction errors is mathematically equivalent to the derivative gain gap, leading to transient instability and the search for a new local minimum (scoliosis).
