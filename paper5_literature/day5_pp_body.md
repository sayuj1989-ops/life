# Day 5: Predictive Processing and Body Representation

## Core Papers
1. Brown, H., Adams, R. A., Kurth-Nelson, Z., Friston, K., Frith, C., & Moran, R. (2013). Active inference, sensory attenuation and illusions. *Cognitive processing*, 14(4), 411-427. doi:10.1007/s10339-013-0571-3

## Sensory Attenuation and Precision Weighting
In predictive processing, sensory attenuation (e.g., the inability to tickle oneself) is not due to an efference copy cancelling out the sensory input. Instead, it is a necessary feature of active inference.
To initiate a movement, the brain must transiently down-weight (attenuate) the precision of the sensory prediction errors that indicate "I am not currently moving." If it didn't do this, the system would immediately correct the prediction error by perceiving the body as stationary, and no movement would occur. By attenuating the precision of the current state, the top-down prediction of the *desired* state can drive the motor reflexes to move the body.

## Connection to the FEP Scoliosis Model
In the adolescent spine:
During the derivative gain gap, the generative model's predictions about velocity are systematically wrong due to rapid morphological changes.
Just like in sensory attenuation, the system must down-weight the precision of these unreliable velocity prediction errors.
However, unlike healthy sensory attenuation (which is transient and goal-directed), this precision collapse is sustained and pathological.
Because the system no longer trusts its velocity predictions, it effectively operates with a reduced derivative gain ($K_d$). It becomes sluggish in resisting perturbations, leading to transient postural instability.

This provides the mechanistic explanation for one of Paper 5's testable predictions: Adolescents with AIS (during the gain gap window) should exhibit elevated sensory attenuation (e.g., reduced ticklishness or altered force-matching) even when not actively moving, because their baseline proprioceptive precision is persistently down-weighted.
