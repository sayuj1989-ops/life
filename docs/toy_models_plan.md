# Toy Models Plan (2026-03-10)

This plan outlines simple, low-complexity models to de-risk the theoretical framework and provide intuitive explanations.

## 1. 1D Active Spring Chain (Information-Elasticity Coupling)
**Objective:** Demonstrate that a spatially varying "information field" $I(x)$ can generate emergent curvature/strain patterns without complex Cosserat mechanics.
- **Model:** A chain of springs $k_i$ connected by nodes $x_i$.
- **Mechanism:** Information $I(x_i)$ modulates local rest length $L_0(i)$ or stiffness $k_i$.
    - $L_0(i) = L_{base} \cdot (1 + \alpha I(x_i))$
- **Prediction:** A sinusoidal information field $I(x) = \sin(kx)$ produces a sinusoidal strain pattern.
- **Complexity:** Minimal (linear algebra).
- **Status:** Proposed.

## 2. Thermostat Controller (Exploding Gradient)
**Objective:** Demonstrate the "Exploding Gradient" instability in a simple scalar control loop.
- **Model:** A variable $x(t)$ (temperature/curvature) controlled by a heater $u(t)$ (muscle/growth) with delayed feedback.
    - $\dot{x} = -kx + u(t) + \eta(t)$ (system dynamics + noise)
    - $u(t) = -G \cdot (x(t-\tau) - x_{target})$ (delayed feedback)
- **Mechanism:** High gain $G$ combined with delay $\tau$ and noise $\eta$ leads to divergent oscillations.
- **Prediction:** Critical threshold $G_{crit}$ for instability.
- **Complexity:** ODE (1 variable).
- **Status:** Proposed.

## 3. Circadian Oscillator (Spinal Jetlag)
**Objective:** Demonstrate resonance and destructive interference in a driven oscillator.
- **Model:** Damped harmonic oscillator driven by two forces: Gravity (constant) and Clock (periodic).
    - $\ddot{x} + \gamma \dot{x} + \omega_0^2 x = F_{grav} + F_{clock} \cos(\omega_{clock} t + \phi)$
- **Mechanism:** Phase mismatch $\phi$ determines amplitude of oscillation.
- **Prediction:** Resonance peak at $\omega_{clock} \approx \omega_0$. Maximum amplitude at specific phase.
- **Complexity:** ODE (1 variable).
- **Status:** Proposed.
