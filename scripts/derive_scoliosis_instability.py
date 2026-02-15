
import numpy as np
import matplotlib.pyplot as plt
import os
from dataclasses import dataclass
from typing import List, Tuple

# Ensure outputs directory exists
os.makedirs("outputs/figures", exist_ok=True)

@dataclass
class SimulationResult:
    time: np.ndarray
    curvature: np.ndarray
    is_stable: bool
    growth_velocity: float
    delay: float
    gain: float

def simulate_growing_spine(
    gain_base: float,
    delay_base: float,
    growth_rate: float,
    t_max: float = 20.0,
    dt: float = 0.01
) -> SimulationResult:
    """
    Simulates the dynamics of spinal curvature under delayed feedback control
    during growth.

    Model:
    d/dt kappa(t) = - damping * kappa(t) - gain(t) * kappa(t - delay(t))

    Where:
    - Length L(t) = L0 + growth_rate * t
    - Delay tau(t) = delay_base * (L(t) / L0)  (Transport delay increases with length)
    - Gain K(t) = gain_base * (L(t) / L0)^2    (Mechanical moment arm increases with L^2)
    """

    t = np.arange(0, t_max, dt)
    n_steps = len(t)
    kappa = np.zeros(n_steps)

    # Initial perturbation
    kappa[0:int(1.0/dt)] = 0.1

    L0 = 0.4 # meters
    damping = 1.0

    for i in range(1, n_steps):
        current_time = t[i]

        # Growth dynamics
        L_t = L0 + growth_rate * current_time
        scaling_factor = L_t / L0

        current_delay = delay_base * scaling_factor
        current_gain = gain_base * (scaling_factor**2) # Moment arm effect

        # Find delayed index
        delayed_time = current_time - current_delay
        if delayed_time < 0:
            kappa_delayed = 0.1 # Initial condition
        else:
            delayed_idx = int(delayed_time / dt)
            kappa_delayed = kappa[delayed_idx]

        # Euler integration
        d_kappa = (-damping * kappa[i-1] - current_gain * kappa_delayed) * dt
        kappa[i] = kappa[i-1] + d_kappa

        # Check for blow-up
        if abs(kappa[i]) > 10.0:
            kappa[i:] = 10.0 * np.sign(kappa[i])
            return SimulationResult(t, kappa, False, growth_rate, delay_base, gain_base)

    # Check stability (amplitude at end vs beginning of free response)
    # We look at the last 20% of the signal
    tail_amplitude = np.max(np.abs(kappa[int(0.8*n_steps):]))
    is_stable = tail_amplitude < 0.2 # Threshold for stability

    return SimulationResult(t, kappa, is_stable, growth_rate, delay_base, gain_base)

def plot_stability_phase_diagram():
    """
    Generates a phase diagram of stability in the (Growth Rate, Delay) plane.
    """
    growth_rates = np.linspace(0.0, 0.1, 20) # m/s (very fast for biology, but illustrative)
    delays = np.linspace(0.01, 0.5, 20)      # seconds

    stability_map = np.zeros((len(delays), len(growth_rates)))

    gain_fixed = 5.0 # Fixed base gain

    print("Running stability analysis...")
    for i, d in enumerate(delays):
        for j, g_rate in enumerate(growth_rates):
            res = simulate_growing_spine(gain_fixed, d, g_rate)
            stability_map[i, j] = 1.0 if res.is_stable else 0.0

    plt.figure(figsize=(10, 8))
    plt.imshow(
        stability_map,
        extent=[growth_rates[0], growth_rates[-1], delays[0], delays[-1]],
        origin='lower',
        aspect='auto',
        cmap='RdBu'
    )
    plt.colorbar(label='Stability (1=Stable, 0=Unstable)')
    plt.xlabel(r'Growth Velocity $\dot{L}$ (m/s)')
    plt.ylabel(r'Neural Delay $\tau$ (s)')
    plt.title('Phase Diagram: Delay-Induced Instability in Growing Spine')

    # Overlay theoretical boundary: K * tau ~ constant?
    # Here effective gain K_eff increases with time due to growth.
    # Instability happens if K_eff * tau_eff > pi/2 at some point in the simulation window.

    plt.savefig('outputs/figures/scoliosis_instability_phase.png')
    print("Saved outputs/figures/scoliosis_instability_phase.png")

def demonstrate_twist_bend_coupling():
    """
    Simulates the symmetry breaking where planar buckling couples to torsion.
    Using a simplified 2x2 matrix model of the coupled modes.
    """

    # Mode vector: [u (lateral), phi (axial rotation)]
    # Dynamics: M d2x/dt2 + K x = 0
    # K matrix includes coupling term chi

    chi_values = np.linspace(0, 5, 50)
    eigenvalues = []

    K_bend = 10.0
    K_twist = 5.0

    for chi in chi_values:
        # Stiffness matrix with coupling
        # | K_bend      chi    |
        # | chi       K_twist  |
        K_matrix = np.array([
            [K_bend, chi],
            [chi, K_twist]
        ])

        # Solve eigenvalues (frequencies squared)
        evals = np.linalg.eigvals(K_matrix)
        eigenvalues.append(np.sort(evals))

    eigenvalues = np.array(eigenvalues)

    plt.figure(figsize=(10, 6))
    plt.plot(chi_values, eigenvalues[:, 0], label='Mode 1 (Coupled Twist-Bend)')
    plt.plot(chi_values, eigenvalues[:, 1], label='Mode 2 (Coupled Twist-Bend)')
    plt.axhline(0, color='k', linestyle='--', linewidth=0.5)
    plt.xlabel(r'Coupling Strength $\chi$ (Twist-Bend Interaction)')
    plt.ylabel(r'Eigenvalues $\lambda$ (Stiffness)')
    plt.title('Symmetry Breaking: Eigenvalue Splitting due to Twist-Bend Coupling')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Region where eigenvalue < 0 implies buckling instability
    # If coupling is strong enough, one mode can become unstable even if K_bend, K_twist > 0?
    # No, for positive definite matrix, off-diagonal must be small.
    # If chi^2 > K_bend * K_twist, determinant < 0 -> unstable saddle point.

    instability_threshold = np.sqrt(K_bend * K_twist)
    plt.axvline(instability_threshold, color='r', linestyle=':', label='Instability Threshold')
    plt.legend()

    plt.savefig('outputs/figures/twist_bend_coupling.png')
    print("Saved outputs/figures/twist_bend_coupling.png")

if __name__ == "__main__":
    plot_stability_phase_diagram()
    demonstrate_twist_bend_coupling()
