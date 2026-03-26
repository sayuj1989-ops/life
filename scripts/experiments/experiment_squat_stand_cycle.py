#!/usr/bin/env python3
"""
Thermodynamic Longevity Study: Squat-to-Stand Cycle
===================================================

Simulates the squat-to-stand motion as a thermodynamic cycle, calculating
the energy dissipation (eta_p, eta_a, Gamma_m) during the transition.
Models coupling decay chi(t) = chi_0 * exp(-Delta_t / tau_decay) which
is periodically reset by thermodynamic perturbation cycles (like
squatting-to-standing). Connects framework to Okinawa longevity observations.

Author: Dr. Sayuj Krishnan S
"""

import csv
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Ensure src is in path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from scripts.experiments.experiment_utils import StandardExperimentParser

def define_squat_stand_trajectory(L: float, n_points: int, is_deep: bool = True) -> List[Tuple[float, float, InfoField1D]]:
    """
    Defines a sequence of quasi-static steps over a T_cycle trajectory.
    If is_deep (floor-sit), theta transitions from 90° (standing) to 0° (deep squat).
    If not is_deep (chair-sit), theta transitions from 90° (standing) to 45° (shallow squat).

    Returns: List of (time_t, theta_deg, info_field)
    """
    T_cycle = 4.0
    dt_step = 0.5

    steps = []
    s = np.linspace(0, L, n_points)

    # Pre-compute baseline fields
    I_S_curve = np.sin(2 * np.pi * s / L)**2  # Promotes S-shape (Standing)
    I_C_curve = np.sin(np.pi * s / L)         # Promotes C-shape (Squat)

    min_theta = 0.0 if is_deep else 45.0

    for t in np.arange(0, T_cycle + dt_step/2, dt_step):
        # 0 to T_cycle/2: Stand -> Squat
        # T_cycle/2 to T_cycle: Squat -> Stand
        if t <= T_cycle / 2:
            phase = t / (T_cycle / 2) # 0 to 1
        else:
            phase = 1.0 - (t - T_cycle / 2) / (T_cycle / 2) # 1 to 0

        theta_deg = 90.0 - phase * (90.0 - min_theta)

        # Morph InfoField
        I_t = (1.0 - phase) * I_S_curve + phase * I_C_curve
        dIds_t = np.gradient(I_t, s)

        info = InfoField1D(s=s, I=I_t, dIds=dIds_t)
        steps.append((t, theta_deg, info))

    return steps

def compute_cycle_dissipation(trajectory: List[Tuple[float, float, InfoField1D]], base_params: CounterCurvatureParams, L: float, n_elements: int, E0: float, radius: float, rho: float, gravity_magnitude: float, label: str, output_dir: Path) -> Dict[str, float]:
    """
    Computes energy dissipation terms for one full cycle and plots the curvature heatmap.
    """
    eta_p_sum = 0.0
    eta_a_sum = 0.0
    Gamma_m_sum = 0.0

    dt = trajectory[1][0] - trajectory[0][0]
    prev_kappa = None

    curvature_matrix = []
    times = []

    for t, theta_deg, info in trajectory:
        theta_rad = np.radians(theta_deg)
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

        res = system.run_simulation(final_time=0.2, dt=1e-4, save_every=100, progress_bar=False)

        kappa = res.kappa[-1] # shape (n_nodes, 3)
        bending_mag = np.linalg.norm(kappa[:, :2], axis=1)
        curvature_matrix.append(bending_mag)
        times.append(t)

        eta_a_step = np.sum(bending_mag**2) * (L / n_elements)
        eta_a_sum += eta_a_step * dt

        Gamma_m_step = (np.pi * radius**2 * L) * 1e4
        Gamma_m_sum += Gamma_m_step * dt

        if prev_kappa is not None:
            dkappa_dt = (bending_mag - prev_kappa) / dt
            eta_p_step = np.sum(dkappa_dt**2) * (L / n_elements)
            eta_p_sum += eta_p_step * dt

        prev_kappa = bending_mag

    # Heatmap Plotting
    curvature_matrix = np.array(curvature_matrix).T # (n_nodes, time_steps)
    plt.figure(figsize=(10, 6))
    sns.heatmap(curvature_matrix, cmap='viridis', xticklabels=np.round(times,1), yticklabels=False)
    plt.title(f'Curvature Evolution over {label} Cycle')
    plt.xlabel('Time (s)')
    plt.ylabel('Arc Length s')
    plt.tight_layout()
    plt.savefig(output_dir / f"curvature_heatmap_{label.lower().replace(' ', '_')}.png")
    plt.close()

    return {
        "trajectory": label,
        "eta_p_cycle": eta_p_sum,
        "eta_a_cycle": eta_a_sum,
        "Gamma_m_cycle": Gamma_m_sum,
        "total_dissipation": eta_p_sum + eta_a_sum + Gamma_m_sum
    }

def coupling_decay_model(cycles_per_day: int, days: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    """
    Phenomenological model of coupling chi(t).
    Decays exponentially when inactive, resets by a cycle.
    tau_decay = 16 hours (approx circadian)
    """
    tau_decay = 16.0 # hours
    chi_0 = 1.0

    dt = 0.1 # hours
    total_hours = days * 24.0
    time_h = np.arange(0, total_hours, dt)
    chi = np.zeros_like(time_h)

    chi[0] = chi_0

    if cycles_per_day > 0:
        cycle_interval = 24.0 / cycles_per_day
    else:
        cycle_interval = np.inf

    next_cycle = cycle_interval

    for i in range(1, len(time_h)):
        t = time_h[i]

        if t >= next_cycle:
            chi[i] = chi_0
            next_cycle += cycle_interval
        else:
            chi[i] = chi[i-1] * np.exp(-dt / tau_decay)

    return time_h, chi

def compare_chair_vs_floor(output_dir: Path, base_params: CounterCurvatureParams, L: float, n_elements: int, E0: float, radius: float, rho: float, gravity_magnitude: float):
    """
    Simulates chair-sitting (N=3, shallow) vs Floor-sitting (N=50, deep).
    Computes true dissipation per profile and plots decay preservation.
    """
    n_points = n_elements + 1

    print("  -> Simulating Deep Squat (Floor)...")
    traj_deep = define_squat_stand_trajectory(L, n_points, is_deep=True)
    diss_deep = compute_cycle_dissipation(traj_deep, base_params, L, n_elements, E0, radius, rho, gravity_magnitude, "Deep Floor Squat", output_dir)

    print("  -> Simulating Shallow Squat (Chair)...")
    traj_shallow = define_squat_stand_trajectory(L, n_points, is_deep=False)
    diss_shallow = compute_cycle_dissipation(traj_shallow, base_params, L, n_elements, E0, radius, rho, gravity_magnitude, "Shallow Chair Squat", output_dir)

    # Save Dissipation Comparison CSV
    csv_path = output_dir / "chair_vs_floor_dissipation.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=diss_deep.keys())
        writer.writeheader()
        writer.writerow(diss_deep)
        writer.writerow(diss_shallow)

    # Plot Dissipation Breakdown
    labels = ['eta_p (Proprioceptive)', 'eta_a (Active Moment)', 'Gamma_m (Basal)']
    deep_vals = [diss_deep['eta_p_cycle'], diss_deep['eta_a_cycle'], diss_deep['Gamma_m_cycle']]
    shallow_vals = [diss_shallow['eta_p_cycle'], diss_shallow['eta_a_cycle'], diss_shallow['Gamma_m_cycle']]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8,6))
    ax.bar(x - width/2, deep_vals, width, label='Deep (Floor)')
    ax.bar(x + width/2, shallow_vals, width, label='Shallow (Chair)')

    ax.set_ylabel('Energy Dissipated per Cycle (J)')
    ax.set_title('Dissipation Breakdown: Chair vs Floor')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "dissipation_breakdown.png")
    plt.close()

    # Decay comparison (Chair 3 vs Floor 50)
    t_chair, chi_chair = coupling_decay_model(cycles_per_day=3, days=3)
    t_floor, chi_floor = coupling_decay_model(cycles_per_day=50, days=3)

    plt.figure(figsize=(10, 5))
    plt.plot(t_chair, chi_chair, label='Chair-sitting (3 cycles/day)', color='orange')
    plt.plot(t_floor, chi_floor, label='Floor-sitting (50 cycles/day)', color='blue')
    plt.axhline(y=0.6, color='red', linestyle='--', label='Critical Instability Threshold')

    plt.title('Coupling Preservation $\\chi(t)$ Over 3 Days')
    plt.xlabel('Time (Hours)')
    plt.ylabel('Normalized Coupling $\\chi(t) / \\chi_0$')
    plt.ylim([0, 1.1])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "coupling_preservation_chair_vs_floor.png")
    plt.close()

def run_cycle_frequency_sweep(output_dir: Path):
    N_values = [0, 1, 2, 5, 10, 20, 50, 100]
    results = []

    for N in N_values:
        t, chi = coupling_decay_model(cycles_per_day=N, days=7)
        avg_chi = np.mean(chi)
        min_chi = np.min(chi)
        results.append({
            "cycles_per_day": N,
            "avg_coupling": avg_chi,
            "min_coupling": min_chi
        })

    csv_path = output_dir / "cycle_frequency_sweep.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    N_arr = [r["cycles_per_day"] for r in results]
    avg_arr = [r["avg_coupling"] for r in results]

    plt.figure(figsize=(8, 5))
    plt.plot(N_arr, avg_arr, marker='o')
    plt.title('Average Coupling vs Daily Squat-Stand Cycles')
    plt.xlabel('Cycles per Day (N)')
    plt.ylabel('Average $\\chi(t)$')
    plt.grid(True)
    plt.axvline(x=50, color='green', linestyle=':', label='Okinawa Target (~50-100)')
    plt.axvline(x=3, color='orange', linestyle=':', label='Modern Baseline (~3)')
    plt.legend()
    plt.savefig(output_dir / "avg_coupling_vs_frequency.png")
    plt.close()


def main():
    parser = StandardExperimentParser(description="Squat-Stand Thermodynamic Cycle Sim")
    args = parser.parse_args()

    output_dir = Path("outputs/thermodynamic_cost/squat_stand_cycle")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("  THERMODYNAMIC SQUAT-TO-STAND CYCLE SIMULATION")
    print("=" * 70)

    L = 1.0
    E0 = 1e6
    radius = 0.02
    rho = 1000
    gravity_magnitude = 9.81

    n_elements = 20 if args.quick else 50

    base_params = CounterCurvatureParams(
        chi_E=0.0, chi_kappa=4.0, chi_M=15.0, chi_tau=0.0, scale_length=L
    )

    print("1. Comparing Floor-Sitting (Deep) vs Chair-Sitting (Shallow)...")
    compare_chair_vs_floor(output_dir, base_params, L, n_elements, E0, radius, rho, gravity_magnitude)

    print("2. Running Cycle Frequency Sweep...")
    run_cycle_frequency_sweep(output_dir)

    print(f"✅ Complete. Results saved to {output_dir}")

if __name__ == "__main__":
    main()
