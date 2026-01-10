from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from scripts._config import load_bcc_config
from scripts._iec_beam import run_single


def main() -> None:
    ap = argparse.ArgumentParser(description="Run one rod surrogate simulation and output a standardized JSON/CSV row.")
    ap.add_argument("--config", default="config/default.yaml", help="Path to YAML config")
    ap.add_argument("--gravity", type=float, default=None, help="Override gravity")
    ap.add_argument("--chi-kappa", type=float, default=None, help="Override chi_kappa")
    ap.add_argument("--tag", type=str, default="single", help="Label for output filenames")
    args = ap.parse_args()

    cfg = load_bcc_config(args.config)
    out_dir = cfg.io.results_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    res = run_single(cfg, gravity=args.gravity, chi_kappa=args.chi_kappa)
    row = res["row"]

    csv_path = out_dir / f"sim_single_{args.tag}.csv"
    json_path = out_dir / f"sim_single_{args.tag}.json"

    pd.DataFrame([row]).to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(res, indent=2, default=float))

    print(f"✅ Wrote: {csv_path}")
    print(f"✅ Wrote: {json_path}")


if __name__ == "__main__":
    main()


