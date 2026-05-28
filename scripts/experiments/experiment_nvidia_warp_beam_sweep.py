"""NVIDIA Warp accelerated beam sweep for virtual spine mechanics.

PyElastica remains the reference nonlinear Cosserat-rod solver for the
manuscript. This script adds a GPU-native screening layer: it evaluates a large
Euler-Bernoulli gravity-sag parameter sweep with NVIDIA Warp so that candidate
length/stiffness/radius regimes can be triaged before slower Cosserat runs.

Outputs:
    results/nvidia_warp_beam_sweep/warp_beam_sweep.csv
    results/nvidia_warp_beam_sweep/warp_beam_sweep_summary.json
    results/nvidia_warp_beam_sweep/warp_beam_sweep.md
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
except ImportError as exc:  # pragma: no cover - exercised manually when missing
    raise SystemExit(
        "NVIDIA Warp is required for this optional experiment. Install with:\n"
        "  pip install warp-lang"
    ) from exc

from experiment_pyelastica_beam_validation import run_case as run_pyelastica_case


@wp.kernel
def _beam_sweep_kernel(
    lengths: wp.array(dtype=wp.float32),
    radii: wp.array(dtype=wp.float32),
    youngs_moduli: wp.array(dtype=wp.float32),
    densities: wp.array(dtype=wp.float32),
    gravity: wp.float32,
    tip_sag: wp.array(dtype=wp.float32),
    bg_number: wp.array(dtype=wp.float32),
    sag_ratio: wp.array(dtype=wp.float32),
    risk_score: wp.array(dtype=wp.float32),
):
    i = wp.tid()

    pi = wp.float32(3.141592653589793)
    length = lengths[i]
    radius = radii[i]
    youngs_modulus = youngs_moduli[i]
    density = densities[i]

    area = pi * radius * radius
    second_moment = pi * radius * radius * radius * radius / wp.float32(4.0)
    mass = density * area * length
    load_per_length = density * area * gravity

    sag = load_per_length * length * length * length * length / (
        wp.float32(8.0) * youngs_modulus * second_moment
    )
    bg = youngs_modulus * second_moment / (mass * gravity * length * length)
    ratio = sag / length

    # Dimensionless screening score: values >1 combine the low-Bg regime with
    # a non-trivial passive deflection fraction. This is not a clinical risk
    # model; it is a triage score for selecting slower nonlinear simulations.
    risk = (wp.float32(0.1) / wp.max(bg, wp.float32(1.0e-8))) * (
        ratio / wp.float32(0.01)
    )

    tip_sag[i] = sag
    bg_number[i] = bg
    sag_ratio[i] = ratio
    risk_score[i] = risk


def _linspace_samples(n_samples: int) -> dict[str, np.ndarray]:
    """Create deterministic parameter samples spanning pediatric spine ranges."""

    x = np.linspace(0.0, 1.0, n_samples, dtype=np.float32)
    return {
        "length_m": np.float32(0.25) + np.float32(0.30) * x,
        "radius_m": np.float32(0.007) + np.float32(0.007) * ((x * 17.0) % 1.0),
        "youngs_modulus_pa": np.float32(1.0e6)
        + np.float32(1.499e9) * ((x * 31.0) % 1.0),
        "density_kg_m3": np.float32(900.0) + np.float32(300.0) * ((x * 43.0) % 1.0),
    }


def _select_device(requested: str) -> str:
    if requested != "auto":
        return requested
    return "cuda" if wp.is_cuda_available() else "cpu"


def run_sweep(n_samples: int, requested_device: str) -> dict[str, Any]:
    wp.init()
    device = _select_device(requested_device)
    samples = _linspace_samples(n_samples)

    lengths = wp.array(samples["length_m"], dtype=wp.float32, device=device)
    radii = wp.array(samples["radius_m"], dtype=wp.float32, device=device)
    youngs_moduli = wp.array(samples["youngs_modulus_pa"], dtype=wp.float32, device=device)
    densities = wp.array(samples["density_kg_m3"], dtype=wp.float32, device=device)

    tip_sag = wp.empty(n_samples, dtype=wp.float32, device=device)
    bg_number = wp.empty(n_samples, dtype=wp.float32, device=device)
    sag_ratio = wp.empty(n_samples, dtype=wp.float32, device=device)
    risk_score = wp.empty(n_samples, dtype=wp.float32, device=device)

    if device == "cuda":
        wp.synchronize_device(device)
    start = time.perf_counter()
    wp.launch(
        _beam_sweep_kernel,
        dim=n_samples,
        inputs=[
            lengths,
            radii,
            youngs_moduli,
            densities,
            np.float32(9.81),
            tip_sag,
            bg_number,
            sag_ratio,
            risk_score,
        ],
        device=device,
    )
    wp.synchronize_device(device)
    elapsed = time.perf_counter() - start

    output = {name: value for name, value in samples.items()}
    output.update(
        {
            "tip_sag_m": tip_sag.numpy(),
            "bg_number": bg_number.numpy(),
            "sag_ratio": sag_ratio.numpy(),
            "risk_score": risk_score.numpy(),
        }
    )

    top_idx = np.argsort(output["risk_score"])[-10:][::-1]
    summary = {
        "device": device,
        "n_samples": n_samples,
        "kernel_seconds": elapsed,
        "samples_per_second": n_samples / elapsed if elapsed > 0 else None,
        "bg_min": float(np.min(output["bg_number"])),
        "bg_median": float(np.median(output["bg_number"])),
        "bg_max": float(np.max(output["bg_number"])),
        "sag_ratio_median": float(np.median(output["sag_ratio"])),
        "sag_ratio_p95": float(np.percentile(output["sag_ratio"], 95)),
        "risk_score_p95": float(np.percentile(output["risk_score"], 95)),
        "fraction_bg_below_0_1": float(np.mean(output["bg_number"] < 0.1)),
        "top_risk_indices": [int(i) for i in top_idx],
    }

    return {"summary": summary, "rows": output, "top_idx": top_idx}


def _candidate_from_rows(rows: dict[str, np.ndarray], idx: int) -> dict[str, float]:
    return {name: float(values[idx]) for name, values in rows.items()}


def refine_with_pyelastica(
    result: dict[str, Any],
    refine_count: int,
    n_elements: int,
    final_time: float,
    max_sag_ratio: float,
) -> list[dict[str, Any]]:
    """Run nonlinear PyElastica refinement for selected Warp-screened rows."""

    rows = result["rows"]
    ranked_indices = np.argsort(rows["risk_score"])[::-1]
    candidate_indices = [
        int(idx)
        for idx in ranked_indices
        if float(rows["sag_ratio"][idx]) <= max_sag_ratio
    ][:refine_count]
    refined = []

    for rank, idx in enumerate(candidate_indices, start=1):
        candidate = _candidate_from_rows(rows, int(idx))
        record: dict[str, Any] = {
            "rank": rank,
            "warp_index": int(idx),
            **candidate,
            "pyelastica_success": False,
            "pyelastica_error": "",
        }

        try:
            validation = run_pyelastica_case(
                n_elements=n_elements,
                length=candidate["length_m"],
                radius=candidate["radius_m"],
                youngs_modulus=candidate["youngs_modulus_pa"],
                density=candidate["density_kg_m3"],
                gravity=9.81,
                final_time=final_time,
            )
            record.update(
                {
                    "pyelastica_tip_z_m": validation.pyelastica_tip_z_m,
                    "analytic_tip_z_m": validation.analytic_tip_z_m,
                    "pyelastica_abs_error_m": validation.abs_error_m,
                    "pyelastica_rel_error": validation.rel_error,
                    "pyelastica_success": True,
                }
            )
        except Exception as exc:  # pragma: no cover - depends on nonlinear solver stability
            record["pyelastica_error"] = str(exc)

        refined.append(record)

    return refined


def write_refinement_outputs(refined: list[dict[str, Any]], out_dir: Path) -> None:
    if not refined:
        return

    csv_path = out_dir / "warp_to_pyelastica_refinement.csv"
    fieldnames = list(refined[0].keys())
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(refined)

    summary = {
        "n_refined": len(refined),
        "n_success": sum(1 for row in refined if row["pyelastica_success"]),
        "csv": str(csv_path),
        "max_pyelastica_rel_error": max(
            (
                row.get("pyelastica_rel_error", 0.0)
                for row in refined
                if row["pyelastica_success"]
            ),
            default=None,
        ),
    }
    (out_dir / "warp_to_pyelastica_refinement_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )

    md_path = out_dir / "warp_to_pyelastica_refinement.md"
    with md_path.open("w") as handle:
        handle.write("# Warp to PyElastica Refinement\n\n")
        handle.write(
            "Highest-risk NVIDIA Warp screening rows were re-run with the "
            "validated PyElastica Cosserat-rod beam setup. Large errors against "
            "the analytic small-deflection formula are expected in very soft "
            "large-deflection regimes and indicate that nonlinear refinement is "
            "necessary.\n\n"
        )
        handle.write(f"- Refined cases: {summary['n_refined']}\n")
        handle.write(f"- Successful PyElastica runs: {summary['n_success']}\n")
        if summary["max_pyelastica_rel_error"] is not None:
            handle.write(
                f"- Maximum relative error vs small-deflection analytic formula: "
                f"{summary['max_pyelastica_rel_error']:.4f}\n"
            )
        handle.write("\n| Rank | Bg | sag/L | Warp tip sag (m) | PyElastica tip z (m) | Rel. error |\n")
        handle.write("|---:|---:|---:|---:|---:|---:|\n")
        for row in refined:
            if row["pyelastica_success"]:
                handle.write(
                    f"| {row['rank']} | {row['bg_number']:.4g} | {row['sag_ratio']:.4g} | "
                    f"{row['tip_sag_m']:.4g} | {row['pyelastica_tip_z_m']:.4g} | "
                    f"{row['pyelastica_rel_error']:.4g} |\n"
                )
            else:
                handle.write(
                    f"| {row['rank']} | {row['bg_number']:.4g} | {row['sag_ratio']:.4g} | "
                    f"{row['tip_sag_m']:.4g} | failed | nan |\n"
                )


def write_outputs(
    result: dict[str, Any],
    out_dir: Path,
    max_csv_rows: int,
    refined: list[dict[str, Any]] | None = None,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = result["rows"]
    summary = result["summary"]
    n_rows = min(summary["n_samples"], max_csv_rows)

    csv_path = out_dir / "warp_beam_sweep.csv"
    fieldnames = list(rows.keys())
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(n_rows):
            writer.writerow({name: float(values[i]) for name, values in rows.items()})

    top_cases = []
    for i in result["top_idx"]:
        top_cases.append(_candidate_from_rows(rows, int(i)))
    summary["csv"] = str(csv_path)
    summary["csv_rows_written"] = n_rows
    summary["top_risk_cases"] = top_cases

    summary_path = out_dir / "warp_beam_sweep_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")

    md_path = out_dir / "warp_beam_sweep.md"
    with md_path.open("w") as handle:
        handle.write("# NVIDIA Warp Beam Sweep\n\n")
        handle.write(
            "GPU-accelerated Euler-Bernoulli screening sweep for selecting "
            "candidate regimes before slower nonlinear Cosserat-rod simulation.\n\n"
        )
        handle.write(f"- Device: `{summary['device']}`\n")
        handle.write(f"- Samples: {summary['n_samples']:,}\n")
        handle.write(f"- Kernel time: {summary['kernel_seconds']:.6f} s\n")
        handle.write(f"- Throughput: {summary['samples_per_second']:,.0f} samples/s\n")
        handle.write(f"- Fraction with $B_g < 0.1$: {summary['fraction_bg_below_0_1']:.3f}\n")
        handle.write(f"- Median $B_g$: {summary['bg_median']:.6g}\n")
        handle.write(f"- 95th percentile sag ratio: {summary['sag_ratio_p95']:.6g}\n\n")
        handle.write("## Highest Screening-Risk Cases\n\n")
        handle.write("| L (m) | r (m) | E (Pa) | Bg | sag/L | risk |\n")
        handle.write("|---:|---:|---:|---:|---:|---:|\n")
        for case in top_cases:
            handle.write(
                f"| {case['length_m']:.4f} | {case['radius_m']:.5f} | "
                f"{case['youngs_modulus_pa']:.3e} | {case['bg_number']:.4g} | "
                f"{case['sag_ratio']:.4g} | {case['risk_score']:.4g} |\n"
            )
        if refined:
            handle.write("\n## PyElastica Refinement\n\n")
            handle.write(
                "A subset of high-risk rows was re-run through the validated "
                "PyElastica beam setup. See `warp_to_pyelastica_refinement.md`.\n"
            )

    if refined:
        write_refinement_outputs(refined, out_dir)

    print(json.dumps(summary, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an NVIDIA Warp accelerated beam-parameter sweep."
    )
    parser.add_argument("--n-samples", type=int, default=100_000)
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "results" / "nvidia_warp_beam_sweep",
    )
    parser.add_argument(
        "--max-csv-rows",
        type=int,
        default=10_000,
        help="Limit CSV size while retaining full distribution in the summary.",
    )
    parser.add_argument(
        "--refine-pyelastica",
        action="store_true",
        help="Re-run top Warp-screened cases with the PyElastica beam setup.",
    )
    parser.add_argument("--refine-count", type=int, default=3)
    parser.add_argument("--refine-elements", type=int, default=20)
    parser.add_argument("--refine-final-time", type=float, default=0.5)
    parser.add_argument(
        "--refine-max-sag-ratio",
        type=float,
        default=2.0,
        help="Only refine rows whose analytic sag/length is below this bound.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_sweep(args.n_samples, args.device)
    refined = None
    if args.refine_pyelastica:
        refined = refine_with_pyelastica(
            result=result,
            refine_count=args.refine_count,
            n_elements=args.refine_elements,
            final_time=args.refine_final_time,
            max_sag_ratio=args.refine_max_sag_ratio,
        )
    write_outputs(result, args.out_dir, args.max_csv_rows, refined=refined)


if __name__ == "__main__":
    main()
