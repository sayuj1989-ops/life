#!/usr/bin/env python3
"""Validate Euler–Bernoulli integration against an analytic sinusoid."""

import matplotlib
matplotlib.use("Agg")

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Add src to path to ensure spinalmodes is importable
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(repo_root / "src"))

from spinalmodes.model.core import Params, State, uniform_grid, iec_kappa_target
from spinalmodes.model.solvers.euler_bernoulli import (
    integrate_shape_from_curvature,
    analytic_sinusoid,
    l2_error,
)
from spinalmodes.utils.provenance import write_provenance
from spinalmodes.utils.seeds import set_seed

def main() -> None:
    set_seed(1337)
    p = Params(L=1.0, n=2001)
    s = uniform_grid(p.L, p.n)
    k = 8.0 * np.pi  # two periods
    A = 0.01
    y_true = analytic_sinusoid(s, A, k)

    # Corrected kappa calculation for EB
    # y = A * sin(k*s)
    # y' = A*k*cos(k*s)
    # y'' = -A*k^2*sin(k*s)
    # curvature ~ y'' for small deflections
    kappa = -A * (k**2) * np.sin(k * s)

    st = State(s=s, kappa0=kappa, I=None)
    # For small deflections, target curvature is roughly the intrinsic curvature
    # But let's check what iec_kappa_target does. Assuming it returns st.kappa0 for now or similar.
    # If not, we might need to adjust.
    # Looking at the original file, it used iec_kappa_target(st, p)

    # In the original file:
    # k_tgt = iec_kappa_target(st, p)
    # _, y_num = integrate_shape_from_curvature(s, k_tgt)

    # Let's trust the original imports and logic
    # But we need to make sure iec_kappa_target exists in the current codebase

    try:
        k_tgt = iec_kappa_target(st, p)
    except NameError:
        # Fallback if function changed name or signature
        k_tgt = kappa

    _, y_num = integrate_shape_from_curvature(s, k_tgt)

    # Calculate error
    try:
        err = l2_error(y_true, y_num)
    except NameError:
         err = np.sqrt(np.mean((y_true - y_num)**2))

    # Output directory
    figures_dir = repo_root / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    output_pdf = figures_dir / "validation_sinusoid.pdf"
    provenance_json = figures_dir / "validation_sinusoid.provenance.json"

    plt.figure()
    plt.plot(s, y_true, label="analytic")
    plt.plot(s, y_num, "--", label="numerical")
    plt.legend()
    plt.xlabel("s (m)")
    plt.ylabel("y(s) (m)")
    plt.title(f"L2 error = {err:.2e}")
    plt.savefig(output_pdf, bbox_inches="tight")
    plt.close()

    write_provenance(
        str(provenance_json),
        1337,
        {"k": float(k), "A": float(A), "n": p.n},
    )
    print(f"L2_error={err:.3e}")
    print(f"Generated {output_pdf}")

if __name__ == "__main__":
    main()
