import csv
import os
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Ensure src is in path
sys.path.append(os.getcwd())

from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from scripts.experiments.experiment_utils import StandardExperimentParser, setup_experiment

def define_squat_stand_trajectory(T_cycle, num_steps, L, min_theta_deg=0.0):
    """
    Defines the kinematic and informational trajectory of a squat-to-stand cycle.
    T_cycle: Total time of one cycle (seconds).
    min_theta_deg: The minimum theta representing the depth of the squat. 0=floor, 45=chair.
    theta(t): from 90° (standing, gravity parallel) to min_theta_deg and back.
    I(s, t): morphs from S-curve to C-curve field based on depth.
    """
    t_vals = np.linspace(0, T_cycle, num_steps)
    s = np.linspace(0, L, 200)

    # Base Fields
    I_standing = np.sin(2 * np.pi * s / L)**2  # S-curve
    I_squatting = np.sin(np.pi * s / L)**2     # C-curve

    trajectory = []
    # Calculate how much of a full squat this is (0 to 1)
    depth_ratio = (90.0 - min_theta_deg) / 90.0

    for t in t_vals:
        # Phase goes from 0 to 1 to 0 (squat down then stand up)
        phase = 0.5 * (1 - np.cos(2 * np.pi * t / T_cycle))

        # Theta interpolation (degrees)
        theta_deg = 90.0 - phase * (90.0 - min_theta_deg)

        # Info field interpolation based on effective phase
        effective_phase = phase * depth_ratio
        I_t = (1 - effective_phase) * I_standing + effective_phase * I_squatting
        dIds_t = np.gradient(I_t, s)
        info_t = InfoField1D(s=s, I=I_t, dIds=dIds_t)

        trajectory.append({
            'time': t,
            'theta_deg': theta_deg,
            'info': info_t,
            'phase': phase
        })

    return trajectory

def compute_cycle_dissipation(trajectory, base_params, L, n_elements, E0, radius, rho, gravity_magnitude):
    """
    Quasi-static stepping through the trajectory.
    Computes eta_p, eta_a, Gamma_m terms per step.
    """
    results = []
    centerlines = []

    # Scaling coefficients for dissipation terms
    eta_p_coeff = 1.0
    eta_a_coeff = 1.0
    gamma_m_base = 0.1

    dt_step = trajectory[1]['time'] - trajectory[0]['time'] if len(trajectory) > 1 else 1.0

    prev_kappa = None

    for step, state in enumerate(trajectory):
        t = state['time']
        theta_rad = np.radians(state['theta_deg'])
        info = state['info']

        # Base direction and normal
        base_dir = np.array([np.cos(theta_rad), 0.0, np.sin(theta_rad)])
        normal_dir = np.array([0.0, 1.0, 0.0])

        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=base_params,
            length=L,
            n_elements=n_elements,
            E0=E0,
            radius=radius,
            rho=rho,
            gravity=gravity_magnitude,
            base_direction=tuple(base_dir),
            normal=tuple(normal_dir)
        )

        # Run short quasi-static relaxation
        sim_res = system.run_simulation(final_time=0.5, dt=1e-4, save_every=2000)

        # Final state
        cl = sim_res.centerline[-1]
        kappa = sim_res.kappa[-1][:, 1] # Bending curvature

        # 1. eta_p (Proprioceptive Rate): |dkappa/dt|^2
        eta_p = 0.0
        if prev_kappa is not None:
            # Interpolate kappa to a standard grid if shapes differ, but PyElastica preserves node count
            dkappa_dt = (kappa - prev_kappa) / dt_step
            eta_p = eta_p_coeff * np.trapz(dkappa_dt**2, dx=L/n_elements)

        # 2. eta_a (Active Maintenance): (kappa - kappa_passive)^2
        # For simplicity, assume kappa_passive ~ 0 here.
        eta_a = eta_a_coeff * np.trapz(kappa**2, dx=L/n_elements)

        # 3. Gamma_m (Basal Maintenance)
        gamma_m = gamma_m_base * L

        total_dissipation = eta_p + eta_a + gamma_m

        results.append({
            'time': t,
            'theta_deg': state['theta_deg'],
            'eta_p': eta_p,
            'eta_a': eta_a,
            'gamma_m': gamma_m,
            'total_dissipation': total_dissipation
        })
        centerlines.append((t, state['theta_deg'], cl))

        prev_kappa = kappa

    return results, centerlines

def coupling_decay_model(chi_0, N_cycles_per_day, tau_decay_hours=2.0):
    """
    Exponential decay with periodic reset.
    Returns average coupling ratio chi_avg / chi_0.
    """
    if N_cycles_per_day == 0:
        return 0.0

    T_day = 24.0
    tau = tau_decay_hours
    N = N_cycles_per_day
    T_int = T_day / N

    # chi_avg = (tau / T_int) * (1 - exp(-T_int / tau))
    chi_avg_ratio = (tau / T_int) * (1 - np.exp(-T_int / tau))
    return chi_avg_ratio

def compare_chair_vs_floor(base_params, L, n_elements, E0, radius, rho, gravity_magnitude, out_dir, args):
    """
    Compares chair sitting (N=3, shallow) vs floor sitting (N=50, deep).
    """
    print("Comparing Chair (N=3, shallow) vs Floor (N=50, deep)...")

    T_cycle = 4.0
    num_steps = 20 if not args.quick else 5

    # 1. Chair (Shallow, ~45 degrees min)
    traj_chair = define_squat_stand_trajectory(T_cycle, num_steps, L, min_theta_deg=45.0)
    res_chair, cl_chair = compute_cycle_dissipation(
        traj_chair, base_params, L, n_elements, E0, radius, rho, gravity_magnitude
    )

    # 2. Floor (Deep, 0 degrees min)
    traj_floor = define_squat_stand_trajectory(T_cycle, num_steps, L, min_theta_deg=0.0)
    res_floor, cl_floor = compute_cycle_dissipation(
        traj_floor, base_params, L, n_elements, E0, radius, rho, gravity_magnitude
    )

    # 3. Save CSV
    chair_total = sum(r['total_dissipation'] for r in res_chair)
    floor_total = sum(r['total_dissipation'] for r in res_floor)

    chair_N = 3
    floor_N = 50

    daily_chair_dissipation = chair_total * chair_N
    daily_floor_dissipation = floor_total * floor_N

    chair_chi = coupling_decay_model(1.0, chair_N)
    floor_chi = coupling_decay_model(1.0, floor_N)

    comparison = [
        {"Regimen": "Chair-Sitting", "N_cycles": chair_N, "Depth": "Shallow (45°)",
         "Dissipation_per_cycle": chair_total, "Daily_Dissipation": daily_chair_dissipation,
         "Avg_Coupling_Preserved": chair_chi},
        {"Regimen": "Floor-Sitting", "N_cycles": floor_N, "Depth": "Deep (0°)",
         "Dissipation_per_cycle": floor_total, "Daily_Dissipation": daily_floor_dissipation,
         "Avg_Coupling_Preserved": floor_chi}
    ]

    csv_path = out_dir / "chair_vs_floor_comparison.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=comparison[0].keys())
        writer.writeheader()
        writer.writerows(comparison)

    # 4. Plot Trajectories (Visual)
    plt.figure(figsize=(10, 8))
    for i, (t, theta, cl) in enumerate(cl_chair):
        if i % max(1, len(cl_chair)//4) == 0:
            plt.plot(cl[0, :], cl[2, :], 'b--', alpha=0.5, label=f"Chair t={t:.1f}s" if i==0 else "")

    for i, (t, theta, cl) in enumerate(cl_floor):
        if i % max(1, len(cl_floor)//4) == 0:
            plt.plot(cl[0, :], cl[2, :], 'r-', alpha=0.8, label=f"Floor t={t:.1f}s" if i==0 else "")

    plt.xlabel("Global X (m)")
    plt.ylabel("Global Z (m)")
    plt.title("Spinal Trajectories: Chair (Shallow) vs Floor (Deep) Transition")
    plt.legend()
    plt.axis('equal')
    plt.grid(True)
    plt.savefig(out_dir / "chair_vs_floor_trajectories.png")
    plt.close()

def run_cycle_frequency_sweep(out_dir):
    """
    N = [1, 2, 5, 10, 20, 50, 100] cycles/day.
    """
    N_vals = [0, 1, 2, 3, 5, 10, 20, 50, 80, 100]
    decay_ratios = [coupling_decay_model(1.0, N) for N in N_vals]

    csv_path = out_dir / "coupling_preservation.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cycles_per_day", "chi_avg_ratio"])
        for n, r in zip(N_vals, decay_ratios):
            writer.writerow([n, r])

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(N_vals, np.array(decay_ratios)*100, marker='o', linestyle='-')
    plt.xlabel("Squat-to-Stand Cycles per Day (N)")
    plt.ylabel("Time-Averaged Coupling Capacity (%)")
    plt.title("Coupling Decay Model: Okinawan Longevity vs Chair Sitting")
    plt.axvline(3, color='r', linestyle='--', label='Chair-Sitter (~3 cycles)')
    plt.axvline(50, color='g', linestyle='--', label='Floor-Sitter (~50 cycles)')
    plt.legend()
    plt.grid(True)
    plt.savefig(out_dir / "coupling_preservation.png")
    plt.close()

def main():
    parser = StandardExperimentParser(description="Dynamic Squat-to-Stand Thermodynamic Cycle Simulation")
    args = parser.parse_args()
    out_dir = setup_experiment(args)

    # 1. Simulation Parameters
    L = 1.0
    n_elements = 50 if not args.quick else 20
    E0 = 1e6
    radius = 0.02
    rho = 1000
    gravity_magnitude = 9.81
    T_cycle = 4.0
    num_steps = 20 if not args.quick else 5

    base_params = CounterCurvatureParams(
        chi_E=0.0,
        chi_kappa=4.0,
        chi_M=15.0,
        chi_tau=0.0,
        scale_length=L
    )

    # 2. Define Trajectory
    print(f"Defining Single Squat-to-Stand trajectory (T={T_cycle}s, steps={num_steps})...")
    trajectory = define_squat_stand_trajectory(T_cycle, num_steps, L)

    # 3. Compute Dissipation
    print("Computing single cycle dissipation (quasi-static)...")
    results, centerlines = compute_cycle_dissipation(
        trajectory, base_params, L, n_elements, E0, radius, rho, gravity_magnitude
    )

    # Save Dissipation Results
    csv_path = out_dir / "cycle_dissipation.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # Plot Dissipation Breakdown
    times = [r['time'] for r in results]
    eta_p = [r['eta_p'] for r in results]
    eta_a = [r['eta_a'] for r in results]
    gamma_m = [r['gamma_m'] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(times, eta_p, label='η_p (Proprioceptive Rate)', color='blue')
    plt.plot(times, eta_a, label='η_a (Active Maintenance)', color='red')
    plt.plot(times, gamma_m, label='Γ_m (Basal Maintenance)', color='green')
    plt.xlabel("Time in Cycle (s) [0=Stand, 2=Squat, 4=Stand]")
    plt.ylabel("Dissipation (W)")
    plt.title("Thermodynamic Dissipation During Squat-to-Stand Cycle")
    plt.legend()
    plt.grid(True)
    plt.savefig(out_dir / "dissipation_breakdown.png")
    plt.close()

    # 4. Compare Chair vs Floor
    compare_chair_vs_floor(base_params, L, n_elements, E0, radius, rho, gravity_magnitude, out_dir, args)

    # 5. Run Frequency Sweep
    print("Running Coupling Decay Frequency Sweep...")
    run_cycle_frequency_sweep(out_dir)

    print(f"✅ Experiment complete. Results saved to {out_dir}")

if __name__ == "__main__":
    main()
