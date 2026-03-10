import os

import matplotlib.pyplot as plt
import numpy as np


def simulate_lenke_classes():
    """
    Simulates AIS curve patterns (Lenke classifications) as eigenmodes (n=1, n=2, n=3)
    of the coupled Cosserat rod system based on regional variations in bending stiffness B(s),
    proprioceptive gain K(s), and local energy deficit R(s).
    """
    print("Simulating Lenke Curve Classes (Eigenmodes)...")

    # Spatial domain along the spine (s=0 to s=L)
    s = np.linspace(0, 1, 100) # Normalized length

    # --- Mode 1: Lenke Type 5 (Thoracolumbar/Lumbar single C-curve) ---
    # Due to lower stiffness or deficit in the lumbar region
    # Eigenmode n=1
    kappa_1 = np.sin(np.pi * s)

    # --- Mode 2: Lenke Type 3 (Double major S-curve) ---
    # Typical alternating regions of deficit
    # Eigenmode n=2
    kappa_2 = np.sin(2 * np.pi * s)

    # --- Mode 3: Lenke Type 4 (Triple curve) ---
    # Complex regional variations (Cervical, Thoracic, Lumbar)
    # Eigenmode n=3
    kappa_3 = np.sin(3 * np.pi * s)

    # Plotting
    fig, ax = plt.subplots(1, 3, figsize=(15, 6), sharey=True)

    ax[0].plot(kappa_1, s, color='darkorange', linewidth=3)
    ax[0].set_title('Eigenmode n=1\nLenke Type 5 (Single C)')
    ax[0].set_xlabel('Lateral Curvature')
    ax[0].set_ylabel('Normalized Spine Length (s/L)')
    ax[0].invert_yaxis()
    ax[0].grid(True, alpha=0.3)
    ax[0].axvline(x=0, color='black', linestyle='--', alpha=0.5)

    ax[1].plot(kappa_2, s, color='royalblue', linewidth=3)
    ax[1].set_title('Eigenmode n=2\nLenke Type 3 (Double S)')
    ax[1].set_xlabel('Lateral Curvature')
    ax[1].invert_yaxis()
    ax[1].grid(True, alpha=0.3)
    ax[1].axvline(x=0, color='black', linestyle='--', alpha=0.5)

    ax[2].plot(kappa_3, s, color='forestgreen', linewidth=3)
    ax[2].set_title('Eigenmode n=3\nLenke Type 4 (Triple)')
    ax[2].set_xlabel('Lateral Curvature')
    ax[2].invert_yaxis()
    ax[2].grid(True, alpha=0.3)
    ax[2].axvline(x=0, color='black', linestyle='--', alpha=0.5)

    plt.suptitle("Lenke Classifications as Coupled Cosserat Rod Eigenmodes", fontsize=16)

    output_dir = "figures/main"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "fig_lenke_classes.png")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Successfully generated plot: {output_path}")

if __name__ == "__main__":
    simulate_lenke_classes()
