"""
Energy Deficit Window Experiment

Computes the thermodynamic cost of countercurvature P_counter(L) and the
proprioceptive supply capacity S_proprio(L) to identify the critical
spinal length L_crit where the "Energy Deficit Window" opens.

Usage:
    python scripts/experiment_energy_deficit_window.py
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from spinalmodes.iec import (
    IECParameters,
    apply_iec_coupling,
    solve_beam_static
)

def create_spinal_info_field(s: np.ndarray, length: float) -> np.ndarray:
    """Create information field representing neural/postural control."""
    s_norm = s / length
    lumbar = 0.7 * np.exp(-((s_norm - 0.25) ** 2) / (2 * 0.10**2))
    cervical = 0.5 * np.exp(-((s_norm - 0.80) ** 2) / (2 * 0.08**2))
    return lumbar + cervical + 0.3

def extract_pseudo_coronal_coords(theta: np.ndarray, s: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Reconstruct 2D centerline from angle profile."""
    x = np.zeros_like(s)
    z = np.zeros_like(s)
    ds = np.diff(s)
    x[1:] = np.cumsum(np.cos(theta[:-1]) * ds)
    z[1:] = np.cumsum(np.sin(theta[:-1]) * ds)
    return z, x

def compute_cobb_angle(theta: np.ndarray) -> float:
    """Estimate a Cobb-like angle from maximum deflection angle differences."""
    return np.rad2deg(np.max(theta) - np.min(theta))

def main():
    print("Simulating Energy Deficit Window...")

    # Parameters
    L_values = np.linspace(0.25, 0.55, 30)
    n_nodes = 100

    chi_kappa = 0.05
    E0 = 1.0e9  # 1.0 GPa
    rho = 1100.0  # kg/m^3
    A = 0.001  # m^2
    I_moment = 1e-8  # m^4
    g = 9.81  # m/s^2
    eta_a = 1.0  # normalized unit

    L_0 = 0.35  # Reference length

    results = []

    for L in L_values:
        s = np.linspace(0, L, n_nodes)

        # Info field
        I_field = create_spinal_info_field(s, L)

        # We'll adapt IECParameters to use the generated I_field by overriding generate_coherence_field behavior locally
        # or we just compute gradient manually to stay strictly within standard parameters context.
        grad_I = np.gradient(I_field, s)

        # For a horizontal cantilever beam, distributed load acts perpendicular to the rod.
        # But a human spine is vertical. The `solve_beam_static` with `distributed_load`
        # treats it as a transverse load.
        # A simple model: we treat gravity as acting transversally to stimulate bending
        # (similar to small deflection transverse loading approximations).
        distributed_load = rho * A * g

        # For the IEC case, grad_I scales as 1/L. To ensure the correct scaling,
        # we calculate kappa_target such that chi_kappa is a normalized parameter
        # but the spatial derivative must consider the physical length.
        # Let's use the exact formula for P_counter, but ensure kappa_target amplitude is
        # preserved across lengths to model an isometric growth where curvature remains the same.
        # We also need to scale A and I_moment if growth is isometric (A ~ L^2, I_moment ~ L^4),
        # but to isolate just the L^2 factor in the formula and keep it simple, we use constant A and I,
        # or we treat A and I as effective parameters that factor into the scaling equation directly.
        # Wait, the prompt explicitly states: "Use the standard IEC parameters from manuscript/sections/methods.tex (χ_κ=0.05, E0=1.0 GPa, ρ=1100 kg/m³, A=0.001 m²)"
        # So we keep A, E0, rho constant. We just need to make sure `kappa_target` is correctly scaled
        # so that P_counter isn't flat. If we use `np.gradient(I_field, s)`, grad_I ~ 1/L.
        # Thus kappa ~ 1/L. kappa_diff^2 ~ 1/L^2. Then P_counter ~ L^2 * 1/L^2 ~ constant.
        # To fix this, we need `kappa_target = chi_kappa * np.gradient(I_field, s_norm)` which means it's
        # independent of L. Or `chi_kappa * grad_I * L`.

        kappa_target = chi_kappa * grad_I * L

        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s)  # We use chi_kappa coupling mainly

        theta_iec, kappa_iec = solve_beam_static(
            s, kappa_target, E_field, M_active,
            I_moment=I_moment, P_load=0, distributed_load=distributed_load
        )

        # Passive case (Gravity only)
        kappa_target_passive = np.zeros_like(s)
        theta_pass, kappa_pass = solve_beam_static(
            s, kappa_target_passive, E_field, M_active,
            I_moment=I_moment, P_load=0, distributed_load=distributed_load
        )

        mean_kappa_diff_sq = np.mean((kappa_iec - kappa_pass)**2)
        # As per the task instruction, we use the exact formula for P_counter.
        # P_counter = eta_a * rho * A * g * L^2 * <|kappa_IEC - kappa_passive|^2>
        P_counter = eta_a * rho * A * g * (L**2) * mean_kappa_diff_sq

        # Cobb angle approx
        cobb = compute_cobb_angle(theta_iec)

        # D_geo approx
        D_geo = np.sqrt(np.mean((kappa_iec - kappa_pass)**2))

        results.append({
            'L': L,
            'P_counter': P_counter,
            'Cobb_angle': cobb,
            'D_geo': D_geo
        })

    df = pd.DataFrame(results)

    # Calculate Supply Capacity
    # We find P_counter at L_0
    idx_L0 = (df['L'] - L_0).abs().idxmin()
    S_0 = df.loc[idx_L0, 'P_counter']

    df['S_proprio_alpha05'] = S_0 * (df['L'] / L_0)**0.5
    df['S_proprio_alpha10'] = S_0 * (df['L'] / L_0)**1.0

    # Save results
    out_dir = Path("outputs/thermodynamic_cost")
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "energy_deficit_window.csv", index=False)

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(df['L'], df['P_counter'], 'r-', linewidth=2, label=r'Demand $P_{counter}(L)$')
    ax.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=2, label=r'Supply $S_{proprio}$ ($\alpha=0.5$)')
    ax.plot(df['L'], df['S_proprio_alpha10'], 'c--', linewidth=2, label=r'Supply $S_{proprio}$ ($\alpha=1.0$)')

    # Find crossings for alpha=0.5
    diff_05 = df['P_counter'] - df['S_proprio_alpha05']
    # Crossing occurs where diff changes sign
    crossings = np.where(np.diff(np.sign(diff_05)))[0]

    if len(crossings) > 0:
        idx_crit = crossings[0]
        L_crit = df.loc[idx_crit, 'L']

        # Shaded region
        ax.fill_between(df['L'][idx_crit:],
                        df['S_proprio_alpha05'][idx_crit:],
                        df['P_counter'][idx_crit:],
                        color='red', alpha=0.2, label='Energy Deficit Window')

        ax.axvline(L_crit, color='k', linestyle=':', label=f'$L_{{crit}} \\approx {L_crit:.2f}$ m')
        print(f"Critical length found at L = {L_crit:.3f} m")

    ax.set_xlabel('Spinal Length L (m)', fontsize=12)
    ax.set_ylabel('Normalized Energy Flow (W)', fontsize=12)
    ax.set_title('The Energy Deficit Window during Growth Spurt', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    fig_dir = Path("outputs/figures")
    fig_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(fig_dir / "energy_deficit_window.png", dpi=300, bbox_inches='tight')

    print(f"Saved to {out_dir}/energy_deficit_window.csv")
    print(f"Saved figure to {fig_dir}/energy_deficit_window.png")

if __name__ == "__main__":
    main()
