"""CPU-only inspection of completed frozen evidence; never imports Newton/Warp.

This is a retrospective diagnostic, not a replacement convergence assessment.
All inputs are read-only. Output is confined to this review directory.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "results/newton_mechanism_campaign_2026-09-12"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def condition(result, index):
    return {"world": int(index), **result["conditions"][index]}


def mechanical_summary(result, limits):
    events = [("initial", 0, result["ages"][0], result["observations"][0])]
    for month in range(1, len(result["observations"])):
        events.append(("shake_before_update", month, result["ages"][month - 1],
                       result["shake_diagnostics"][month - 1]))
        events.append(("monthly_after_settle", month, result["ages"][month],
                       result["observations"][month]))
    summary = {}
    for field, limit_key in [("axial_anchor_strain", "anchor_strain"),
                             ("shear_anchor_strain", "anchor_strain"),
                             ("out_of_plane", "planarity"),
                             ("quaternion_error", "quaternion_norm_error")]:
        peak = {"value": -np.inf}
        first = None
        count = 0
        for phase, month, age, observation in events:
            values = np.atleast_1d(observation[field]).astype(float)
            if not np.isfinite(values).all():
                raise ValueError("Nonfinite saved diagnostic")
            index = int(np.argmax(values))
            location = {"phase": phase, "month": month, "age_model_years": age}
            if field != "quaternion_error":
                location.update(condition(result, index))
            if values[index] > peak["value"]:
                peak = {"value": float(values[index]), **location}
            if np.any(values > limits[limit_key]):
                count += 1
                if first is None:
                    first = {"value": float(values[index]), **location}
        summary[field] = {"limit": limits[limit_key], "peak": peak,
                          "first_breaching_event": first, "breaching_events": count}
    replayed = all(row["breaching_events"] == 0 for row in summary.values())
    if replayed != result["mechanically_valid"]:
        raise AssertionError("Saved mechanical flag disagrees with recorded-state replay")
    return {"replayed_mechanically_valid": replayed, "metrics": summary,
            "scope": "Recorded initial/shake/monthly events only; no every-step claim"}


def inspect_states(result, directory, inputs):
    n = result["job"]["segments"]
    worlds = len(result["conditions"])
    spacing = np.asarray(result["material"]["joint_spacing_m"])
    bend_error, signed_error = 0., 0.
    min_dot, maximum_bend = 1., 0.
    for month, observation in enumerate(result["observations"]):
        path = directory / f"state_{month:03}.npz"
        inputs[str(path.relative_to(ROOT))] = digest(path)
        with np.load(path, allow_pickle=False) as state:
            body = state["body_q"].astype(np.float64)
            permanent = state["permanent_curvature"]
        if body.shape != (worlds * n, 7) or permanent.shape != (worlds, n - 1):
            raise ValueError("Unexpected saved-state topology")
        if not np.isfinite(body).all() or not np.isfinite(permanent).all():
            raise ValueError("Nonfinite saved state")
        x, y, z, w = body[:, 3:7].T
        tangent = np.stack([2 * (x * z + w * y), 2 * (y * z - w * x),
                            1 - 2 * (x*x + y*y)], axis=1).reshape(worlds, n, 3)
        left, right = tangent[:, :-1], tangent[:, 1:]
        cross_y = np.cross(left, right)[:, :, 1]
        dot = np.einsum("wij,wij->wi", left, right)
        local_angle = np.arctan2(cross_y, dot)
        reference_angle = np.asarray(observation["curvature_rad_per_m"]) * spacing
        independent_bend = np.degrees(np.abs(local_angle).sum(axis=1))
        bend_error = max(bend_error, float(np.max(np.abs(
            independent_bend - observation["bend_deg"]))))
        signed_error = max(signed_error, float(np.max(np.abs(local_angle - reference_angle))))
        normalized_dot = dot / (np.linalg.norm(left, axis=2) * np.linalg.norm(right, axis=2))
        min_dot = min(min_dot, float(normalized_dot.min()))
        maximum_bend = max(maximum_bend, float(independent_bend.max()))
    return {"monthly_states_inspected": len(result["observations"]),
            "max_abs_independent_bend_error_deg": bend_error,
            "max_abs_signed_joint_angle_error_rad": signed_error,
            "minimum_adjacent_tangent_dot": min_dot,
            "maximum_total_absolute_bend_deg": maximum_bend,
            "method": "float64 atan2 of adjacent-tangent cross-y and dot, independent of global angle unwrap",
            "scope": "Monthly planar readout only; no local twist, anchors or internal-step replay"}


def replay_comparison(a, b, limits):
    if a["conditions"] != b["conditions"] or a["ages"] != b["ages"]:
        raise ValueError("Unmatched comparison")
    fields = {}
    for key in ["bend_deg", "permanent_bend_deg"]:
        x = np.asarray([row[key] for row in a["observations"]])
        y = np.asarray([row[key] for row in b["observations"]])
        difference = np.abs(x-y)
        peak_indices = np.argmax(difference, axis=0)
        error = difference[peak_indices, np.arange(len(a["conditions"]))]
        allowed = np.maximum(limits["absolute_bend_deg"],
                             limits["relative_peak"] * np.max(np.abs(y), axis=0))
        rows = []
        for i, month in enumerate(peak_indices):
            rows.append({**condition(a, i), "max_error_deg": float(error[i]),
                         "allowed_error_deg": float(allowed[i]), "pass": bool(error[i] <= allowed[i]),
                         "at_month": int(month), "age_model_years": a["ages"][month],
                         "value_a_deg": float(x[month, i]), "value_b_deg": float(y[month, i])})
        fields[key] = {"pass": bool(np.all(error <= allowed)),
                       "failed_worlds": int(np.sum(error > allowed)), "worlds": rows}
    crossings = []
    for i in range(len(a["conditions"])):
        first = [next((age for age, obs in zip(r["ages"], r["observations"])
                       if obs["bend_deg"][i] > 10), None) for r in (a, b)]
        passes = (first[0] is None and first[1] is None or
                  all(age is not None for age in first) and
                  abs(first[0]-first[1]) <= limits["crossing_age_years"] + 1e-10)
        crossings.append(bool(passes))
    passes = (all(field["pass"] for field in fields.values()) and all(crossings)
              and a["mechanically_valid"] and b["mechanically_valid"])
    return {"pass": bool(passes), "fields": fields,
            "crossing_failures": sum(not value for value in crossings),
            "crossing_pass_per_world": crossings,
            "mechanical_flags": [a["mechanically_valid"], b["mechanically_valid"]]}


def run():
    inputs = {}
    def read(path):
        inputs[str(path.relative_to(ROOT))] = digest(path)
        return json.loads(path.read_text())
    ledger = read(CAMPAIGN / "campaign.json")
    assessment = read(CAMPAIGN / "assessment.json")
    protocol = read(CAMPAIGN / "protocol.json")
    protocol_digest = hashlib.sha256(json.dumps(protocol, sort_keys=True, separators=(",", ":"),
                                                allow_nan=False).encode()).hexdigest()
    if protocol_digest != ledger["protocol_sha256"]:
        raise ValueError("Protocol identity mismatch")
    complete = {}
    run_diagnostics = {}
    for item in ledger["runs"]:
        if item["status"] != "completed":
            continue
        directory = CAMPAIGN / item["directory"]
        result = read(directory / "result.json")
        if result["status"] != "completed" or result["protocol_sha256"] != protocol_digest:
            raise ValueError("Completed input identity mismatch")
        complete[item["job"]] = result
        run_diagnostics[item["job"]] = mechanical_summary(result, protocol["agreement"])
        run_diagnostics[item["job"]]["independent_readout"] = inspect_states(result, directory, inputs)
    comparisons = {}
    for name, saved in assessment["comparisons"].items():
        a, b = name.split("_vs_")
        if a not in complete or b not in complete:
            comparisons[name] = {"pass": None, "missing_jobs": [job for job in (a, b) if job not in complete]}
            continue
        fresh = replay_comparison(complete[a], complete[b], protocol["agreement"])
        if fresh["pass"] != saved["pass"] or fresh["crossing_pass_per_world"] != saved["crossing_pass_per_world"]:
            raise AssertionError("Comparison verdict or crossing replay disagrees")
        for key, field in fresh["fields"].items():
            if field["pass"] != saved["fields"][key]["pass"]:
                raise AssertionError("Field verdict replay disagrees")
            for values, saved_key in [("max_error_deg", "max_error_deg"),
                                      ("allowed_error_deg", "allowed_error_deg")]:
                if not np.allclose([row[values] for row in field["worlds"]],
                                   saved["fields"][key][saved_key], rtol=0, atol=1e-10):
                    raise AssertionError("Comparison numeric replay disagrees")
        comparisons[name] = fresh
    for rel in ["scripts/experiments/newton/campaign/core.py",
                "scripts/experiments/newton/campaign/report.py",
                "scripts/experiments/newton/campaign/worker.py"]:
        inputs[rel] = digest(ROOT / rel)
    return {"schema": 1, "generated_utc": datetime.now(timezone.utc).isoformat(),
            "scope": "Retrospective saved-evidence diagnosis; original verdict unchanged; no GPU run",
            "protocol_sha256": protocol_digest, "original_verdict": assessment["verdict"],
            "comparison_replay_matches": True, "comparisons": comparisons,
            "run_diagnostics": run_diagnostics,
            "input_sha256": inputs,
            "diagnostic_script_sha256": digest(Path(__file__))}


if __name__ == "__main__":
    payload = run()
    destination = Path(__file__).with_name("saved_campaign_diagnostics.json")
    destination.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"comparison_replay_matches": payload["comparison_replay_matches"],
                      "original_verdict": payload["original_verdict"],
                      "completed_runs_inspected": len(payload["run_diagnostics"]),
                      "states_inspected": sum(row["independent_readout"]["monthly_states_inspected"]
                                              for row in payload["run_diagnostics"].values())}, indent=2))
    print(destination)
