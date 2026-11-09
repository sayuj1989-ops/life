"""Reproducible gravity-torque identities on synthetic centerlines.

This checks external-load geometry only. It does not solve spinal equilibrium,
model growth, identify tissue parameters, or predict treatment response.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]


def axial_gravity_moment(points, segment_masses, gravity=9.81):
    """Distal gravitational moment projected onto each segment tangent [N m].

    Points are in metres, segment masses in kg, and gravity in m/s^2 along -z.
    Each segment's weight acts at its midpoint. Cuts lie at segment starts.
    This is an external moment requiring balance, not vertebral rotation.
    """
    points = np.asarray(points, dtype=float)
    masses = np.asarray(segment_masses, dtype=float)
    if (points.ndim != 2 or points.shape[1] != 3 or len(points) < 3
            or masses.shape != (len(points) - 1,)
            or not np.isfinite(points).all() or not np.isfinite(masses).all()
            or (masses < 0).any() or not math.isfinite(gravity) or gravity < 0):
        raise ValueError("Require finite 3D points, nonnegative segment masses and gravity")
    segments = np.diff(points, axis=0)
    lengths = np.linalg.norm(segments, axis=1)
    if (lengths == 0).any():
        raise ValueError("Centerline segments must have positive length")
    tangents = segments / lengths[:, None]
    midpoints = (points[:-1] + points[1:]) / 2
    distal_mass = np.cumsum(masses[::-1])[::-1]
    distal_first_moment = np.cumsum((masses[:, None] * midpoints)[::-1], axis=0)[::-1]
    lever_mass = distal_first_moment - points[:-1] * distal_mass[:, None]
    moment = np.cross(lever_mass, np.array([0., 0., -gravity]))
    return np.einsum("ij,ij->i", tangents, moment)


def helix(segments, *, radius=.025, height=.5, turns=1.):
    z = np.linspace(0., height, segments + 1)
    phase = 2 * np.pi * turns * z / height
    return np.column_stack((radius * np.cos(phase), radius * np.sin(phase), z))


def analytic_helix_base_torque(*, mass=30., radius=.025, height=.5, turns=1., gravity=9.81):
    """Closed form for uniform mass per unit height on a smooth circular helix."""
    k = 2 * np.pi * turns / height
    return mass / height * gravity * radius**2 / math.sqrt(1 + (radius * k)**2) * (
        math.sin(k * height) - k * height)


def source_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    n, mass = 256, 30.
    z = np.linspace(0., .5, n + 1)
    masses = np.full(n, mass / n)
    straight = np.column_stack((0 * z, 0 * z, z))
    sagittal = np.column_stack((.03 * np.sin(2 * np.pi * z / .5), 0 * z, z))
    rigid_angle = .73
    c, s = np.cos(rigid_angle), np.sin(rigid_angle)
    rotation = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.]])
    rotated_plane = sagittal @ rotation.T
    spatial = helix(n)
    reflected = spatial * np.array([1., -1., 1.])
    torque = axial_gravity_moment(spatial, masses)
    controls = {
        "straight_max_abs_Nm": float(np.max(np.abs(axial_gravity_moment(straight, masses)))),
        "sagittal_plane_max_abs_Nm": float(np.max(np.abs(axial_gravity_moment(sagittal, masses)))),
        "rotated_vertical_plane_max_abs_Nm": float(np.max(np.abs(axial_gravity_moment(rotated_plane, masses)))),
        "zero_gravity_max_abs_Nm": float(np.max(np.abs(axial_gravity_moment(spatial, masses, 0.)))),
        "mirror_max_abs_sum_Nm": float(np.max(np.abs(torque + axial_gravity_moment(reflected, masses)))),
        "double_gravity_max_abs_error_Nm": float(np.max(np.abs(2 * torque - axial_gravity_moment(spatial, masses, 19.62)))),
        "translation_max_abs_error_Nm": float(np.max(np.abs(torque - axial_gravity_moment(spatial + np.array([.2, -.1, .3]), masses)))),
    }
    expected = analytic_helix_base_torque()
    refinement = []
    for segments in [32, 64, 128, 256, 512, 1024]:
        measured = float(axial_gravity_moment(helix(segments), np.full(segments, mass / segments))[0])
        refinement.append({"segments": segments, "base_torque_Nm": measured,
                           "analytic_error_Nm": abs(measured - expected)})
    errors = [row["analytic_error_Nm"] for row in refinement]
    analytic_pass = all(a > b for a, b in zip(errors, errors[1:])) and errors[-1] < 1e-4
    controls_pass = all(value < 1e-10 for value in controls.values())
    if not controls_pass or not analytic_pass:
        raise AssertionError({"controls": controls, "refinement": refinement})

    # Extract only the existing scalar formula; avoid package import side effects.
    iec_path = ROOT / "src/spinalmodes/iec.py"
    tree = ast.parse(iec_path.read_text())
    node = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name == "compute_helical_threshold")
    namespace = {}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(iec_path), "exec"), namespace)
    threshold = namespace["compute_helical_threshold"]
    campaign_dir = ROOT / "results/newton_mechanism_campaign_2026-09-12"
    campaign_path = campaign_dir / "campaign.json"
    assessment_path = campaign_dir / "assessment.json"
    campaign = json.loads(campaign_path.read_text())
    assessment = json.loads(assessment_path.read_text())
    sealed = campaign.get("source_hashes", assessment.get("source_sha256", {}))
    source_checks = {}
    for path, digest in sealed.items():
        absolute = Path(path) if Path(path).is_absolute() else ROOT / path
        if absolute.is_file():
            source_checks[path] = source_digest(absolute) == digest
    return {
        "schema": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Synthetic external gravity-torque identities; no growth/equilibrium/clinical inference",
        "backend": "numpy CPU; GPU validation unavailable in this session",
        "synthetic_parameters": {"mass_kg": mass, "radius_m": .025, "height_m": .5, "turns": 1.,
                                 "gravity_m_s2": 9.81, "mass_distribution": "uniform per unit height"},
        "controls": controls, "controls_pass": controls_pass,
        "synthetic_helix_max_abs_torque_Nm": float(np.max(np.abs(torque))),
        "analytic_base_torque_Nm": expected,
        "refinement": refinement, "analytic_refinement_pass": analytic_pass,
        "legacy_helical_threshold_audit": {
            "arguments": [arg.arg for arg in node.args.args],
            "contains_gravity_growth_geometry_or_material_inputs": False,
            "case_delta_b_0_gradient_0_chi_0": threshold(0., 0., 0.),
            "case_delta_b_0_gradient_1_chi_0_05": threshold(0., 1., .05),
            "interpretation": "Existing heuristic is not an identified physical instability boundary",
        },
        "saved_campaign": {
            "status": campaign["status"], "heartbeat_utc": campaign.get("heartbeat_utc"),
            "verdict": assessment["verdict"], "active_hours": assessment.get("active_hours"),
            "completed_jobs": assessment.get("completed_jobs"),
            "comparison_passes": {name: row.get("pass") for name, row in assessment["comparisons"].items()},
            "file_source_seals": source_checks,
            "directory_dependency_seals_checked": False,
        },
        "sha256": {str(path.relative_to(ROOT)): source_digest(path) for path in
                   [Path(__file__).resolve(), iec_path, campaign_path, assessment_path]},
    }


if __name__ == "__main__":
    payload = run()
    output = Path(__file__).with_name("gravity_torque_checks.json")
    output.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    print(json.dumps({key: payload[key] for key in ["controls_pass", "analytic_refinement_pass",
          "synthetic_helix_max_abs_torque_Nm", "analytic_base_torque_Nm"]}, indent=2))
    print(output)
