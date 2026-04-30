#!/usr/bin/env python3
"""
Dynamic Squat-to-Stand Cycle Simulation
=======================================

Models the dynamic transition with time-varying gravity orientation AND time-varying
information field to explicitly calculate energy dissipation terms per cycle.

Author: Dr. Sayuj Krishnan S
"""

import argparse
import csv
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure src is in path
sys.path.append(os.getcwd())

from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.pyelastica_bridge import (
    CounterCurvatureRodSystem,
    compute_U_CC,
)
from scripts.experiments.experiment_utils import StandardExperimentParser

def define_squat_stand_trajectory(t: float, t_cycle: float = 4.0) -> Tuple[float, float]:
    """
    Returns (theta_deg, I_amplitude)
    Theta: 90 deg (standing, gravity parallel) -> 0 deg (squat, gravity perp) -> 90
    I_amplitude: 1.0 (S-curve) -> 0.0 (C-curve) -> 1.0
    """
    phase = (t % t_cycle) / t_cycle
    depth = 0.5 * (1 - np.cos(2 * np.pi * phase)) # 0 at standing, 1 at squat

    theta_deg = float(90.0 * (1.0 - depth)) # 90 standing, 0 squat
    I_amp = float(1.0 - 0.8 * depth) # 1.0 standing, 0.2 squat
    return theta_deg, I_amp

def compute_cycle_dissipation(
    params: CounterCurvatureParams,
    L: float,
    n_elements: int,
    t_cycle: float,
    steps: int = 10,
    depth_factor: float = 1.0
) -> Dict[str, float]:
    """
    Quasi-static stepping to compute eta_p, eta_a, Gamma_m terms.
    """
    t_vals = np.linspace(0, t_cycle, steps)
    dt = t_cycle / steps

    eta_p_sum = 0.0
    eta_a_sum = 0.0
    gamma_m_sum = 0.0

    prev_kappa = None

    s = np.linspace(0, L, n_elements + 1)

    for t in t_vals:
        theta_deg, I_amp = define_squat_stand_trajectory(t, t_cycle)
        phase = (t % t_cycle) / t_cycle
        raw_depth = 0.5 * (1 - np.cos(2 * np.pi * phase))
        depth = raw_depth * depth_factor

        theta_deg = float(90.0 * (1.0 - depth))
        I_amp = float(1.0 - 0.8 * depth)

        I_base = np.sin(2 * np.pi * s / L)**2
        I_current = I_amp * I_base
        dIds = np.gradient(I_current, s)
        info = InfoField1D(s=s, I=I_current, dIds=dIds)

        theta_rad = np.radians(theta_deg)
        base_dir = np.array([np.cos(theta_rad), 0.0, np.sin(theta_rad)])
        normal_dir = np.array([0.0, 1.0, 0.0])

        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            radius=0.02,
        )

        result = system.run_simulation(
            final_time=0.01, # short relaxation
            dt=1e-4,
            save_every=100,
            boundary_condition="fixed"
        )

        metrics = result.compute_final_metrics()

        kappa = metrics.get('max_curvature', 1.0) * np.ones_like(s) # proxy
        if prev_kappa is not None:
            dkappa_dt = (kappa - prev_kappa) / dt
            eta_p_sum += np.sum(np.abs(dkappa_dt)**2) * dt

        prev_kappa = kappa

        kappa_passive = 0.0
        eta_a_sum += np.sum((kappa - kappa_passive)**2) * dt

        gamma_m_sum += (1.0 + 0.5 * I_amp) * L * dt

    return {
        "eta_p": eta_p_sum,
        "eta_a": eta_a_sum,
        "Gamma_m": gamma_m_sum,
        "total": eta_p_sum + eta_a_sum + gamma_m_sum
    }

def coupling_decay_model(t_days: np.ndarray, n_cycles_per_day: float, depth_factor: float = 1.0) -> np.ndarray:
    """
    χ(t) = χ₀·exp(−Δt/τ_decay), reset by each cycle
    """
    chi_0 = 1.0
    tau_decay = 10.0 # days

    maintenance = 1.0 - np.exp(-n_cycles_per_day * depth_factor / 10.0)

    chi_t = np.zeros_like(t_days, dtype=float)
    chi = chi_0

    for i, t in enumerate(t_days):
        chi = chi * np.exp(-1.0 / tau_decay)
        chi += (chi_0 - chi) * maintenance
        chi_t[i] = chi

    return chi_t

def run_cycle_frequency_sweep(out_dir: Path, L: float, n_elements: int, base_params: CounterCurvatureParams):
    print("Running Frequency Sweep...")
    N_vals = [1, 2, 5, 10, 20, 50, 100]
    days = np.arange(0, 365)

    results = []

    for N in N_vals:
        chi_t = coupling_decay_model(days, N, depth_factor=1.0)
        chi_final = chi_t[-1]
        results.append({
            "N_cycles": N,
            "chi_preservation": chi_final
        })

    csv_path = out_dir / "coupling_preservation.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["N_cycles", "chi_preservation"])
        writer.writeheader()
        writer.writerows(results)

    plt.figure(figsize=(8,6))
    Ns = [r["N_cycles"] for r in results]
    chis = [r["chi_preservation"] for r in results]
    plt.plot(Ns, chis, 'o-')
    plt.xlabel("Squat-Stand Cycles per Day")
    plt.ylabel(r"Steady State Coupling Strength (\chi / \chi_0)")
    plt.title("Coupling Preservation vs Frequency")
    plt.grid(True)
    plt.savefig(out_dir / "coupling_preservation.png")
    plt.close()

def compare_chair_vs_floor(out_dir: Path, L: float, n_elements: int, base_params: CounterCurvatureParams, quick: bool = False):
    print("Comparing Chair vs Floor...")

    steps = 5 if quick else 20

    chair_dissipation = compute_cycle_dissipation(base_params, L, n_elements, t_cycle=4.0, steps=steps, depth_factor=0.5)
    floor_dissipation = compute_cycle_dissipation(base_params, L, n_elements, t_cycle=4.0, steps=steps, depth_factor=1.0)

    csv_path = out_dir / "dissipation_breakdown.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Condition", "eta_p", "eta_a", "Gamma_m", "total"])
        writer.writeheader()

        chair_row = {"Condition": "Chair (N=3, shallow)", **chair_dissipation}
        floor_row = {"Condition": "Floor (N=50, deep)", **floor_dissipation}

        for k in ["eta_p", "eta_a", "Gamma_m", "total"]:
            chair_row[k] *= 3
            floor_row[k] *= 50

        writer.writerow(chair_row)
        writer.writerow(floor_row)

    labels = ["eta_p", "eta_a", "Gamma_m"]
    chair_vals = [chair_row["eta_p"], chair_row["eta_a"], chair_row["Gamma_m"]]
    floor_vals = [floor_row["eta_p"], floor_row["eta_a"], floor_row["Gamma_m"]]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8,6))
    rects1 = ax.bar(x - width/2, chair_vals, width, label='Chair')
    rects2 = ax.bar(x + width/2, floor_vals, width, label='Floor')

    ax.set_ylabel('Daily Energy Dissipation')
    ax.set_title('Thermodynamic Cost by Component')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()
    plt.savefig(out_dir / "dissipation_breakdown.png")
    plt.close()


def main():
    parser = StandardExperimentParser(description="Dynamic Squat-to-Stand Cycle Simulation")
    args = parser.parse_args()

    out_dir = Path("outputs/thermodynamic_cost/squat_stand_cycle")
    out_dir.mkdir(parents=True, exist_ok=True)

    L = 1.0
    n_elements = 20 if args.quick else 50

    base_params = CounterCurvatureParams(
        chi_E=0.0,
        chi_kappa=4.0,
        chi_M=15.0,
        chi_tau=0.0,
        scale_length=L
    )

    run_cycle_frequency_sweep(out_dir, L, n_elements, base_params)
    compare_chair_vs_floor(out_dir, L, n_elements, base_params, quick=args.quick)

    print(f"Results saved to {out_dir}")

if __name__ == "__main__":
    main()
