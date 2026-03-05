#!/usr/bin/env python3
"""
Dynamic Squat-to-Stand Cycle Simulation
=======================================

Models the dynamic transition with time-varying gravity orientation and
time-varying information field. Interprets squat-to-stand as thermodynamic
cycling of the standing wave, computing the energy budget per cycle and modeling
coupling decay.

Functions:
- define_squat_stand_trajectory: T_cycle=4s, theta(t) from 90 to 0 to 90
- compute_cycle_dissipation: Computes eta_p, eta_a, Gamma_m terms per step
- coupling_decay_model: Exponential decay with periodic reset
- run_cycle_frequency_sweep: N=[1,2,5,10,20,50,100] cycles/day
- compare_chair_vs_floor: chair vs floor trajectories

Author: Dr. Sayuj Krishnan S
"""

import csv
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

# Ensure src is in path
sys.path.append(os.getcwd())


from scripts.experiments.experiment_utils import StandardExperimentParser, setup_experiment
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem


def define_squat_stand_trajectory(T_cycle, n_steps, L):
    """
    Defines the time-varying gravity tilt and information field shape.
    theta(t) from 90 deg (standing) to 0 deg (deep squat) and back.
    I(s,t) morphs from S-curve to C-curve field.
    """
    t_vals = np.linspace(0, T_cycle, n_steps)
    thetas = []
    infos = []

    s = np.linspace(0, L, 100)
    # I_stand: Sinusoidal -> promotes S-shape
    I_stand = np.sin(2 * np.pi * s / L)**2
    # I_squat: Parabolic -> promotes C-shape (kyphosis only)
    I_squat = 4 * (s/L) * (1 - s/L)

    for t in t_vals:
        # Phase 0 to 1: 0=stand, 0.5=squat, 1.0=stand
        phase = t / T_cycle
        if phase < 0.5:
            # Stand to squat
            mix = phase * 2  # 0 to 1
        else:
            # Squat to stand
            mix = (1.0 - phase) * 2  # 1 to 0

        # Theta: 90 (stand) to 0 (squat)
        theta_deg = 90.0 - (mix * 90.0)
        thetas.append(theta_deg)

        # Info field: mix of stand and squat
        I_t = (1 - mix) * I_stand + mix * I_squat
        dIds = np.gradient(I_t, s)
        infos.append(InfoField1D(s=s, I=I_t, dIds=dIds))

    return t_vals, thetas, infos

def compute_cycle_dissipation(theta_deg, info, L, base_params, E0, radius, rho, n_elements):
    """
    Quasi-static stepping: run a short simulation for the given parameters
    and return the energy terms and final state.

    Dissipation Functional F_dot = integral[ eta_p |dkappa/dt|^2 + eta_a (kappa - kappa_passive)^2 + Gamma_m(s) ] ds
    """
    theta_rad = np.radians(theta_deg)

    # We rotate the rod base direction relative to gravity
    # rod along X rotated by theta. Gravity -Z.
    # when theta=0 (squat), rod horizontal. Gravity perpendicular.
    # when theta=90 (stand), rod vertical. Gravity parallel.
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
        gravity=9.81,
        base_direction=tuple(base_dir),
        normal=tuple(normal_dir)
    )

    # Run short quasi-static step
    sim_res = system.run_simulation(final_time=0.5, dt=1e-4, save_every=500, progress_bar=False)

    # Final configuration
    final_kappa = sim_res.kappa[-1]
    bending_k = final_kappa[:, 1]  # sagittal bending

    avg_k = np.mean(np.abs(bending_k))

    # Calculate energy components
    # eta_a term: Active moment maintenance. Modeled as (kappa - kappa_passive)^2.
    # For simplicity, assume kappa_passive ~ 0 for lateral, natural kyphosis for sagittal.
    # Let's use the magnitude of active curvature needed to oppose gravity.
    # More practically, active maintenance is proportional to the bending load.
    eta_a_base = 1e-2 # Scaling constant
    # Integration over rod length (sum of kappa^2 scaled by element length ds)
    ds = L / n_elements
    eta_a_term = eta_a_base * np.sum((bending_k)**2) * ds

    # Gamma_m term: Basal tissue maintenance
    # Baseline maintenance cost is relatively constant but boosted by muscle activity
    # Gamma_m = Gamma_base + SIRT1/PPARGC1A exercise-induced boost
    Gamma_base = 0.5 * L # proportional to volume/length
    # Boost is proportional to active muscular effort (eta_a) + proprioceptive demand
    # SIRT1 activated by high energy turnover
    Gamma_m_term = Gamma_base + (0.1 * eta_a_term)

    return avg_k, eta_a_term, Gamma_m_term, final_kappa

def coupling_decay_model(chi_0, N_cycles, tau_decay_hrs=2.0, T_day_hrs=24.0):
    """
    Exponential decay of spinal coupling with periodic reset.
    Returns average coupling chi_avg over the day.
    """
    if N_cycles == 0:
        return 0.0

    # Average of an exponential decay over the interval T_day/N
    # (1/T_int) * integral_0^{T_int} exp(-t/tau) dt
    T_int = T_day_hrs / N_cycles
    chi_avg = chi_0 * (tau_decay_hrs / T_int) * (1 - np.exp(-T_int / tau_decay_hrs))
    return chi_avg

def run_cycle_frequency_sweep(out_dir):
    N_list = [0, 1, 2, 3, 5, 10, 20, 50, 80, 100]
    chi_0 = 15.0 # Base active muscle coupling

    results = []
    for N in N_list:
        chi_avg = coupling_decay_model(chi_0, N)
        pct = (chi_avg / chi_0) * 100

        # Categorize lifestyle based on cycles
        if N <= 1: lifestyle = "Sedentary / Bedridden"
        elif N <= 5: lifestyle = "Chair-sitter"
        elif N <= 20: lifestyle = "Active-sitter"
        elif N <= 60: lifestyle = "Floor-sitter"
        else: lifestyle = "Okinawan elder"

        results.append({
            "N_cycles": N,
            "chi_avg": chi_avg,
            "preservation_pct": pct,
            "lifestyle": lifestyle
        })

    csv_path = out_dir / "coupling_preservation.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # Plot
    Ns = [r["N_cycles"] for r in results]
    pcts = [r["preservation_pct"] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(Ns, pcts, 'bo-', linewidth=2, markersize=8)

    # Add annotations for lifestyles
    for r in results:
        if r["N_cycles"] in [0, 3, 20, 50, 80]:
            plt.annotate(r["lifestyle"],
                        (r["N_cycles"], r["preservation_pct"]),
                        xytext=(10, -10), textcoords='offset points')

    plt.axhline(y=90, color='r', linestyle='--', label='90% threshold (Healthy Aging)')
    plt.axhline(y=30, color='g', linestyle='--', label='30% threshold (Risk Zone)')

    plt.xlabel('Squat-to-Stand Cycles per Day')
    plt.ylabel('Spinal Coupling Preservation (%)')
    plt.title('Spinal Coupling Maintenance via Thermodynamic Cycling')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "coupling_preservation.png", dpi=300)
    plt.close()

    return results

def compare_chair_vs_floor(out_dir, quick_mode=False):
    """
    Simulates the actual thermodynamic cycle for a chair-sitter vs floor-sitter,
    calculating the three dissipation terms per step.
    """
    # Chair (N=3, shallow depth proxy: scaled chi_M)
    # Floor (N=50, deep depth proxy: near full chi_M)
    T_cycle = 4.0
    n_steps = 5 if quick_mode else 20
    L = 1.0
    E0 = 1e6
    radius = 0.02
    rho = 1000
    n_elements = 20 if quick_mode else 50

    t_vals, thetas, infos = define_squat_stand_trajectory(T_cycle, n_steps, L)
    dt_step = T_cycle / (n_steps - 1)

    # Calculate base parameters for Chair (decayed chi_M) and Floor (preserved chi_M)
    chi_0 = 15.0
    chi_chair = coupling_decay_model(chi_0, 3)
    chi_floor = coupling_decay_model(chi_0, 50)

    chair_params = CounterCurvatureParams(chi_E=0.0, chi_kappa=4.0, chi_M=chi_chair, chi_tau=0.0, scale_length=L)
    floor_params = CounterCurvatureParams(chi_E=0.0, chi_kappa=4.0, chi_M=chi_floor, chi_tau=0.0, scale_length=L)

    chair_results = []
    floor_results = []

    prev_k_chair = None
    prev_k_floor = None

    print(f"Running trajectory points: {n_steps}")

    for i in range(n_steps):
        theta = thetas[i]
        info = infos[i]

        print(f"  Step {i+1}/{n_steps}: Theta = {theta:.1f} deg")

        avg_k_c, eta_a_c, Gamma_c, kap_c = compute_cycle_dissipation(theta, info, L, chair_params, E0, radius, rho, n_elements)
        avg_k_f, eta_a_f, Gamma_f, kap_f = compute_cycle_dissipation(theta, info, L, floor_params, E0, radius, rho, n_elements)

        # dkappa/dt (eta_p term) - Proprioceptive feedback cost
        # PIEZO1/2 activation from curvature rate
        eta_p_base = 1e-4 # Scaling constant
        ds = L / n_elements
        if prev_k_chair is not None:
            # Approximate dkappa/dt using finite difference
            dk_dt_c = (kap_c[:,1] - prev_k_chair[:,1]) / dt_step
            dk_dt_f = (kap_f[:,1] - prev_k_floor[:,1]) / dt_step

            eta_p_c = eta_p_base * np.sum(dk_dt_c**2) * ds
            eta_p_f = eta_p_base * np.sum(dk_dt_f**2) * ds
        else:
            eta_p_c = 0.0
            eta_p_f = 0.0

        chair_results.append({
            "time": t_vals[i], "theta": theta, "avg_k": avg_k_c,
            "eta_a": eta_a_c, "eta_p": eta_p_c, "Gamma_m": Gamma_c,
            "total_dissipation": eta_a_c + eta_p_c + Gamma_c
        })

        floor_results.append({
            "time": t_vals[i], "theta": theta, "avg_k": avg_k_f,
            "eta_a": eta_a_f, "eta_p": eta_p_f, "Gamma_m": Gamma_f,
            "total_dissipation": eta_a_f + eta_p_f + Gamma_f
        })

        prev_k_chair = kap_c
        prev_k_floor = kap_f

    # Save results
    with open(out_dir / "chair_trajectory.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=chair_results[0].keys())
        writer.writeheader()
        writer.writerows(chair_results)

    with open(out_dir / "floor_trajectory.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=floor_results[0].keys())
        writer.writeheader()
        writer.writerows(floor_results)

    # Energy Plot: Breakdown of the three terms
    plot_dissipation_breakdown(out_dir, floor_results, "Floor-Sitter Dissipation Profile", "floor_dissipation.png")
    plot_dissipation_breakdown(out_dir, chair_results, "Chair-Sitter Dissipation Profile", "chair_dissipation.png")

    # Summary Trajectory Plot
    t = [r["time"] for r in chair_results]

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    plt.plot(t, [r["avg_k"] for r in chair_results], 'r--', label=f'Chair-sitter (chi={chi_chair:.1f})')
    plt.plot(t, [r["avg_k"] for r in floor_results], 'b-', label=f'Floor-sitter (chi={chi_floor:.1f})')
    plt.ylabel('Average Curvature (1/m)')
    plt.title('Dynamic Squat-to-Stand Cycle: Trajectory')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 1, 2)
    plt.plot(t, [r["total_dissipation"] for r in chair_results], 'r--', label='Chair-sitter')
    plt.plot(t, [r["total_dissipation"] for r in floor_results], 'b-', label='Floor-sitter')
    plt.xlabel('Cycle Time (s)')
    plt.ylabel('Total Thermodynamic Dissipation (a.u.)')
    plt.title('Thermodynamic Perturbation Magnitude')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_dir / "cycle_trajectories.png", dpi=300)
    plt.close()

def plot_dissipation_breakdown(out_dir, results, title, filename):
    t = [r["time"] for r in results]
    eta_p = [r["eta_p"] for r in results]
    eta_a = [r["eta_a"] for r in results]
    Gamma_m = [r["Gamma_m"] for r in results]

    plt.figure(figsize=(10, 6))

    # Stackplot for the three terms
    plt.stackplot(t, Gamma_m, eta_a, eta_p,
                  labels=['Γ_m (Basal + SIRT1/PGC-1α)', 'η_a (VIM/LMNA Tension)', 'η_p (PIEZO/Klotho Rate)'],
                  colors=['#a1dab4', '#41b6c4', '#225ea8'], alpha=0.8)

    # The eta_p term should peak during the middle of the transition (high velocity)
    # The eta_a term is highest at the ends (standing)

    plt.xlabel('Cycle Time (s) [0=Stand, 2=Squat, 4=Stand]')
    plt.ylabel('Dissipation Rate (dF/dt)')
    plt.title(title)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / filename, dpi=300)
    plt.close()

def main():
    parser = StandardExperimentParser(description="Dynamic Squat-to-Stand Cycle Simulation")
    args = parser.parse_args()
    out_dir = setup_experiment(args)

    print("1. Running Cycle Frequency Sweep...")
    run_cycle_frequency_sweep(out_dir)

    print("2. Comparing Chair vs Floor trajectories...")
    compare_chair_vs_floor(out_dir, quick_mode=args.quick)

    print(f"Simulation complete. Results in {out_dir}")

if __name__ == "__main__":
    main()
