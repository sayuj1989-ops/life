import os
import numpy as np
import matplotlib.pyplot as plt

def run_tensegrity_model():
    """
    Toy Model F: 2D Spinal Tensegrity Model

    Objective: Demonstrate that a tensegrity structure with rigid struts
    and an active tension network (representing proprioceptive control)
    can stabilize against gravitational loads (representing Biological Countercurvature).
    """
    print("Running Toy Model: 2D Spinal Tensegrity...")

    # -----------------------------
    # 1. System Definition
    # -----------------------------
    n_nodes = 8
    n_struts = 4

    # Initial resting coordinates for nodes
    # Two columns of nodes, left and right, creating 4 segments (struts)
    x = np.array([0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0])
    y = np.array([0.0, 0.0, 1.5, 1.5, 3.0, 3.0, 4.5, 4.5])

    # Stack into a (N, 2) array
    coords = np.column_stack((x, y))
    v = np.zeros_like(coords)

    # Define struts (rigid elements, like vertebrae)
    struts = [(0, 1), (2, 3), (4, 5), (6, 7)]

    # Define cables (elastic elements, like muscles/ligaments)
    # Connecting nodes vertically and diagonally
    cables = [
        (0, 2), (1, 3), # level 1 verticals
        (2, 4), (3, 5), # level 2 verticals
        (4, 6), (5, 7), # level 3 verticals
        (0, 3), (1, 2), # level 1 diagonals
        (2, 5), (3, 4), # level 2 diagonals
        (4, 7), (5, 6)  # level 3 diagonals
    ]

    # Base nodes are fixed
    fixed_nodes = [0, 1]

    # Physical parameters
    k_cable = 50.0 # Cable stiffness
    k_strut = 1000.0 # Strut stiffness (penalty for length change)
    damping = 0.5  # System damping
    mass = 1.0
    dt = 0.01
    n_steps = 1000

    # Calculate initial resting lengths
    L0_struts = []
    for (i, j) in struts:
        L0_struts.append(np.linalg.norm(coords[i] - coords[j]))

    L0_cables = []
    for (i, j) in cables:
        # Pre-tension: resting length is slightly shorter than initial distance
        L0_cables.append(np.linalg.norm(coords[i] - coords[j]) * 0.8)

    # Apply gravity
    g = np.array([0.0, -9.81])

    # Run simulation
    trajectory = []
    for step in range(n_steps):
        force = np.zeros_like(coords)

        # Add gravity to non-fixed nodes
        for i in range(n_nodes):
            if i not in fixed_nodes:
                force[i] += g * mass

        # Strut forces (high stiffness springs to approximate rigidity)
        for idx, (i, j) in enumerate(struts):
            vec = coords[i] - coords[j]
            L = np.linalg.norm(vec)
            if L > 1e-6:
                dir = vec / L
                f_mag = k_strut * (L - L0_struts[idx])
                force[i] -= f_mag * dir
                force[j] += f_mag * dir

        # Cable forces
        for idx, (i, j) in enumerate(cables):
            vec = coords[i] - coords[j]
            L = np.linalg.norm(vec)
            if L > 1e-6:
                dir = vec / L
                # Cables only pull, they don't push
                if L > L0_cables[idx]:
                    f_mag = k_cable * (L - L0_cables[idx])
                    force[i] -= f_mag * dir
                    force[j] += f_mag * dir

        # Apply bounds to prevent numerical explosions
        force = np.clip(force, -1000, 1000)

        # Update velocities and positions
        for i in range(n_nodes):
            if i not in fixed_nodes:
                a = force[i] / mass
                v[i] = v[i] + a * dt
                v[i] = v[i] * (1.0 - damping * dt) # Damping
                coords[i] = coords[i] + v[i] * dt

        # Optional: Add small lateral perturbation halfway
        if step == 200:
            for i in range(n_nodes):
                if i not in fixed_nodes:
                    coords[i, 0] += 0.2

        trajectory.append(coords.copy())

    final_coords = coords

    # -----------------------------
    # 2. Plotting
    # -----------------------------
    os.makedirs('outputs/figures', exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 8))

    # Plot initial state (faded)
    init_coords = trajectory[0]
    for (i, j) in struts:
        ax.plot([init_coords[i, 0], init_coords[j, 0]], [init_coords[i, 1], init_coords[j, 1]], 'k-', alpha=0.3, lw=4)
    for (i, j) in cables:
        ax.plot([init_coords[i, 0], init_coords[j, 0]], [init_coords[i, 1], init_coords[j, 1]], 'b--', alpha=0.2, lw=1)

    # Plot final state
    for (i, j) in struts:
        ax.plot([final_coords[i, 0], final_coords[j, 0]], [final_coords[i, 1], final_coords[j, 1]], 'k-', lw=5, label='Rigid Strut (Vertebra)' if i==0 else "")
    for (i, j) in cables:
        ax.plot([final_coords[i, 0], final_coords[j, 0]], [final_coords[i, 1], final_coords[j, 1]], 'r-', lw=2, alpha=0.7, label='Active Tension (Muscle/Ligament)' if i==0 else "")

    ax.scatter(final_coords[:, 0], final_coords[:, 1], c='gray', s=100, zorder=5)

    # Formatting
    ax.set_aspect('equal')
    ax.set_title('2D Spinal Tensegrity Model\nBiological Countercurvature Stabilization')
    ax.set_xlabel('Lateral Displacement (m)')
    ax.set_ylabel('Vertical Position (m)')
    ax.grid(True, linestyle=':', alpha=0.6)

    # Custom legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left')

    out_path = 'outputs/figures/toy_model_tensegrity_spine.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    print(f"Figure saved to {out_path}")

if __name__ == "__main__":
    run_tensegrity_model()
