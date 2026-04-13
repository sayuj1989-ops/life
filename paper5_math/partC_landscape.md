# Phase 3, Day 13: Formal Derivation Part C (Landscape)

## Free-Energy Landscape
The variational free energy $F$ defines a landscape over the generalized states $\tilde{x}$. The system seeks the minimum of this landscape.
Under normal conditions (high precision), the landscape has a single, deep global minimum at the upright posture ($x = 0$, assuming a symmetric prior).
$$ F(x) = \frac{1}{2} \Pi_y (y(x) - \mu_y)^2 + \frac{1}{2} \Pi_v (x - \mu_v)^2 $$

## The Effect of Precision Collapse on the Landscape
When the precision of velocity prediction errors ($\Pi_{y,1}$) collapses (as derived in Part B), the effective restoring force (equivalent to $K_d$) weakens.
Because the system is delayed ($\tau$), the state estimation must project forward in time: $\mu_x(t) \approx y(t-\tau) + \tau y'(t-\tau)$.
When $\Pi_{y,1} \downarrow$, the system effectively ignores $y'$, rendering the forward projection inaccurate. This inaccurate state estimation flattens the free-energy well around $x=0$.

## Bifurcation and Local Minima
As the precision drops below a critical threshold (the Bayesian equivalent of the stability boundary in Paper 2), the deep minimum at $x=0$ becomes a saddle point. The free-energy landscape undergoes a pitchfork bifurcation.
Two new local minima emerge at $x = \pm x_{scoliosis}$.
These minima represent states where the mechanical restoring forces (which are non-linear at larger angles) balance the degraded active inference controller. The system settles into one of these minima (determined by small initial asymmetries, handedness, or lateral loading) to minimize free energy in its new, degraded precision regime.

## Comparison with Paper 2
- **Paper 2 (Control Theory):** Analyzed the roots of the characteristic equation. Showed that when $K_d$ drops, complex conjugate roots cross into the right-half plane, causing oscillatory instability that settles into a structural limit cycle or new equilibrium point.
- **Paper 5 (Active Inference):** Analyzes the shape of the free energy functional $F$. Shows that when $\Pi_{y,1}$ drops, the curvature of $F$ at $x=0$ becomes negative (a maximum), creating a double-well potential where lateral curvature represents the new minimal surprise state.
