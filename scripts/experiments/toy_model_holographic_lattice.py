import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from experiment_utils import StandardExperimentParser, setup_experiment
from matplotlib.collections import LineCollection

def run_holographic_lattice(chi_kappa: float, seed: int, N: int = 15):
    """
    Simulates a minimal 2D spring-mass lattice where resting lengths update
    based on local stress gradients, driven by high information-coupling (chi_kappa).

    Returns the final configuration (x, y coordinates).
    """
    np.random.seed(seed)

    # Grid of nodes (Nx2)
    # The spine is a column, standing up in Y
    y = np.linspace(0, 1, N)
    x1 = np.zeros(N) - 0.05 # Left side
    x2 = np.zeros(N) + 0.05 # Right side

    nodes = np.zeros((2 * N, 2))
    nodes[:N, 0] = x1
    nodes[:N, 1] = y
    nodes[N:, 0] = x2
    nodes[N:, 1] = y

    # Add random isotropic noise to initial resting lengths/positions
    # This acts as the "isotropic initial conditions"
    nodes += np.random.normal(0, 0.002, nodes.shape)

    # Edges
    edges = []

    # Vertical springs (left and right columns)
    for i in range(N-1):
        edges.append((i, i+1))        # Left
        edges.append((i+N, i+1+N))    # Right

    # Horizontal rungs
    for i in range(N):
        edges.append((i, i+N))

    # Diagonal braces (X-bracing)
    for i in range(N-1):
        edges.append((i, i+1+N))
        edges.append((i+N, i+1))

    num_edges = len(edges)

    # Initial resting lengths
    L0 = np.zeros(num_edges)
    for i, (n1, n2) in enumerate(edges):
        L0[i] = np.linalg.norm(nodes[n1] - nodes[n2])

    # Simulation settings
    dt = 0.02
    steps = 150
    k_spring = 200.0

    # Base fixed (node 0 and N are at y=0)
    base_indices = [0, N]

    # Gravity-like load (pushing down)
    F_ext = np.zeros_like(nodes)
    F_ext[:, 1] = -0.05

    for step in range(steps):
        # 1. Compute forces and stress
        F_int = np.zeros_like(nodes)
        stress = np.zeros(num_edges)

        for i, (n1, n2) in enumerate(edges):
            vec = nodes[n2] - nodes[n1] # From n1 to n2
            dist = np.linalg.norm(vec)

            if dist < 1e-5:
                continue

            dir_vec = vec / dist

            # Hooke's law: positive = tension (pulled apart), negative = compression
            force_mag = k_spring * (dist - L0[i])
            stress[i] = force_mag

            # n1 feels pull towards n2 if tension (+ force_mag)
            force_vec = force_mag * dir_vec

            F_int[n1] += force_vec
            F_int[n2] -= force_vec

        # Add a damping term to prevent explosive forces
        gamma = 10.0

        # 2. Update positions (overdamped: dx/dt = F)
        v = (F_int + F_ext) / gamma
        v[base_indices] = 0.0 # Fixed base

        # Clip velocities to avoid exploding NaNs
        v = np.clip(v, -1.0, 1.0)

        nodes += v * dt

        # 3. Information-Coupled Resting Length Update
        # "Holographic instability": coupling the reference metric L0 to the current stress
        # If compressed (stress < 0), it wants to grow (L0 increases) to resist compression
        # If tension (stress > 0), it wants to shrink (L0 decreases)
        dL0 = -chi_kappa * stress * dt

        # Clip dL0 to avoid massive jumps
        dL0 = np.clip(dL0, -0.1, 0.1)

        L0 += dL0

        L0 = np.clip(L0, 0.01, 2.0)

    # Return center line (average of left and right x coordinates)
    center_line_x = (nodes[:N, 0] + nodes[N:, 0]) / 2.0
    center_line_y = (nodes[:N, 1] + nodes[N:, 1]) / 2.0

    # Calculate curvature approximation (max deviation from straight)
    max_dev = np.max(np.abs(center_line_x))

    return nodes, edges, center_line_x, center_line_y, max_dev

def execute_lattice_ensemble(fig_path: Path, num_seeds: int = 100):
    """
    Runs the lattice simulation across 100 random noise seeds to verify
    the emergence of macroscopic curvature under high information-coupling.
    """
    print(f"Running holographic instability lattice ensemble with {num_seeds} seeds...")

    chi_low = 0.01  # Passive / Stable
    chi_high = 0.5  # Exploding gradient / Unstable

    deviations_low = []
    deviations_high = []

    # For plotting one representative example
    rep_nodes_low = None
    rep_edges_low = None
    rep_nodes_high = None
    rep_edges_high = None

    for seed in range(num_seeds):
        # Low coupling
        nodes_low, edges_low, cx_l, cy_l, dev_l = run_holographic_lattice(chi_low, seed)
        deviations_low.append(dev_l)

        # High coupling
        nodes_high, edges_high, cx_h, cy_h, dev_h = run_holographic_lattice(chi_high, seed)
        deviations_high.append(dev_h)

        if seed == 0:
            rep_nodes_low, rep_edges_low = nodes_low, edges_low
            rep_nodes_high, rep_edges_high = nodes_high, edges_high

    # Success Metric Check
    mean_dev_high = np.mean(deviations_high)
    mean_dev_low = np.mean(deviations_low)

    print(f"Mean max deviation (Low chi): {mean_dev_low:.4f}")
    print(f"Mean max deviation (High chi): {mean_dev_high:.4f}")

    if mean_dev_high > 5 * mean_dev_low:
        print("Success Metric Met: Macroscopic curvature reliably emerges under high coupling.")

    # --- Plotting ---
    fig, axs = plt.subplots(1, 3, figsize=(15, 6))

    # Plot representative low coupling lattice
    ax = axs[0]
    lines = [[rep_nodes_low[n1], rep_nodes_low[n2]] for n1, n2 in rep_edges_low]
    lc = LineCollection(lines, colors='blue', alpha=0.5, linewidths=1.5)
    ax.add_collection(lc)
    ax.scatter(rep_nodes_low[:, 0], rep_nodes_low[:, 1], c='black', s=10)
    ax.set_aspect('equal')
    ax.set_title(f'Low Coupling (Passive)\n$\\chi_\\kappa={chi_low}$')
    ax.set_xlim(-0.3, 0.3)
    ax.set_ylim(-0.1, 1.1)

    # Plot representative high coupling lattice
    ax = axs[1]
    lines = [[rep_nodes_high[n1], rep_nodes_high[n2]] for n1, n2 in rep_edges_high]
    lc = LineCollection(lines, colors='red', alpha=0.5, linewidths=1.5)
    ax.add_collection(lc)
    ax.scatter(rep_nodes_high[:, 0], rep_nodes_high[:, 1], c='black', s=10)
    ax.set_aspect('equal')
    ax.set_title(f'High Coupling (Active Buckling)\n$\\chi_\\kappa={chi_high}$')
    ax.set_xlim(-0.3, 0.3)
    ax.set_ylim(-0.1, 1.1)

    # Plot deviation histogram
    ax = axs[2]
    ax.hist(deviations_low, bins=15, alpha=0.7, label=f'Low $\\chi_\\kappa$', color='blue')
    ax.hist(deviations_high, bins=15, alpha=0.7, label=f'High $\\chi_\\kappa$', color='red')
    ax.set_xlabel('Max Lateral Deviation (Macroscopic Curvature)')
    ax.set_ylabel('Frequency')
    ax.set_title('Deviation Distribution (100 Seeds)')
    ax.legend()

    plt.tight_layout()
    out_file = fig_path / 'toy_model_holographic_lattice.png'
    plt.savefig(out_file, dpi=300)
    print(f"Plot saved to {out_file}")

def main():
    parser = StandardExperimentParser(
        description="Holographic Instability Lattice: Verify Exploding Gradient region."
    )
    args = parser.parse_args()
    out_dir = setup_experiment(args)

    fig_path = Path('outputs/figures')
    fig_path.mkdir(parents=True, exist_ok=True)

    execute_lattice_ensemble(fig_path, num_seeds=100)

if __name__ == "__main__":
    main()
