import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from experiment_utils import StandardExperimentParser, setup_experiment
from matplotlib.patches import Patch

def simulate_delayed_thermostatic(L: float, tau: float, duration: float = 20.0, dt: float = 0.01):
    """
    Simulates a 1D column with a delayed feedback loop regulating stiffness based on strain.

    Equations:
    The strain x(t) (or deviation from straight) is driven by a gravity-like force and resisted
    by an active stiffness K(t) which is updated based on past strain x(t-tau).

    This is an active PID-like model where the active restoring force F_active(t) = -K * x(t-tau).
    If the delay is too large, the system over-corrects, causing "hunting" (oscillatory instability).

    Returns True if stable, False if oscillatory/unstable.
    """
    n_steps = int(duration / dt)

    x = np.zeros(n_steps)
    v = np.zeros(n_steps) # velocity

    delay_steps = int(tau / dt)

    # Model parameters mapping to biology
    # Stiffness gain (proprioceptive loop strength) increases with length (demand)
    K_p = 10.0 * L
    K_d = 2.0 * L    # Derivative gain (damping)

    # Gravitational destabilization (scales as L^2 locally)
    G = 5.0 * L**2

    # Inertia
    M = L**3

    # Initial perturbation
    x[0] = 0.05
    v[0] = 0.0

    for i in range(1, n_steps):
        # Delayed state
        if i > delay_steps:
            past_x = x[i - delay_steps - 1]
            past_v = v[i - delay_steps - 1]
        else:
            past_x = x[0]
            past_v = v[0]

        # Forces
        F_gravity = G * x[i-1] # Destabilizing
        F_active = -K_p * past_x - K_d * past_v # Delayed active restoring force

        # Passive stiffness (basal tone)
        F_passive = -2.0 * x[i-1]

        # Total acceleration
        a = (F_gravity + F_active + F_passive) / M

        # Euler integration
        v[i] = v[i-1] + a * dt
        x[i] = x[i-1] + v[i] * dt

        # Break early if diverging to save time
        if abs(x[i]) > 10.0:
            return False

    # Check stability (e.g. max amplitude in last 20% of simulation)
    tail_start = int(0.8 * n_steps)
    tail_x = x[tail_start:]

    std_x = np.std(tail_x)
    mean_x = np.mean(tail_x)

    # If the standard deviation is large, it's hunting/oscillating
    # If mean is large, it's buckled
    is_stable = (std_x < 0.1) and (abs(mean_x) < 1.0)

    return is_stable

def generate_phase_diagram(fig_path: Path):
    """Maps the stable vs unstable regions across (tau, L) parameter space."""

    print("Generating phase diagram for delayed thermostatic column...")

    taus = np.linspace(0.0, 0.5, 40)
    Ls = np.linspace(0.2, 1.5, 40)

    stability_map = np.zeros((len(taus), len(Ls)))

    for i, tau in enumerate(taus):
        for j, L in enumerate(Ls):
            stable = simulate_delayed_thermostatic(L, tau)
            stability_map[i, j] = 1 if stable else 0

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 6))

    L_grid, T_grid = np.meshgrid(Ls, taus)

    c = ax.contourf(T_grid, L_grid, stability_map, levels=[-0.5, 0.5, 1.5], colors=['red', 'green'], alpha=0.5)

    # Custom legend
    legend_elements = [
        Patch(facecolor='green', edgecolor='k', alpha=0.5, label='Stable (Straight)'),
        Patch(facecolor='red', edgecolor='k', alpha=0.5, label='Unstable (Hunting/Buckling)')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.set_xlabel('Sensor Delay $\\tau$ (s)')
    ax.set_ylabel('Spinal Length $L$ (m)')
    ax.set_title('Toy Model: Information-Coupled Thermostatic Stability')

    out_file = fig_path / 'toy_model_delayed_thermostatic.png'
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    print(f"Plot saved to {out_file}")

def main():
    parser = StandardExperimentParser(
        description="Information-Coupled Thermostatic Column: Demonstrate oscillatory instability with delayed feedback."
    )
    args = parser.parse_args()
    out_dir = setup_experiment(args)

    fig_path = Path('outputs/figures')
    fig_path.mkdir(parents=True, exist_ok=True)

    generate_phase_diagram(fig_path)

if __name__ == "__main__":
    main()
