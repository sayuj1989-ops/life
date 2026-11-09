"""Audit conditional arithmetic; no physiological or survival simulation."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def mean_reset_fraction(period_h, tau_h, count):
    interval_h = period_h / count
    return -math.expm1(-interval_h / tau_h) * tau_h / interval_h


def independent_mean(period_h, tau_h, count, samples=100000):
    interval_h = period_h / count
    step = interval_h / samples
    integral = math.fsum(
        math.exp(-((i + 0.5) * step) / tau_h) * step
        for i in range(samples)
    )
    return integral / interval_h


def main():
    reviewed = [
        ROOT / "research/longevity_squat_stand_feasibility.md",
        ROOT / "scripts/experiments/experiment_squat_stand_cycle.py",
        ROOT / "reports/helical_growth_research_2026-10-01/RESEARCH_BRIEF.md",
        ROOT / "reports/helical_growth_research_2026-10-01/DIAGNOSTIC_RESULTS.md",
    ]
    rows = []
    for period_h in (24.0, 16.0):
        for tau_h in (0.5, 2.0, 8.0):
            for count in (3, 10, 50, 100):
                analytic = mean_reset_fraction(period_h, tau_h, count)
                numeric = independent_mean(period_h, tau_h, count)
                error = abs(analytic - numeric)
                assert error < 1e-9, (period_h, tau_h, count, error)
                rows.append({
                    "period_h": period_h,
                    "assumed_decay_h": tau_h,
                    "assumed_evenly_spaced_resets": count,
                    "analytic_fraction": analytic,
                    "independent_integral_fraction": numeric,
                    "absolute_difference": error,
                })

    mass_kg, gravity_m_s2 = 70.0, 9.81
    energy = []
    for label, rise_m in (("hypothetical_floor_rise", 0.70),
                          ("hypothetical_chair_rise", 0.35)):
        delta_j = mass_kg * gravity_m_s2 * rise_m
        energy.append({
            "scenario": label,
            "hypothetical_mass_kg": mass_kg,
            "hypothetical_com_rise_m": rise_m,
            "positive_potential_energy_change_j": delta_j,
            "return_descent_potential_energy_change_j": -delta_j,
            "closed_cycle_net_potential_energy_change_j": 0.0,
            "metabolic_energy_j": None,
        })

    result = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "ARITHMETIC_VERIFIED_BIOLOGY_UNCALIBRATED",
        "meaning": "Conditional reset-model arithmetic and hypothetical gravitational work only",
        "input_sha256": {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                         for p in reviewed},
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "reset_model_sensitivity": rows,
        "max_independent_integral_error": max(r["absolute_difference"] for r in rows),
        "hypothetical_energy_examples": energy,
        "lifespan_effect": None,
        "floor_specific_benefit": None,
        "empirically_identified_decay_time": None,
    }
    (OUT / "assumption_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    headline = [r for r in rows if r["period_h"] == 24 and r["assumed_decay_h"] == 2
                and r["assumed_evenly_spaced_resets"] in (3, 50, 100)]
    print(json.dumps({"status": result["status"], "headline": headline,
                      "max_integration_error": result["max_independent_integral_error"],
                      "hypothetical_energy_examples": energy}, indent=2))


if __name__ == "__main__":
    main()
