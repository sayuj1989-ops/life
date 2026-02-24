# Proprioceptive Latency and Spinal Instability: A Control Theory Perspective

## Overview
This report documents the findings from the "Delayed Feedback Control" simulation (`scripts/experiment_delayed_control.py`), which models the spine as an inverted pendulum stabilized by a time-delayed Proprioceptive-Derivative (PD) controller. This work introduces a new "Dynamical Instability" layer to the existing "Thermodynamic Buckling" framework.

## Key Findings

### 1. The "Latency Trap" (Hopf Bifurcation)
Simulation results confirm that for a fixed set of neural gains ($K_p=15, K_d=2$), there exists a **Critical Spinal Length ($L_{crit}$)** beyond which the system becomes unstable.

*   **Result:** $L_{crit} \approx 0.77$ meters.
*   **Mechanism:** As length $L$ increases, the neural round-trip delay $\tau = 2L/v_{nerve}$ increases. When the phase lag caused by this delay (plus inertial lag) exceeds 180 degrees at the crossover frequency, the feedback becomes positive, driving oscillation.
*   **Implication:** Rapid adolescent growth pushes the spine towards this critical length. If the nervous system cannot adaptively increase gains or reduce delays (biologically impossible), instability is inevitable without external stabilization.

### 2. The "Disorder Effect" (Noise-Induced Instability)
We simulated "Disordered Proprioception" by adding Gaussian noise to the control signal, representing the stochastic behavior of high-disorder proteins like PIEZO2.

*   **Result:** Even at stable lengths ($L=0.5$m), high noise levels ($\sigma > 1.0$) induce large-amplitude swaying that mimics the onset of instability.
*   **Implication:** Patients with "Disordered Proprioception" (e.g., PIEZO2 variants) effectively have a lower $L_{crit}$ because the noise consumes the stability margin (Phase Margin).

## Integration with Existing Theory
*   **Metabolic Buckling:** The "Energy Deficit" makes it metabolically expensive to maintain high gains ($K_p$). This control theory model shows that *low gains* lower the $L_{crit}$. Thus, Energy Deficit -> Low Gains -> Early Latency Instability.
*   **Thermodynamic Standing Wave:** The "standing wave" is actually a **Limit Cycle Oscillation** arising from the Hopf bifurcation.

## Figures
*   `outputs/control_theory/growth_instability.png`: Shows the explosion of oscillation amplitude at $L_{crit}$.
*   `outputs/control_theory/unstable_dynamics.png`: Phase portrait showing the limit cycle.

## Conclusion
Scoliosis can be mathematically defined as a **Hopf Bifurcation** in the spinal postural control loop, triggered when the **Growth Velocity** pushes the **Delay** beyond the **Phase Margin**.
