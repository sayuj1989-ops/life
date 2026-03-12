import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la


def simulate_lenke_classes():
    """
    Simulates AIS curve patterns (Lenke classifications) as eigenmodes
    of the coupled Cosserat rod system based on regional variations in bending stiffness B(s),
    proprioceptive gain K(s), and local energy deficit R(s).

    Instead of arbitrary sine waves, this solves the generalized eigenvalue problem:
    (B y'')'' = lambda Q y
    where B is the regional stiffness and Q is the regional instability drive
    (proportional to delay/damping or energy deficit).
    """
    print("Simulating Lenke Curve Classes (Eigenmodes) via Generalized Eigenvalue Problem...")

    N = 100
    s = np.linspace(0, 1, N)
    ds = s[1] - s[0]

    # Construct 2nd derivative matrix D2
    D2 = np.zeros((N, N))
    for i in range(1, N-1):
        D2[i, i-1] = 1
        D2[i, i] = -2
        D2[i, i+1] = 1
    D2 = D2 / (ds**2)

    # Restrict to interior nodes for pinned-pinned boundary conditions
    D2_int = D2[1:-1, 1:-1]

    def solve_buckling_mode(EI, tau_proprio, b_damping, num_modes=1):
        """
        Solves (EI y'')'' = lambda (tau/b) y
        Finds the fundamental buckling modes.
        """
        Q = tau_proprio / b_damping
        B_int = np.diag(EI[1:-1])
        L = D2_int @ B_int @ D2_int
        Q_int = np.diag(Q[1:-1])

        # L and Q are symmetric and positive definite (for physical parameters)
        evals, evecs = la.eigh(L, Q_int)

        modes = []
        for i in range(num_modes):
            y = np.zeros(N)
            y[1:-1] = evecs[:, i]
            # Normalize to max amplitude 1
            y = y / np.max(np.abs(y))
            # Ensure consistent sign (positive peak)
            if y[np.argmax(np.abs(y))] < 0:
                y = -y
            modes.append(y)
        return modes

    def smooth_step(x, x0, width=0.05):
        return 0.5 * (1 + np.tanh((x - x0) / width))

    def window(x, x_start, x_end, width=0.05):
        return smooth_step(x, x_start, width) - smooth_step(x, x_end, width)

    # Define base mechanical properties
    EI_base = np.ones(N)
    # The rib cage buttressing effect increases stiffness in the thoracic spine (approx s=0.2 to 0.6)
    EI_base += 1.0 * window(s, 0.2, 0.6)
    # The lower lumbar and sacral region is also naturally stiffer
    EI_base += 1.0 * window(s, 0.7, 1.0)

    tau_base = np.ones(N)
    b_base = np.ones(N)

    # --- Mode 1: Lenke Type 1 (Main Thoracic) ---
    # Due to increased delay/deficit primarily in the thoracic region
    tau_1 = np.copy(tau_base)
    tau_1 += 5.0 * window(s, 0.2, 0.6)
    modes_1 = solve_buckling_mode(EI_base, tau_1, b_base)

    # --- Mode 2: Lenke Type 5 (Thoracolumbar/Lumbar) ---
    # Due to increased delay/deficit primarily in the lumbar region
    tau_5 = np.copy(tau_base)
    tau_5 += 5.0 * window(s, 0.6, 1.0)
    modes_5 = solve_buckling_mode(EI_base, tau_5, b_base)

    # --- Mode 3: Lenke Type 3 (Double Major) ---
    # Deficits in both Thoracic and Lumbar regions, separated by a stiff/stable thoracolumbar junction
    EI_3 = np.copy(EI_base)
    EI_3 += 50.0 * window(s, 0.55, 0.65) # Extremely stiff junction to act as a node
    tau_3 = np.copy(tau_base)
    tau_3 += 10.0 * window(s, 0.2, 0.55)
    tau_3 += 10.0 * window(s, 0.65, 0.95)
    modes_3 = solve_buckling_mode(EI_3, tau_3, b_base, num_modes=2)
    # Mode 1 might be a C-curve depending on exact symmetry, Mode 2 is typically the S-curve.
    mode_3_curve = modes_3[1]

    # --- Mode 4: Lenke Type 4 (Triple Major) ---
    # Deficits in Cervical/Upper Thoracic, Main Thoracic, and Lumbar regions
    EI_4 = np.copy(EI_base)
    EI_4 += 20.0 * window(s, 0.3, 0.4)
    EI_4 += 20.0 * window(s, 0.6, 0.7)
    tau_4 = np.copy(tau_base)
    tau_4 += 10.0 * window(s, 0.1, 0.3)
    tau_4 += 10.0 * window(s, 0.4, 0.6)
    tau_4 += 10.0 * window(s, 0.7, 0.95)
    modes_4 = solve_buckling_mode(EI_4, tau_4, b_base, num_modes=3)
    mode_4_curve = modes_4[2] # Mode 3 is the triple curve


    # Plotting
    fig, axes = plt.subplots(1, 4, figsize=(16, 6), sharey=True)

    # Helper function to plot shaded deficit regions
    def shade_regions(ax, regions, color):
        for (start, end) in regions:
            ax.fill_betweenx(s, -1.2, 1.2, where=(s>start)&(s<end), color=color, alpha=0.1)

    # Lenke 1
    ax = axes[0]
    ax.plot(modes_1[0], s, color='royalblue', linewidth=3)
    ax.set_title("Lenke 1: Main Thoracic")
    shade_regions(ax, [(0.2, 0.6)], 'royalblue')

    # Lenke 5
    ax = axes[1]
    ax.plot(modes_5[0], s, color='darkorange', linewidth=3)
    ax.set_title("Lenke 5: Thoracolumbar/Lumbar")
    shade_regions(ax, [(0.6, 1.0)], 'darkorange')

    # Lenke 3
    ax = axes[2]
    ax.plot(mode_3_curve, s, color='forestgreen', linewidth=3)
    ax.set_title("Lenke 3: Double Major")
    shade_regions(ax, [(0.2, 0.55), (0.65, 0.95)], 'forestgreen')

    # Lenke 4
    ax = axes[3]
    ax.plot(mode_4_curve, s, color='firebrick', linewidth=3)
    ax.set_title("Lenke 4: Triple Major")
    shade_regions(ax, [(0.1, 0.3), (0.4, 0.6), (0.7, 0.95)], 'firebrick')

    # Common formatting
    for ax in axes:
        ax.invert_yaxis()
        ax.axvline(0, color='black', linestyle='-', linewidth=1)
        ax.set_xlim(-1.2, 1.2)
        ax.set_xlabel("Lateral Curvature Mode")

    axes[0].set_ylabel("Normalized Spine Length (Cranial -> Caudal)")
    plt.suptitle("Lenke Classifications as Coupled Cosserat Rod Eigenmodes\n(Shaded regions indicate localized metabolic energy deficits / increased neural delay)", fontsize=16)

    output_dir = "manuscript/figures"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "fig_lenke_classes.png")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated plot: {output_path}")

if __name__ == "__main__":
    simulate_lenke_classes()
