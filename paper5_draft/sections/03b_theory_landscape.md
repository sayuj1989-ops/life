# 3.5 The Free-Energy Landscape and Pathological Local Minima

Having established that rapid adolescent growth induces a transient collapse in velocity precision ($\Pi_{x'} \downarrow$), we now examine how this alters the topology of the brain's free-energy landscape.

## 3.5.1 The Healthy Landscape: A Global Minimum

In a healthy, mature postural control system, the free energy $F(\tilde{x})$ is a function of the state $\tilde{x}$. This landscape represents the "surprise" of different postures. The system possesses a single global minimum corresponding to the upright, symmetrical posture ($\theta = 0$).

The precision parameters $\Pi$ shape the "steepness" of the basin of attraction around this minimum. A high precision on velocity ($\Pi_{x'}$) means the system strongly penalises deviations from zero velocity, creating steep walls that aggressively damp perturbations and drive the system back to the bottom of the basin.

The overall free energy $F$ is a sum of precision-weighted prediction errors. For a simple 1D spinal segment subject to gravity, we can approximate this landscape as:

$$ F = \Pi_{pos} (x_{obs} - x_{prior})^2 + \Pi_{vel} (v_{obs} - v_{prior})^2 + \Pi_{grav} (T_{grav}(\theta))^2 $$

Where $T_{grav}(\theta)$ is the gravitational torque, which acts to pull the system away from the upright ($\theta=0$) equilibrium point. The "prior" $x_{prior}=0$ and $v_{prior}=0$ are the expectations of the generative model.

## 3.5.2 Precision Collapse and Bifurcation

When $\Pi_{vel}$ (equivalent to $K_d$) drops during the "gain gap" phase, the system's ability to penalise deviations from zero velocity decreases. The walls of the basin of attraction become shallow. The system becomes "under-damped" and begins to oscillate (sway) more widely around the upright position.

Crucially, because the gravitational torque is non-linear ($T_{grav}(\theta) = mgl\sin(\theta)$), these larger oscillations push the system into non-linear regimes where the restorative prior ($\Pi_{pos}$) is insufficient to overcome the destabilising force of gravity.

Mathematically, as $\Pi_{vel}$ falls below a critical threshold, the system undergoes a pitchfork bifurcation. The original global minimum at $\theta=0$ flattens out and becomes a saddle point (an unstable equilibrium). Simultaneously, two new local minima emerge at $\theta = \pm \theta_{curve}$.

## 3.5.3 The Scoliosis "Dark Room" Variant

Once the system falls into one of these new local minima, it is trapped.

In active inference, the "dark room" problem refers to the theoretical puzzle of why an agent doesn't simply minimise free energy by sitting in a dark, quiet room where sensory input is perfectly predictable (surprise is zero). The solution is that the agent has strong prior beliefs (evolutionary imperatives) that it should not be in a dark room (e.g., it expects to be warm, fed, and active).

The scoliotic curve represents a pathological variant of this problem. The system minimises free energy by predicting an asymmetric, curved posture and then using action (asymmetric muscle tone) to maintain it. It avoids the high "surprise" (and high free-energy) of the unstable upright posture by settling into a stable, but deformed, local minimum. The scoliosis curve *is* the local minimum.

To return to the upright posture ($\theta=0$), the system would have to traverse a higher free-energy state. It would require generating high-precision motor commands to force the spine back to vertical. But the system cannot generate these commands precisely because its generative model of velocity is currently degraded. The precision ($\Pi_{x'}$) is too low to drive the system out of the basin.

The spine thus settles into an asymmetric equilibrium, and the continuous asymmetric mechanical loading triggers Heuter-Volkmann bone remodelling, ossifying the dynamic free-energy minimum into a permanent structural deformity.
