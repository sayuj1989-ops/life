"""
2D Spinal Tensegrity Toy Model (TOY_06_Tensegrity)

Demonstrates the Biological Countercurvature theory by modeling the spine
as rigid struts stabilized by an active tension network.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def simulate_tensegrity(active_curvature_gain=0.0, save_path=None):
    np.random.seed(42)
    N_vert = 15
    N_nodes = 2 * N_vert

    pos = np.zeros((N_nodes, 2))
    for i in range(N_vert):
        # Initial slight kyphotic bend
        x_tilt = 0.02 * i**2
        pos[2*i] = [-0.5 + x_tilt, i * 1.0]
        pos[2*i+1] = [0.5 + x_tilt, i * 1.0]

    vel = np.zeros_like(pos)
    mass = 1.0
    dt = 0.005
    steps = 5000

    # rigid bodies (vertebrae)
    struts = []
    for i in range(N_vert):
        struts.append((2*i, 2*i+1))

    L_strut = 1.0
    k_strut = 50000.0

    # Tension network (muscles / ligaments)
    cables = []
    for i in range(N_vert - 1):
        # Left cable
        cables.append((2*i, 2*(i+1), 1.0, 500.0, 'L'))
        # Right cable
        cables.append((2*i+1, 2*(i+1)+1, 1.0, 500.0, 'R'))
        # Cross bracing
        cables.append((2*i, 2*(i+1)+1, np.sqrt(2), 200.0, 'D1'))
        cables.append((2*i+1, 2*(i+1), np.sqrt(2), 200.0, 'D2'))

    gravity = np.array([0.0, -9.81])

    for step in range(steps):
        force = np.zeros_like(pos)

        # Gravity
        for i in range(N_nodes):
            force[i] += gravity * mass

        # Base fixed
        force[0] += -10000.0 * (pos[0] - np.array([-0.5, 0.0])) - 100.0 * vel[0]
        force[1] += -10000.0 * (pos[1] - np.array([0.5, 0.0])) - 100.0 * vel[1]

        # Vertebral struts (very stiff springs)
        for (n1, n2) in struts:
            vec = pos[n2] - pos[n1]
            dist = np.linalg.norm(vec)
            if dist > 0:
                dir_vec = vec / dist
                f = k_strut * (dist - L_strut)
                force[n1] += f * dir_vec
                force[n2] -= f * dir_vec

        # Active tension cables
        for (n1, n2, L0, k, side) in cables:
            vec = pos[n2] - pos[n1]
            dist = np.linalg.norm(vec)
            if dist > 0:
                dir_vec = vec / dist
                active_L0 = L0

                # S-curve generation: upper spine pulls one way, lower spine pulls other
                # Map height to phase
                s_coord = pos[n1, 1] / float(N_vert - 1)

                # Active contraction: smaller resting length means it pulls harder
                if side == 'L':
                    # Contract left side in lumbar, extend in thoracic
                    contraction = active_curvature_gain * 0.15 * np.sin(2.0 * np.pi * s_coord)
                    active_L0 = L0 * (1.0 - contraction)
                elif side == 'R':
                    # Contract right side in thoracic, extend in lumbar
                    contraction = active_curvature_gain * 0.15 * np.sin(2.0 * np.pi * s_coord)
                    active_L0 = L0 * (1.0 + contraction)

                # Cables only pull, they don't push
                if dist > active_L0:
                    f = k * (dist - active_L0)
                    force[n1] += f * dir_vec
                    force[n2] -= f * dir_vec

        # Damping
        force -= 15.0 * vel

        # Bounded forces (prevent explosion)
        force = np.clip(force, -1000, 1000)

        # Integrate
        vel += (force / mass) * dt
        pos += vel * dt

    return pos, struts, cables

def run_experiment():
    print("Running 2D Spinal Tensegrity Toy Model...")

    # 1. Passive Collapse (Gravity wins)
    print("Simulating passive collapse...")
    pos_pass, struts, cables = simulate_tensegrity(active_curvature_gain=0.0)

    # 2. Active Countercurvature (Tensegrity S-shape)
    print("Simulating active counter-curvature...")
    pos_act, struts, cables = simulate_tensegrity(active_curvature_gain=1.0)

    # 3. Pathological (High gain / Scoliotic Buckling)
    print("Simulating pathological over-correction...")
    pos_path, struts, cables = simulate_tensegrity(active_curvature_gain=2.5)

    os.makedirs('outputs/figures', exist_ok=True)
    os.makedirs('figures/main', exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 8))

    titles = ['Passive Collapse (0g Info)', 'Healthy Countercurvature (1g Info)', 'Scoliotic Buckling (Excess Info)']
    positions = [pos_pass, pos_act, pos_path]
    colors = ['gray', 'blue', 'red']

    for ax, pos, title, c in zip(axes, positions, titles, colors):
        # Draw cables
        for (n1, n2, L0, k, side) in cables:
            ax.plot([pos[n1, 0], pos[n2, 0]], [pos[n1, 1], pos[n2, 1]], color='orange', alpha=0.3, linewidth=1)

        # Draw struts
        for (n1, n2) in struts:
            ax.plot([pos[n1, 0], pos[n2, 0]], [pos[n1, 1], pos[n2, 1]], color='black', linewidth=4)

        # Plot center line
        center_x = (pos[::2, 0] + pos[1::2, 0]) / 2.0
        center_y = (pos[::2, 1] + pos[1::2, 1]) / 2.0
        ax.plot(center_x, center_y, color=c, linestyle='--', linewidth=2, label='Spinal Axis')

        ax.set_title(title)
        ax.set_aspect('equal')
        ax.set_xlim(-6, 6)
        ax.set_ylim(-1, 15)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig('outputs/figures/toy_model_tensegrity.png', dpi=300)
    plt.savefig('figures/main/toy_model_tensegrity.png', dpi=300)
    print("Saved plots to outputs/figures/toy_model_tensegrity.png and figures/main/toy_model_tensegrity.png")

if __name__ == '__main__':
    run_experiment()
