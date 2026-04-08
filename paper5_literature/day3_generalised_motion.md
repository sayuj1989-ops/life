# Phase 1, Day 3: Generalised Coordinates of Motion in the Free-Energy Principle

## Objective
Review Friston's formalism for encoding dynamic states as "generalised motion" and understand how the precision on these coordinates relates to derivative control in biological systems, serving as the mathematical bridge for our postural model.

## Key Concepts

### 1. Generalised Coordinates of Motion
In Friston's active inference framework, an agent doesn't just maintain a belief about its current state $x$; it maintains beliefs about the state and all its higher-order temporal derivatives:
$\tilde{x} = [x, x', x'', x''', \dots]^T$
where $x'$ is velocity, $x''$ is acceleration, and so on.

This formalism is crucial for modeling biological dynamics because sensory data is not a static snapshot but an evolving trajectory. The generative model predicts this trajectory, leading to a hierarchy of prediction errors:
- $\varepsilon_0$: error on position ($x$)
- $\varepsilon_1$: error on velocity ($x'$)
- $\varepsilon_2$: error on acceleration ($x''$)

### 2. Precision Matrices
Each level of prediction error is weighted by its *precision* (inverse variance), denoted by $\Pi$. In a linear Gaussian model, the free-energy objective function includes terms of the form:
$F \approx \frac{1}{2} \tilde{\varepsilon}^T \tilde{\Pi} \tilde{\varepsilon}$

Where $\tilde{\Pi}$ is a block-diagonal precision matrix for the generalized coordinates. The components of this matrix determine how much the system "trusts" its sensory evidence versus its internal predictions at each derivative level.

### 3. The Link to Derivative Control ($K_d$)
As established in prior work (e.g., Baltieri & Buckley 2019), classical PID control can be mapped onto active inference.
- The **Proportional Gain ($K_p$)** maps to the precision on position prediction errors ($\Pi_0$).
- The **Derivative Gain ($K_d$)** maps to the precision on velocity prediction errors ($\Pi_1$).

When an organism detects that its velocity predictions are consistently unreliable (high prediction error, $\varepsilon_1$), Bayesian updating dictates that the precision ($\Pi_1$) assigned to those errors should be decreased.

### 4. Application to the Postural Model (Paper 2)
During the rapid adolescent growth spurt, the physical body (the "plant") changes faster than the brain's generative model can update. This causes a systematic miscalibration of velocity predictions.
- **Model Misspecification:** $\varepsilon_1$ increases chronically.
- **Precision Collapse:** The brain optimally down-weights $\Pi_1$ to avoid acting on noisy/biased velocity estimates.
- **The Derivative Gain Gap:** This drop in $\Pi_1$ is mathematically equivalent to the degradation of $K_d$ posited in Paper 2. The adolescent transiently loses optimal derivative control because the brain ceases to trust its velocity predictions.

## Mathematical Formulation to Carry Forward
Let the sensory prediction error be $\varepsilon_y = y - g(x, v)$. In generalized coordinates, the precision-weighted error is $\Pi \tilde{\varepsilon}$. We need to explicitly derive how a time-varying plant parameter (growth) influences the optimal update of $\Pi_1$, leading to the "precision collapse" that defines the derivative gain gap.

## Next Steps
- Day 4: Thorough review of Baltieri & Buckley (2019) to solidify the exact mathematical mapping between active inference and PID control before we add delayed observations and time-varying parameters.
