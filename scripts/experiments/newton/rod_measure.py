"""Pure-numpy curvature measurement for Newton rod columns (no warp import, so it is
unit-testable in the plain ~/life venv).

Frame facts this relies on (newton/_src/utils/cable.py, builder.add_rod, and the VBD
rod kernels `_measure_rod_bend_twist_z` / `init_rod_rest_bend_twist`):
  * add_rod aligns each capsule's local +Z with its segment direction, so the segment
    tangent is R(q)·ẑ from the body quaternion — not a difference of body positions
    (with body_frame_origin="com" the origins sit at segment midpoints, and the original
    atan2(px, py) measured each body's azimuth about the vertical, which is meaningless).
  * The joint's bend strain is the DER finite curvature binormal kb = 2 t0×t1/(1+t0·t1)
    (an angle-like vector per joint, NOT a curvature in 1/m), expressed in the parent
    segment's local frame; components 0/1 are bend, 2 is twist.
  * A column tilted and shaken in the world x–z plane bends about +y. Parallel transport
    from +Z through rotations about y keeps local y = world y, so that bend lives in
    component 1 of kb. The original experiment wrote component 0 (bend about local x,
    the y–z plane the load never enters).
"""
from __future__ import annotations

import numpy as np


def segment_tangents(body_q, body_ids):
    """Unit tangent of each segment, R(q)·ẑ with q = (x, y, z, w) from body_q[:, 3:7]."""
    q = np.asarray(body_q, dtype=np.float64)[body_ids][:, 3:7]
    x, y, z, w = q.T
    return np.stack([2.0 * (x * z + w * y), 2.0 * (y * z - w * x), 1.0 - 2.0 * (x * x + y * y)], axis=1)


def joint_dtheta(body_q, body_ids):
    """Signed bend angle at each joint in the x–z plane (rotation about +y), one per joint
    (N segments -> N-1 joints). Positive = tangent rotating from +z toward +x."""
    t = segment_tangents(body_q, body_ids)
    return np.diff(np.unwrap(np.arctan2(t[:, 0], t[:, 2])))


def out_of_plane(body_q, body_ids) -> float:
    """max |t_y|: the planar dtheta above is only meaningful while this stays ~0."""
    return float(np.abs(segment_tangents(body_q, body_ids)[:, 1]).max())


def rest_kb_from_curvature(rest_kp, seg_l):
    """(n_joints, 3) parent-local rest curvature-binormal for a per-joint permanent-set
    curvature rest_kp [1/m]: kb_y = 2 tan(dθ/2) with dθ = rest_kp·seg_l, sign-matched to
    joint_dtheta (kb = 2 t0×t1/(1+t0·t1) has only a +y component for x–z bending)."""
    kp = np.asarray(rest_kp, dtype=np.float64).reshape(-1)
    kb = np.zeros((kp.size, 3), dtype=np.float64)
    kb[:, 1] = 2.0 * np.tan(0.5 * kp * seg_l)
    return kb
