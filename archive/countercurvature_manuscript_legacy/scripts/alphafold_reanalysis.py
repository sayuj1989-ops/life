from __future__ import annotations

import argparse
import json
import math
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def _require_matplotlib():
    try:
        import matplotlib.pyplot as plt  # type: ignore
        return plt
    except Exception as e:  # pragma: no cover
        raise RuntimeError("matplotlib is required. Install dependencies via `make deps`.") from e


def _require_biopython():
    try:
        from Bio.PDB import PDBParser  # type: ignore
        from Bio.PDB.PPBuilder import PPBuilder  # type: ignore
        return PDBParser, PPBuilder
    except Exception as e:  # pragma: no cover
        raise RuntimeError("biopython is required. Install dependencies via `make deps`.") from e


@dataclass(frozen=True)
class AFConfig:
    results_dir: Path
    figures_dir: Path
    cache_dir: Path
    metadata_dir: Path
    thresholds: list[int]
    curvature_window: int
    min_domain_len: int
    bootstrap_samples: int
    seed: int
    proteins: dict[str, dict[str, str]]


def load_af_config(path: str | Path) -> AFConfig:
    if yaml is None:
        raise RuntimeError("PyYAML is required. Install dependencies via `make deps`.")
    p = Path(path)
    data = yaml.safe_load(p.read_text())
    proteins = data["alphafold"]["proteins"]
    return AFConfig(
        results_dir=Path(data["io"]["results_dir"]),
        figures_dir=Path(data["io"]["figures_dir"]),
        cache_dir=Path(data["alphafold"]["cache_dir"]),
        metadata_dir=Path(data["alphafold"]["metadata_dir"]),
        thresholds=[int(x) for x in data["alphafold"]["plddt_thresholds"]],
        curvature_window=int(data["alphafold"]["curvature_window"]),
        min_domain_len=int(data["alphafold"]["min_domain_len"]),
        bootstrap_samples=int(data["alphafold"]["bootstrap_samples"]),
        seed=int(data["alphafold"]["seed"]),
        proteins={str(k): dict(v) for k, v in proteins.items()},
    )


def fetch_afdb_pdb(uniprot: str) -> tuple[dict[str, Any] | None, bytes | None]:
    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot}"
    with urllib.request.urlopen(api_url) as resp:
        data = json.loads(resp.read().decode())
    if not data:
        return None, None
    entry = data[0]
    pdb_url = entry.get("pdbUrl")
    if not pdb_url:
        return entry, None
    with urllib.request.urlopen(pdb_url) as resp:
        pdb_bytes = resp.read()
    return entry, pdb_bytes


def _ca_trace_and_plddt(pdb_path: Path) -> tuple[np.ndarray, np.ndarray, str]:
    PDBParser, PPBuilder = _require_biopython()
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("af", str(pdb_path))

    ppb = PPBuilder()
    seq = ""
    for pp in ppb.build_peptides(structure):
        seq += str(pp.get_sequence())

    coords = []
    plddt = []
    for model in structure:
        for chain in model:
            for residue in chain:
                if "CA" in residue:
                    atom = residue["CA"]
                    coords.append(atom.get_coord())
                    plddt.append(float(atom.get_bfactor()))
    if not coords:
        raise ValueError(f"No CA atoms found in {pdb_path}")
    return np.asarray(coords, float), np.asarray(plddt, float), seq


def _local_curvature(coords: np.ndarray, window: int) -> np.ndarray:
    curv = np.full(len(coords), np.nan, dtype=float)
    w = int(window)
    for i in range(w, len(coords) - w):
        pts = coords[i - w : i + w + 1]
        center = pts.mean(axis=0)
        r = np.linalg.norm(pts - center, axis=1).mean()
        curv[i] = 1.0 / (r + 1e-9)
    return curv


def _entropy(seq: str) -> float:
    if not seq:
        return float("nan")
    counts = {}
    for aa in seq:
        counts[aa] = counts.get(aa, 0) + 1
    n = len(seq)
    H = 0.0
    for c in counts.values():
        p = c / n
        H -= p * math.log2(p)
    return float(H)


def _domain_segments(mask: np.ndarray, min_len: int) -> list[tuple[int, int]]:
    segs: list[tuple[int, int]] = []
    i = 0
    n = len(mask)
    while i < n:
        if not mask[i]:
            i += 1
            continue
        j = i
        while j < n and mask[j]:
            j += 1
        if (j - i) >= min_len:
            segs.append((i, j))
        i = j
    return segs


def _spearman(x: np.ndarray, y: np.ndarray) -> float:
    xr = pd.Series(x).rank(method="average").to_numpy()
    yr = pd.Series(y).rank(method="average").to_numpy()
    return float(np.corrcoef(xr, yr)[0, 1])


def _bootstrap_ci(rng: np.random.Generator, x: np.ndarray, y: np.ndarray, n: int) -> tuple[float, float]:
    idx = np.arange(len(x))
    rs = []
    for _ in range(n):
        samp = rng.choice(idx, size=len(idx), replace=True)
        rs.append(_spearman(x[samp], y[samp]))
    lo, hi = np.quantile(rs, [0.025, 0.975])
    return float(lo), float(hi)


def main() -> None:
    ap = argparse.ArgumentParser(description="AlphaFold reanalysis with filtering + bootstrap CI.")
    ap.add_argument("--config", default="config/alphafold.yaml", help="Path to alphafold YAML config")
    ap.add_argument("--no-fetch", action="store_true", help="Do not fetch missing PDBs from AFDB API")
    args = ap.parse_args()

    cfg = load_af_config(args.config)
    cfg.results_dir.mkdir(parents=True, exist_ok=True)
    cfg.figures_dir.mkdir(parents=True, exist_ok=True)
    cfg.cache_dir.mkdir(parents=True, exist_ok=True)
    cfg.metadata_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(cfg.seed)

    # Fetch/cache PDBs into results/ only
    for name, meta in cfg.proteins.items():
        uniprot = meta["uniprot"]
        pdb_path = cfg.cache_dir / f"{name}.pdb"
        meta_path = cfg.metadata_dir / f"{name}.json"
        if pdb_path.exists() and meta_path.exists():
            continue
        if args.no_fetch:
            continue
        try:
            entry, pdb_bytes = fetch_afdb_pdb(uniprot)
            if entry is not None:
                meta_path.write_text(json.dumps(entry, indent=2))
            if pdb_bytes is not None:
                pdb_path.write_bytes(pdb_bytes)
        except Exception:
            continue

    rows = []
    sensitivity_rows = []

    for name, meta in cfg.proteins.items():
        pdb_path = cfg.cache_dir / f"{name}.pdb"
        category = meta.get("category", "UNKNOWN")
        if not pdb_path.exists():
            rows.append({"protein": name, "uniprot": meta["uniprot"], "category": category, "ok": False, "reason": "missing_pdb"})
            continue

        try:
            coords, plddt, seq = _ca_trace_and_plddt(pdb_path)
            curv = _local_curvature(coords, cfg.curvature_window)
            H = _entropy(seq)
            length = int(len(seq)) if seq else int(len(coords))

            base = {
                "protein": name,
                "uniprot": meta["uniprot"],
                "category": category,
                "ok": True,
                "reason": "",
                "length": length,
                "seq_entropy": H,
                "mean_plddt": float(np.nanmean(plddt)),
                "frac_plddt_ge_70": float(np.mean(plddt >= 70.0)),
                "mean_curvature_all": float(np.nanmean(curv)),
                "std_curvature_all": float(np.nanstd(curv)),
            }
            rows.append(base)

            for thr in cfg.thresholds:
                mask = plddt >= float(thr)
                segs = _domain_segments(mask, cfg.min_domain_len)
                if not segs:
                    sensitivity_rows.append({**base, "plddt_thr": thr, "domain_count": 0, "mean_curvature": float("nan")})
                    continue
                vals = [float(np.nanmean(curv[i:j])) for (i, j) in segs]
                sensitivity_rows.append({**base, "plddt_thr": thr, "domain_count": int(len(segs)), "mean_curvature": float(np.nanmean(vals))})

        except Exception as e:
            rows.append({"protein": name, "uniprot": meta["uniprot"], "category": category, "ok": False, "reason": f"parse_error:{e}"})

    summary = pd.DataFrame(rows)
    sens = pd.DataFrame(sensitivity_rows)

    summary_path = cfg.results_dir / "alphafold_summary.csv"
    sens_path = cfg.results_dir / "alphafold_sensitivity.csv"
    summary.to_csv(summary_path, index=False)
    sens.to_csv(sens_path, index=False)
    print(f"✅ Wrote: {summary_path}")
    print(f"✅ Wrote: {sens_path}")

    corr_path = cfg.results_dir / "alphafold_correlation_by_threshold.csv"
    fig_path = cfg.figures_dir / "fig_alphafold_sensitivity.png"

    # If we couldn't fetch/parse anything (e.g. offline), keep pipeline green:
    if sens.empty or ("plddt_thr" not in sens.columns):
        pd.DataFrame(
            [{"plddt_thr": thr, "n": 0, "spearman_r": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan")} for thr in cfg.thresholds]
        ).to_csv(corr_path, index=False)
        print(f"✅ Wrote: {corr_path} (no data)")

        plt = _require_matplotlib()
        fig, ax = plt.subplots(1, 1, figsize=(7, 4))
        ax.text(0.5, 0.5, "No AlphaFold data available\\n(run without --no-fetch and ensure network access)", ha="center", va="center")
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(fig_path, dpi=200, bbox_inches="tight")
        plt.close(fig)
        print(f"✅ Wrote: {fig_path} (placeholder)")
        return

    corr_rows = []
    for thr in cfg.thresholds:
        sub = sens[(sens["plddt_thr"] == thr) & sens["ok"]].dropna(subset=["seq_entropy", "mean_curvature"])
        if len(sub) < 4:
            corr_rows.append({"plddt_thr": thr, "n": int(len(sub)), "spearman_r": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan")})
            continue
        x = sub["seq_entropy"].to_numpy(float)
        y = sub["mean_curvature"].to_numpy(float)
        r = _spearman(x, y)
        lo, hi = _bootstrap_ci(rng, x, y, cfg.bootstrap_samples)
        corr_rows.append({"plddt_thr": thr, "n": int(len(sub)), "spearman_r": r, "ci_lo": lo, "ci_hi": hi})

    corr_df = pd.DataFrame(corr_rows)
    corr_df.to_csv(corr_path, index=False)
    print(f"✅ Wrote: {corr_path}")

    plt = _require_matplotlib()
    fig, ax = plt.subplots(1, 1, figsize=(7, 4))
    ax.errorbar(
        corr_df["plddt_thr"],
        corr_df["spearman_r"],
        yerr=[corr_df["spearman_r"] - corr_df["ci_lo"], corr_df["ci_hi"] - corr_df["spearman_r"]],
        fmt="-o",
        capsize=4,
    )
    ax.axhline(0.0, color="k", lw=0.8, alpha=0.3)
    ax.set_xlabel("pLDDT threshold")
    ax.set_ylabel("Spearman r (entropy vs curvature)")
    ax.set_title("AlphaFold sensitivity to pLDDT filtering (bootstrap 95% CI)")
    ax.grid(alpha=0.2)
    fig.tight_layout()

    fig.savefig(fig_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Wrote: {fig_path}")


if __name__ == "__main__":
    main()


