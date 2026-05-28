"""Validate PyElastica gravity sag against the analytic cantilever solution.

This experiment is intentionally narrow: it checks that the nonlinear Cosserat
rod backend reproduces the classical small-deflection Euler-Bernoulli result in
the gravity-only limit. That makes later information-coupled simulations easier
to defend as a solver extension rather than a numerical artifact.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from spinalmodes.countercurvature.coupling import CounterCurvatureParams
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem


@dataclass
class ValidationRow:
    n_elements: int
    length_m: float
    radius_m: float
    youngs_modulus_pa: float
    density_kg_m3: float
    gravity_m_s2: float
    dt_s: float
    final_time_s: float
    pyelastica_tip_z_m: float
    analytic_tip_z_m: float
    abs_error_m: float
    rel_error: float
    pass_20pct: bool


def analytic_cantilever_tip_sag(
    *,
    length: float,
    radius: float,
    youngs_modulus: float,
    density: float,
    gravity: float,
) -> float:
    """Return downward tip deflection for a horizontal circular cantilever."""

    area = np.pi * radius**2
    second_moment = np.pi * radius**4 / 4.0
    load_per_length = density * area * gravity
    return -(load_per_length * length**4) / (8.0 * youngs_modulus * second_moment)


def run_case(
    *,
    n_elements: int,
    length: float,
    radius: float,
    youngs_modulus: float,
    density: float,
    gravity: float,
    final_time: float,
) -> ValidationRow:
    s = np.linspace(0.0, length, n_elements + 1)
    info = InfoField1D(s=s, I=np.full_like(s, 0.5), dIds=np.zeros_like(s))
    params = CounterCurvatureParams(scale_length=length)

    rod_system = CounterCurvatureRodSystem.from_iec(
        info=info,
        params=params,
        length=length,
        n_elements=n_elements,
        E0=youngs_modulus,
        rho=density,
        radius=radius,
        gravity=gravity,
        base_position=(0.0, 0.0, 0.0),
        base_direction=(1.0, 0.0, 0.0),
        normal=(0.0, 1.0, 0.0),
    )

    wave_speed = float(np.sqrt(youngs_modulus / density))
    dt = 0.5 * (length / n_elements) / wave_speed
    save_every = max(1, int(0.01 / dt))

    result = rod_system.run_simulation(
        final_time=final_time,
        dt=dt,
        save_every=save_every,
        gravity=gravity,
        damping_constant=0.5,
        progress_bar=False,
    )

    pyelastica_tip_z = float(result.centerline[-1, -1, 2])
    analytic_tip_z = analytic_cantilever_tip_sag(
        length=length,
        radius=radius,
        youngs_modulus=youngs_modulus,
        density=density,
        gravity=gravity,
    )
    abs_error = abs(pyelastica_tip_z - analytic_tip_z)
    rel_error = abs_error / max(abs(analytic_tip_z), 1e-12)

    return ValidationRow(
        n_elements=n_elements,
        length_m=length,
        radius_m=radius,
        youngs_modulus_pa=youngs_modulus,
        density_kg_m3=density,
        gravity_m_s2=gravity,
        dt_s=dt,
        final_time_s=final_time,
        pyelastica_tip_z_m=pyelastica_tip_z,
        analytic_tip_z_m=analytic_tip_z,
        abs_error_m=abs_error,
        rel_error=rel_error,
        pass_20pct=rel_error < 0.20,
    )


def write_outputs(rows: list[ValidationRow], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "pyelastica_beam_validation.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    summary = {
        "n_cases": len(rows),
        "all_pass_20pct": all(row.pass_20pct for row in rows),
        "max_rel_error": max(row.rel_error for row in rows),
        "mean_rel_error": float(np.mean([row.rel_error for row in rows])),
        "csv": str(csv_path),
    }
    (out_dir / "pyelastica_beam_validation_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )

    md_path = out_dir / "pyelastica_beam_validation.md"
    with md_path.open("w") as handle:
        handle.write("# PyElastica Beam Validation\n\n")
        handle.write(
            "Gravity-only PyElastica simulations were compared with the analytic "
            "Euler-Bernoulli cantilever tip-deflection formula.\n\n"
        )
        handle.write(f"- Cases: {summary['n_cases']}\n")
        handle.write(f"- All cases <20% relative error: {summary['all_pass_20pct']}\n")
        handle.write(f"- Maximum relative error: {summary['max_rel_error']:.4f}\n")
        handle.write(f"- Mean relative error: {summary['mean_rel_error']:.4f}\n\n")
        handle.write("| Elements | PyElastica tip z (m) | Analytic tip z (m) | Rel. error |\n")
        handle.write("|---:|---:|---:|---:|\n")
        for row in rows:
            handle.write(
                f"| {row.n_elements} | {row.pyelastica_tip_z_m:.6e} | "
                f"{row.analytic_tip_z_m:.6e} | {row.rel_error:.4f} |\n"
            )

    print(json.dumps(summary, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate PyElastica against analytic gravity sag."
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "results" / "pyelastica_beam_validation",
    )
    parser.add_argument("--n-elements", type=int, nargs="+", default=[20, 40, 80])
    parser.add_argument("--length", type=float, default=0.4)
    parser.add_argument("--radius", type=float, default=0.01)
    parser.add_argument("--youngs-modulus", type=float, default=1e9)
    parser.add_argument("--density", type=float, default=1000.0)
    parser.add_argument("--gravity", type=float, default=9.81)
    parser.add_argument("--final-time", type=float, default=1.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [
        run_case(
            n_elements=n,
            length=args.length,
            radius=args.radius,
            youngs_modulus=args.youngs_modulus,
            density=args.density,
            gravity=args.gravity,
            final_time=args.final_time,
        )
        for n in args.n_elements
    ]
    write_outputs(rows, args.out_dir)


if __name__ == "__main__":
    main()
