#!/usr/bin/env python3
"""
Experiment: Energy Deficit Window
Computes the thermodynamic cost of countercurvature (P_counter) and proprioceptive
supply capacity (S_proprio) as a function of spinal length L. Identifies the
critical length where the energy deficit window opens.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure src is in the python path
src_dir = Path(__file__).parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from spinalmodes.iec import solve_beam_static, compute_gradient

def generate_bimodal_info_field(s: np.ndarray, L: float) -> np.ndarray:
    """Generate bimodal Gaussian coherence field representing HOX domains."""
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08

    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10

    I_0 = 0.3

    s_norm = s / L

    I_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    I_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

    return I_c + I_l + I_0

def main():
    # IEC parameters
    chi_kappa = 0.05
    E0 = 1.0e9
    rho = 1100.0
    A_cross = 0.001
    g = 9.81
    eta_a = 1.0

    n_nodes = 100

    L_array = np.linspace(0.25, 0.55, 30)

    L_0 = 0.35 # Pre-adolescent reference length

    # Store results
    L_vals = []
    P_counter_vals = []
    mean_sq_diff_vals = []
    Cobb_vals = []
    D_geo_vals = []

    for L in L_array:
        s = np.linspace(0, L, n_nodes)
        I_field = generate_bimodal_info_field(s, L)
        grad_I = compute_gradient(I_field, s)

        # IEC-1: Target curvature bias
        kappa_target_IEC = chi_kappa * grad_I * L  # Fixed curvature assumption

        # Baseline IEC properties
        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s)

        I_moment = 1e-8

        distributed_load = rho * A_cross * g

        # 1. Compute full IEC curvature
        theta_IEC, kappa_IEC = solve_beam_static(
            s=s,
            kappa_target=kappa_target_IEC,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load,
        )

        # 2. Compute passive curvature (gravity only)
        kappa_target_passive = np.zeros_like(s)
        theta_passive, kappa_passive = solve_beam_static(
            s=s,
            kappa_target=kappa_target_passive,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load,
        )

        # 3. Compute P_counter
        # P_counter(L) = \eta_a * \rho * A * g * L^2 * mean(|kappa_IEC - kappa_passive|^2)
        mean_diff_sq = np.mean(np.abs(kappa_IEC - kappa_passive)**2)
        P_counter = eta_a * rho * A_cross * g * (L**2) * mean_diff_sq

        # For outputs we also need Cobb_angle and D_geo
        # Cobb angle approx: max(theta) - min(theta) converted to degrees
        Cobb_angle = np.rad2deg(np.max(theta_IEC) - np.min(theta_IEC))

        # Geodesic Deviation: D_geo
        D_geo = float(np.sqrt(np.mean((theta_IEC - theta_passive)**2)))

        L_vals.append(L)
        P_counter_vals.append(P_counter)
        mean_sq_diff_vals.append(mean_diff_sq)
        Cobb_vals.append(Cobb_angle)
        D_geo_vals.append(D_geo)

    L_vals = np.array(L_vals)
    P_counter_vals = np.array(P_counter_vals)
    mean_sq_diff_vals = np.array(mean_sq_diff_vals)
    Cobb_vals = np.array(Cobb_vals)
    D_geo_vals = np.array(D_geo_vals)

    # 4. Compute proprioceptive supply capacity curves
    # Interpolate P_counter to find S_0 at L_0
    S_0 = np.interp(L_0, L_vals, P_counter_vals)

    S_proprio_alpha05 = S_0 * (L_vals / L_0)**0.5
    S_proprio_alpha10 = S_0 * (L_vals / L_0)**1.0

    # Output directories
    out_dir_csv = Path("outputs/thermodynamic_cost")
    out_dir_csv.mkdir(parents=True, exist_ok=True)

    out_dir_fig = Path("outputs/figures")
    out_dir_fig.mkdir(parents=True, exist_ok=True)
    out_dir_manuscript_fig = Path("manuscript/figures")
    out_dir_manuscript_fig.mkdir(parents=True, exist_ok=True)

    # 5. Save results to CSV
    df = pd.DataFrame({
        "L": L_vals,
        "P_counter": P_counter_vals,
        "mean_sq_diff": mean_sq_diff_vals,
        "Cobb_angle": Cobb_vals,
        "D_geo": D_geo_vals,
        "S_proprio_alpha05": S_proprio_alpha05,
        "S_proprio_alpha10": S_proprio_alpha10,
    })

    csv_path = out_dir_csv / "energy_deficit_window.csv"
    df.to_csv(csv_path, index=False)
    print(f"Results saved to {csv_path}")

    # 6. Generate figure
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(L_vals, P_counter_vals, 'r-', linewidth=2.5, label=r'Metabolic Demand: $P_{\mathrm{counter}} \propto L^2$')
    ax.plot(L_vals, S_proprio_alpha05, 'b--', linewidth=2, label=r'Proprioceptive Supply: $S_{\mathrm{proprio}} \propto L^{0.5}$')
    ax.plot(L_vals, S_proprio_alpha10, 'g--', linewidth=1.5, label=r'Linear Supply: $S \propto L^{1.0}$')

    # Highlight the Energy Deficit Window
    # Find indices where Demand > Supply (and only for L > L_0 to be sure)
    deficit_indices = (P_counter_vals > S_proprio_alpha05) & (L_vals >= L_0)
    if np.any(deficit_indices):
        ax.fill_between(L_vals[deficit_indices], S_proprio_alpha05[deficit_indices], P_counter_vals[deficit_indices],
                        color='red', alpha=0.2, label='Energy Deficit Window')

    ax.axvline(x=L_0, color='k', linestyle=':', label=r'$L_{\mathrm{crit}} = 0.35$ m')

    ax.set_xlabel('Spinal Length $L$ (m)', fontsize=14)
    ax.set_ylabel('Power / Supply Rate (A.U.)', fontsize=14)
    ax.set_title('Thermodynamic Collapse: The Energy Deficit Window', fontsize=16)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3)

    fig_path = out_dir_fig / "energy_deficit_window.png"
    manuscript_fig_path = out_dir_manuscript_fig / "energy_deficit_window.png"
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.savefig(manuscript_fig_path, dpi=300)
    plt.close()
    print(f"Figure saved to {fig_path}")
    print(f"Figure saved to {manuscript_fig_path}")

if __name__ == "__main__":
    main()
