from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from scripts._config import load_bcc_config
from scripts._eigenmodes import eigenmodes
from scripts._iec_beam import info_field, gamma_field, geff_field, intrinsic_curvature, solve_equilibrium_beam


def _require_matplotlib():
    try:
        import matplotlib.pyplot as plt  # type: ignore
        return plt
    except Exception as e:  # pragma: no cover
        raise RuntimeError("matplotlib is required. Install dependencies via `make deps`.") from e


def _load_csv(cfg, name: str) -> pd.DataFrame:
    path = cfg.io.results_dir / name
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run `make data` first.")
    return pd.read_csv(path)


def fig1_gene_to_geometry(cfg) -> None:
    plt = _require_matplotlib()
    s = np.linspace(0.0, cfg.simulation.length, cfg.simulation.n_nodes)
    I = info_field(s, cfg)
    gamma = gamma_field(I, cfg)
    geff = geff_field(gamma)
    k0 = intrinsic_curvature(s, I, cfg)

    fig, axs = plt.subplots(3, 1, figsize=(7, 7), sharex=True)
    axs[0].plot(s, I, lw=2)
    axs[0].set_ylabel("I(s)")
    axs[0].set_title("Fig 1: Gene→Geometry mapping (phenomenological)")
    axs[1].plot(s, geff, lw=2)
    axs[1].set_ylabel("g_eff(s)")
    axs[2].plot(s, k0, lw=2)
    axs[2].set_ylabel("kappa0(s)")
    axs[2].set_xlabel("arc-length s")
    for ax in axs:
        ax.grid(alpha=0.2)
    fig.tight_layout()

    out = cfg.io.figures_dir / f"fig_gene_to_geometry.{cfg.figures.fmt}"
    fig.savefig(out, dpi=cfg.figures.dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Wrote: {out}")


def fig2_mode_spectrum(cfg) -> None:
    plt = _require_matplotlib()
    s = np.linspace(0.0, cfg.simulation.length, cfg.simulation.n_nodes)

    B_passive = cfg.material.B0 * np.ones_like(s)
    em0 = eigenmodes(B_passive, s, n_modes=max(6, cfg.figures.n_modes_plot))

    I = info_field(s, cfg)
    B_iec = cfg.material.B0 * (1.0 + cfg.iec.chi_E * I)
    em1 = eigenmodes(B_iec, s, n_modes=max(6, cfg.figures.n_modes_plot))

    nm = cfg.figures.n_modes_plot
    fig, axs = plt.subplots(2, nm, figsize=(3.4 * nm, 6.0), sharex=True)
    for i in range(nm):
        axs[0, i].plot(s, em0["modes"][:, i], lw=2)
        axs[0, i].set_title(f"Passive mode {i+1}\nω={em0['omega'][i]:.3g}")
        axs[0, i].grid(alpha=0.2)

        axs[1, i].plot(s, em1["modes"][:, i], lw=2)
        axs[1, i].set_title(f"IEC mode {i+1}\nω={em1['omega'][i]:.3g}")
        axs[1, i].grid(alpha=0.2)

    axs[0, 0].set_ylabel("mode shape")
    axs[1, 0].set_ylabel("mode shape")
    for i in range(nm):
        axs[1, i].set_xlabel("s")
    fig.suptitle("Fig 2: Euler–Bernoulli eigenmodes (linear surrogate)")
    fig.tight_layout()

    out = cfg.io.figures_dir / f"fig_mode_spectrum.{cfg.figures.fmt}"
    fig.savefig(out, dpi=cfg.figures.dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Wrote: {out}")


def fig3_countercurvature(cfg) -> None:
    plt = _require_matplotlib()
    s = np.linspace(0.0, cfg.simulation.length, cfg.simulation.n_nodes)
    I = info_field(s, cfg)
    k0 = intrinsic_curvature(s, I, cfg)
    B = cfg.material.B0 * (1.0 + cfg.iec.chi_E * I)
    q = cfg.material.rhoA * cfg.simulation.gravity * np.ones_like(s)

    passive = solve_equilibrium_beam(s, q=q, B=B, kappa0=np.zeros_like(k0))
    info = solve_equilibrium_beam(s, q=q, B=B, kappa0=k0)

    fig, ax = plt.subplots(1, 1, figsize=(7, 4))
    ax.plot(s, passive["y"], label="passive (kappa0=0)", lw=2, color="gray")
    ax.plot(s, info["y"], label="IEC (kappa0~dI/ds)", lw=2, color="C0")
    ax.axhline(0, color="k", lw=0.5, alpha=0.3)
    ax.set_xlabel("s")
    ax.set_ylabel("deflection y(s)")
    ax.set_title("Fig 3: Passive sag vs IEC-stabilized countercurvature (surrogate)")
    ax.grid(alpha=0.2)
    ax.legend()
    fig.tight_layout()

    out = cfg.io.figures_dir / f"fig_countercurvature_panelA.{cfg.figures.fmt}"
    fig.savefig(out, dpi=cfg.figures.dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Wrote: {out}")


def fig4_phase_diagram(cfg) -> None:
    plt = _require_matplotlib()
    df = _load_csv(cfg, "sweep_grid.csv")
    pivot = df.pivot(index="chi_kappa", columns="gravity", values="D_geo_hat")
    chi = pivot.index.to_numpy()
    g = pivot.columns.to_numpy()
    Z = pivot.to_numpy()

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    im = ax.imshow(
        Z,
        origin="lower",
        aspect="auto",
        extent=[g.min(), g.max(), chi.min(), chi.max()],
        cmap="viridis",
    )
    ax.set_xlabel("gravity g")
    ax.set_ylabel("chi_kappa")
    ax.set_title("Fig 4: Phase diagram proxy (D_geo_hat)")
    fig.colorbar(im, ax=ax, label="D_geo_hat")
    fig.tight_layout()

    out = cfg.io.figures_dir / f"fig_phase_diagram_scoliosis.{cfg.figures.fmt}"
    fig.savefig(out, dpi=cfg.figures.dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Wrote: {out}")


def fig5_mode_transition(cfg) -> None:
    plt = _require_matplotlib()
    df = _load_csv(cfg, "sweep_chi_kappa.csv").sort_values("chi_kappa")
    fig, ax = plt.subplots(1, 1, figsize=(7, 4))
    ax.plot(df["chi_kappa"], df["mode_score"], lw=2)
    ax.set_xlabel("chi_kappa")
    ax.set_ylabel("mode_score (0=C, 1=balanced S)")
    ax.set_title("Fig 5: Mode transition proxy (planar surrogate)")
    ax.grid(alpha=0.2)
    fig.tight_layout()

    out = cfg.io.figures_dir / f"fig_scoliosis_proxy.{cfg.figures.fmt}"
    fig.savefig(out, dpi=cfg.figures.dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Wrote: {out}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Regenerate all figures into figures/")
    ap.add_argument("--config", default="config/default.yaml", help="Path to YAML config")
    args = ap.parse_args()

    cfg = load_bcc_config(args.config)
    cfg.io.results_dir.mkdir(parents=True, exist_ok=True)
    cfg.io.figures_dir.mkdir(parents=True, exist_ok=True)

    fig1_gene_to_geometry(cfg)
    fig2_mode_spectrum(cfg)
    fig3_countercurvature(cfg)
    fig4_phase_diagram(cfg)
    fig5_mode_transition(cfg)


if __name__ == "__main__":
    main()


