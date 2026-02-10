"""
Weekly Simulation: Energy Deficit Bifurcation.

Performs a 2D parameter sweep of the Energy Deficit Window across (chi_kappa, L) space.
Generates a phase diagram showing where AIS vulnerability is highest.

Parameters:
- chi_kappa (IEC coupling strength): 0.01 to 0.10
- L (spinal length): 0.25 to 0.55 m
- Fixed: rho=1100, A=0.001, g=9.81, E0=1.0 GPa

Outputs:
- outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv
- outputs/figures/phase_diagram_energy_deficit.png
- outputs/figures/phase_diagram_energy_deficit_cobb.png
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import time

# Add src to python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
    from spinalmodes.countercurvature.info_fields import InfoField1D
    from spinalmodes.countercurvature.coupling import CounterCurvatureParams
    from spinalmodes.countercurvature.scoliosis_metrics import build_lateral_curvature_bump
except ImportError:
    # Fallback for different environment setups
    sys.path.append(str(Path(__file__).parent.parent / "research/alphafold_countercurvature/src"))
    from spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
    from spinalmodes.countercurvature.info_fields import InfoField1D
    from spinalmodes.countercurvature.coupling import CounterCurvatureParams
    from spinalmodes.countercurvature.scoliosis_metrics import build_lateral_curvature_bump

def generate_bimodal_gaussian_field(s, L):
    """
    Generate the bimodal Gaussian information field I(s).
    Matches manuscript/sections/theory.tex description.
    """
    if L <= 0:
        return np.zeros_like(s), np.zeros_like(s)

    s_norm = s / L

    # Parameters from manuscript
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08

    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10

    I_0 = 0.3

    # Calculate I(s)
    term_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    term_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))
    I = term_c + term_l + I_0

    # Calculate dI/ds (gradient)
    # d/ds = (1/L) * d/ds_norm
    d_term_c = term_c * (-1.0 * (s_norm - s_c) / sigma_c**2) / L
    d_term_l = term_l * (-1.0 * (s_norm - s_l) / sigma_l**2) / L
    dIds = d_term_c + d_term_l

    return I, dIds

def run_simulation(chi_kappa, L, is_passive=False):
    """
    Run a single simulation for a given chi_kappa and Length.
    If is_passive is True, sets chi_kappa=0 but keeps other params.
    """
    # Fixed Parameters
    rho = 1100.0
    A = 0.001
    g = 9.81
    E0 = 1.0e9 # 1.0 GPa
    radius = np.sqrt(A / np.pi)

    # Asymmetry perturbation
    epsilon_lat = 0.03

    # Discretization
    # Reduced to 20 for speed (User constraint: 20x20 sweep needs to finish quickly)
    n_elements = 20

    # Time settings
    # High stiffness E=1e9 requires small dt.
    # Stable dt proportional to dx. With n_elements=20 (larger dx), we can use larger dt.
    # Natural freq T ~ 0.1s. 0.2s is 2 periods, enough with damping.
    dt = 2.0e-5
    final_time = 0.2

    # 1. Create Info Field
    s = np.linspace(0, L, n_elements + 1)
    I, dIds = generate_bimodal_gaussian_field(s, L)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    # 2. Create Params
    # If passive, chi_kappa is effectively 0 for the active drive.
    effective_chi_kappa = 0.0 if is_passive else chi_kappa

    params = CounterCurvatureParams(
        chi_kappa=effective_chi_kappa,
        chi_tau=0.0,
        chi_E=0.10, # Constitutive bias kept (material property)
        chi_M=0.0,
        scale_length=1.0
    )

    # 3. Create Lateral Perturbation (kappa_gen)
    # kappa_gen is (3, n_nodes)
    # Index 0: Lateral (Binormal)
    # Index 1: Sagittal (Normal)
    # Index 2: Torsion (Tangent)
    kappa_lat = build_lateral_curvature_bump(s, epsilon_lat=epsilon_lat)
    kappa_gen = np.zeros((3, len(s)))
    kappa_gen[0, :] = kappa_lat

    # 4. Create System
    system = CounterCurvatureRodSystem.from_iec(
        info=info,
        params=params,
        length=L,
        n_elements=n_elements,
        radius=radius,
        E0=E0,
        rho=rho,
        gravity=g,
        base_direction=(0.0, 0.0, 1.0), # Vertical +Z
        normal=(0.0, 1.0, 0.0), # Sagittal plane normal Y
        kappa_gen=kappa_gen, # Apply perturbation
        stiffness_anisotropy=1.0 # Isotropic for this sweep
    )

    # 5. Run
    # Suppress progress bar for batch runs
    res = system.run_simulation(
        final_time=final_time,
        dt=dt,
        save_every=int(final_time/dt), # Only save final state effectively
        progress_bar=False,
        damping_constant=1.0 # Slightly higher damping for faster convergence
    )

    # 6. Extract Metrics
    # Get kappa from final step: shape (n_nodes, 3)
    if len(res.kappa) > 0:
        final_kappa = res.kappa[-1]
    else:
        final_kappa = np.zeros((len(s), 3))

    metrics = res.compute_final_metrics()
    cobb_angle = metrics.get('cobb_angle', 0.0)

    return final_kappa, cobb_angle

def main():
    print("Starting Weekly Simulation: Energy Deficit Bifurcation Phase Diagram...")

    # Output Setup
    output_dir_data = Path("outputs/thermodynamic_cost")
    output_dir_figs = Path("outputs/figures")
    output_dir_data.mkdir(parents=True, exist_ok=True)
    output_dir_figs.mkdir(parents=True, exist_ok=True)

    # Sweep Parameters
    chi_kappa_vals = np.linspace(0.01, 0.10, 20)
    L_vals = np.linspace(0.25, 0.55, 20)

    # Constants
    rho = 1100.0
    A = 0.001
    g = 9.81
    L_ref = 0.35
    chi_ref = 0.05

    # 1. Compute Reference Energy S_0
    print(f"Computing Reference Energy S_0 at L={L_ref}, chi_kappa={chi_ref}...")
    k_ref_pass, _ = run_simulation(chi_ref, L_ref, is_passive=True)
    k_ref_act, _ = run_simulation(chi_ref, L_ref, is_passive=False)

    # Difference squared (element-wise vector norm squared)
    diff_sq_ref = np.sum((k_ref_act - k_ref_pass)**2, axis=1)
    mean_diff_sq_ref = np.mean(diff_sq_ref)

    P_ref = rho * A * g * (L_ref**2) * mean_diff_sq_ref
    S_0 = P_ref
    print(f"Reference S_0 = {S_0:.6e} J/s (normalized)")

    # 2. Pre-compute Passive States for each L
    print("Pre-computing passive states for L sweep...")
    passive_kappas = {}
    for L in L_vals:
        k_pass, _ = run_simulation(0.0, L, is_passive=True)
        passive_kappas[L] = k_pass

    # 3. Full 2D Sweep
    results = []
    print(f"Starting 2D Sweep ({len(chi_kappa_vals)}x{len(L_vals)} = {len(chi_kappa_vals)*len(L_vals)} simulations)...")

    total_runs = len(chi_kappa_vals) * len(L_vals)
    count = 0
    start_time = time.time()

    for L in L_vals:
        # Get passive reference for this Length
        k_pass = passive_kappas[L]

        # Calculate Proprioceptive Supply
        # S_proprio = S_0 * (L / L_0)^0.7
        S_proprio = S_0 * (L / L_ref)**0.7

        for chi in chi_kappa_vals:
            count += 1
            if count % 10 == 0:
                elapsed = time.time() - start_time
                rate = count / elapsed
                remaining = (total_runs - count) / rate
                print(f"Run {count}/{total_runs} | L={L:.2f}, chi={chi:.3f} | ETA: {remaining/60:.1f} min", end='\r')

            # Run Active Simulation
            k_act, cobb = run_simulation(chi, L, is_passive=False)

            # Compute Metrics
            diff_sq = np.sum((k_act - k_pass)**2, axis=1)
            mean_diff_sq = np.mean(diff_sq)

            P_counter = rho * A * g * (L**2) * mean_diff_sq

            # Geodesic Deviation Metric (D_geo)
            # D_geo = sqrt(mean( ||k_act - k_pass||^2 ))
            # Note: This is sqrt(mean_diff_sq).
            # Some definitions might normalize by L, but curvature is 1/L.
            # D_geo is roughly dimensionless if multiplied by L?
            # api.geodesic_curvature_deviation returns sqrt(trapz(g_eff * dk^2)).
            # Here we use mean square.
            D_geo = np.sqrt(mean_diff_sq)

            R_deficit = P_counter / S_proprio if S_proprio > 0 else np.inf

            results.append({
                'chi_kappa': chi,
                'L': L,
                'P_counter': P_counter,
                'S_proprio': S_proprio,
                'R_deficit': R_deficit,
                'D_geo': D_geo,
                'cobb_angle': cobb
            })

    print(f"\nSweep Complete. Saving results...")

    # Save CSV
    df = pd.DataFrame(results)
    csv_path = output_dir_data / "phase_diagram_energy_deficit.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV to {csv_path}")

    # 4. Plotting
    # Pivot for heatmaps
    # Rows: chi_kappa (y-axis), Cols: L (x-axis)
    pivot_R = df.pivot(index='chi_kappa', columns='L', values='R_deficit')
    pivot_Cobb = df.pivot(index='chi_kappa', columns='L', values='cobb_angle')

    # Extent for imshow
    extent = [L_vals[0], L_vals[-1], chi_kappa_vals[0], chi_kappa_vals[-1]]

    # Plot 1: Energy Deficit Ratio R_deficit
    plt.figure(figsize=(10, 8))
    im = plt.imshow(pivot_R, origin='lower', aspect='auto', extent=extent, cmap='viridis', vmin=0, vmax=2.0)
    cbar = plt.colorbar(im, label='Energy Deficit Ratio ($R_{deficit} = P_{counter} / S_{proprio}$)')

    # Contour line at R=1
    # We need grid for contour
    X, Y = np.meshgrid(L_vals, chi_kappa_vals)
    CS = plt.contour(X, Y, pivot_R, levels=[1.0], colors='white', linewidths=2, linestyles='dashed')
    plt.clabel(CS, inline=True, fmt='R=1.0', fontsize=12)

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('IEC Coupling Strength $\chi_\kappa$')
    plt.title('Energy Deficit Phase Diagram\n(Wedge of Instability)')
    plt.tight_layout()
    plt.savefig(output_dir_figs / "phase_diagram_energy_deficit.png", dpi=300)
    plt.close()

    # Plot 2: Cobb Angle
    plt.figure(figsize=(10, 8))
    im = plt.imshow(pivot_Cobb, origin='lower', aspect='auto', extent=extent, cmap='magma')
    plt.colorbar(im, label='Cobb Angle (deg)')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('IEC Coupling Strength $\chi_\kappa$')
    plt.title('Scoliosis Emergence (Cobb Angle)')
    plt.tight_layout()
    plt.savefig(output_dir_figs / "phase_diagram_energy_deficit_cobb.png", dpi=300)
    plt.close()

    print("Figures saved.")

if __name__ == "__main__":
    main()
