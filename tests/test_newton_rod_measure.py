"""Pins the rod curvature measurement that the Newton ratchet experiment consumes.
The 2026-09-03 run reported a 15,628° Cobb angle because joint_dtheta took atan2 of body
positions; these tests make the tangent-based replacement fail loudly if it regresses."""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "experiments" / "newton"))
from rod_measure import joint_dtheta, out_of_plane, rest_kb_from_curvature, segment_tangents  # noqa: E402

SEG_L = 0.5 / 24


def _body_q_from_angles(thetas, axis="y"):
    """body_q rows (px,py,pz, qx,qy,qz,qw) for segments whose tangent is ẑ rotated by
    theta about `axis`; positions are deliberately garbage to prove they are unused."""
    rows = []
    for th in thetas:
        s, c = math.sin(th / 2), math.cos(th / 2)
        q = (0.0, s, 0.0, c) if axis == "y" else (s, 0.0, 0.0, c)
        rows.append([np.random.uniform(-9, 9), np.random.uniform(-9, 9), np.random.uniform(-9, 9), *q])
    return np.array(rows)


def test_straight_tilted_rod_has_zero_joint_angles():
    tilt = math.radians(0.5)
    bq = _body_q_from_angles([tilt] * 24)
    t = segment_tangents(bq, np.arange(24))
    assert np.allclose(t, [[math.sin(tilt), 0.0, math.cos(tilt)]] * 24, atol=1e-12)
    assert np.allclose(joint_dtheta(bq, np.arange(24)), 0.0, atol=1e-12)
    assert out_of_plane(bq, np.arange(24)) < 1e-12


def test_circular_arc_recovers_its_curvature_with_sign():
    R = 2.0
    thetas = np.arange(24) * SEG_L / R
    d = joint_dtheta(_body_q_from_angles(thetas), np.arange(24))
    assert d.shape == (23,)
    assert np.allclose(d / SEG_L, 1.0 / R, rtol=1e-9)
    d_neg = joint_dtheta(_body_q_from_angles(-thetas), np.arange(24))
    assert np.allclose(d_neg / SEG_L, -1.0 / R, rtol=1e-9)


def test_rest_kb_is_an_angle_in_the_bend_about_y_component():
    kb = rest_kb_from_curvature(np.full(23, 1.0 / 2.0), SEG_L)
    assert kb.shape == (23, 3)
    assert np.all(kb[:, 0] == 0.0) and np.all(kb[:, 2] == 0.0)
    assert np.allclose(kb[:, 1], 2 * math.tan(0.5 * SEG_L / 2.0))
    assert np.allclose(kb[:, 1], SEG_L / 2.0, rtol=1e-4)      # small-angle: an angle, not 1/m


def test_out_of_plane_bend_is_flagged():
    bq = _body_q_from_angles([0.1] * 24, axis="x")
    assert out_of_plane(bq, np.arange(24)) > 0.09
