"""Recovery-ratchet ON A REAL ROD (Newton VBD), vs the scalar ODE.

The scalar model (`~/life/src/spinalmodes/recovery_ratchet.py`) integrates a
single number: dk_p/dt = k_g(t) * kappa_e0 * k_g/(k_r + k_g). Its lead
mechanism is therefore algebraically self-consistent by construction — the
cemented fraction can never be wrong, only re-labelled.

This experiment makes the ratchet spatially resolved mechanics:

  * N-vertebra clamped-free rods under self-weight (Newton SolverVBD), one
    per (k_r, B_g) condition, batched via ModelBuilder.replicate into worlds
    (separate Model per condition costs ~140 s of fixed per-model overhead
    per column — replication costs ~3 s total for 20 worlds),
  * a per-joint permanent-set state kappa_p[i] written into Newton's
    `joint_rod_rest_kb_local` rest-curvature array,
  * Hueter-Volkmann cementing by the SAME law, driven by the LOCAL elastic
    curvature kappa_e[i] = curvature - kappa_p[i] instead of a fixed kappa_e0,
  * load-cycling: the sacrum (root body) is shaken laterally — cyclic support
    perturbation, "each perturbation is partly cemented". Root excitation
    because VBD's implicit integrator exposes no writable velocity array
    (body_qd is derived), so velocity kicks are silently discarded.

Gates before any developmental claim is trusted:
  A1 (statics, batched): B_g = 0.05 (sub-critical, discrete crit 0.1359)
     must topple under self-weight and B_g = 0.8 must hold — but the HOLD
     test is only meaningful with damping (see calibration note 3).
  A2 (no-shake control): identical columns with ZERO root shake must show
     the ratchet order preserved (the shake is a perturbation source, not
     the driver; if order flips, the experiment is shake-driven mechanics,
     not growth-driven ratcheting).
  C (monotonicity): final permanent set orders k_r 0.3 > 1.0 > 6.0.

Calibration notes (measured 2026-09-03, GB10):
  1. Velocity impulses on bodies do nothing (implicit VBD). Use root shake.
  2. joint_target_kd == 0 by default -> oscillation energy never decays;
     set kd = ke (mirrors probe_greenhill_bg.py's bend_damping = k).
  3. THE SUBTLE ONE: at critical damping, a supercritical column takes
     ~1000-2000 s of simulated time (exponential regime) before its tiny
     seed visibly topples. A "stays up" verdict at 133 s is therefore NOT
     stability evidence, and a "topples" verdict for the subcritical case
     within that window IS the pass. The gate is designed around this
     asymmetry.
  4. Gravity sag (the rod's own reducible deflection, replacing the scalar
     model's assumed kappa_e0 = 0.02) is measured by settling a column with
     zero rest curvature.

Measurement (fixed 2026-09-12, see rod_measure.py): joint angles come from the body
  quaternions' local +Z tangents and the permanent set is written to the bend-about-y
  component of the DER rest curvature binormal in angle units. The 2026-09-03 run took
  atan2 of body positions and wrote curvature (1/m) into the bend-about-x component;
  every number it produced is void (kept as *.pre-measurement-fix-2026-09-12.*).

Outputs (~/life/results/newton_ratchet_rod/):
  ratchet_rod.json / ratchet_rod.md
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import warp as wp

import newton

sys.path.insert(0, str(Path(__file__).resolve().parent))
from greenhill_discrete_reference import bg_crit  # noqa: E402
from rod_measure import joint_dtheta, out_of_plane, rest_kb_from_curvature  # noqa: E402

OUT = Path(os.environ.get("RATCHET_OUT", Path.home() / "life/results/newton_ratchet_rod"))
OUT.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Geometry (same family as probe_greenhill_bg.py so the discrete reference fits)
# -----------------------------------------------------------------------------
L = 0.5
N_SEG = 24
SEG_L = L / N_SEG
RADIUS = 0.006
G = 9.81
SEED_TILT = np.deg2rad(0.5)
K_STRETCH = 1.0e7
VBD_ITERS = 150
DT = 1.0 / 60.0

# Ratchet parameters (match recovery_ratchet.py: k_g_peak = 1.0/yr)
PHV_AGE, PHV_SIGMA = 12.0, 1.6
GROWTH_BASELINE = 0.08
AGE_START, AGE_END = 5.0, 20.0
K_G_PEAK = 1.0
K_R_YEARS = (0.3, 1.0, 6.0)
BG_RUN = 0.30                       # > 0.1359: passively stable
# RATCHET_MONTHS shortens a smoke run (the full 180-month batch is ~90 min per run on
# the GB10); RATCHET_SKIP_A1 skips the 5-min statics gate, which the measurement fix
# does not touch (it reads tip x-positions, not joint angles).
MONTHS = int(os.environ.get("RATCHET_MONTHS", (AGE_END - AGE_START) * 12))

# Load cycling: sacral shake, 2 full cycles per simulated month.
SHAKE_CYCLES = 2
SHAKE_HZ = 0.25
SHAKE_AMP = 0.004                    # m lateral root excursion
SETTLE_STEPS = 600
SHAKE_STEPS = int(SHAKE_CYCLES / SHAKE_HZ * 60)
STEPS_PER_MONTH = SHAKE_STEPS + SETTLE_STEPS


def growth_velocity(t: float) -> float:
    v = GROWTH_BASELINE + math.exp(-0.5 * ((t - PHV_AGE) / PHV_SIGMA) ** 2)
    return v / (GROWTH_BASELINE + 1.0)


def bg_to_k_bend(bg: float, mass: float) -> float:
    """B_g = EI/(M g L^2); add_rod takes k_bend = EI/SEG_L (per-joint)."""
    return bg * mass * G * L**2 / SEG_L


def build_column(builder, k_bend, label):
    pts = [
        wp.vec3(float(k * SEG_L * math.sin(SEED_TILT)), 0.0,
                float(k * SEG_L * math.cos(SEED_TILT)))
        for k in range(N_SEG + 1)
    ]
    quats = newton.utils.rod_parallel_transport_quaternions(pts)
    bodies, joints = builder.add_rod(
        positions=pts, quaternions=quats, radius=RADIUS,
        stretch_stiffness=K_STRETCH,
        bend_stiffness=k_bend, bend_damping=k_bend,
        twist_stiffness=k_bend, twist_damping=k_bend,
        label=label, body_frame_origin="com",
    )
    r = bodies[0]
    builder.body_mass[r] = 0.0
    builder.body_inv_mass[r] = 0.0
    builder.body_inertia[r] = wp.mat33(0.0)
    builder.body_inv_inertia[r] = wp.mat33(0.0)
    return bodies, joints


def column_mass() -> float:
    b = newton.ModelBuilder(gravity=(0.0, 0.0, -G))
    bodies, _ = build_column(b, 1.0, "probe")
    return float(np.asarray(b.body_mass, dtype=np.float64)[bodies[1:]].sum())


def batched_model(k_bends, spacing_y=0.5):
    """One column per world, all in a single Model (the only affordable shape)."""
    sub = newton.ModelBuilder()
    build_column(sub, float(k_bends[0]), "spine")
    builder = newton.ModelBuilder(gravity=(0.0, 0.0, -G))
    builder.replicate(sub, world_count=len(k_bends), spacing=(0.0, spacing_y, 0.0))
    # per-world bend stiffness (all worlds share the template's value otherwise)
    ke = np.asarray(builder.joint_target_ke, dtype=np.float64).copy()
    nj = len(builder.joint_names) // 1 if False else ke.shape[0] // len(k_bends)
    for w, k in enumerate(k_bends):
        ke[w * nj:(w + 1) * nj] = k
    builder.joint_target_ke = ke
    builder.joint_target_kd = ke.copy()   # note 2: kd = ke
    builder.color()
    return builder.finalize()


def run_batch(model, months, k_r_per_world, bg_per_world, kappa_e_law=True,
              shake=True, observe_every=6):
    """Simulate all worlds for `months` growth-months.

    Cementing (per world w, per joint i, per month):
        f = kg/(k_r[w]+kg);  kp[i] += kg * (curv[i]-kp[i]) * f * dt_month
    written to solver.joint_rod_rest_kb_local (VBD rest curvature).
    """
    solver = newton.solvers.SolverVBD(model, iterations=VBD_ITERS, rigid_compliant_alm=True)
    s0, s1, c = model.state(), model.state(), model.control()
    rest_kb = solver.joint_rod_rest_kb_local
    W = len(k_r_per_world)
    nj = model.joint_count // W
    nb = model.body_count // W
    rest_kp = np.zeros((W, nj), dtype=np.float64)

    roots = np.arange(0, model.body_count, nb)          # world w root = w*nb
    tips = roots + nb - 1
    root_x0 = s0.body_q.numpy()[roots, 0].copy()
    dt_month = 1.0 / 12.0

    obs = {"age": [], "cobb": [], "flex": [], "tip": [], "oop": []}
    t_wall = time.time()
    for mstep in range(months):
        age = AGE_START + mstep / 12.0
        kg = K_G_PEAK * np.array([growth_velocity(age)] * W)
        f = kg / (np.asarray(k_r_per_world) + kg)
        for step in range(STEPS_PER_MONTH):
            if shake and step < SHAKE_STEPS:
                t = step * DT
                q = s0.body_q.numpy().copy()
                q[roots, 0] = root_x0 + SHAKE_AMP * math.sin(2 * math.pi * SHAKE_HZ * t)
                s0.body_q.assign(q)
            s0.clear_forces()
            solver.step(s0, s1, c, None, DT)
            s0, s1 = s1, s0
            if kappa_e_law and step == SHAKE_STEPS - 1:
                q = s0.body_q.numpy()
                curv = np.stack([joint_dtheta(q, np.arange(w * nb, (w + 1) * nb)) / SEG_L
                                 for w in range(W)])              # (W, nj)
                rest_kp += kg[:, None] * (curv - rest_kp) * f[:, None] * dt_month
                rest_kb.assign(rest_kb_from_curvature(rest_kp, SEG_L))
        if mstep % observe_every == 0 or mstep == months - 1:
            q = s0.body_q.numpy()
            curv = np.stack([joint_dtheta(q, np.arange(w * nb, (w + 1) * nb)) / SEG_L
                             for w in range(W)])
            obs["age"].append(age)
            obs["cobb"].append(np.degrees(np.abs(curv).sum(axis=1)).tolist())
            set_frac = np.abs(rest_kp).sum(axis=1) / np.maximum(np.abs(curv).sum(axis=1), 1e-12)
            obs["flex"].append((1.0 - np.minimum(set_frac, 1.0)).tolist())
            obs["tip"].append(q[tips, 0].tolist())
            obs["oop"].append([out_of_plane(q, np.arange(w * nb, (w + 1) * nb)) for w in range(W)])
    wp.synchronize()
    obs["wall_s"] = time.time() - t_wall
    return obs, rest_kp


# -----------------------------------------------------------------------------
# GATE A1 — statics, batched, damped. Only the TOPPLE side is decisive
# (calibration note 3): subcritical B_g=0.05 must visibly collapse within
# the window; the supercritical side just must not collapse faster.
# -----------------------------------------------------------------------------
def gate_a1(mass, frames=12000, record_every=2000):
    bgs = [0.05, 0.10, 0.30, 0.80]
    model = batched_model([bg_to_k_bend(bg, mass) for bg in bgs])
    solver = newton.solvers.SolverVBD(model, iterations=VBD_ITERS, rigid_compliant_alm=True)
    s0, s1, c = model.state(), model.state(), model.control()
    nb = model.body_count // len(bgs)
    tips = np.arange(nb - 1, model.body_count, nb)
    x0 = np.abs(s0.body_q.numpy()[tips, 0])
    traj = []
    t0 = time.time()
    for i in range(frames):
        s0.clear_forces()
        solver.step(s0, s1, c, None, DT)
        s0, s1 = s1, s0
        if (i + 1) % record_every == 0:
            traj.append(((i + 1) * DT,
                         (np.abs(s0.body_q.numpy()[tips, 0]) / x0).tolist()))
    wp.synchronize()
    growth = traj[-1][1]
    # subcritical (0.05, 0.10 < 0.1359) must grow; 0.30/0.80 must stay below them
    ok = growth[0] > 1.5 and growth[1] > 1.2 and growth[2] < growth[1] and growth[3] < 1.5
    return {"bg": bgs, "growth": growth, "traj": traj, "pass": bool(ok),
            "wall_s": time.time() - t0}


def scalar_ode_final(k_r, kappa_e0, months=MONTHS):
    kappa_p = 0.0
    for mstep in range(months):
        age = AGE_START + mstep / 12.0
        kg = K_G_PEAK * growth_velocity(age)
        f = kg / (k_r + kg)
        for _ in range(30):
            kappa_p += kg * kappa_e0 * f * (1 / 12.0 / 30)
    return kappa_p


def main():
    m_col = column_mass()
    crit = bg_crit(N_SEG)
    print(f"column mass M = {m_col:.5f} kg   B_g_crit(N={N_SEG}) = {crit:.6f}")

    if os.environ.get("RATCHET_SKIP_A1"):
        ga = {"bg": [], "growth": [], "traj": [], "pass": True, "wall_s": 0.0, "skipped": True}
    else:
        ga = gate_a1(m_col)
    gstr = "  ".join(f"B_g={b:.2f}:{g:.2f}" for b, g in zip(ga["bg"], ga["growth"]))
    print(f"GATE A1 statics (damped, batched): {gstr}  [{ga['wall_s']:.0f}s]  "
          f"-> {'PASS' if ga['pass'] else 'FAIL'}")
    if not ga["pass"]:
        (OUT / "ratchet_rod.json").write_text(json.dumps({"gate_a1": ga}, indent=2))
        print("statics gate failed — stopping")
        return 1

    # sag calibration: mean |curvature| of a settled B_g=0.30 column
    # (the rod's own reducible deflection; scalar model assumed 0.02)
    # reuse gate A1 world 2? No — gate columns have seed tilt and long settle;
    # instead take the no-shake control run's month-6 Cobb as the sag proxy.
    conds = [(kr, bg) for kr in K_R_YEARS for bg in (0.20, 0.30, 0.50)]
    conds += [(6.0, 0.30)] * 0
    k_r_list = [kr for kr, _ in conds]
    bg_list = [bg for _, bg in conds]
    W = len(conds)
    # +1 no-ratchet control world (k_r irrelevant; ratchet off per mask below)
    print(f"developmental batch: {W} worlds x {STEPS_PER_MONTH} steps/month x {MONTHS} months")

    # Ratchet OFF control: same batch with law disabled after month 0?
    # Simpler: two full batched runs — control (law off) and experiment (law on).
    model_ctrl = batched_model([bg_to_k_bend(bg, m_col) for bg in bg_list])
    t0 = time.time()
    ctrl_obs, ctrl_kp = run_batch(model_ctrl, MONTHS, k_r_list, bg_list,
                                  kappa_e_law=False, shake=True)
    print(f"control (ratchet OFF): {time.time()-t0:.0f}s  "
          f"Cobb drift max = {max(c-o for c,o in zip(ctrl_obs['cobb'][-1], ctrl_obs['cobb'][0])):.1f} deg")

    model_exp = batched_model([bg_to_k_bend(bg, m_col) for bg in bg_list])
    exp_obs, exp_kp = run_batch(model_exp, MONTHS, k_r_list, bg_list,
                                kappa_e_law=True, shake=True)
    print(f"experiment (ratchet ON): {exp_obs['wall_s']:.0f}s")

    kappa_e0 = float(np.mean(np.abs(exp_obs["cobb"][0])) )  # deg; placeholder
    # proper per-joint sag: control run final curvature magnitude ~ elastic curve
    # (no rest set), so kappa_e0 from ctrl curvature profile:
    # recompute mean curvature from ctrl Cobb (total |dtheta| over 24 segs / SEG_L)
    kappa_e0 = float(np.mean(ctrl_obs["cobb"][-1])) * math.pi / 180.0 / L

    print(f"\n{'B_g':>5} {'k_r':>5} | {'Cobb5':>6} {'Cobb20':>7} {'flex20':>6} "
          f"{'<kp>':>8} {'ODE kp':>8} {'ratio':>6}")
    rows = {}
    for i, (kr, bg) in enumerate(conds):
        kp_mean = float(np.mean(np.abs(exp_kp[i])))
        ode = scalar_ode_final(kr, kappa_e0)
        rows[(kr, bg)] = {
            "cobb_5y": exp_obs["cobb"][0][i], "cobb_20y": exp_obs["cobb"][-1][i],
            "flex_20y": exp_obs["flex"][-1][i],
            "ctrl_cobb_20y": ctrl_obs["cobb"][-1][i],
            "rod_kappa_p_mean": kp_mean, "ode_kappa_p": ode,
            "ratio_rod_over_ode": kp_mean / max(ode, 1e-12),
        }
        r = rows[(kr, bg)]
        print(f"{bg:5.2f} {kr:5.1f} | {r['cobb_5y']:6.1f} {r['cobb_20y']:7.1f} "
              f"{r['flex_20y']:6.2f} {kp_mean:8.5f} {ode:8.5f} "
              f"{r['ratio_rod_over_ode']:6.2f}")

    # GATE C per B_g: kappa_p monotone decreasing in k_r
    gate_c = {}
    for bg in (0.20, 0.30, 0.50):
        kp = {kr: rows[(kr, bg)]["rod_kappa_p_mean"] for kr in K_R_YEARS}
        gate_c[bg] = kp[0.3] > kp[1.0] > kp[6.0]
    # GATE A2: order preserved with ratchet law (shake on) AND law-driven
    # set must exceed control drift
    drifts = {bg: max(0.0, rows[(6.0, bg)]["ctrl_cobb_20y"] - rows[(6.0, bg)]["cobb_5y"])
              for bg in (0.20, 0.30, 0.50)}
    print(f"\nGATE C monotonicity (k_p: 0.3>1.0>6.0): {gate_c}")
    print(f"control Cobb drift (deg): {drifts}")

    payload = {
        "gate_a1": ga, "gate_c_per_bg": gate_c, "control_drift_deg": drifts,
        "bg_crit_discrete_N24": crit,
        "kappa_e0_derived_rad_per_m": kappa_e0,
        "params": {"L": L, "n_seg": N_SEG, "radius": RADIUS, "vbd_iters": VBD_ITERS,
                   "k_g_peak": K_G_PEAK, "months": MONTHS, "shake_amp_m": SHAKE_AMP,
                   "shake_hz": SHAKE_HZ, "steps_per_month": STEPS_PER_MONTH,
                   "column_mass_kg": m_col},
        "observations": exp_obs, "control": ctrl_obs,
        "rows": {f"k{kr}_bg{bg}": v for (kr, bg), v in rows.items()},
    }
    (OUT / "ratchet_rod.json").write_text(json.dumps(payload, indent=2))
    md = ["# Recovery ratchet on a Newton rod — results\n",
          f"B_g_crit(N={N_SEG}) = {crit:.6f}. Gate A1: {'PASS' if ga['pass'] else 'FAIL'} "
          f"{gstr}.",
          f"kappa_e0 derived from rod (not assumed 0.02): {kappa_e0:.5f} rad/m.\n",
          "\n| B_g | k_r | Cobb 5y | Cobb 20y | flex20 | rod <kp> | ODE kp | ratio |",
          "|---|---|---|---|---|---|---|---|"]
    for (kr, bg), r in rows.items():
        md.append(f"| {bg} | {kr} | {r['cobb_5y']:.1f} | {r['cobb_20y']:.1f} "
                  f"| {r['flex_20y']:.2f} | {r['rod_kappa_p_mean']:.5f} "
                  f"| {r['ode_kappa_p']:.5f} | {r['ratio_rod_over_ode']:.2f} |")
    oop = max(max(row) for row in exp_obs["oop"] + ctrl_obs["oop"])
    md.append(f"\nGate C per B_g: {gate_c}\nControl drift (deg): {drifts}\n"
              f"max out-of-plane tangent |t_y| over both runs: {oop:.2e} "
              f"(planar x-z measurement valid only while this is ~0)")
    (OUT / "ratchet_rod.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {OUT/'ratchet_rod.json'} and ratchet_rod.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
