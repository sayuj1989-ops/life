# Phase 1, Day 3: Generalised coordinates of motion in FEP

## Core Concepts
In Friston's formulation of the free-energy principle (FEP) and active inference, the system represents dynamical states using **generalised coordinates of motion**. This means the generative model tracks not just the position of a state, but its velocity, acceleration, jerk, and higher-order derivatives.

A state vector $\tilde{x} = [x, x', x'', x''', \dots]$ encapsulates the state and its local trajectory in time.

## Generative Model in Generalised Coordinates
The generative model prescribes equations of motion for these coordinates:
- Sensory observations: $\tilde{y} = g(\tilde{x}, \tilde{v}) + \tilde{\omega}$
- Hidden states: $\tilde{x}' = f(\tilde{x}, \tilde{v}) + \tilde{\omega}_x$

Crucially, the prediction error $\varepsilon$ is also represented in generalised coordinates:
- $\tilde{\varepsilon}_y = \tilde{y} - g(\tilde{x}, \tilde{v})$
- $\tilde{\varepsilon}_x = \tilde{x}' - f(\tilde{x}, \tilde{v})$

## Precision Weighting and Derivative Control
Prediction errors are weighted by precision matrices ($\Pi = \Sigma^{-1}$), which encode the system's confidence in its predictions versus sensory evidence.
The precision matrix for sensory observations, $\Pi_y$, can be partitioned into blocks corresponding to each order of motion:
- $\Pi_{y,0}$: precision on position prediction errors
- $\Pi_{y,1}$: precision on velocity prediction errors
- $\Pi_{y,2}$: precision on acceleration prediction errors, etc.

**Link to PID Control:**
As shown by Baltieri & Buckley (2019), when the variational update equations (gradient descent on free energy) are applied to a linear generative model with these precision weightings:
- The update term driven by the position prediction error $\varepsilon_{y,0}$ weighted by $\Pi_{y,0}$ functions mathematically identically to the **Proportional gain ($K_p$)**.
- The update term driven by the velocity prediction error $\varepsilon_{y,1}$ weighted by $\Pi_{y,1}$ functions mathematically identically to the **Derivative gain ($K_d$)**.
- The Integral gain ($K_i$) relates to the prior precision on persistent hierarchical causes ($\tilde{v}$).

## Relevance to the Derivative Gain Gap
In our scoliosis model, the derivative gain gap represents a transient loss of stability due to a degradation in $K_d$.
Translated into the FEP framework:
1. Rapid skeletal growth changes the physical mapping between muscle activation and body velocity (plant dynamics).
2. The internal generative model $f(\tilde{x}, \tilde{v})$ becomes temporarily misspecified relative to the true body dynamics because the growth velocity exceeds the model's learning rate.
3. This misspecification leads to systematic errors in predicting velocity (generalised motion of order 1).
4. The system optimally responds to unreliable velocity predictions by reducing their precision weighting ($\Pi_{y,1} \downarrow$).
5. Since $\Pi_{y,1}$ maps directly to $K_d$, the effective derivative gain drops, causing the "Derivative Gain Gap" and paving the way for the system to settle into a local free-energy minimum (scoliosis).
