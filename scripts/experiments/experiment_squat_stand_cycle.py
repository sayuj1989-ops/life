#!/usr/bin/env python3
"""
Squat-to-Stand Cycle Simulation
===============================
Models the dynamic transition between squatting and standing to explicitly
calculate energy dissipation terms per cycle, and phenomenal coupling decay.

Outputs:
  - CSVs of trajectory and dissipation breakdown
  - Figures of posture trajectory, dissipation terms, coupling decay
"""

import csv
import math
import sys
import os
import time
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from scripts.experiments.experiment_utils import StandardExperimentParser, setup_experiment

def define_squat_stand_trajectory(T_cycle: float, num_steps: int):
    """
    T_cycle=4s
    theta(t) from 90 deg (standing, gravity parallel to spine)
    to 0 deg (deep squat, gravity perpendicular) and back.
    I(s,t) morphs from S-curve to C-curve field.
    """
    times = np.linspace(0, T_cycle, num_steps)
    thetas = []

    for t in times:
        # Half cycle squat, half cycle stand
        # Using a smooth cosine transition for theta
        # t=0 -> theta=90 (stand)
        # t=T/2 -> theta=0 (squat)
        # t=T -> theta=90 (stand)
        theta = 45 * (1 + math.cos(2 * math.pi * t / T_cycle))
        thetas.append(theta)

    return times, np.array(thetas)

def compute_cycle_dissipation(times, thetas, L, n_elements, base_params, E0, radius, rho, gravity_magnitude):
    results = []
    centerlines = []
    kappas = []

    n_points = n_elements + 1
    s = np.linspace(0, L, n_points)

    # Base field I_stand (S-curve) and I_squat (C-curve)
    I_stand = np.sin(2 * np.pi * s / L)**2
    I_squat = np.sin(np.pi * s / L)**2

    for i, t in enumerate(times):
        theta_deg = thetas[i]
        theta_rad = np.radians(theta_deg)

        # Morph Info Field
        # t=0 (stand): I_stand
        # t=T/2 (squat): I_squat
        phase = 0.5 * (1 - math.cos(2 * math.pi * t / times[-1]))
        I_t = I_stand * (1 - phase) + I_squat * phase
        dIds_t = np.gradient(I_t, s)
        info_t = InfoField1D(s=s, I=I_t, dIds=dIds_t)

        base_dir = np.array([np.cos(theta_rad), 0.0, np.sin(theta_rad)])
        normal_dir = np.array([0.0, 1.0, 0.0])

        system = CounterCurvatureRodSystem.from_iec(
            info=info_t,
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

        # Quasi-static stepping
        sim_res = system.run_simulation(final_time=1.0, dt=1e-4, save_every=200)

        final_kappa = sim_res.kappa[-1]
        bending_k = final_kappa[:, 1]
        kappas.append(bending_k)

        tip_pos = sim_res.centerline[-1][:, -1]



        # Compute exact energies for the thermodynamic terms
        from src.spinalmodes.countercurvature.pyelastica_bridge import compute_U_CC
        metrics = compute_U_CC(sim_res, info_t, base_params, gravity_magnitude, rho, E0, radius)

        results.append({
            "time": t,
            "theta_deg": theta_deg,
            "tip_x": tip_pos[0],
            "tip_z": tip_pos[2],
            "U_gravity": metrics.get("U_gravity", 0.0),
            "U_elastic": metrics.get("U_elastic", 0.0),
            "U_info": metrics.get("U_info", 0.0),
            "U_CC": metrics.get("U_CC", 0.0)
        })


        centerlines.append((t, sim_res.centerline[-1]))

    # Calculate dissipation terms
    # F_dot = integral[ eta_p |dkappa/dt|^2 + eta_a (kappa - kappa_passive)^2 + Gamma_m(s) ] ds
    # For simulation, we simplify tracking the terms

    dt_arr = np.diff(times)
    eta_p_total = 0
    eta_a_total = 0
    gamma_m_total = 0

    # Arbitrary scaling constants for the terms to produce realistic relative magnitudes
    c_p = 10.0
    c_a = 5.0
    c_g = 1.0

    dissipation_breakdown = []

    for i in range(len(times)):
        # eta_a: maintenance cost (proportional to total elastic energy)
        # We use U_elastic as a proxy for (kappa - kappa_passive)^2
        eta_a_i = c_a * results[i]["U_elastic"]

        # Gamma_m: basal cost (constant baseline + scaled by info field complexity)
        gamma_m_i = c_g * (1.0 + results[i]["U_info"])

        # eta_p: proprioceptive cost (rate of change of curvature)
        eta_p_i = 0
        if i > 0:
            dk = kappas[i] - kappas[i-1]
            dt_step = dt_arr[i-1]
            if dt_step > 0:
                dk_dt = dk / dt_step
                # integrate over s
                eta_p_i = c_p * np.trapz(dk_dt**2, x=s)

        eta_p_total += eta_p_i * (dt_arr[i-1] if i > 0 else 0)
        eta_a_total += eta_a_i * (dt_arr[i-1] if i > 0 else 0)
        gamma_m_total += gamma_m_i * (dt_arr[i-1] if i > 0 else 0)

        results[i]["eta_p_rate"] = eta_p_i
        results[i]["eta_a_rate"] = eta_a_i
        results[i]["gamma_m_rate"] = gamma_m_i
        results[i]["total_dissipation_rate"] = eta_p_i + eta_a_i + gamma_m_i

    cycle_totals = {
        "eta_p_total": eta_p_total,
        "eta_a_total": eta_a_total,
        "gamma_m_total": gamma_m_total,
        "total": eta_p_total + eta_a_total + gamma_m_total
    }

    return results, centerlines, cycle_totals

def coupling_decay_model(N_cycles_per_day, days=10, tau_decay_hours=2.0):
    chi_0 = 1.0
    T_day = 24.0 # hours

    if N_cycles_per_day == 0:
        times = np.linspace(0, days * 24, 1000)
        chi = chi_0 * np.exp(-times / tau_decay_hours)
        return times, chi, np.mean(chi)

    T_int = T_day / N_cycles_per_day
    times = []
    chi = []

    current_chi = chi_0
    for day in range(days):
        for cycle in range(N_cycles_per_day):
            t_start = day * 24 + cycle * T_int
            t_end = t_start + T_int

            # Decay phase
            t_phase = np.linspace(t_start, t_end, 100)
            chi_phase = current_chi * np.exp(-(t_phase - t_start) / tau_decay_hours)

            times.extend(t_phase)
            chi.extend(chi_phase)

            # Reset at end of cycle
            current_chi = chi_0

    times = np.array(times)
    chi = np.array(chi)

    chi_avg = chi_0 * (tau_decay_hours / T_int) * (1 - np.exp(-T_int / tau_decay_hours))

    return times, chi, chi_avg


def compare_chair_vs_floor():
    print("Comparing Chair vs Floor...")

    times_floor, thetas_floor = define_squat_stand_trajectory(T_cycle=4.0, num_steps=21)
    # Chair cycle: shallow angle (45 deg instead of 0 deg)
    times_chair = times_floor
    thetas_chair = [45 + 45 * (1 + math.cos(2 * math.pi * t / 4.0)) / 2 for t in times_chair]

    L = 1.0
    n_elements = 20
    E0 = 1e6
    radius = 0.02
    rho = 1000
    gravity_magnitude = 9.81

    base_params = CounterCurvatureParams(
        chi_E=0.0,
        chi_kappa=4.0,
        chi_M=15.0,
        chi_tau=0.0,
        scale_length=L
    )

    res_floor, centerlines_floor, totals_floor = compute_cycle_dissipation(
        times_floor, thetas_floor, L, n_elements, base_params, E0, radius, rho, gravity_magnitude
    )

    res_chair, centerlines_chair, totals_chair = compute_cycle_dissipation(
        times_chair, thetas_chair, L, n_elements, base_params, E0, radius, rho, gravity_magnitude
    )

    # Plot dissipation breakdown comparison
    labels = [r"$\eta_p$", r"$\eta_a$", r"$\Gamma_m$"]
    floor_totals = [totals_floor["eta_p_total"], totals_floor["eta_a_total"], totals_floor["gamma_m_total"]]
    chair_totals = [totals_chair["eta_p_total"], totals_chair["eta_a_total"], totals_chair["gamma_m_total"]]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(x - width/2, floor_totals, width, label='Floor-sitter (Deep, N=50)')
    ax.bar(x + width/2, chair_totals, width, label='Chair-sitter (Shallow, N=3)')

    ax.set_ylabel('Total Dissipated Energy per Cycle')
    ax.set_title('Thermodynamic Cost Comparison: Chair vs Floor')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.grid(alpha=0.3, axis='y')
    plt.tight_layout()

    return fig, floor_totals, chair_totals

def run_cycle_frequency_sweep():
    N_values = [0, 1, 3, 10, 20, 50, 80]
    labels = ["Bedridden (0)", "Sedentary (1)", "Chair-sitter (3)", "Active-sitter (10)", "Floor-sitter (50)", "Okinawan (80)"]

    tau_decay = 2.0

    results = []
    plt.figure(figsize=(10, 6))

    for N in N_values:
        times, chi, chi_avg = coupling_decay_model(N, days=2, tau_decay_hours=tau_decay)
        results.append({"N_cycles": N, "chi_avg_ratio": chi_avg})

        if N in [0, 3, 20, 50, 80]:
            plt.plot(times, chi, label=f"N={N} (Avg: {chi_avg:.2%})")

    plt.axhline(1.0, color='k', linestyle='--', alpha=0.5, label="Optimal (100%)")
    plt.xlabel("Time (hours)")
    plt.ylabel(r"Coupling Strength $\chi(t) / \chi_0$")
    plt.title("Coupling Decay Model: Frequent Resets Preserve Mechanosensory Capacity")
    plt.ylim(0, 1.1)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    return results, plt.gcf()

def run_simulation(args):
    out_dir = setup_experiment(args)

    # 1. Trajectory and Dissipation
    T_cycle = 4.0
    num_steps = 11 if args.quick else 41

    L = 1.0
    n_elements = 20 if args.quick else 50
    E0 = 1e6
    radius = 0.02
    rho = 1000
    gravity_magnitude = 9.81

    base_params = CounterCurvatureParams(
        chi_E=0.0,
        chi_kappa=4.0,
        chi_M=15.0,
        chi_tau=0.0,
        scale_length=L
    )

    times, thetas = define_squat_stand_trajectory(T_cycle, num_steps)

    print(f"Running dynamic cycle simulation (steps={num_steps})...")
    res, centerlines, cycle_totals = compute_cycle_dissipation(
        times, thetas, L, n_elements, base_params, E0, radius, rho, gravity_magnitude
    )

    # Save dissipation results
    csv_path = out_dir / "cycle_dissipation.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=res[0].keys())
        writer.writeheader()
        writer.writerows(res)

    print(f"Cycle totals: eta_p={cycle_totals['eta_p_total']:.2f}, eta_a={cycle_totals['eta_a_total']:.2f}, gamma_m={cycle_totals['gamma_m_total']:.2f}")

    # Plot shape morphing
    plt.figure(figsize=(10, 8))
    for t, cl in centerlines[::max(1, len(centerlines)//10)]:
        alpha = 0.3 + 0.7 * (t / T_cycle)
        plt.plot(cl[0, :], cl[2, :], alpha=alpha, label=f"t={t:.1f}s")

    plt.xlabel("Global X (m)")
    plt.ylabel("Global Z (m)")
    plt.title("Spinal Trajectory during Squat-to-Stand Cycle")
    plt.axis('equal')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.savefig(out_dir / "trajectory_shapes.png")
    plt.close()

    # Plot dissipation rates
    t_vals = [r["time"] for r in res]
    eta_p_vals = [r["eta_p_rate"] for r in res]
    eta_a_vals = [r["eta_a_rate"] for r in res]
    gamma_m_vals = [r["gamma_m_rate"] for r in res]

    plt.figure(figsize=(10, 6))
    plt.plot(t_vals, eta_p_vals, label=r"$\eta_p$ (Proprioceptive)", color='tab:blue')
    plt.plot(t_vals, eta_a_vals, label=r"$\eta_a$ (Active Maintenance)", color='tab:orange')
    plt.plot(t_vals, gamma_m_vals, label=r"$\Gamma_m$ (Basal Cost)", color='tab:green')
    plt.xlabel("Time (s)")
    plt.ylabel("Dissipation Rate (Energy/s)")
    plt.title("Thermodynamic Dissipation during Squat-to-Stand Cycle")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "dissipation_rates.png")
    plt.close()

    # 2. Coupling Decay Model
    print("Running coupling decay model...")
    decay_res, fig_decay = run_cycle_frequency_sweep()
    fig_decay.savefig(out_dir / "coupling_preservation.png")
    plt.close(fig_decay)

    csv_decay_path = out_dir / "coupling_decay.csv"
    with open(csv_decay_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=decay_res[0].keys())
        writer.writeheader()
        writer.writerows(decay_res)


    # 3. Chair vs Floor Comparison
    fig_compare, totals_floor, totals_chair = compare_chair_vs_floor()
    fig_compare.savefig(out_dir / "dissipation_breakdown.png")
    plt.close(fig_compare)

    csv_compare_path = out_dir / "chair_vs_floor_dissipation.csv"
    with open(csv_compare_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Floor_Cycle", "Chair_Cycle"])
        writer.writerow(["eta_p_total", totals_floor[0], totals_chair[0]])
        writer.writerow(["eta_a_total", totals_floor[1], totals_chair[1]])
        writer.writerow(["gamma_m_total", totals_floor[2], totals_chair[2]])
        writer.writerow(["total", sum(totals_floor), sum(totals_chair)])

    print(f"Results saved to {out_dir}")

if __name__ == "__main__":
    parser = StandardExperimentParser(
        description="Squat-to-Stand Thermodynamic Cycle Simulation",
        default_out_dir="outputs/thermodynamic_cost/squat_stand_cycle"
    )
    args = parser.parse_args()
    run_simulation(args)
