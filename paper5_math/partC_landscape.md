# Day 13: Formal Derivation Part C - The Free-Energy Landscape

## 1. The Landscape

The free-energy $F(\tilde{x})$ is a function of the state $\tilde{x}$. For a biological system, the landscape represents the "surprise" of different postures.
A healthy system has a single global minimum corresponding to the upright posture ($\theta = 0$). The precision parameters $\Pi$ shape the "steepness" of the basin of attraction around this minimum.

## 2. Bifurcation and Precision Collapse

From Part B, we showed that the adolescent growth spurt causes a transient precision collapse on velocity ($\Pi_{x'} \downarrow$).
In the FEP framework, this fundamentally alters the topology of the free-energy landscape.

The overall free energy $F$ is a sum of precision-weighted prediction errors:
$$ F = \Pi_{pos} (x_{obs} - x_{prior})^2 + \Pi_{vel} (v_{obs} - v_{prior})^2 + \Pi_{grav} (T_{grav}(\theta))^2 $$

Where $T_{grav}(\theta)$ is the gravitational torque, which acts to pull the system away from the upright ($\theta=0$) equilibrium point. The "prior" $x_{prior}=0$ and $v_{prior}=0$ are the expectations of the generative model.

When $\Pi_{vel}$ (derivative gain) drops, the system's ability to penalise deviations from zero velocity decreases. The system becomes "under-damped" and oscillates around the upright position.

Because the gravitational torque is nonlinear ($T_{grav}(\theta) = mgl\sin(\theta)$), these larger oscillations push the system into nonlinear regimes where the restorative prior ($\Pi_{pos}$) is insufficient to overcome gravity.

Mathematically, the drop in $\Pi_{vel}$ triggers a pitchfork bifurcation. The original global minimum at $\theta=0$ becomes a saddle point, and two new local minima emerge at $\theta = \pm \theta_{curve}$.

## 3. The "Dark Room" Variant

The system is now trapped in a local free-energy minimum. It cannot easily return to $\theta=0$ because doing so would require traversing a higher free-energy state (it would require generating high-precision motor commands, which the system currently cannot do because its predictive model is degraded).

This is a variant of the "dark room" problem in active inference. A system minimises free energy by predicting an asymmetric, curved posture and then using action to maintain it. It avoids the "surprise" of the unstable upright posture by settling into a stable, but deformed, local minimum. The scoliosis curve *is* the local minimum.
