#!/usr/bin/env python3
"""
Longevity Squat-to-Stand Cycle Simulation
==========================================

Demonstrates that the squat-to-stand transition is the fundamental thermodynamic pulse
that exercises the three dissipation terms ($\eta_p, \eta_a, \Gamma_m$) of the
countercurvature framework. It shows how regular cycling preserves the mechanical
coupling strength $\chi$, preventing age-related structural decay.

Author: Dr. Sayuj Krishnan S
Date: 2026-02-07
"""

import logging
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add src to path if running directly
sys.path.append(os.getcwd())

from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from scripts.experiments.experiment_utils import StandardExperimentParser

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

# Rod Parameters
L = 0.5            # Spinal length (m)
N_ELEMENTS = 40    # Resolution
E0 = 5e6           # Base stiffness (Pa)
RADIUS = 0.02      # Effective radius (m)
RHO = 1100         # Density (kg/m^3)
GRAVITY = 9.81     # Gravity (m/s^2)

# Thermodynamic Dissipation Coefficients (Arbitrary units for demo)
ETA_P = 1500.0     # Proprioceptive cost (scales with d\kappa/dt)
ETA_A = 5000.0     # Active maintenance cost (scales with \kappa)
GAMMA_M_BASE = 50.0 # Basal maintenance (steady state)
GAMMA_M_EXERTION = 300.0 # Exertion multiplier

# Coupling Decay Model
CHI_0 = 10.0       # Peak coupling strength
TAU_DECAY = 2.0    # Hours to decay by 1/e (derived from microgravity rapid loss)


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def setup_experiment(args) -> Path:
    out_dir = Path("outputs/sim") / args.date
    out_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Experiment setup complete.")
    logging.info(f"Output directory: {out_dir}")

    if args.quick:
        logging.warning("Running in QUICK mode (reduced parameters).")
        global N_ELEMENTS
        N_ELEMENTS = 10

    return out_dir


def define_squat_stand_trajectory(t_eval: np.ndarray, is_chair: bool = False):
    """
    Defines the trajectory of a sit-to-stand transition.
    A floor squat is a deep transition (90 deg swing).
    A chair sit is a shallow transition (45 deg swing).
    """
    s = np.linspace(0, L, N_ELEMENTS + 1)
    thetas = []
    info_fields = []

    for t in t_eval:
        # Phase from 0 to 1 over the 4s cycle
        phase = t / 4.0

        # Cosine interpolation between Standing (phase=0,1) and Squat (phase=0.5)
        # alpha goes from 1.0 (Stand) to 0.0 (Squat) to 1.0 (Stand)
        alpha = 0.5 * (1.0 + np.cos(2 * np.pi * phase))

        # 1. Orientation Theta
        # Standing = 90 deg (gravity parallel to spine)
        # Deep Squat = 0 deg (gravity perp to spine)
        # Chair Sit = 45 deg
        min_theta = 45.0 if is_chair else 0.0
        theta_deg = min_theta + (90.0 - min_theta) * alpha
        thetas.append(theta_deg)

        # 2. Information Field Morphing
        # Standing (alpha=1): S-curve -> sine wave squared
        I_stand = np.sin(2 * np.pi * s / L)**2
        # Squatting (alpha=0): C-curve -> simple parabolic or constant
        I_squat = 4 * (s/L) * (1 - (s/L))

        # Morph I
        I_t = alpha * I_stand + (1 - alpha) * I_squat
        dIds_t = np.gradient(I_t, s)

        info_fields.append(InfoField1D(s=s, I=I_t, dIds=dIds_t))

    return np.array(thetas), info_fields


def compute_cycle_dissipation(thetas: np.ndarray, info_fields: list, dt_step: float, out_dir: Path, chi_current: float = CHI_0):
    """
    Performs quasi-static stepping through the trajectory using PyElastica.
    Computes \eta_p, \eta_a, \Gamma_m per step.
    """
    logging.info(f"Computing thermodynamic cycle over {len(thetas)} steps with chi={chi_current:.2f}...")

    results = []
    centerlines = []
    kappas = []

    # Store previous curvature for d\kappa/dt
    prev_kappa = None

    for i, (theta_deg, info) in enumerate(zip(thetas, info_fields)):
        t_current = i * dt_step

        theta_rad = np.radians(theta_deg)
        base_dir = np.array([np.cos(theta_rad), 0.0, np.sin(theta_rad)])
        normal_dir = np.array([0.0, 1.0, 0.0])

        params = CounterCurvatureParams(
            chi_E=0.0,
            chi_kappa=chi_current,
            chi_M=chi_current, # Active muscle moment tracking coupling
            chi_tau=0.0,
            scale_length=L
        )

        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=N_ELEMENTS,
            E0=E0,
            radius=RADIUS,
            rho=RHO,
            gravity=GRAVITY,
            base_direction=tuple(base_dir),
            normal=tuple(normal_dir)
        )

        # Quasi-static relaxation (1.0s is usually enough for the rod to settle)
        sim_res = system.run_simulation(final_time=1.0, dt=1e-4, save_every=1000, progress_bar=False)

        # Extract final shape
        cl = sim_res.centerline[-1]
        kappa = sim_res.kappa[-1]  # (n_nodes, 3)
        bending_k = kappa[:, 1]  # Sagittal bending

        # Calculate Rate of Change (d\kappa/dt)
        if prev_kappa is not None:
            dk_dt = (bending_k - prev_kappa) / dt_step
        else:
            dk_dt = np.zeros_like(bending_k)
        prev_kappa = bending_k

        # Calculate Dissipation Terms
        # 1. Proprioceptive (eta_p |dk/dt|^2) -> integrates over length
        term_p = ETA_P * np.trapz(dk_dt**2, dx=L/N_ELEMENTS)

        # 2. Active Maintenance (eta_a |k - k_pass|^2)
        # For simplicity, assume passive geodesic is straight (k_pass = 0)
        # under zero active moments. The cost is maintaining the actual curvature.
        term_a = ETA_A * np.trapz(bending_k**2, dx=L/N_ELEMENTS)

        # 3. Basal Maintenance (\Gamma_m)
        # Higher during the transition (muscular exertion)
        # We model exertion by checking the magnitude of dk/dt
        exertion_factor = np.mean(np.abs(dk_dt))
        # Add baseline + exertion spike
        term_g = (GAMMA_M_BASE + GAMMA_M_EXERTION * exertion_factor) * L

        total_dissipation = term_p + term_a + term_g

        results.append({
            "time": t_current,
            "theta": theta_deg,
            "eta_p": term_p,
            "eta_a": term_a,
            "gamma_m": term_g,
            "total_dissipation": total_dissipation
        })
        centerlines.append(cl)
        kappas.append(bending_k)

    df_res = pd.DataFrame(results)
    df_res.to_csv(out_dir / "cycle_dissipation.csv", index=False)

    # Plot Dissipation Breakdown
    plt.figure(figsize=(10, 6))
    plt.plot(df_res["time"], df_res["eta_p"], label="$\\eta_p$ (Proprioceptive/Sensing)", color='red')
    plt.plot(df_res["time"], df_res["eta_a"], label="$\\eta_a$ (Active Maintenance)", color='blue')
    plt.plot(df_res["time"], df_res["gamma_m"], label="$\\Gamma_m$ (Basal Maintenance)", color='green')
    plt.xlabel("Cycle Time (s)")
    plt.ylabel("Dissipation Rate (Energy/Time)")
    plt.title("Thermodynamic Cost of Squat-to-Stand Transition")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "dissipation_breakdown.png", dpi=300)
    plt.close()

    return df_res, centerlines, kappas


def coupling_decay_model(n_cycles_per_day: int, t_hours: np.ndarray):
    """
    Models the phenomenological decay of coupling strength (\chi) without cycling.
    Each cycle resets \chi to CHI_0.
    """
    chi_t = np.zeros_like(t_hours)

    if n_cycles_per_day == 0:
        return CHI_0 * np.exp(-t_hours / TAU_DECAY)

    cycle_interval = 24.0 / n_cycles_per_day

    for i, t in enumerate(t_hours):
        time_since_last_cycle = t % cycle_interval
        chi_t[i] = CHI_0 * np.exp(-time_since_last_cycle / TAU_DECAY)

    return chi_t


def run_cycle_frequency_sweep(out_dir: Path):
    """
    Runs a sweep over different cycle frequencies to demonstrate the coupling preservation.
    """
    logging.info("Running cycle frequency sweep...")

    frequencies = [0, 1, 3, 5, 10, 20, 50, 80, 100]
    t_hours = np.linspace(0, 24, 1000)

    results = []

    plt.figure(figsize=(12, 8))

    for n in frequencies:
        chi_t = coupling_decay_model(n, t_hours)
        avg_chi = np.mean(chi_t)
        pct_preserved = (avg_chi / CHI_0) * 100

        results.append({
            "cycles_per_day": n,
            "avg_chi": avg_chi,
            "pct_preserved": pct_preserved
        })

        if n in [0, 3, 20, 50, 80]:
            plt.plot(t_hours, chi_t / CHI_0, label=f"N={n} ({pct_preserved:.1f}%)")

    plt.xlabel("Time (hours)")
    plt.ylabel("Coupling Strength $\chi(t) / \chi_0$")
    plt.title("Coupling Decay vs Daily Squat-to-Stand Cycles")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "coupling_decay.png", dpi=300)
    plt.close()

    df_res = pd.DataFrame(results)
    df_res.to_csv(out_dir / "cycle_frequency_preservation.csv", index=False)

    # Plot preservation curve
    plt.figure(figsize=(10, 6))
    plt.plot(df_res["cycles_per_day"], df_res["pct_preserved"], 'o-', color='blue')
    plt.xlabel("Cycles per Day")
    plt.ylabel("Time-Averaged Coupling Preserved (%)")
    plt.title("Longevity Effect of Squat-to-Stand Cycling")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "preservation_curve.png", dpi=300)
    plt.close()


def compare_chair_vs_floor(out_dir: Path, quick: bool = False):
    """
    Compares chair-sitting (shallow transition) vs floor-sitting (deep transition).
    """
    logging.info("Comparing Chair vs Floor sitting transitions...")

    # Compute decayed coupling parameters
    t_eval_decay = np.linspace(0, 24, 100)
    chi_floor_arr = coupling_decay_model(50, t_eval_decay)  # Floor: 50 cycles/day
    chi_chair_arr = coupling_decay_model(3, t_eval_decay)   # Chair: 3 cycles/day

    chi_floor = np.mean(chi_floor_arr)
    chi_chair = np.mean(chi_chair_arr)

    # Floor: Deep squat (0 deg), Chair: Shallow (45 deg)
    dt_step = 1.0 if quick else 0.2
    t_eval = np.arange(0, 4.0 + dt_step, dt_step)

    thetas_floor, info_floor = define_squat_stand_trajectory(t_eval, is_chair=False)
    df_floor, cl_floor, _ = compute_cycle_dissipation(thetas_floor, info_floor, dt_step, out_dir / "floor", chi_current=chi_floor)

    thetas_chair, info_chair = define_squat_stand_trajectory(t_eval, is_chair=True)
    df_chair, cl_chair, _ = compute_cycle_dissipation(thetas_chair, info_chair, dt_step, out_dir / "chair", chi_current=chi_chair)

    # Total Dissipation Comparison
    floor_diss = df_floor["total_dissipation"].sum() * dt_step
    chair_diss = df_chair["total_dissipation"].sum() * dt_step

    logging.info(f"Total Thermodynamic Dose - Floor: {floor_diss:.2f}, Chair: {chair_diss:.2f}")

    # Visual comparison of trajectories
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    for i, cl in enumerate(cl_floor):
        alpha = 0.3 + 0.7 * (i / len(cl_floor))
        plt.plot(cl[0, :], cl[2, :], 'b-', alpha=alpha)
    plt.title("Floor Squat-to-Stand (Deep)")
    plt.xlabel("X (m)")
    plt.ylabel("Z (m)")
    plt.axis('equal')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    for i, cl in enumerate(cl_chair):
        alpha = 0.3 + 0.7 * (i / len(cl_chair))
        plt.plot(cl[0, :], cl[2, :], 'r-', alpha=alpha)
    plt.title("Chair Sit-to-Stand (Shallow)")
    plt.xlabel("X (m)")
    plt.ylabel("Z (m)")
    plt.axis('equal')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_dir / "trajectory_comparison.png", dpi=300)
    plt.close()


def main():
    parser = StandardExperimentParser(description="Longevity Squat-to-Stand Cycle Simulation")
    args = parser.parse_args()
    out_dir = setup_experiment(args)

    # Create subdirs for comparisons
    (out_dir / "floor").mkdir(parents=True, exist_ok=True)
    (out_dir / "chair").mkdir(parents=True, exist_ok=True)

    # 1. Run frequency sweep
    run_cycle_frequency_sweep(out_dir)

    # 2. Compare Chair vs Floor (Thermodynamic Cost)
    compare_chair_vs_floor(out_dir, quick=args.quick)

    logging.info(f"Experiment completed. Results saved to {out_dir}")


if __name__ == "__main__":
    main()
