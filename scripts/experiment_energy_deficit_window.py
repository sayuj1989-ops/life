import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.append(".")
from src.spinalmodes.iec import solve_beam_static, compute_gradient

def run_experiment():
    L_vals = np.linspace(0.25, 0.55, 30)
    chi_kappa = 0.05
    E0 = 1.0e9
    rho = 1100.0
    A = 0.001
    g = 9.81
    eta_a = 1.0
    n_nodes = 200
    I_moment = 1e-8

    results = []

    def calc_P_counter(L):
        s = np.linspace(0, L, n_nodes)
        s_norm = s / L

        # Info field
        A_c, s_c, sigma_c = 0.5, 0.80, 0.08
        A_l, s_l, sigma_l = 0.7, 0.25, 0.10
        I_0 = 0.3
        I_field = I_0 + A_c * np.exp(-((s_norm - s_c)**2)/(2*sigma_c**2)) + A_l * np.exp(-((s_norm - s_l)**2)/(2*sigma_l**2))

        grad_I = compute_gradient(I_field, s)

        # Mechanics
        distributed_load = rho * A * g
        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s)

        # Passive (chi_kappa = 0)
        kappa_target_passive = np.zeros_like(s)
        _, kappa_passive = solve_beam_static(
            s=s,
            kappa_target=kappa_target_passive,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load
        )

        # IEC
        kappa_target_iec = chi_kappa * grad_I
        _, kappa_iec = solve_beam_static(
            s=s,
            kappa_target=kappa_target_iec,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load
        )

        mean_diff_sq = np.mean((kappa_iec - kappa_passive)**2)
        # Calculate real angle to extract a "cobb_angle" proxy and get a real P_counter.
        # In reality, if we just set chi_kappa = constant, the curvature decreases with L
        # because the info gradient gets stretched over a longer length L.
        # To maintain the "fixed-curvature assumption" stated in the paper, we actually
        # need to scale chi_kappa with L to keep the target curvature profile constant,
        # OR scale the info field. We will scale chi_kappa proportionally to L so that
        # chi_kappa * grad_I remains constant in magnitude.

        # Calculate Cobb Angle proxy: angle difference between ends
        # theta is the integral of curvature
        # kappa_iec is curvature.
        theta = np.zeros_like(s)
        ds = np.diff(s)
        theta[1:] = np.cumsum(0.5 * (kappa_iec[1:] + kappa_iec[:-1]) * ds)

        cobb_angle = np.abs(np.rad2deg(theta[-1] - theta[0]))

        # D_geo proxy
        D_geo = np.sqrt(np.mean((kappa_iec - kappa_passive)**2))

        P_counter = eta_a * rho * A * g * (L**2) * mean_diff_sq
        return P_counter, cobb_angle, D_geo

    # Find S_0 for reference at L_0
    L_0 = 0.35
    # Save original chi_kappa
    base_chi_kappa = chi_kappa

    # Pre-calculate base S_0
    chi_kappa = base_chi_kappa * (L_0 / L_0)
    P_0, _, _ = calc_P_counter(L_0)
    S_0 = P_0

    for L in L_vals:
        # Scale chi_kappa linearly with L to maintain fixed curvature amplitude
        # since grad_I scales as 1/L.
        chi_kappa = base_chi_kappa * (L / L_0)

        P_counter, cobb_angle, D_geo = calc_P_counter(L)

        S_proprio_alpha05 = S_0 * (L / L_0)**0.5
        S_proprio_alpha10 = S_0 * (L / L_0)**1.0

        results.append({
            "L": L,
            "P_counter": P_counter,
            "S_proprio_alpha05": S_proprio_alpha05,
            "S_proprio_alpha10": S_proprio_alpha10,
            "Cobb_angle": cobb_angle,
            "D_geo": D_geo
        })

    df = pd.DataFrame(results)

    out_dir_csv = Path("outputs/thermodynamic_cost")
    out_dir_csv.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir_csv / "energy_deficit_window.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved {csv_path}")

    plt.figure(figsize=(10, 6))
    plt.plot(df["L"], df["P_counter"], "r-", linewidth=2, label="P_counter (Demand, ~L^2)")
    plt.plot(df["L"], df["S_proprio_alpha05"], "b--", linewidth=2, label="S_proprio (Supply, α=0.5)")
    plt.plot(df["L"], df["S_proprio_alpha10"], "b:", linewidth=2, label="S_proprio (Supply, α=1.0)")

    deficit_mask = df["P_counter"] > df["S_proprio_alpha05"]
    if deficit_mask.any():
        L_crit_idx = np.where(deficit_mask)[0][0]
        L_crit = df["L"].iloc[L_crit_idx]
        plt.fill_between(
            df["L"],
            df["P_counter"],
            df["S_proprio_alpha05"],
            where=deficit_mask,
            color="red", alpha=0.2,
            label="Energy Deficit Window"
        )
        plt.axvline(L_crit, color="k", linestyle="--", label=f"L_crit ≈ {L_crit:.2f} m")

    plt.xlabel("Spinal Length L (m)", fontsize=12)
    plt.ylabel("Thermodynamic Cost P_counter (W)", fontsize=12)
    plt.title("Thermodynamic Cost of Countercurvature vs Supply", fontsize=14)
    plt.legend()
    plt.grid(alpha=0.3)

    out_dir_fig = Path("outputs/figures")
    out_dir_fig.mkdir(parents=True, exist_ok=True)
    fig_path = out_dir_fig / "energy_deficit_window.png"
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    print(f"Saved {fig_path}")

if __name__ == "__main__":
    run_experiment()
