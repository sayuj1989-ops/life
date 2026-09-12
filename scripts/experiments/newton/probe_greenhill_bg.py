"""Does Newton's VBD rod reproduce the Allometric-Trap threshold, and is it
solver-independent?

The manuscript asserts a passive-stability boundary at B_g = EI/(MgL^2) ~ 0.1.
Greenhill's self-buckling criterion for a clamped-free column loaded by its own
weight gives that constant exactly: (qL)_crit = 7.8373 EI/L^2, so
B_g_crit = 1/7.8373 = 0.12759.

Slightly-tilted vertical columns, one per B_g, settled under self-weight; a
column has collapsed if the seed imperfection grows instead of recoiling.
The sweep is repeated at several VBD iteration counts, because an
under-converged VBD chain is artificially compliant and moves the threshold.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import warp as wp

import newton

GREENHILL = 7.837347

L = 0.5
N_SEG = 24
SEG_L = L / N_SEG
RADIUS = 0.006
G = 9.81
SEED_TILT = np.deg2rad(0.5)
Y_SEP = 0.25


def _points(y: float):
    return [
        wp.vec3(float(k * SEG_L * np.sin(SEED_TILT)), float(y), float(k * SEG_L * np.cos(SEED_TILT)))
        for k in range(N_SEG + 1)
    ]


def _add_column(builder, y: float, bend_k: float, label: str):
    pts = _points(y)
    quats = newton.utils.rod_parallel_transport_quaternions(pts)
    bodies, _ = builder.add_rod(
        positions=pts, quaternions=quats, radius=RADIUS,
        stretch_stiffness=1.0e7,
        bend_stiffness=bend_k, bend_damping=bend_k,
        twist_stiffness=bend_k, twist_damping=bend_k,
        label=label, body_frame_origin="com",
    )
    r = bodies[0]
    builder.body_mass[r] = 0.0
    builder.body_inv_mass[r] = 0.0
    builder.body_inertia[r] = wp.mat33(0.0)
    builder.body_inv_inertia[r] = wp.mat33(0.0)
    return bodies


def column_mass() -> float:
    b = newton.ModelBuilder(gravity=(0.0, 0.0, -G))
    bodies = _add_column(b, 0.0, 1.0, "probe")
    return float(np.asarray(b.body_mass, dtype=np.float64)[bodies[1:]].sum())


def sweep(bg_values, k_bend, iterations, substeps, frames):
    builder = newton.ModelBuilder(gravity=(0.0, 0.0, -G))
    rods = [
        _add_column(builder, (i - (len(k_bend) - 1) * 0.5) * Y_SEP, float(k), f"c{i}")
        for i, k in enumerate(k_bend)
    ]
    builder.color()
    model = builder.finalize()
    solver = newton.solvers.SolverVBD(model, iterations=iterations, rigid_compliant_alm=True)
    s0, s1, c = model.state(), model.state(), model.control()
    dt = 1.0 / 60.0 / substeps
    tips = [int(b[-1]) for b in rods]
    q0 = s0.body_q.numpy()
    x0 = np.array([q0[t][0] for t in tips])

    t0 = time.time()
    for _ in range(frames):
        for _ in range(substeps):
            s0.clear_forces()
            solver.step(s0, s1, c, None, dt)
            s0, s1 = s1, s0
    wp.synchronize()
    el = time.time() - t0
    q = s0.body_q.numpy()
    x = np.array([q[t][0] for t in tips])
    return np.abs(x) / np.abs(x0), el


def main() -> int:
    bg_values = np.array([0.02, 0.04, 0.06, 0.08, 0.10, 0.1276, 0.16, 0.20,
                          0.26, 0.34, 0.45, 0.60, 0.80, 1.10, 1.50, 2.20, 3.50, 6.00])
    m_col = column_mass()
    k_bend = bg_values * m_col * G * L**2 / SEG_L

    print(f"column mass M = {m_col:.5f} kg  L = {L} m  {N_SEG} x {SEG_L*1000:.1f} mm segments")
    print(f"Greenhill prediction: B_g_crit = 1/{GREENHILL:.4f} = {1/GREENHILL:.5f}\n")

    configs = [(24, 10, 500), (60, 20, 500), (150, 20, 500), (400, 20, 500)]
    table, brackets = {}, {}
    for iters, subs, frames in configs:
        growth, el = sweep(bg_values, k_bend, iters, subs, frames)
        table[iters] = growth
        stable = bg_values[growth < 1.1]
        collapsed = bg_values[growth > 1.5]
        if len(collapsed) and len(stable):
            lo = float(collapsed.max())
            above = stable[stable > lo]
            hi = float(above.min()) if len(above) else float("nan")
        else:
            lo, hi = float("nan"), float("nan")
        brackets[iters] = (lo, hi)
        print(f"iter={iters:4d} sub={subs:3d}  {len(bg_values)} columns x {frames*subs} steps "
              f"in {el:5.1f}s   threshold bracket: {lo:.4f} < B_g_crit <= {hi:.4f}")

    print(f"\n{'B_g':>8} " + " ".join(f"{'it'+str(i):>10}" for i in table))
    for j, b in enumerate(bg_values):
        row = " ".join(f"{table[i][j]:10.2f}" for i in table)
        print(f"{b:8.4f} {row}")
    print("\n(values are seed growth: >1.5 collapsed, <1.1 recoiled)")

    los = [brackets[i][0] for i in brackets if np.isfinite(brackets[i][0])]
    if len(los) > 1:
        print(f"\nthreshold lower bound across iteration counts: "
              f"{min(los):.4f} -> {max(los):.4f}  ({max(los)/min(los):.1f}x drift)")
    print(f"Greenhill 1/7.8373 = {1/GREENHILL:.5f}")

    out = Path("/home/sayuj/life/results/newton_greenhill")
    out.mkdir(parents=True, exist_ok=True)
    (out / "greenhill_bg.json").write_text(json.dumps({
        "L": L, "n_seg": N_SEG, "column_mass_kg": m_col, "seed_tilt_deg": 0.5,
        "greenhill_bg_crit": 1 / GREENHILL, "bg": bg_values.tolist(),
        "k_bend": k_bend.tolist(),
        "growth_by_iterations": {str(k): v.tolist() for k, v in table.items()},
        "brackets_by_iterations": {str(k): list(v) for k, v in brackets.items()},
        "newton": newton.__version__, "warp": wp.__version__,
    }, indent=2))
    print(f"\nwrote {out/'greenhill_bg.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
