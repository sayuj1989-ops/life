#!/usr/bin/env python3
"""
Simulate P_counter(L) energy deficit window.

Computes the thermodynamic cost of countercurvature as a function of spinal length L,
identifying the critical L where the Energy Deficit Window opens.
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from spinalmodes.iec import solve_beam_static, compute_amplitude

# Constants
RHO = 1100.0  # kg/m^3
G_GRAVITY = 9.81  # m/s^2
E0 = 1.0e9    # Pa (1.0 GPa)
CHI_KAPPA_IEC = 0.05
CHI_KAPPA_PASSIVE = 0.0

# Standard Reference
L_REF = 0.4      # m
A_REF = 0.001    # m^2

# Information Field Parameters (Bimodal Gaussian)
# I(s) = A_c exp(...) + A_l exp(...) + I_0
A_C = 0.5
S_C_REL = 0.80
SIGMA_C_REL = 0.08
A_L = 0.7
S_L_REL = 0.25
SIGMA_L_REL = 0.10
I_0 = 0.3

def generate_bimodal_I(s, L):
    """Generate bimodal Gaussian information field I(s)."""
    s_norm = s / L

    term_c = A_C * np.exp(-((s_norm - S_C_REL)**2) / (2 * SIGMA_C_REL**2))
    term_l = A_L * np.exp(-((s_norm - S_L_REL)**2) / (2 * SIGMA_L_REL**2))

    return term_c + term_l + I_0

def run_simulation():
    # Length sweep
    L_values = np.linspace(0.25, 0.55, 30)
    results = []

    # Store curves for plotting
    P_counter_curve = []

    for L in L_values:
        # Isometric Scaling: A ~ L^2
        # A = A_ref * (L / L_ref)^2
        A_val = A_REF * (L / L_REF)**2

        # Derived geometric props
        I_moment = (A_val**2) / (4 * np.pi)  # m^4
        distributed_load = RHO * A_val * G_GRAVITY  # N/m

        # Spatial grid
        s = np.linspace(0, L, 100)

        # 1. Generate Information Field
        I_field = generate_bimodal_I(s, L)
        grad_I = np.gradient(I_field, s)

        # 2. Compute kappa_IEC (Active)
        # kappa_target = kappa_gen_baseline (0) + chi_kappa * grad_I
        kappa_target_IEC = 0.0 + CHI_KAPPA_IEC * grad_I

        # E_field is constant E0 (chi_E = 0)
        E_field = np.full_like(s, E0)

        # M_active is 0 (chi_f = 0)
        M_active = np.zeros_like(s)

        theta_IEC, kappa_IEC = solve_beam_static(
            s=s,
            kappa_target=kappa_target_IEC,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load
        )

        # 3. Compute kappa_passive (Gravity Only)
        # kappa_target = 0
        kappa_target_passive = np.zeros_like(s)

        theta_passive, kappa_passive = solve_beam_static(
            s=s,
            kappa_target=kappa_target_passive,
            E_field=E_field,
            M_active=M_active, # Still 0
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load
        )

        # 4. Compute Metrics
        # P_counter ~ eta_a * rho * A * g * L^2 * mean(|kappa_IEC - kappa_passive|^2)
        # eta_a = 1.0
        mse_kappa = np.mean((kappa_IEC - kappa_passive)**2)
        P_val = 1.0 * RHO * A_val * G_GRAVITY * (L**2) * mse_kappa

        # Cobb angle (amplitude of theta_IEC in degrees)
        cobb_angle = compute_amplitude(theta_IEC)

        # D_geo (RMS curvature deviation)
        d_geo = np.sqrt(mse_kappa)

        results.append({
            "L": L,
            "P_counter": P_val,
            "Cobb_angle": cobb_angle,
            "D_geo": d_geo
        })
        P_counter_curve.append(P_val)

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # 5. Compute Proprioceptive Supply S_proprio
    # S_proprio(L) = S_0 * (L / L_0)^alpha
    # L_0 = 0.35
    # S_0 = P_counter(L_0)

    L_0 = 0.35
    # Interpolate P_counter at L_0
    S_0 = np.interp(L_0, df["L"], df["P_counter"])

    df["S_proprio_alpha05"] = S_0 * (df["L"] / L_0)**0.5
    df["S_proprio_alpha10"] = S_0 * (df["L"] / L_0)**1.0

    # 6. Save Results
    os.makedirs("outputs/thermodynamic_cost", exist_ok=True)
    df.to_csv("outputs/thermodynamic_cost/energy_deficit_window.csv", index=False)
    print("Saved CSV to outputs/thermodynamic_cost/energy_deficit_window.csv")

    # 7. Generate Figure
    plt.figure(figsize=(10, 6))

    # P_counter (Demand)
    plt.plot(df["L"], df["P_counter"], 'r-', linewidth=2.5, label=r'Metabolic Demand $P_{counter} \sim L^2$')

    # S_proprio (Supply)
    plt.plot(df["L"], df["S_proprio_alpha05"], 'b--', linewidth=2.0, label=r'Supply Capacity $S_{proprio} \sim L^{0.5}$')
    plt.plot(df["L"], df["S_proprio_alpha10"], 'b:', linewidth=2.0, label=r'Supply Capacity $S_{proprio} \sim L^{1.0}$')

    # Shade Energy Deficit Window (L > L_0)
    # Using alpha=0.5 as the primary supply curve
    mask = df["P_counter"] > df["S_proprio_alpha05"]
    plt.fill_between(df["L"], df["P_counter"], df["S_proprio_alpha05"],
                     where=mask, color='red', alpha=0.2, label='Energy Deficit Window')

    # Vertical line at L_crit = L_0
    plt.axvline(x=L_0, color='k', linestyle='--', alpha=0.5, label=r'$L_{crit} \approx 0.35$ m')

    # Annotate Deficit at L=0.45
    L_target = 0.45
    P_target = np.interp(L_target, df["L"], df["P_counter"])
    S_target = np.interp(L_target, df["L"], df["S_proprio_alpha05"])
    deficit_pct = (P_target - S_target) / S_target * 100

    plt.annotate(f"Deficit: +{deficit_pct:.1f}%",
                 xy=(L_target, P_target),
                 xytext=(L_target, P_target * 1.2),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    plt.title("Thermodynamic Cost vs. Proprioceptive Supply")
    plt.xlabel("Spinal Length L (m)")
    plt.ylabel("Metabolic Power (Normalized)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    os.makedirs("outputs/figures", exist_ok=True)
    plt.savefig("outputs/figures/energy_deficit_window.png", dpi=300)
    print("Saved Figure to outputs/figures/energy_deficit_window.png")
    plt.close()

if __name__ == "__main__":
    run_simulation()
