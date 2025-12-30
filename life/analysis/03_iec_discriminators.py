#!/usr/bin/env python3
"""
Generate IEC Discriminators 3-Panel Figure.

This is the main publication figure demonstrating all three IEC mechanisms:
- Panel A: IEC-1 (Target Curvature Bias) - Node drift vs χ_κ
- Panel B: IEC-2 (Constitutive Bias) - Amplitude vs χ_E
- Panel C: IEC-3 (Active Moment) - Helical threshold vs ||∇I||

Output:
    - outputs/figs/fig_iec_discriminators.png (300 DPI)
    - outputs/figs/fig_iec_discriminators.pdf (vector)
    - outputs/figs/fig_iec_discriminators.json (provenance)

Usage:
    python analysis/03_iec_discriminators.py [--output-dir DIR] [--seed SEED]
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parents[1]))

import argparse
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

from model.core import IECParameters
from model.solvers.bvp_scipy import BVPSolver
from model.couplings import compute_helical_threshold
from analysis.utils import (
    setup_plot_style,
    save_figure_with_provenance,
    create_provenance_dict,
    add_panel_label,
    COLORS,
)


def generate_panel_a_iec1(ax: plt.Axes, seed: int = 1337) -> dict:
    """
    Panel A: IEC-1 node drift without wavelength change.

    Shows that χ_κ shifts node positions while preserving wavelength.

    Args:
        ax: Matplotlib axes for plotting
        seed: Random seed for reproducibility

    Returns:
        Dictionary with data for provenance
    """
    np.random.seed(seed)

    # Parameter sweep for chi_kappa
    chi_kappa_range = np.linspace(0, 0.06, 13)
    node_drifts = []
    wavelengths = []

    print("\nPanel A: IEC-1 Node Drift")
    print("=" * 50)

    for i, chi_k in enumerate(chi_kappa_range):
        params = IECParameters(
            chi_kappa=chi_k,
            I_mode="linear",  # Linear gradient more numerically stable than step
            I_gradient=1.0,   # Strong gradient to show node drift
            n_nodes=150,
            random_seed=seed,
        )

        solver = BVPSolver(params)
        state = solver.solve()
        metrics = state.compute_metrics()

        node_drifts.append(metrics["node_drift_mm"])
        wavelengths.append(metrics["wavelength_mm"])

        if i % 3 == 0:
            print(f"  χ_κ = {chi_k:.3f}: drift = {metrics['node_drift_mm']:.2f} mm, "
                  f"λ = {metrics['wavelength_mm']:.1f} mm")

    # Plot node drift
    ax.plot(
        chi_kappa_range * 1000,
        node_drifts,
        "o-",
        color=COLORS["blue"],
        label="Node drift",
        linewidth=2,
        markersize=6,
    )

    # Plot wavelength (should be nearly constant)
    ax_twin = ax.twinx()
    mean_wavelength = np.mean([w for w in wavelengths if w > 0])
    ax_twin.axhline(
        mean_wavelength,
        ls="--",
        color=COLORS["gray"],
        alpha=0.5,
        label=f"Wavelength: {mean_wavelength:.1f} mm",
    )
    ax_twin.set_ylabel("Wavelength (mm)", color=COLORS["gray"])
    ax_twin.tick_params(axis="y", labelcolor=COLORS["gray"])

    # Formatting
    ax.set_xlabel(r"$\chi_\kappa$ (mm)")
    ax.set_ylabel("Node drift (mm)", color=COLORS["blue"])
    ax.tick_params(axis="y", labelcolor=COLORS["blue"])
    ax.set_title("IEC-1: Target Curvature Bias", fontweight="bold")
    ax.grid(True, alpha=0.3)

    # Legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_twin.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left", framealpha=0.9)

    add_panel_label(ax, "A")

    print(f"✓ Panel A complete: {len(chi_kappa_range)} points")

    return {
        "chi_kappa_range": chi_kappa_range.tolist(),
        "node_drifts_mm": node_drifts,
        "wavelengths_mm": wavelengths,
        "mean_wavelength_mm": float(mean_wavelength),
    }


def generate_panel_b_iec2(ax: plt.Axes, seed: int = 1337) -> dict:
    """
    Panel B: IEC-2 amplitude modulation at fixed load.

    Shows that χ_E modulates deformation amplitude while preserving
    load-response proportionality.

    Args:
        ax: Matplotlib axes for plotting
        seed: Random seed

    Returns:
        Dictionary with data for provenance
    """
    np.random.seed(seed)

    # Parameter sweep for chi_E
    chi_E_range = np.linspace(-0.3, 0.3, 13)
    amplitudes = []

    print("\nPanel B: IEC-2 Amplitude Modulation")
    print("=" * 50)

    for i, chi_E in enumerate(chi_E_range):
        params = IECParameters(
            chi_E=chi_E,
            I_mode="constant",
            I_amplitude=1.0,
            n_nodes=100,
            random_seed=seed,
        )

        solver = BVPSolver(params)
        state = solver.solve()
        amplitude = state.compute_metrics()["amplitude_deg"]
        amplitudes.append(amplitude)

        if i % 3 == 0:
            print(f"  χ_E = {chi_E:.2f}: amplitude = {amplitude:.2f}°")

    # Plot
    ax.plot(
        chi_E_range,
        amplitudes,
        "s-",
        color=COLORS["orange"],
        linewidth=2,
        markersize=6,
    )

    # Highlight baseline (chi_E = 0)
    baseline_idx = np.argmin(np.abs(chi_E_range))
    ax.plot(
        chi_E_range[baseline_idx],
        amplitudes[baseline_idx],
        "o",
        color=COLORS["red"],
        markersize=10,
        label=f"Baseline: {amplitudes[baseline_idx]:.1f}°",
        zorder=5,
    )

    # Formatting
    ax.set_xlabel(r"$\chi_E$ (dimensionless)")
    ax.set_ylabel("Amplitude (degrees)")
    ax.set_title("IEC-2: Constitutive Bias", fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", framealpha=0.9)

    add_panel_label(ax, "B")

    print(f"✓ Panel B complete: {len(chi_E_range)} points")

    return {
        "chi_E_range": chi_E_range.tolist(),
        "amplitudes_deg": amplitudes,
        "baseline_amplitude_deg": float(amplitudes[baseline_idx]),
    }


def generate_panel_c_iec3(ax: plt.Axes, seed: int = 1337) -> dict:
    """
    Panel C: IEC-3 helical threshold reduction.

    Shows that active moments from information gradients lower the
    barrier for three-dimensional instability.

    Args:
        ax: Matplotlib axes for plotting
        seed: Random seed

    Returns:
        Dictionary with data for provenance
    """
    np.random.seed(seed)

    # Parameter sweep for ||∇I||
    gradI_range = np.linspace(0, 0.1, 21)
    delta_b = 0.1  # Fixed asymmetry parameter
    chi_f = 0.05  # Active coupling strength

    thresholds_active = []
    thresholds_baseline = []

    print("\nPanel C: IEC-3 Helical Threshold")
    print("=" * 50)

    for i, gradI in enumerate(gradI_range):
        # With active coupling
        threshold_active = compute_helical_threshold(
            delta_b=delta_b, grad_I_norm=gradI, chi_f=chi_f
        )
        thresholds_active.append(threshold_active)

        # Baseline (no active coupling)
        threshold_baseline = compute_helical_threshold(
            delta_b=delta_b, grad_I_norm=gradI, chi_f=0.0
        )
        thresholds_baseline.append(threshold_baseline)

        if i % 5 == 0:
            print(f"  ||∇I|| = {gradI:.3f}: threshold = {threshold_active:.3f} "
                  f"(baseline: {threshold_baseline:.3f})")

    # Plot both curves
    ax.plot(
        gradI_range,
        thresholds_baseline,
        "--",
        color=COLORS["gray"],
        linewidth=2,
        label=r"Baseline ($\chi_f = 0$)",
        alpha=0.7,
    )

    ax.plot(
        gradI_range,
        thresholds_active,
        "^-",
        color=COLORS["green"],
        linewidth=2,
        markersize=6,
        label=r"Active ($\chi_f = 0.05$)",
    )

    # Highlight reduction at high gradient
    idx_high = -1
    reduction_pct = (
        (thresholds_baseline[idx_high] - thresholds_active[idx_high])
        / thresholds_baseline[idx_high]
        * 100
    )
    ax.annotate(
        f"{reduction_pct:.0f}% reduction",
        xy=(gradI_range[idx_high], thresholds_active[idx_high]),
        xytext=(gradI_range[idx_high] - 0.02, thresholds_active[idx_high] + 0.02),
        arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=1.5),
        fontsize=9,
        color=COLORS["green"],
    )

    # Formatting
    ax.set_xlabel(r"$||\nabla I||$ (dimensionless)")
    ax.set_ylabel("Helical threshold")
    ax.set_title("IEC-3: Active Moment", fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", framealpha=0.9)

    add_panel_label(ax, "C")

    print(f"✓ Panel C complete: {len(gradI_range)} points")

    return {
        "gradI_range": gradI_range.tolist(),
        "thresholds_active": thresholds_active,
        "thresholds_baseline": thresholds_baseline,
        "delta_b": delta_b,
        "chi_f": chi_f,
        "reduction_pct_at_max_gradI": float(reduction_pct),
    }


def main(output_dir: Path = Path("outputs/figs"), seed: int = 1337):
    """
    Generate complete IEC discriminators figure.

    Args:
        output_dir: Output directory for figures
        seed: Random seed for reproducibility
    """
    print("\n" + "=" * 60)
    print("IEC DISCRIMINATORS FIGURE GENERATION")
    print("=" * 60)
    print(f"Output: {output_dir}")
    print(f"Seed: {seed}")

    # Set up plotting style
    setup_plot_style()

    # Create figure with 3 panels
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Generate each panel
    data_a = generate_panel_a_iec1(axes[0], seed=seed)
    data_b = generate_panel_b_iec2(axes[1], seed=seed)
    data_c = generate_panel_c_iec3(axes[2], seed=seed)

    # Adjust layout
    plt.tight_layout()

    # Create provenance
    provenance = create_provenance_dict(
        script_name="analysis/03_iec_discriminators.py",
        parameters={
            "panel_a": data_a,
            "panel_b": data_b,
            "panel_c": data_c,
        },
        figure_spec={
            "dpi": 300,
            "width_inches": 18,
            "height_inches": 5,
            "format": "PNG + PDF",
            "n_panels": 3,
        },
        random_seed=seed,
    )

    # Save figure
    output_path = output_dir / "fig_iec_discriminators"
    save_figure_with_provenance(fig, output_path, provenance, formats=("png", "pdf"))

    print("\n" + "=" * 60)
    print("✅ IEC DISCRIMINATORS FIGURE COMPLETE")
    print("=" * 60)
    print(f"Figure: {output_path}.png")
    print(f"Vector: {output_path}.pdf")
    print(f"Metadata: {output_path}.json")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate IEC Discriminators 3-Panel Figure"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/figs"),
        help="Output directory for figures (default: outputs/figs)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=1337,
        help="Random seed for reproducibility (default: 1337)",
    )

    args = parser.parse_args()
    main(args.output_dir, args.seed)
