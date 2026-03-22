#!/usr/bin/env python3
"""
Toy Model: Spinal Tensegrity under Gravity
-------------------------------------------
This script models the spine as a simplified tensegrity structure (2D) to
demonstrate an innovative "out-of-the-box" perspective for the
Biological Countercurvature theory.

Instead of a continuous Cosserat rod, the spine is modeled as rigid struts
(vertebrae) connected by a continuous tension network (ligaments, muscles,
and the hypothesized information-elasticity coupling \\chi_\\kappa).

We simulate the structure under a vertical gravitational load.
- Low \\chi_\\kappa (Passive): The tensional network is weak; the structure buckles or collapses.
- High \\chi_\\kappa (Active): The tensional network actively pre-stresses the struts, maintaining a stable upright (or defined S-curve) shape against gravity.
"""

import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("outputs/figures", exist_ok=True)

def simulate_tensegrity(chi_kappa, gravity=9.81, n_struts=5, dt=0.01, steps=1000):
    # Simplified 2D simulation:
    # Nodes: [x, y] coordinates
    # We have n_struts, so n_nodes = 2 * n_struts
    n_nodes = 2 * n_struts

    # Initial vertical zigzag configuration
    pos = np.zeros((n_nodes, 2))
    width = 0.5
    height_per_strut = 1.0

    for i in range(n_struts):
        base_y = i * height_per_strut
        if i % 2 == 0:
            pos[2*i] = [-width/2, base_y]
            pos[2*i+1] = [width/2, base_y + height_per_strut]
        else:
            pos[2*i] = [width/2, base_y]
            pos[2*i+1] = [-width/2, base_y + height_per_strut]

    # Fix the bottom two nodes (sacrum)
    fixed_nodes = [0, 1] if n_struts > 1 else [0]

    # Define connectivity
    # Struts: connected nodes that maintain fixed distance (high compressive stiffness)
    struts = [(2*i, 2*i+1) for i in range(n_struts)]

    # Cables: connected nodes that only provide tension (representing muscles/ligaments/chi_kappa)
    # Connect adjacent struts
    cables = []
    for i in range(n_struts - 1):
        cables.append((2*i+1, 2*(i+1)))
        cables.append((2*i, 2*(i+1)+1))
        # Vertical stabilizing cables
        cables.append((2*i, 2*(i+1)))
        cables.append((2*i+1, 2*(i+1)+1))

    # Rest lengths
    def dist(p1, p2):
        return np.linalg.norm(p1 - p2)

    L0_struts = [dist(pos[u], pos[v]) for u, v in struts]
    L0_cables = [dist(pos[u], pos[v]) * 0.9 for u, v in cables] # Pre-tension: rest length is shorter

    # Physical parameters
    k_strut = 1e5
    # The active tension coupling chi_kappa acts as a gain on the cable stiffness/pre-stress
    k_cable = 50.0 + chi_kappa * 150.0
    mass = 1.0
    damping = 5.0

    vel = np.zeros_like(pos)

    for step in range(steps):
        force = np.zeros_like(pos)

        # Gravity
        force[:, 1] -= mass * gravity

        # Strut forces (compression resistance)
        for i, (u, v) in enumerate(struts):
            d = pos[u] - pos[v]
            l = np.linalg.norm(d)
            if l > 0:
                f = k_strut * (L0_struts[i] - l) * (d / l)
                force[u] += f
                force[v] -= f

        # Cable forces (tension only)
        for i, (u, v) in enumerate(cables):
            d = pos[u] - pos[v]
            l = np.linalg.norm(d)
            if l > L0_cables[i]: # Only pull, never push
                f = k_cable * (L0_cables[i] - l) * (d / l)
                force[u] += f
                force[v] -= f

        # Damping
        force -= damping * vel

        # Limit force to avoid explosions
        force = np.clip(force, -1000, 1000)

        # Update
        acc = force / mass
        vel += acc * dt
        pos += vel * dt

        # Boundary conditions
        for n in fixed_nodes:
            pos[n] = pos[n] - vel[n]*dt # Undo movement
            vel[n] = 0.0

    return pos, struts, cables

def plot_tensegrity(pos_passive, pos_active, struts, cables):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    def draw_struct(ax, pos, title):
        ax.set_title(title, fontsize=14)
        ax.set_aspect('equal')
        # Draw cables
        for u, v in cables:
            ax.plot([pos[u,0], pos[v,0]], [pos[u,1], pos[v,1]], 'b--', alpha=0.5, linewidth=1)
        # Draw struts
        for u, v in struts:
            ax.plot([pos[u,0], pos[v,0]], [pos[u,1], pos[v,1]], 'k-', linewidth=4)
        # Draw nodes
        ax.scatter(pos[:,0], pos[:,1], c='red', s=50, zorder=5)
        ax.grid(True, linestyle=':', alpha=0.6)

    draw_struct(ax1, pos_passive, r"Passive (Low $\chi_\kappa$): Buckling")
    draw_struct(ax2, pos_active, r"Active (High $\chi_\kappa$): Tensegrity Stabilization")

    # Find max bounds to keep axes consistent
    all_pos = np.vstack([pos_passive, pos_active])
    pad = 0.5
    min_x, max_x = np.min(all_pos[:,0]) - pad, np.max(all_pos[:,0]) + pad
    min_y, max_y = np.min(all_pos[:,1]) - pad, np.max(all_pos[:,1]) + pad

    ax1.set_xlim(min_x, max_x)
    ax1.set_ylim(min_y, max_y)
    ax2.set_xlim(min_x, max_x)
    ax2.set_ylim(min_y, max_y)

    plt.suptitle("Spinal Tensegrity: Active Tensional Network Counteracting Gravity", fontsize=16, y=1.02)
    plt.tight_layout()

    out_path = "outputs/figures/toy_model_tensegrity.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {out_path}")

if __name__ == "__main__":
    print("Running Spinal Tensegrity Toy Model...")

    # Run passive case (low chi_kappa)
    pos_passive, struts, cables = simulate_tensegrity(chi_kappa=0.1, gravity=20.0, steps=2000)

    # Run active case (high chi_kappa)
    pos_active, _, _ = simulate_tensegrity(chi_kappa=10.0, gravity=20.0, steps=2000)

    # Plot results
    plot_tensegrity(pos_passive, pos_active, struts, cables)
