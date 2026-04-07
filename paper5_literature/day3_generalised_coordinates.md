# Phase 1, Day 3: Generalised Coordinates and Precision

## Core Concepts
In active inference, the generative model must account for the dynamics of the world, not just static states. Friston's formalism handles this using **generalised coordinates of motion**.

A state $\tilde{x}$ is represented as a vector comprising the state itself, its velocity, acceleration, jerk, and so on:
$\tilde{x} = [x, x', x'', x''', \dots]^T$

The generative model encodes beliefs about these generalized states and minimizes free energy by suppressing prediction errors at all orders of motion.

## Precision Matrices and Controller Gains
As shown by **Baltieri & Buckley (2019)**, a linear active inference formulation mapped onto a motor control plant yields a direct equivalence between the precision (inverse variance) of prediction errors at different orders of motion and classical PID control gains.

- **Proportional Gain ($K_p$):** Corresponds to the precision on positional prediction errors ($\Pi_0$).
- **Derivative Gain ($K_d$):** Corresponds to the precision on velocity prediction errors ($\Pi_1$).
- **Integral Gain ($K_i$):** Arises from the internal dynamics of the generative model integrating errors over time (often linked to higher-order predictions or specific generative model architectures).

## The Predictive Processing Bridge to Counter-Curvature
This equivalence provides the mathematical bridge for Paper 5.

If the precision on velocity ($\Pi_1$) drops, the effective derivative gain ($K_d$) drops.
Why would $\Pi_1$ drop? In predictive processing, precision is down-weighted when sensory input is noisy or systematically unpredictable.

During the adolescent growth spurt, long-bone growth outpaces neuromuscular adaptation (the "relative velocity" issue). The mapping between motor commands and expected proprioceptive feedback (velocity of movement) becomes transiently unreliable. The brain down-weights the precision of these noisy velocity prediction errors ($\Pi_1 \downarrow$).

**Mathematical Consequence:** $K_d \downarrow$. The spine becomes transiently under-damped, leading to buckling and the emergence of S-shaped counter-curvature as the system seeks a new stable energy minimum. [VERIFY]

## Falsifiable Tests
- **Test 1:**
  - **Data Needed:** High-frequency kinematic tracking of spinal motion and EMG in early adolescent idiopathic scoliosis (AIS) patients vs. healthy age-matched controls during rapid postural perturbations.
  - **Refutation Criteria:** If AIS patients do not exhibit increased latency in velocity-dependent reflex arcs (decreased effective $K_d$) compared to controls *prior* to structural deformity.
- **Test 2:**
  - **Data Needed:** Computational simulation of a multi-segment inverted pendulum with an active inference controller where $\Pi_1$ is manually degraded over simulated developmental time.
  - **Refutation Criteria:** If degrading $\Pi_1$ (velocity precision) does not predictably induce multi-segment buckling (S-shape) matching the clinical Lenke types.

## References
1. Baltieri, M., & Buckley, C. L. (2019). PID control as a process of active inference with linear generative models. *Entropy*, 21(3), 257.
2. Friston, K., Mattout, J., Trujillo-Barreto, N., Ashburner, J., & Penny, W. (2007). Variational free energy and the Laplace approximation. *Neuroimage*, 34(1), 220-234.
3. Burwell, R. G., Dangerfield, P. H., & Freeman, B. J. C. (2008). Etiologic theories of idiopathic scoliosis: somatic nervous system and the NOTOM hypothesis. *Studies in Health Technology and Informatics*, 140, 197-207.
