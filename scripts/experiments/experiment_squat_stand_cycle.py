#!/usr/bin/env python3
"""
Longevity Study Through Squat-to-Stand Thermodynamic Cycling

Models the dynamic transition with time-varying gravity orientation
AND time-varying information field.

Computes the free energy dissipation per cycle:
F_dot = integral[ eta_p |dkappa/dt|^2 + eta_a (kappa - kappa_passive)^2 + Gamma_m ] ds
"""

import sys
import os
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from dataclasses import dataclass

sys.path.append(os.getcwd())

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from scripts.experiments.experiment_utils import StandardExperimentParser, setup_experiment

# Biological constants
ETA_P = 1.0     # cost of sensory feedback
ETA_A = 10.0    # active muscle maintenance cost
GAMMA_M_BASE = 0.5  # basal tissue turnover

def define_squat_stand_trajectory(T_cycle: float, num_steps: int):
    """
    T_cycle=4s, theta(t) from 90° (standing) to 0° (deep squat) and back.
    I(s,t) morphs from S-curve to C-curve field.
    """
    times = np.linspace(0, T_cycle, num_steps)

    # theta: 90 -> 0 -> 90
    # Use cosine for smooth transition
    # at t=0, cos(0)=1 -> theta=90
    # at t=T/2, cos(pi)=-1 -> theta=0
    # at t=T, cos(2pi)=1 -> theta=90
    theta_deg = 45.0 + 45.0 * np.cos(2 * np.pi * times / T_cycle)

    return times, theta_deg

def compute_cycle_dissipation(shapes_kappa, dt, ds):
    """
    Computes η_p, η_a, Γ_m terms per step using quasi-static shapes.
    shapes_kappa: array of shape (num_steps, n_nodes)
    """
    num_steps, n_nodes = shapes_kappa.shape

    term_p = np.zeros(num_steps)
    term_a = np.zeros(num_steps)
    term_m = np.zeros(num_steps)

    # For η_p we need |dkappa/dt|^2
    # Simple finite diff
    dkappa_dt = np.zeros_like(shapes_kappa)
    dkappa_dt[1:-1] = (shapes_kappa[2:] - shapes_kappa[:-2]) / (2*dt)

    for i in range(num_steps):
        # 1. Proprioceptive term (eta_p * |dkappa/dt|^2)
        p_density = ETA_P * (dkappa_dt[i]**2)
        term_p[i] = np.sum(p_density) * ds

        # 2. Active maintenance term (eta_a * kappa^2)
        # Assuming kappa_passive ~ 0 for simplicity
        a_density = ETA_A * (shapes_kappa[i]**2)
        term_a[i] = np.sum(a_density) * ds

        # 3. Basal maintenance
        m_density = np.ones_like(shapes_kappa[i]) * GAMMA_M_BASE
        term_m[i] = np.sum(m_density) * ds

    total_dissipation = np.sum(term_p + term_a + term_m) * dt
    return term_p, term_a, term_m, total_dissipation

def coupling_decay_model(N_cycles_per_day: int, chi_0: float = 1.0, tau_decay: float = 2.0):
    """
    Exponential decay with periodic reset.
    Returns the time-averaged coupling strength over a day.
    """
    if N_cycles_per_day == 0:
        return 0.0

    T_day = 24.0 # hours

    # formula from framework
    chi_avg = chi_0 * (tau_decay * N_cycles_per_day / T_day) * (1 - np.exp(-T_day / (N_cycles_per_day * tau_decay)))
    return chi_avg

def run_quasi_static_cycle(system_factory, times, theta_deg, L, n_elements):
    """
    Run sequence of short equilibrium simulations at each time step.
    """
    num_steps = len(times)
    kappas = np.zeros((num_steps, n_elements + 1))

    s = np.linspace(0, L, n_elements + 1)

    for i, theta in enumerate(theta_deg):
        theta_rad = np.radians(theta)

        # Base direction based on tilt angle
        base_dir = np.array([np.cos(theta_rad), 0.0, np.sin(theta_rad)])
        normal_dir = np.array([0.0, 1.0, 0.0])

        # Info Field Morphing
        # Standing (90 deg): S-curve -> sin^2
        # Squat (0 deg): C-curve -> uniform or linear
        weight_s = (theta / 90.0)
        I_s = np.sin(2 * np.pi * s / L)**2
        I_c = 4 * (s/L) * (1 - s/L) # Parabola (C-curve)

        I = weight_s * I_s + (1 - weight_s) * I_c
        dIds = np.gradient(I, s)
        info = InfoField1D(s=s, I=I, dIds=dIds)

        # Create system with current params
        system = system_factory(base_dir, normal_dir, info)

        # Quasi-static run: short simulation
        sim_res = system.run_simulation(final_time=0.5, dt=1e-4, save_every=100)

        final_kappa = sim_res.kappa[-1] # (n_nodes, 3)
        bending_k = final_kappa[:, 1]
        kappas[i] = bending_k

    return kappas

def main():
    parser = StandardExperimentParser("Dynamic Squat-to-Stand Cycle Simulation")
    args = parser.parse_args()

    out_dir = setup_experiment(args)

    # Constants
    L = 1.0
    n_elements = 20 if args.quick else 50
    E0 = 1e6
    radius = 0.02
    rho = 1000
    gravity_magnitude = 9.81

    chi_kappa = 4.0
    chi_M = 15.0

    base_params = CounterCurvatureParams(
        chi_E=0.0,
        chi_kappa=chi_kappa,
        chi_M=chi_M,
        chi_tau=0.0,
        scale_length=L
    )

    def system_factory(base_dir, normal_dir, info):
        return CounterCurvatureRodSystem.from_iec(
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

    # 1. Run full deep squat cycle (floor vs chair)
    T_cycle = 4.0
    num_steps = 10 if args.quick else 40

    times, theta_deg_floor = define_squat_stand_trajectory(T_cycle, num_steps)

    # Chair cycle: shallow squat (90 -> 45 -> 90)
    theta_deg_chair = 67.5 + 22.5 * np.cos(2 * np.pi * times / T_cycle)

    print("Running floor cycle (deep squat)...")
    kappas_floor = run_quasi_static_cycle(system_factory, times, theta_deg_floor, L, n_elements)

    print("Running chair cycle (shallow squat)...")
    kappas_chair = run_quasi_static_cycle(system_factory, times, theta_deg_chair, L, n_elements)

    dt = T_cycle / num_steps
    ds = L / n_elements

    p_f, a_f, m_f, total_f = compute_cycle_dissipation(kappas_floor, dt, ds)
    p_c, a_c, m_c, total_c = compute_cycle_dissipation(kappas_chair, dt, ds)

    # 2. Compare Chair vs Floor
    with open(out_dir / "cycle_dissipation.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Condition", "Term_P_sum", "Term_A_sum", "Term_M_sum", "Total_Dissipation"])
        writer.writerow(["Floor (Deep)", np.sum(p_f)*dt, np.sum(a_f)*dt, np.sum(m_f)*dt, total_f])
        writer.writerow(["Chair (Shallow)", np.sum(p_c)*dt, np.sum(a_c)*dt, np.sum(m_c)*dt, total_c])

    # Plot Trajectories
    plt.figure()
    plt.plot(times, theta_deg_floor, label="Floor (Deep Squat)")
    plt.plot(times, theta_deg_chair, label="Chair (Shallow Squat)")
    plt.xlabel("Time (s)")
    plt.ylabel("Tilt Angle (deg)")
    plt.title("Squat-to-Stand Trajectories")
    plt.legend()
    plt.grid(True)
    plt.savefig(out_dir / "trajectories.png")
    plt.close()

    # Plot Dissipation Breakdown
    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    plt.plot(times, p_f, label="Floor")
    plt.plot(times, p_c, label="Chair")
    plt.title(r"$\eta_p$ Proprioceptive Cost")
    plt.xlabel("Time (s)")

    plt.subplot(132)
    plt.plot(times, a_f, label="Floor")
    plt.plot(times, a_c, label="Chair")
    plt.title(r"$\eta_a$ Active Maintenance Cost")
    plt.xlabel("Time (s)")
    plt.legend()

    plt.subplot(133)
    plt.plot(times, m_f, label="Floor")
    plt.plot(times, m_c, label="Chair")
    plt.title(r"$\Gamma_m$ Basal Cost")
    plt.xlabel("Time (s)")

    plt.tight_layout()
    plt.savefig(out_dir / "dissipation_breakdown.png")
    plt.close()

    # Plot Curvature Heatmap (Floor)
    plt.figure()
    plt.imshow(kappas_floor.T, aspect='auto', origin='lower', cmap='RdBu',
               extent=[0, T_cycle, 0, L])
    plt.colorbar(label="Curvature $\\kappa$ (1/m)")
    plt.xlabel("Time (s)")
    plt.ylabel("Spinal Length $s$ (m)")
    plt.title("Spinal Curvature during Floor Squat Cycle")
    plt.savefig(out_dir / "curvature_heatmap.png")
    plt.close()

    # 3. Run cycle frequency sweep (Coupling Decay)
    N_values = [0, 1, 2, 3, 5, 10, 20, 50, 100]
    chi_avgs = [coupling_decay_model(N, chi_0=1.0) for N in N_values]

    with open(out_dir / "coupling_decay.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["N_cycles_per_day", "Avg_Coupling_Ratio"])
        for N, c in zip(N_values, chi_avgs):
            writer.writerow([N, c])

    plt.figure()
    plt.plot(N_values, chi_avgs, 'o-')
    plt.axvline(x=3, color='r', linestyle='--', label='Chair-sitter (N=3)')
    plt.axvline(x=50, color='g', linestyle='--', label='Floor-sitter (N=50)')
    plt.xlabel("Cycles per Day")
    plt.ylabel("Time-averaged Coupling Ratio $\\chi_{avg} / \\chi_0$")
    plt.title("Coupling Preservation vs Cycle Frequency")
    plt.legend()
    plt.grid(True)
    plt.savefig(out_dir / "coupling_preservation.png")
    plt.close()

    print(f"Results saved to {out_dir}")

if __name__ == "__main__":
    main()
