import os
import glob
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from plot_style import apply_nature_style

def get_latest_sim_plot(pattern):
    """Find the latest modified plot matching the pattern in outputs/sim/"""
    files = glob.glob(pattern, recursive=True)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def assemble_figures():
    apply_nature_style()

    out_dir = Path("outputs/figures/assembled")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Files to assemble
    fig1_path = "outputs/figures/toy_model_thermostatic.png"
    fig2_path = "outputs/figures/cross_species_scaling.png"
    fig3_path = "outputs/optimization_failure/optimization_failure_phase_diagram.png"

    # The active curvature sweep output depends on the date directory
    fig4_path = get_latest_sim_plot("outputs/sim/*/plot_curvature_cobb.png")

    paths = [fig1_path, fig2_path, fig3_path, fig4_path]
    labels = ["a", "b", "c", "d"]
    titles = [
        "Figure 1: The Stiffness Deficit Bifurcation",
        "Figure 2: Cross-Species Scaling (The Allometric Trap)",
        "Figure 3: Phase Diagram of Optimization Failure",
        "Figure 4: Cobb Angle vs Active Curvature"
    ]

    # 2x2 grid for the assembled figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for i, path in enumerate(paths):
        ax = axes[i]
        ax.axis('off')

        if path and os.path.exists(path):
            img = mpimg.imread(path)
            ax.imshow(img)
            # Add panel label (a, b, c, d)
            ax.text(0.05, 0.95, labels[i], transform=ax.transAxes,
                    fontsize=16, fontweight='bold', va='top', ha='left')
        else:
            ax.text(0.5, 0.5, f"Image not found:\n{path}",
                    ha='center', va='center', transform=ax.transAxes)

        ax.set_title(titles[i], pad=10, fontsize=14)

    plt.tight_layout()
    out_file = out_dir / "Figure_1_to_4.png"
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Successfully assembled figures to {out_file}")

if __name__ == "__main__":
    assemble_figures()
