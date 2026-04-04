# Day 2: Active Inference and Motor Control

## Objective
To understand how active inference models motor control, specifically focusing on the equilibrium-point hypothesis, and to draw parallels to the postural control model.

## Key Literature
- **Adams, Shipp, & Friston (2013). "Predictions not commands: active inference in the motor system."** Brain Structure and Function. DOI: 10.1007/s00429-012-0475-5.

## Key Concepts
- **Predictions, Not Commands**: In the active inference framework, the motor cortex does not send explicit motor commands (e.g., specifying muscle forces). Instead, it sends *descending predictions* of proprioceptive sensory states to the spinal cord.
- **Action as Fulfilling Predictions**: Action occurs because peripheral reflex arcs (like the stretch reflex) act to fulfill these descending proprioceptive predictions, minimizing proprioceptive prediction errors. Thus, movement is the process of the physical body aligning with the brain's generative model.
- **The Equilibrium-Point Hypothesis**: Classical motor control proposes that descending signals specify an equilibrium point for the motor system, and muscles act like springs to reach this point. Active inference elegantly subsumes this: the descending top-down prediction *is* the equilibrium point. Reflexes drive the system towards this predicted state.
- **Role of Precision**: For action to occur, the brain must attenuate (reduce the precision of) the current sensory evidence. If it didn't, the discrepancy between the current state and the desired (predicted) state would just lead to a perceptual update (updating the belief to match the current non-moving state). By lowering sensory precision and keeping prediction precision high, the system is forced to resolve the free energy via action.

## Relevance to the PID Model and Derivative Gain Gap
- The postural PID controller's target upright state is the "descending prediction" (the equilibrium point).
- The $K_p$ (proportional gain) relates to the precision of this position prediction versus current sensory evidence.
- When rapid growth occurs, the generative model for how to achieve this equilibrium (specifically the mapping of velocities, handled by the derivative term) becomes misspecified.
- The "effective $K_d$ degradation" is a collapse in the precision of velocity prediction errors because the model correctly recognizes that its temporal predictions are failing. Action (reflexes) can no longer properly fulfill the predictions, leading to instability around the equilibrium point.
