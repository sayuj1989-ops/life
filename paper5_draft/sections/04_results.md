# 4. Results: Simulations of Precision Collapse

To demonstrate the active inference derivation in practice, we implemented the FEP equivalent of the PID model developed in Paper 2 using a Python simulation of a single-segment inverted pendulum. This model explicitly incorporates the growth-dependent precision collapse dynamics derived in Section 3.

## 4.1 Replicating the Derivative Gain Gap via Precision Dynamics

The core finding of Paper 2 was that a rapid increase in the mechanical parameters of the spine (mass $m$ and length $L$) coupled with a sensory delay ($\tau$) leads to a transient degradation of the derivative gain ($K_d$), causing postural instability.

In our FEP simulation, the system does not have an explicit $K_d$ parameter. Instead, the agent maintains a generative model of the delayed state ($x, x'$) and updates the precision ($\Pi_{vel}$) of its velocity prediction errors based on the empirical variance of those errors over time.

Figure 1 illustrates the result of simulating two distinct growth regimes: a "slow growth" scenario ($v_{growth} = 1 \text{ cm/year}$) representative of pre-adolescent development, and a "fast growth" scenario ($v_{growth} = 20 \text{ cm/year}$) representative of the peak height velocity (PHV) during the adolescent growth spurt. The system maintains a constant proprioceptive delay of $\tau = 200 \text{ ms}$.

As shown in the right panel of Figure 1, during slow growth, the model's Bayesian updating is able to track the changing plant parameters. The variance of the velocity prediction error remains low, allowing the system to maintain a high precision ($\Pi_{vel}$). This high precision corresponds to a high effective derivative gain, and the postural angle (left panel) remains tightly controlled near the upright set-point ($\theta = 0$).

Conversely, during fast growth, the rate of change outstrips the model's learning rate. The generative model's velocity predictions become systematically biased. The variance of the prediction error increases rapidly, forcing the optimal Bayesian estimator to down-weight the precision ($\Pi_{vel}$). As the precision collapses, the system's ability to damp oscillations fails. The postural angle diverges from the set-point, exhibiting the characteristic micro-sway instability that marks the onset of the derivative gain gap.

This simulation confirms that the purely mechanical phenomenon described in Paper 2 can be entirely reproduced by the information-theoretic dynamics of precision updating within an active inference framework. The "gap" is an optimal, but ultimately pathological, cognitive response to a rapidly changing physical body.

## 4.2 The Emergence of Local Minima

When the precision on velocity ($\Pi_{vel}$) collapses during the fast-growth scenario, the free-energy landscape undergoes a pitchfork bifurcation (as described in Section 3.5). The system is no longer able to maintain the upright posture ($\theta = 0$) because it lacks the necessary precision to penalise deviations in velocity and damp the resulting oscillations.

As the oscillations grow, the system encounters the non-linear boundaries of the gravitational torque. It eventually settles into a new, stable equilibrium point ($\theta_{curve} \neq 0$). This asymmetric posture represents a local free-energy minimum—a "dark room" where the prediction errors on position and velocity are balanced against the constant gravitational load. The system minimises free energy by predicting an asymmetric state and maintaining it, rather than attempting the high-surprise (and currently unachievable) task of returning to true vertical.
