"""
Analysis pipeline for IEC Model figure generation.

This module provides reproducible scripts for generating all publication figures
with full provenance tracking (git SHA, timestamp, random seed, parameters).

Modules:
    utils: Shared plotting utilities, provenance tracking, figure validation
    03_iec_discriminators: Main 3-panel figure (IEC-1/2/3 mechanisms)
    04_sensitivity_analysis: Sobol/Morris sensitivity analysis
    05_phase_diagrams: Parameter space (ΔB, ||∇I||) maps
"""

__version__ = "0.2.0"
__author__ = "Dr. Sayuj Krishnan"

from .utils import (
    setup_plot_style,
    save_figure_with_provenance,
    get_git_sha,
    create_provenance_dict,
)

__all__ = [
    "setup_plot_style",
    "save_figure_with_provenance",
    "get_git_sha",
    "create_provenance_dict",
]
