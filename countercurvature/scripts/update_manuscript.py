from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from scripts._config import load_bcc_config


def _fmt(x: float, nd: int = 3) -> str:
    return f"{x:.{nd}g}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Update manuscript placeholders with computed values + add reproducibility section.")
    ap.add_argument("--config", default="config/default.yaml", help="Path to YAML config")
    args = ap.parse_args()

    cfg = load_bcc_config(args.config)
    res_dir = cfg.io.results_dir

    micro = pd.read_csv(res_dir / "sweep_microgravity.csv").sort_values("gravity")
    grid = pd.read_csv(res_dir / "sweep_grid.csv")
    ksw = pd.read_csv(res_dir / "sweep_chi_kappa.csv").sort_values("chi_kappa")

    g_min = float(micro["gravity"].min())
    g_max = float(micro["gravity"].max())
    D_min = float(micro.loc[micro["gravity"].idxmin(), "D_geo_hat"])
    D_max = float(micro.loc[micro["gravity"].idxmax(), "D_geo_hat"])
    D_ratio = float(D_min / (D_max + 1e-12))

    E_min = float(micro.loc[micro["gravity"].idxmin(), "E_total"])
    E_max = float(micro.loc[micro["gravity"].idxmax(), "E_total"])
    E_drop_pct = float(100.0 * (1.0 - E_min / (E_max + 1e-12)))

    gd = grid.loc[grid["D_geo_hat"].idxmin()]
    idom = grid.loc[grid["D_geo_hat"].idxmax()]

    s_like = ksw[ksw["inflection_count"] >= 1.0]
    chi_s = float(s_like["chi_kappa"].iloc[0]) if len(s_like) else float("nan")

    rr_path = Path("RESEARCH_REPORT_BCC.md")
    text = rr_path.read_text()

    repl_block = (
        "Microgravity persistence:\n"
        f"- At g = {g_max}: Dhat_geo = {_fmt(D_max)}, E_total = {_fmt(E_max)}\n"
        f"- At g = {g_min}: Dhat_geo = {_fmt(D_min)}, E_total = {_fmt(E_min)}\n"
        f"- E_total reduction: {_fmt(E_drop_pct, 3)}% (g={g_max}→{g_min})\n"
        f"- Dhat_geo persistence ratio: {_fmt(D_ratio, 3)}\n"
        "\n"
        "Phase diagram regimes (example anchors):\n"
        f"- Low Dhat_geo point: chi_kappa={_fmt(float(gd['chi_kappa']))}, g={_fmt(float(gd['gravity']))}, Dhat_geo={_fmt(float(gd['D_geo_hat']))}\n"
        f"- High Dhat_geo point: chi_kappa={_fmt(float(idom['chi_kappa']))}, g={_fmt(float(idom['gravity']))}, Dhat_geo={_fmt(float(idom['D_geo_hat']))}\n"
        "\n"
        "Mode transition (baseline gravity):\n"
        f"- First S-like (>=1 inflection) chi_kappa: {_fmt(chi_s)}\n"
    )

    marker = "### Key numbers box (template)"
    if marker in text:
        before, after = text.split(marker, 1)
        new_after = after
        if "```" in new_after:
            first = new_after.find("```")
            second = new_after.find("```", first + 3)
            if second != -1:
                new_after = new_after[second + 3 :]
        text = before + marker + "\n\n" + repl_block + "\n" + new_after.lstrip()
    else:
        text = text.rstrip() + "\n\n" + marker + "\n\n" + repl_block + "\n"

    rr_path.write_text(text)
    print(f"✅ Updated: {rr_path}")

    ms_path = Path("MANUSCRIPT_COMPLETE.md")
    ms = ms_path.read_text()
    rep_header = "## Reproducibility"
    if rep_header not in ms:
        ms = ms.rstrip() + "\n\n" + rep_header + "\n\n" + (
            "All quantitative results and figures in this repository are reproducible from a clean environment using:\n\n"
            "- `make all` (creates a virtualenv, generates CSVs in `results/`, regenerates figures in `figures/`, and updates derived numbers)\n"
            "- `make data` (CSV generation only)\n"
            "- `make figs` (figure generation only; requires `results/`)\n\n"
            "The primary configuration is `config/default.yaml` (simulation + sweeps) and `config/alphafold.yaml` (AlphaFold reanalysis).\n"
        )
        ms_path.write_text(ms)
        print(f"✅ Updated: {ms_path}")
    else:
        print(f"ℹ️ Reproducibility section already present: {ms_path}")


if __name__ == "__main__":
    main()


