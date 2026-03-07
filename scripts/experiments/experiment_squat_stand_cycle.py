#!/usr/bin/env python3
"""
Squat-to-Stand Thermodynamic Cycle Simulation
===========================================

Simulates the energetic cost and coupling preservation of frequent
floor-to-stand transitions (thermodynamic cycling), validating the
longevity framework hypothesis.

Models the dynamic transition with time-varying gravity orientation
and a time-varying information field, calculating η_p, η_a, and Γ_m.

Author: Jules
Date: 2026-02-07
"""

import csv
import logging
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import os
import sys
# Adjust imports to match project structure
sys.path.append(os.getcwd())
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from scripts.experiments.experiment_utils import StandardExperimentParser, setup_experiment


def define_squat_stand_trajectory(t: float, t_cycle: float = 4.0) -> tuple[float, np.ndarray]:
    """
    Defines the time-varying posture (gravity angle) and information field.

    Args:
        t: Current time in the cycle (s)
        t_cycle: Total cycle duration (s)

    Returns:
        theta_deg: Angle of the spine relative to horizontal (90 = standing, 0 = squatting)
        I: The information field array for the current time
    """
    # 0 to t_cycle/2: Squat down (90 -> 0)
    # t_cycle/2 to t_cycle: Stand up (0 -> 90)
    phase = (t % t_cycle) / t_cycle

    if phase < 0.5:
        # Downward phase
        normalized_t = phase * 2  # 0 to 1
        theta_deg = 90.0 - 90.0 * (0.5 - 0.5 * np.cos(np.pi * normalized_t))
    else:
        # Upward phase
        normalized_t = (phase - 0.5) * 2  # 0 to 1
        theta_deg = 90.0 * (0.5 - 0.5 * np.cos(np.pi * normalized_t))

    # Info Field: S-shape (standing) to C-shape (squatting)
    L = 1.0
    s = np.linspace(0, L, 50)

    # Standing (S-shape): I_stand = sin^2(2*pi*s/L)
    I_stand = np.sin(2 * np.pi * s / L)**2

    # Squatting (C-shape): I_squat = sin(pi*s/L)
    I_squat = np.sin(np.pi * s / L)

    # Interpolate based on theta (90 = pure stand, 0 = pure squat)
    weight_stand = theta_deg / 90.0
    I = weight_stand * I_stand + (1.0 - weight_stand) * I_squat

    return theta_deg, I


def compute_cycle_dissipation(
    dt_step: float = 0.1,
    t_cycle: float = 4.0,
    quick: bool = False,
    min_theta: float = 0.0
) -> tuple[dict, list, list, list]:
    """
    Runs a quasi-static simulation of a single squat-stand cycle to
    compute the components of the dissipation functional over time.
    """
    L = 1.0
    n_elements = 20 if quick else 50
    E0 = 1e6
    radius = 0.02
    rho = 1000
    gravity_magnitude = 9.81

    # Base parameters matching run_posture_sweep
    chi_kappa = 4.0
    chi_M = 15.0

    t_steps = np.arange(0, t_cycle + dt_step, dt_step)

    # Results accumulators
    eta_p_total = 0.0
    eta_a_total = 0.0
    Gamma_m_total = 0.0

    # Assume phenomenological constants for the dissipation terms
    c_p = 10.0   # Weight for |dkappa/dt|^2
    c_a = 5.0    # Weight for (kappa - kappa_passive)^2
    c_m = 1.0    # Baseline metabolic rate

    prev_kappa = None
    time_series = []
    kappas = []
    centerlines = []

    logging.info(f"Simulating single cycle (T={t_cycle}s) with {len(t_steps)} steps")

    for i, t in enumerate(t_steps):
        phase = (t % t_cycle) / t_cycle
        if phase < 0.5:
            normalized_t = phase * 2
            theta_deg = 90.0 - (90.0 - min_theta) * (0.5 - 0.5 * np.cos(np.pi * normalized_t))
        else:
            normalized_t = (phase - 0.5) * 2
            theta_deg = 90.0 - (90.0 - min_theta) * (0.5 + 0.5 * np.cos(np.pi * normalized_t))

        theta_rad = np.radians(theta_deg)

        # Build info field
        s = np.linspace(0, L, n_elements + 1)
        s_base = np.linspace(0, L, 50)
        I_stand = np.sin(2 * np.pi * s_base / L)**2
        I_squat = np.sin(np.pi * s_base / L)
        weight_stand = theta_deg / 90.0
        I_grid = weight_stand * I_stand + (1.0 - weight_stand) * I_squat
        I = np.interp(s, s_base, I_grid)
        dIds = np.gradient(I, s)
        info = InfoField1D(s=s, I=I, dIds=dIds)

        params = CounterCurvatureParams(
            chi_E=0.0,
            chi_kappa=chi_kappa,
            chi_M=chi_M,
            chi_tau=0.0,
            scale_length=L
        )

        # Rod direction based on posture
        base_dir = np.array([np.cos(theta_rad), 0.0, np.sin(theta_rad)])
        normal_dir = np.array([0.0, 1.0, 0.0])

        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=E0,
            radius=radius,
            rho=rho,
            gravity=gravity_magnitude,
            base_direction=tuple(base_dir),
            normal=tuple(normal_dir)
        )

        # Short relaxation for quasi-static assumption
        sim_res = system.run_simulation(final_time=0.1, dt=1e-4, save_every=1000, progress_bar=False)

        # Get final kappa and centerline
        kappa = sim_res.kappa[-1][:, 1]  # Bending component
        kappas.append(kappa)
        centerlines.append(sim_res.centerline[-1])

        # Dissipation Calculation
        eta_p = 0.0
        if prev_kappa is not None:
            # eta_p term: proprioceptive cost |dkappa/dt|^2
            dkappa_dt = (kappa - prev_kappa) / dt_step
            eta_p = c_p * np.sum(dkappa_dt**2) * (L / n_elements) * dt_step
            eta_p_total += eta_p

        # eta_a term: active maintenance (kappa - 0)^2 assuming passive is straight
        eta_a = c_a * np.sum(kappa**2) * (L / n_elements) * dt_step
        eta_a_total += eta_a

        # Gamma_m term: baseline + metabolic boost from work done
        # Work is proportional to change in potential energy + active moment
        Gamma_m = c_m * L * dt_step  # Simplified baseline
        Gamma_m_total += Gamma_m

        time_series.append({
            "time": t,
            "theta_deg": theta_deg,
            "eta_p": eta_p,
            "eta_a": eta_a,
            "Gamma_m": Gamma_m
        })

        prev_kappa = kappa

    totals = {
        "eta_p": eta_p_total,
        "eta_a": eta_a_total,
        "Gamma_m": Gamma_m_total,
        "total_dissipation": eta_p_total + eta_a_total + Gamma_m_total
    }
    return totals, time_series, kappas, centerlines


def compare_chair_vs_floor(out_dir: Path, quick: bool = False):
    """
    Compares the thermodynamic trajectories of chair-sitting (N=3, shallow squat)
    vs floor-sitting (N=50, deep squat).
    """
    L = 1.0
    t_cycle = 4.0

    chair_totals, chair_ts, chair_kappas, chair_centerlines = compute_cycle_dissipation(quick=quick, min_theta=45.0)
    floor_totals, floor_ts, floor_kappas, floor_centerlines = compute_cycle_dissipation(quick=quick, min_theta=0.0)

    # Plotting trajectories
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    def plot_cl(ax, cl_list, title):
        ax.set_title(title)
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Z (m)")
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        indices = [0, len(cl_list)//2, -1]
        labels = ["Start (Stand)", "Max Depth", "End (Stand)"]
        colors = ['blue', 'red', 'green']
        for idx, label, color in zip(indices, labels, colors):
            if idx < len(cl_list):
                cl = cl_list[idx]
                ax.plot(cl[0, :], cl[2, :], label=label, color=color, linewidth=2)
        ax.legend()

    plot_cl(axes[0], chair_centerlines, "Chair-Sitting Trajectory")
    plot_cl(axes[1], floor_centerlines, "Floor-Sitting Trajectory")

    plt.tight_layout()
    plt.savefig(out_dir / "chair_vs_floor_trajectories.png")
    plt.close()

    # Generate Curvature Heatmap for deep squat
    kappas_arr = np.array(floor_kappas)  # (time_steps, n_nodes)
    plt.figure(figsize=(10, 6))
    plt.imshow(kappas_arr.T, aspect='auto', origin='lower', cmap='coolwarm',
               extent=[0, t_cycle, 0, L])
    plt.colorbar(label='Curvature $\kappa$ (1/m)')
    plt.xlabel('Cycle Time (s)')
    plt.ylabel('Spinal Arc Length (m)')
    plt.title('Spinal Curvature Heatmap During Squat-Stand Cycle')
    plt.savefig(out_dir / "curvature_heatmap.png")
    plt.close()

    # Plot Dissipation Time Series Comparison
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    times = [d['time'] for d in floor_ts]

    # Plot eta_p (Proprioceptive)
    floor_eta_p = [d['eta_p'] for d in floor_ts]
    chair_eta_p = [d['eta_p'] for d in chair_ts]
    axes[0].plot(times, floor_eta_p, label='Floor (Deep)', color='blue')
    axes[0].plot(times, chair_eta_p, label='Chair (Shallow)', color='orange')
    axes[0].set_title(r"Proprioceptive Cost $\eta_p \left| \frac{\partial \kappa}{\partial t} \right|^2$")
    axes[0].set_ylabel("Dissipation Rate")
    axes[0].legend()
    axes[0].grid(True)

    # Plot eta_a (Active Maintenance)
    floor_eta_a = [d['eta_a'] for d in floor_ts]
    chair_eta_a = [d['eta_a'] for d in chair_ts]
    axes[1].plot(times, floor_eta_a, label='Floor (Deep)', color='blue')
    axes[1].plot(times, chair_eta_a, label='Chair (Shallow)', color='orange')
    axes[1].set_title(r"Active Maintenance $\eta_a (\kappa - \kappa_{passive})^2$")
    axes[1].set_ylabel("Dissipation Rate")
    axes[1].legend()
    axes[1].grid(True)

    # Plot Gamma_m
    floor_gamma = [d['Gamma_m'] for d in floor_ts]
    chair_gamma = [d['Gamma_m'] for d in chair_ts]
    axes[2].plot(times, floor_gamma, label='Floor (Deep)', color='blue')
    axes[2].plot(times, chair_gamma, label='Chair (Shallow)', color='orange')
    axes[2].set_title(r"Basal Maintenance $\Gamma_m$")
    axes[2].set_xlabel("Cycle Time (s)")
    axes[2].set_ylabel("Dissipation Rate")
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig(out_dir / "chair_vs_floor_dissipation_timeseries.png")
    plt.close()

    # Save CSVs
    with open(out_dir / "chair_dissipation_timeseries.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=chair_ts[0].keys())
        writer.writeheader()
        writer.writerows(chair_ts)

    with open(out_dir / "floor_dissipation_timeseries.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=floor_ts[0].keys())
        writer.writeheader()
        writer.writerows(floor_ts)


def coupling_decay_model(
    cycles_per_day: int,
    tau_decay: float = 2.0,
    chi_0: float = 1.0,
    days: int = 1
) -> tuple[np.ndarray, np.ndarray, float]:
    """
    Models the phenomenological decay of coupling strength over time.
    chi(t) = chi_0 * exp(-dt / tau_decay)

    Args:
        cycles_per_day: N cycles per 24 hours
        tau_decay: Decay time constant in hours
        chi_0: Peak coupling strength
        days: Simulation duration

    Returns:
        t_hours: Time array in hours
        chi_t: Coupling strength array
        chi_avg: Time-averaged coupling strength
    """
    t_total = days * 24.0
    dt = 0.1
    t_hours = np.arange(0, t_total, dt)
    chi_t = np.zeros_like(t_hours)

    if cycles_per_day == 0:
        # Zero cycles: pure decay from start
        chi_t = chi_0 * np.exp(-t_hours / tau_decay)
        chi_avg = np.mean(chi_t)
        return t_hours, chi_t, chi_avg

    # Interval between cycles
    interval = 24.0 / cycles_per_day
    cycle_times = np.arange(0, t_total, interval)

    current_chi = chi_0
    last_cycle_t = 0.0

    for i, t in enumerate(t_hours):
        # Did a cycle just happen?
        if len(cycle_times) > 0 and t >= cycle_times[0]:
            current_chi = chi_0  # Reset
            last_cycle_t = t
            cycle_times = cycle_times[1:]

        # Decay
        chi_t[i] = chi_0 * np.exp(-(t - last_cycle_t) / tau_decay)

    # Analytical average (steady state)
    T_int = 24.0 / cycles_per_day
    chi_avg_analytical = chi_0 * (tau_decay / T_int) * (1 - np.exp(-T_int / tau_decay))

    return t_hours, chi_t, chi_avg_analytical


def run_cycle_frequency_sweep(out_dir: Path):
    """
    Sweeps the number of daily cycles to generate the coupling preservation curve.
    """
    frequencies = [0, 1, 3, 10, 20, 50, 80, 100]
    tau_decay = 2.0

    results = []

    plt.figure(figsize=(10, 6))

    for n in frequencies:
        t_hours, chi_t, chi_avg = coupling_decay_model(cycles_per_day=n, tau_decay=tau_decay)
        results.append({
            "cycles_per_day": n,
            "chi_avg_relative": chi_avg
        })

        # Plot the first 24 hours for a few key frequencies
        if n in [0, 3, 20, 50]:
            label = f"{n} cycles/day ({chi_avg*100:.1f}%)"
            if n == 3: label = f"Chair-sitter: {label}"
            elif n == 50: label = f"Floor-sitter: {label}"
            plt.plot(t_hours[:240], chi_t[:240], label=label)

    plt.xlabel("Time (hours)")
    plt.ylabel("Relative Coupling Strength χ(t)/χ₀")
    plt.title("Coupling Decay and Periodic Reset (Squat-to-Stand)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig(out_dir / "coupling_preservation_timeseries.png")
    plt.close()

    # Save CSV
    with open(out_dir / "coupling_preservation.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["cycles_per_day", "chi_avg_relative"])
        writer.writeheader()
        writer.writerows(results)

    # Plot preservation curve
    cycles = [r["cycles_per_day"] for r in results]
    chi_avgs = [r["chi_avg_relative"] * 100 for r in results]

    plt.figure(figsize=(8, 5))
    plt.plot(cycles, chi_avgs, 'o-', color='navy', linewidth=2)
    plt.axhline(90, color='g', linestyle='--', alpha=0.5, label='Healthy Threshold')
    plt.axvline(3, color='r', linestyle=':', label='Chair-Sitter (~3/day)')
    plt.axvline(50, color='b', linestyle=':', label='Floor-Sitter (~50/day)')
    plt.xlabel("Squat-to-Stand Cycles per Day")
    plt.ylabel("Time-Averaged Coupling Capacity (%)")
    plt.title("Mechanotransduction Preservation vs Cycling Frequency")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "coupling_preservation_curve.png")
    plt.close()


def main():
    parser = StandardExperimentParser(description="Squat-to-Stand Thermodynamic Cycle Sim")
    args = parser.parse_args()
    out_dir = setup_experiment(args)

    logging.info("Starting Longevity Squat-to-Stand Simulation")

    # 1. Compare chair vs floor trajectories and save detailed dissipation logs
    compare_chair_vs_floor(out_dir, quick=args.quick)

    # For pie chart, use deep squat data
    floor_totals, _, _, _ = compute_cycle_dissipation(quick=args.quick, min_theta=0.0)

    logging.info(f"Deep Squat (Floor) Dissipation Results:")
    logging.info(f"  eta_p (Proprioception): {floor_totals['eta_p']:.4f}")
    logging.info(f"  eta_a (Active Maint.):  {floor_totals['eta_a']:.4f}")
    logging.info(f"  Gamma_m (Basal Maint.): {floor_totals['Gamma_m']:.4f}")

    with open(out_dir / "cycle_dissipation_totals.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=floor_totals.keys())
        writer.writeheader()
        writer.writerow(floor_totals)

    # Create pie chart
    labels = ['η_p (Sensing)', 'η_a (Actuation)', 'Γ_m (Maintenance)']
    sizes = [floor_totals['eta_p'], floor_totals['eta_a'], floor_totals['Gamma_m']]
    colors = ['#ff9999','#66b3ff','#99ff99']

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Thermodynamic Cost Breakdown (Single Squat-Stand Cycle)')
    plt.savefig(out_dir / "dissipation_breakdown.png")
    plt.close()

    # 2. Run frequency sweep and coupling decay
    run_cycle_frequency_sweep(out_dir)

    logging.info(f"Experiment completed. Results in {out_dir}")

if __name__ == "__main__":
    main()
