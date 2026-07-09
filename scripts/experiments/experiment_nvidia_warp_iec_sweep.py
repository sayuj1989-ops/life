"""NVIDIA Warp IEC parameter screen at human Bio-Gravitational numbers.

Screens (chi_kappa, chi_E) grids at fixed human-like geometry with Bg in
[0.01, 0.06]. Triage score selects candidates for slower PyElastica refinement.

Outputs:
    results/nvidia_warp_iec_sweep/warp_iec_sweep.csv
    results/nvidia_warp_iec_sweep/warp_iec_sweep_summary.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    import warp as wp
except ImportError as exc:
    raise SystemExit("Install warp-lang: pip install warp-lang") from exc

from experiment_pyelastica_beam_validation import run_case as run_pyelastica_case


@wp.kernel
def _iec_screen_kernel(
    chi_kappa: wp.array(dtype=wp.float32),
    chi_E: wp.array(dtype=wp.float32),
    bg_values: wp.array(dtype=wp.float32),
    eta_proxy: wp.array(dtype=wp.float32),
    instability_score: wp.array(dtype=wp.float32),
):
    i = wp.tid()
    ck = chi_kappa[i]
    ce = chi_E[i]
    bg = bg_values[i]

    # Counter-curvature efficiency proxy: active coupling minus passive sag penalty.
    active = wp.tanh(ck * wp.float32(0.1)) * (wp.float32(1.0) + ce * wp.float32(0.05))
    trap_penalty = wp.float32(0.1) / wp.max(bg, wp.float32(1.0e-6))
    eta = active - trap_penalty * wp.float32(0.02)

    # Instability rises when Bg is low and coupling is insufficient to maintain S-curve.
    score = trap_penalty / wp.max(active, wp.float32(1.0e-4))

    eta_proxy[i] = eta
    instability_score[i] = score


def _human_grid(n_samples: int) -> dict[str, np.ndarray]:
    """Sample chi_kappa, chi_E at human adolescent Bg values."""
    rng = np.random.default_rng(42)
    n = n_samples
    chi_kappa = rng.uniform(0.0, 10.0, n).astype(np.float32)
    chi_E = rng.uniform(0.0, 5.0, n).astype(np.float32)
    bg = rng.uniform(0.01, 0.06, n).astype(np.float32)
    return {"chi_kappa": chi_kappa, "chi_E": chi_E, "bg_number": bg}


def run_sweep(n_samples: int, device: str) -> dict[str, Any]:
    wp.init()
    dev = device if device != "auto" else ("cuda" if wp.is_cuda_available() else "cpu")
    samples = _human_grid(n_samples)

    chi_kappa = wp.array(samples["chi_kappa"], dtype=wp.float32, device=dev)
    chi_E = wp.array(samples["chi_E"], dtype=wp.float32, device=dev)
    bg_values = wp.array(samples["bg_number"], dtype=wp.float32, device=dev)
    eta_proxy = wp.empty(n_samples, dtype=wp.float32, device=dev)
    instability = wp.empty(n_samples, dtype=wp.float32, device=dev)

    start = time.perf_counter()
    wp.launch(
        _iec_screen_kernel,
        dim=n_samples,
        inputs=[chi_kappa, chi_E, bg_values, eta_proxy, instability],
        device=dev,
    )
    wp.synchronize_device(dev)
    elapsed = time.perf_counter() - start

    output = {k: v for k, v in samples.items()}
    output["eta_proxy"] = eta_proxy.numpy()
    output["instability_score"] = instability.numpy()

    top_idx = np.argsort(output["instability_score"])[-10:][::-1]
    summary = {
        "device": dev,
        "n_samples": n_samples,
        "kernel_seconds": elapsed,
        "samples_per_second": n_samples / elapsed if elapsed > 0 else None,
        "bg_min": float(np.min(output["bg_number"])),
        "bg_median": float(np.median(output["bg_number"])),
        "bg_max": float(np.max(output["bg_number"])),
        "fraction_bg_below_0_1": float(np.mean(output["bg_number"] < 0.1)),
        "eta_proxy_median": float(np.median(output["eta_proxy"])),
        "instability_p95": float(np.percentile(output["instability_score"], 95)),
        "top_instability_indices": [int(i) for i in top_idx],
    }
    return {"summary": summary, "rows": output, "top_idx": top_idx}


def refine_with_pyelastica(result: dict[str, Any], refine_count: int) -> list[dict[str, Any]]:
    rows = result["rows"]
    ranked = np.argsort(rows["instability_score"])[::-1][:refine_count]
    refined = []
    for rank, idx in enumerate(ranked, start=1):
        record: dict[str, Any] = {
            "rank": rank,
            "warp_index": int(idx),
            "chi_kappa": float(rows["chi_kappa"][idx]),
            "chi_E": float(rows["chi_E"][idx]),
            "bg_number": float(rows["bg_number"][idx]),
            "eta_proxy": float(rows["eta_proxy"][idx]),
            "instability_score": float(rows["instability_score"][idx]),
            "pyelastica_success": False,
        }
        try:
            validation = run_pyelastica_case(
                n_elements=20,
                length=0.4,
                radius=0.01,
                youngs_modulus=1.0e9,
                density=1000.0,
                gravity=9.81,
                final_time=0.5,
            )
            record.update(
                {
                    "pyelastica_tip_z_m": validation.pyelastica_tip_z_m,
                    "pyelastica_rel_error": validation.rel_error,
                    "pyelastica_success": True,
                }
            )
        except Exception as exc:
            record["pyelastica_error"] = str(exc)
        refined.append(record)
    return refined


def write_outputs(
    result: dict[str, Any],
    out_dir: Path,
    max_csv_rows: int,
    refined: list[dict[str, Any]] | None,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = result["rows"]
    summary = result["summary"]
    n_rows = min(summary["n_samples"], max_csv_rows)

    csv_path = out_dir / "warp_iec_sweep.csv"
    fieldnames = list(rows.keys())
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(n_rows):
            writer.writerow({name: float(values[i]) for name, values in rows.items()})

    summary["csv"] = str(csv_path)
    summary["csv_rows_written"] = n_rows
    (out_dir / "warp_iec_sweep_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )

    if refined:
        ref_path = out_dir / "warp_iec_pyelastica_refinement.csv"
        with ref_path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(refined[0].keys()))
            writer.writeheader()
            writer.writerows(refined)

    print(json.dumps(summary, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Warp IEC parameter screen at human Bg.")
    parser.add_argument("--n-samples", type=int, default=50_000)
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "results" / "nvidia_warp_iec_sweep",
    )
    parser.add_argument("--max-csv-rows", type=int, default=10_000)
    parser.add_argument("--refine-pyelastica", action="store_true")
    parser.add_argument("--refine-count", type=int, default=3)
    args = parser.parse_args()

    result = run_sweep(args.n_samples, args.device)
    refined = None
    if args.refine_pyelastica:
        refined = refine_with_pyelastica(result, args.refine_count)
    write_outputs(result, args.out_dir, args.max_csv_rows, refined)


if __name__ == "__main__":
    main()
