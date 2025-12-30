"""
Shared utilities for analysis pipeline.

Provides:
- Publication-quality plotting style
- Provenance tracking (git SHA, timestamp, parameters)
- Figure saving with metadata
- Standard color schemes
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import matplotlib.pyplot as plt
import numpy as np


def get_git_sha() -> Optional[str]:
    """
    Get current git commit SHA.

    Returns:
        Short git SHA (7 chars) or None if not in git repo
    """
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return sha
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def setup_plot_style():
    """
    Set up publication-quality matplotlib style.

    Standards:
    - Font: Arial or Helvetica, 10pt for labels, 8pt for ticks
    - Line width: 1.5pt
    - DPI: 300 minimum
    - Grid: Light gray, alpha 0.3
    - Colors: Colorblind-friendly palette
    """
    plt.style.use("seaborn-v0_8-darkgrid" if hasattr(plt.style, "library") else "default")

    plt.rcParams.update({
        # Font settings
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 11,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 9,

        # Figure settings
        "figure.dpi": 150,  # Screen display
        "savefig.dpi": 300,  # Publication quality
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,

        # Line and marker settings
        "lines.linewidth": 1.5,
        "lines.markersize": 6,
        "axes.linewidth": 1.0,

        # Grid
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,

        # Colors - colorblind-friendly
        "axes.prop_cycle": plt.cycler(
            color=["#0173B2", "#DE8F05", "#029E73", "#CC78BC", "#CA9161", "#949494"]
        ),
    })


def create_provenance_dict(
    script_name: str,
    parameters: Dict[str, Any],
    figure_spec: Optional[Dict[str, Any]] = None,
    random_seed: int = 1337,
) -> Dict[str, Any]:
    """
    Create provenance dictionary for figure metadata.

    Args:
        script_name: Name of analysis script generating the figure
        parameters: Dictionary of parameters used
        figure_spec: Optional figure specifications (DPI, dimensions, etc.)
        random_seed: Random seed for reproducibility

    Returns:
        Complete provenance dictionary
    """
    provenance = {
        "script": script_name,
        "timestamp": datetime.now().isoformat(),
        "git_sha": get_git_sha(),
        "random_seed": random_seed,
        "parameters": parameters,
    }

    if figure_spec:
        provenance["figure_spec"] = figure_spec

    return provenance


def save_figure_with_provenance(
    fig: plt.Figure,
    output_path: Path,
    provenance: Dict[str, Any],
    formats: tuple = ("png", "pdf"),
):
    """
    Save figure with provenance metadata.

    Args:
        fig: Matplotlib figure object
        output_path: Output path (without extension)
        provenance: Provenance dictionary
        formats: Tuple of formats to save ("png", "pdf", "svg")

    Saves:
        - Figure in requested formats
        - JSON sidecar with provenance metadata
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save figure in requested formats
    for fmt in formats:
        fig_path = output_path.with_suffix(f".{fmt}")
        fig.savefig(fig_path, dpi=300, bbox_inches="tight")
        print(f"✓ Saved: {fig_path}")

    # Save provenance JSON
    json_path = output_path.with_suffix(".json")
    with open(json_path, "w") as f:
        json.dump(provenance, f, indent=2)
    print(f"✓ Provenance: {json_path}")


def add_panel_label(ax: plt.Axes, label: str, x: float = -0.1, y: float = 1.05):
    """
    Add panel label (A, B, C, etc.) to subplot.

    Args:
        ax: Matplotlib axes object
        label: Panel label (e.g., "A", "B", "C")
        x: X position in axes coordinates
        y: Y position in axes coordinates
    """
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="top",
        ha="right",
    )


def format_parameter_name(param: str) -> str:
    r"""
    Format parameter name for display with proper Greek letters.

    Args:
        param: Parameter name (e.g., "chi_kappa", "chi_E")

    Returns:
        Formatted string with LaTeX (e.g., r"$\chi_\kappa$")
    """
    param_map = {
        "chi_kappa": r"$\chi_\kappa$",
        "chi_E": r"$\chi_E$",
        "chi_C": r"$\chi_C$",
        "chi_f": r"$\chi_f$",
        "delta_b": r"$\Delta B$",
        "gradI": r"$||\nabla I||$",
    }
    return param_map.get(param, param)


# Colorblind-friendly color palette
COLORS = {
    "blue": "#0173B2",
    "orange": "#DE8F05",
    "green": "#029E73",
    "purple": "#CC78BC",
    "brown": "#CA9161",
    "gray": "#949494",
    "red": "#D55E00",
    "yellow": "#ECE133",
}
