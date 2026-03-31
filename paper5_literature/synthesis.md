# Day 10: Synthesis - Mapping PID to FEP

This synthesis maps every element of the Paper 2 PID model onto the Free-Energy Principle (FEP) formalism.

| Paper 2 Concept (Engineering Control) | FEP Equivalent (Active Inference) |
| :--- | :--- |
| **Plant** | The biomechanical body (spine/trunk) evolving in continuous time. |
| **State ($x$)** | True hidden states of the world (e.g., joint angles, angular velocity). |
| **Sensor ($y$)** | Sensory observations (proprioception, vision, vestibular). |
| **Set-point ($r$)** | Top-down prior expectation (the "desired" upright posture). |
| **Error ($e = r - y$)** | Sensory prediction error ($\epsilon_y = \mu_y - y$). |
| **Proportional Gain ($K_p$)** | Precision on position prediction errors ($\Pi_{y, pos}$). Dictates the reliance on sensory state estimates relative to priors. |
| **Derivative Gain ($K_d$)** | Precision on velocity (generalised motion) prediction errors ($\Pi_{y, vel}$). Penalises rapid changes, providing damping. |
| **Integral Gain ($K_i$)** | Precision on slowly-varying hidden causes (e.g., persistent biases or gravitational torques). |
| **Delay ($\tau$)** | The temporal lag in sensory transmission. Requires the generative model to explicitly predict the *current* state given *delayed* observations. |
| **Action ($u$)** | Motor commands driving the plant to minimise prediction errors (active inference via reflex arcs). |
| **Derivative Gain Gap** | A pathological, transient collapse in the precision of velocity prediction errors ($\Pi_{y, vel} \downarrow$) due to model misspecification during rapid growth. |

## The Mathematical Gaps to Fill (Phase 3)
1.  **Formal Derivation:** We must explicitly show how the Euler-Lagrange equations for minimising variational free energy, given a linear Gaussian generative model with delayed observations, reduce to the delayed PID control equations. We will build on Baltieri & Buckley (2019), adding the delay term $\tau$.
2.  **Precision Dynamics:** We need a formal equation for how precision on velocity ($\Pi_{y, vel}$) changes as a function of the growth velocity ($v_{growth}$) and the model's learning rate. This is the mathematical derivation of the "gap".
3.  **Bifurcation Analysis:** We must show how this precision collapse alters the free-energy landscape, shifting the system from a single global minimum (upright) to multiple local minima (asymmetric/scoliotic postures).
