"""Diagnostic: does a Newton VBD rod hold up under its own weight?

Horizontal cantilever, Newton's own example geometry, gravity ON, no tip force.
Analytic self-weight tip deflection: delta = q L^4 / (8 EI), with EI = k_bend * seg_L.
"""
import numpy as np, warp as wp, newton

N, SEG, R = 16, 0.10, 0.01
Lc = N * SEG
G = 9.81

def run(k_bend, iterations, substeps, frames, root_kinematic=True):
    b = newton.ModelBuilder(gravity=(0.0, 0.0, -G))
    pts = newton.utils.cable_straight_points(
        start=wp.vec3(0.0, 0.0, 0.0), direction=wp.vec3(1.0, 0.0, 0.0),
        length=Lc, num_segments=N)
    quats = newton.utils.rod_parallel_transport_quaternions(pts)
    bodies, joints = b.add_rod(positions=pts, quaternions=quats, radius=R,
        stretch_stiffness=1.0e6, bend_stiffness=k_bend, bend_damping=k_bend,
        twist_stiffness=k_bend*0.77, twist_damping=k_bend*0.77,
        label="cant", body_frame_origin="com")
    if root_kinematic:
        r = bodies[0]
        b.body_mass[r] = 0.0; b.body_inv_mass[r] = 0.0
        b.body_inertia[r] = wp.mat33(0.0); b.body_inv_inertia[r] = wp.mat33(0.0)
    b.color()
    m = b.finalize()
    mass = m.body_mass.numpy()
    total = float(mass[bodies[1:]].sum())
    s = newton.solvers.SolverVBD(m, iterations=iterations, rigid_compliant_alm=True)
    s0, s1, c = m.state(), m.state(), m.control()
    dt = 1.0/60.0/substeps
    z0 = float(s0.body_q.numpy()[bodies[-1]][2])
    root_z0 = float(s0.body_q.numpy()[bodies[0]][2])
    for _ in range(frames):
        for _ in range(substeps):
            s0.clear_forces(); s.step(s0, s1, c, None, dt); s0, s1 = s1, s0
    wp.synchronize()
    q = s0.body_q.numpy()
    return total, z0 - float(q[bodies[-1]][2]), root_z0 - float(q[bodies[0]][2])

for k in (900.0, 90.0, 9.0):
    EI = k * SEG
    for it, ss, fr in ((20, 10, 480), (60, 20, 480)):
        M, tip, root = run(k, it, ss, fr)
        q = M * G / Lc
        analytic = q * Lc**4 / (8.0 * EI)
        print(f"k={k:7.1f} EI={EI:6.2f}  iter={it:3d} sub={ss:3d} | "
              f"M={M:.4f}kg  tip_droop={tip*1000:9.2f}mm  analytic={analytic*1000:8.2f}mm  "
              f"ratio={tip/analytic:7.2f}  root_moved={root*1000:7.3f}mm")
