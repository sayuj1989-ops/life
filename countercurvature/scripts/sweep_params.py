from __future__ import annotations

import argparse

import pandas as pd

from scripts._config import load_bcc_config
from scripts._iec_beam import run_single


def main() -> None:
    ap = argparse.ArgumentParser(description="Parameter sweeps for IEC beam surrogate. Writes results/*.csv only.")
    ap.add_argument("--config", default="config/default.yaml", help="Path to YAML config")
    args = ap.parse_args()

    cfg = load_bcc_config(args.config)
    results_dir = cfg.io.results_dir
    results_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for g in cfg.sweeps.gravity_values:
        for chi_k in cfg.sweeps.chi_kappa_values:
            rows.append(run_single(cfg, gravity=g, chi_kappa=chi_k)["row"])

    df = pd.DataFrame(rows)
    grid_path = results_dir / "sweep_grid.csv"
    df.to_csv(grid_path, index=False)
    print(f"✅ Wrote: {grid_path} ({len(df)} rows)")

    micro = pd.DataFrame([run_single(cfg, gravity=g, chi_kappa=cfg.iec.chi_kappa)["row"] for g in cfg.sweeps.gravity_values])
    micro_path = results_dir / "sweep_microgravity.csv"
    micro.to_csv(micro_path, index=False)
    print(f"✅ Wrote: {micro_path} ({len(micro)} rows)")

    ksw = pd.DataFrame([run_single(cfg, gravity=cfg.simulation.gravity, chi_kappa=chi_k)["row"] for chi_k in cfg.sweeps.chi_kappa_values])
    k_path = results_dir / "sweep_chi_kappa.csv"
    ksw.to_csv(k_path, index=False)
    print(f"✅ Wrote: {k_path} ({len(ksw)} rows)")


if __name__ == "__main__":
    main()


