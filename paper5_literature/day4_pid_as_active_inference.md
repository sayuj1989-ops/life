# Day 4: PID Control as Active Inference

## Core Papers
1. Baltieri, M., & Buckley, C. L. (2019). PID control as a process of active inference with linear generative models. *Entropy*, 21(3), 257. doi:10.3390/e21030257

## Formalising the Relationship
Baltieri & Buckley formally show that standard proportional-integral-derivative (PID) controllers map onto the variational free energy minimisation of a simple linear generative model.

In their derivation:
*   **Proportional gain ($K_p$)** maps to sensory precision on state $\Pi_x$. The system tries to reduce position error (discrepancy from the set-point).
*   **Derivative gain ($K_d$)** maps to sensory precision on velocity $\Pi_{x'}$. The system penalises rapid change, assuming the optimal generative model describes a stationary system. High precision means strong damping of motion.
*   **Integral gain ($K_i$)** maps to the precision on a slowly-varying parameter (or "hidden cause" $v$), typically constant bias.

This is a critical foundation for Paper 5. Baltieri & Buckley prove the equivalence. Paper 5 extends it by incorporating:
1.  **Delayed Observations ($\tau$):** In biological systems like the adolescent spine, proprioception has a significant transmission delay ($\tau \approx 200 \text{ ms}$). This requires the generative model to explicitly predict the *current* state given *delayed* sensory input, and to integrate these over time. FEP models this elegantly.
2.  **Growth-Dependent Misspecification:** Baltieri & Buckley assume a stationary plant. Paper 5 introduces a non-stationary plant (adolescent growth). The plant's parameters (e.g., mass, length, inertia) change over time at a rate $v_{growth}$.

## The FEP Interpretation of the PID Model
The "Adolescent Scoliosis as a Free-Energy Catastrophe" model works as follows:
When $v_{growth}$ is low, the brain can slowly update its generative model to track the plant's parameters.
When $v_{growth}$ spikes (growth spurt), the generative model's velocity predictions become systematically biased.
The system detects the systematic error in velocity predictions and down-weights $\Pi_{x'}$ to avoid being pushed around by "noise".
This precision collapse manifests as a transient drop in $K_d$ — the derivative gain gap.

This FEP perspective offers a mathematically rigorous foundation for the ad-hoc PID model in Paper 2.
