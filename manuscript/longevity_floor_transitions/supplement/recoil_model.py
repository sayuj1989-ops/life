"""Verify an illustrative passive material model, not a human transfer model."""

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import csv
import json
import math
from pathlib import Path


OUT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Material:
    equilibrium_fraction: float
    total_stiffness: float = 1.0
    tau: float = 1.0

    @property
    def k_inf(self):
        return self.equilibrium_fraction * self.total_stiffness

    @property
    def k_1(self):
        return (1.0 - self.equilibrium_fraction) * self.total_stiffness

    def energy(self, x, z):
        return 0.5 * (self.k_inf * x * x + self.k_1 * z * z)


def exact_segment(material, x0, z0, velocity, duration):
    tau = material.tau
    a = velocity * tau
    b = z0 - a
    one_minus = -math.expm1(-duration / tau)
    one_minus_twice = -math.expm1(-2.0 * duration / tau)
    x1 = x0 + velocity * duration
    z1 = a + b * math.exp(-duration / tau)
    work = (0.5 * material.k_inf * (x1*x1 - x0*x0)
            + material.k_1 * velocity * (a*duration + b*tau*one_minus))
    integrated_z2 = (a*a*duration + 2.0*a*b*tau*one_minus
                     + b*b*tau*one_minus_twice/2.0)
    loss = material.k_1 * integrated_z2 / tau
    energy_change = material.energy(x1, z1) - material.energy(x0, z0)
    return {"x": x1, "z": z1, "work": work, "loss": loss,
            "energy_change": energy_change,
            "balance_residual": work - energy_change - loss}


def numerical_segment(material, x0, z0, velocity, duration, count):
    # Independent RK4 integration checks both internal state and energy accounting.
    h = duration / count
    z = z0
    work = loss = returned = injected = 0.0

    def rhs(time, value):
        x = x0 + velocity * time
        power = (material.k_inf*x + material.k_1*value) * velocity
        return (velocity - value/material.tau, power,
                material.k_1*value*value/material.tau,
                max(-power, 0.0), max(power, 0.0))

    for i in range(count):
        t = i*h
        r1 = rhs(t, z)
        r2 = rhs(t+h/2.0, z+h*r1[0]/2.0)
        r3 = rhs(t+h/2.0, z+h*r2[0]/2.0)
        r4 = rhs(t+h, z+h*r3[0])
        delta = [h*(r1[j]+2.0*r2[j]+2.0*r3[j]+r4[j])/6.0 for j in range(5)]
        z += delta[0]
        work += delta[1]
        loss += delta[2]
        returned += delta[3]
        injected += delta[4]
    return {"z": z, "work": work, "loss": loss,
            "returned": returned, "injected": injected}


def scenario(fraction, load_ratio, hold_ratio, unload_ratio):
    material = Material(fraction)
    x = z = 0.0
    segments = [(1.0/load_ratio, load_ratio), (0.0, hold_ratio),
                (-1.0/unload_ratio, unload_ratio)]
    exact = []
    numeric_errors = []
    refinements = []
    unload_numeric = None
    for velocity, duration in segments:
        result = exact_segment(material, x, z, velocity, duration)
        exact.append(result)
        if duration > 0:
            coarse = numerical_segment(material, x, z, velocity, duration, 1000)
            fine = numerical_segment(material, x, z, velocity, duration, 2000)
            error = max(abs(fine[key]-result[key]) for key in ("z", "work", "loss"))
            refinement = max(abs(fine[key]-coarse[key]) for key in ("z", "work", "loss"))
            numeric_errors.append(error)
            refinements.append(refinement)
            if velocity < 0:
                unload_numeric = fine
        assert abs(result["balance_residual"]) < 1e-9, result
        assert result["loss"] > -1e-10, result
        x, z = result["x"], result["z"]

    # The prescribed deformation returns to zero; remaining branch energy decays.
    residual = material.energy(x, z)
    cycle_work = math.fsum(item["work"] for item in exact)
    cycle_loss = math.fsum(item["loss"] for item in exact) + residual
    assert abs(x) < 1e-12
    assert abs(cycle_work-cycle_loss) < 1e-9
    assert cycle_loss > -1e-10
    assert max(numeric_errors) < 1e-7
    assert max(refinements) < 1e-7
    if fraction == 1.0:
        assert abs(cycle_loss) < 1e-12
        assert abs(-exact[2]["work"] - exact[0]["work"]) < 1e-12

    incoming = exact[0]["work"]
    return {
        "equilibrium_stiffness_fraction": fraction,
        "load_duration_over_tau": load_ratio,
        "hold_duration_over_tau": hold_ratio,
        "unload_duration_over_tau": unload_ratio,
        "loading_work_normalized": incoming,
        "stored_energy_before_hold_normalized": material.energy(exact[0]["x"], exact[0]["z"]),
        "stored_energy_after_hold_normalized": material.energy(exact[1]["x"], exact[1]["z"]),
        "hold_loss_normalized": exact[1]["loss"],
        "net_unloading_return_normalized": -exact[2]["work"],
        "net_return_over_loading_work": -exact[2]["work"] / incoming,
        "gross_unloading_return_normalized": unload_numeric["returned"],
        "work_injected_during_unloading_normalized": unload_numeric["injected"],
        "remaining_energy_after_unload_normalized": residual,
        "complete_cycle_loss_normalized": cycle_loss,
        "complete_cycle_balance_residual": cycle_work-cycle_loss,
        "max_independent_integration_error": max(numeric_errors),
        "max_refinement_difference": max(refinements),
    }


def force_at(material, x0, z0, velocity, t):
    tau = material.tau
    a = velocity * tau
    x = x0 + velocity * t
    z = a + (z0 - a) * math.exp(-t / tau)
    return material.k_inf * x + material.k_1 * z


def first_force_zero(material, x0, z0, velocity, duration):
    # Unloading stops at slack: first time the element force reaches zero.
    samples = 2000
    previous = force_at(material, x0, z0, velocity, 0.0)
    for index in range(1, samples + 1):
        t = duration * index / samples
        current = force_at(material, x0, z0, velocity, t)
        if current < 0.0 <= previous:
            low, high = duration * (index - 1) / samples, t
            while high - low > 1e-12 * max(1.0, duration):
                mid = 0.5 * (low + high)
                if force_at(material, x0, z0, velocity, mid) < 0.0:
                    high = mid
                else:
                    low = mid
            return low
        previous = current
    return duration


def tension_only_scenario(fraction, load_ratio, hold_ratio, unload_ratio):
    """Preloaded tension-only variant: the element cannot carry compression, so
    unloading is truncated at the slack point instead of being driven to zero."""
    material = Material(fraction)
    x = z = 0.0
    load = exact_segment(material, x, z, 1.0 / load_ratio, load_ratio)
    x, z = load["x"], load["z"]
    hold = exact_segment(material, x, z, 0.0, hold_ratio)
    x, z = hold["x"], hold["z"]

    velocity = -1.0 / unload_ratio
    slack_time = first_force_zero(material, x, z, velocity, unload_ratio)
    unload = exact_segment(material, x, z, velocity, slack_time)
    x_slack, z_slack = unload["x"], unload["z"]
    net_return = -unload["work"]

    numeric_errors = []
    refinements = []
    for segment_x, segment_z, v, d in ((0.0, 0.0, 1.0 / load_ratio, load_ratio),
                                       (x, z, 0.0, hold_ratio)):
        if d > 0:
            result = exact_segment(material, segment_x, segment_z, v, d)
            coarse = numerical_segment(material, segment_x, segment_z, v, d, 1000)
            fine = numerical_segment(material, segment_x, segment_z, v, d, 2000)
            numeric_errors.append(max(abs(fine[k] - result[k]) for k in ("z", "work", "loss")))
            refinements.append(max(abs(fine[k] - coarse[k]) for k in ("z", "work", "loss")))
    if slack_time > 0:
        coarse = numerical_segment(material, x, z, velocity, slack_time, 1000)
        fine = numerical_segment(material, x, z, velocity, slack_time, 2000)
        numeric_errors.append(max(abs(fine[k] - unload[k]) for k in ("z", "work", "loss")))
        refinements.append(max(abs(fine[k] - coarse[k]) for k in ("z", "work", "loss")))

    for result in (load, hold, unload):
        assert abs(result["balance_residual"]) < 1e-9, result
        assert result["loss"] > -1e-10, result
    # Core property under repair: a tension-only element cannot demand net work
    # to unload, so useful return is never negative.
    assert net_return >= -1e-12, (fraction, load_ratio, hold_ratio, unload_ratio, net_return)
    assert numeric_errors and max(numeric_errors) < 1e-7
    assert refinements and max(refinements) < 1e-7
    if fraction == 1.0:
        assert abs(net_return - load["work"]) < 1e-12
    return {
        "equilibrium_stiffness_fraction": fraction,
        "load_duration_over_tau": load_ratio,
        "hold_duration_over_tau": hold_ratio,
        "unload_duration_over_tau": unload_ratio,
        "loading_work_normalized": load["work"],
        "slack_time_over_planned_unload": slack_time / unload_ratio,
        "net_unloading_return_tension_only_normalized": net_return,
        "net_return_over_loading_work_tension_only": net_return / load["work"],
        "energy_remaining_at_slack_normalized": material.energy(x_slack, z_slack),
        "max_independent_integration_error": max(numeric_errors),
        "max_refinement_difference": max(refinements),
    }


def main():
    rows = [scenario(fraction, load, hold, unload)
            for fraction in (0.0, 0.25, 0.5, 0.75, 1.0)
            for load in (0.1, 1.0, 10.0)
            for hold in (0.0, 0.25, 1.0, 5.0, 20.0)
            for unload in (0.1, 1.0, 10.0)]
    with (OUT / "recoil_sensitivity.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    tension_rows = [tension_only_scenario(fraction, load, hold, unload)
                    for fraction in (0.0, 0.25, 0.5, 0.75, 1.0)
                    for load in (0.1, 1.0, 10.0)
                    for hold in (0.0, 0.25, 1.0, 5.0, 20.0)
                    for unload in (0.1, 1.0, 10.0)]
    with (OUT / "recoil_tension_only.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(tension_rows[0]))
        writer.writeheader()
        writer.writerows(tension_rows)
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "MODEL_ARITHMETIC_VERIFIED_HUMAN_BIOLOGY_UNCALIBRATED",
        "scenarios": len(rows),
        "model": "Passive standard linear solid under prescribed normalized deformation",
        "energy_unit": "k_total * deformation_amplitude_squared; arbitrary scale",
        "time_unit": "assumed material relaxation time; no empirical seconds assigned",
        "negative_net_unloading_return_cases": sum(r["net_unloading_return_normalized"] < -1e-10 for r in rows),
        "tension_only_scenarios": len(tension_rows),
        "tension_only_negative_net_return_cases": sum(
            r["net_unloading_return_tension_only_normalized"] < -1e-12 for r in tension_rows),
        "tension_only_max_independent_integration_error": max(
            r["max_independent_integration_error"] for r in tension_rows),
        "tension_only_max_refinement_difference": max(
            r["max_refinement_difference"] for r in tension_rows),
        "max_complete_cycle_balance_residual": max(abs(r["complete_cycle_balance_residual"]) for r in rows),
        "max_independent_integration_error": max(r["max_independent_integration_error"] for r in rows),
        "max_refinement_difference": max(r["max_refinement_difference"] for r in rows),
        "pure_elastic_control_cases": sum(r["equilibrium_stiffness_fraction"] == 1 for r in rows),
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "human_recoil_fraction": None,
        "metabolic_savings": None,
        "aging_or_survival_effect": None,
    }
    (OUT / "recoil_model_checks.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
