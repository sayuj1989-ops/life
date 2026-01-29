import matplotlib
matplotlib.use("Agg")
"""Validate Euler–Bernoulli integration against an analytic sinusoid."""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

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
    kappa = -A * (k**2) * np.sin(k * s)
    st = State(s=s, kappa0=kappa, I=None)
    k_tgt = iec_kappa_target(st, p)
    _, y_num = integrate_shape_from_curvature(s, k_tgt)
    err = l2_error(y_true, y_num)

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.plot(s, y_true, label="analytic")
    plt.plot(s, y_num, "--", label="numerical")
    plt.legend()
    plt.xlabel("s (m)")
    plt.ylabel("y(s) (m)")
    plt.title(f"L2 error = {err:.2e}")
    plt.savefig("figures/validation_sinusoid.pdf", bbox_inches="tight")
    write_provenance(
        "figures/validation_sinusoid.provenance.json",
        1337,
        {"k": float(k), "A": float(A), "n": p.n},
    )
    print(f"L2_error={err:.3e}")


if __name__ == "__main__":
    main()
