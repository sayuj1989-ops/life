# Day 2: Active Inference and Motor Control

## Core Papers
1. Adams, R. A., Shipp, S., & Friston, K. J. (2013). Predictions not commands: active inference in the motor system. *Brain Structure and Function*, 218(3), 611-643. doi:10.1007/s00429-012-0475-5
2. Friston, K. J., Mattout, J., & Kilner, J. (2011). Action understanding and active inference. *Biological Cybernetics*, 104(1), 137-160. doi:10.1007/s00422-011-0424-z

## Action without Efference Copy
Classical optimal control frameworks (e.g., LQG) often rely on an "efference copy" of motor commands being sent to a forward model to predict sensory consequences.
Active inference provides an alternative: the brain does not issue motor *commands* per se. Instead, it issues proprioceptive *predictions* (top-down expectations about the body's state). Action is simply the peripheral motor reflex arc (the spinal cord) fulfilling these predictions by moving the body to make the prediction true.
Motor control under active inference reduces to classical reflexes minimising proprioceptive prediction errors.

## The Equilibrium-Point Hypothesis as Active Inference
Active inference naturally subsumes Feldman's Equilibrium-Point Hypothesis (EPH). In EPH, the nervous system specifies threshold lengths for muscle activation (referent configurations). In active inference, these referent configurations are exactly the top-down proprioceptive predictions.
The spinal reflexes act as high-gain error minimisers. The higher levels of the hierarchy do not need to compute complex inverse dynamics; they just specify the desired sensory trajectory.
This is crucial for the postural control model in Paper 2: the PID controller's set-point (the upright posture) is the primary top-down prediction.

## Precision Weighting
To move, the system must transiently attenuate the sensory precision of the current state (otherwise, the prediction error would just update the model to say "I am not moving").
Precision (inverse variance) encodes the confidence placed in a prediction or sensory signal.
If precision on proprioceptive prediction errors is high, the system will aggressively try to correct those errors via action (high gain).
If precision is low, the system will be sluggish or fail to correct errors.
*This is the bridge to the Derivative Gain Gap*: The degradation of derivative gain $K_d$ is mathematically equivalent to a drop in the precision weighting of velocity prediction errors.
