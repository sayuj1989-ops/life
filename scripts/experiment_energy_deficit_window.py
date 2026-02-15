
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# Ensure src is in path correctly regardless of execution context
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
src_path = os.path.join(project_root, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    # Fallback for when running from root without src being a package root
    # e.g. if 'src' is not a package but contains packages
    try:
        from src.spinalmodes.iec import solve_beam_static
    except ImportError as e:
        print(f"Error: Could not import solve_beam_static. Checked {src_path} and fallbacks. {e}")
        sys.exit(1)

def run_experiment():
    # Parameters
    rho = 1100.0  # kg/m^3
    g = 9.81      # m/s^2
    E0 = 1.0e9    # Pa (1.0 GPa)
    chi_kappa = 0.05

    # Information field parameters (bimodal Gaussian)
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08
    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10
    I_0 = 0.3

    # Proprioceptive supply parameters
    L_ref = 0.35  # m (pre-adolescent reference for crossing)

    # Setup L sweep
    L_values = np.linspace(0.25, 0.55, 30)

    # Isometric scaling reference
    # Assuming A=0.001 corresponds to an adult-like spine or the 'standard' param
    # We will assume A scales with L^2 to maintain geometric similarity (constant slenderness)
    # Let's set A=0.001 at L=0.5 (approx adult height)
    L_A_ref = 0.5
    A_ref = 0.001

    results = []

    print(f"Running Energy Deficit Window simulation for L in [{L_values[0]:.2f}, {L_values[-1]:.2f}] with Isometric Scaling...")

    for L in L_values:
        # Scale Area isometrically
        A = A_ref * (L / L_A_ref)**2

        # Recalculate I_moment
        I_moment = (A**2) / (4 * np.pi)

        # Spatial discretization
        n_nodes = 100
        s = np.linspace(0, L, n_nodes)
        s_norm = s / L

        # 1. Construct Information Field I(s)
        I_field = (A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2)) +
                   A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2)) +
                   I_0)

        # 2. Compute gradient of I
        grad_I = np.gradient(I_field, s)

        # 3. Compute kappa_IEC (Full model)
        kappa_target_IEC = chi_kappa * grad_I
        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s) # Assuming chi_f=0

        # Distributed load: Gravity acting transversely
        distributed_load = rho * A * g

        theta_IEC, kappa_IEC = solve_beam_static(
            s=s,
            kappa_target=kappa_target_IEC,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load
        )

        # 4. Compute kappa_passive (Gravity only, chi_kappa=0)
        kappa_target_passive = np.zeros_like(s)

        theta_passive, kappa_passive = solve_beam_static(
            s=s,
            kappa_target=kappa_target_passive, # Zero target curvature
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load
        )

        # 5. Compute P_counter
        # P_counter ~ eta_a * rho * A * g * L^2 * <|kappa_IEC - kappa_passive|^2>
        # With A ~ L^2 and kappa ~ L^-1:
        # P ~ L^2 * L^2 * (L^-1)^2 ~ L^2
        eta_a = 1.0
        mse_kappa = np.mean((kappa_IEC - kappa_passive)**2)
        P_counter = eta_a * rho * A * g * (L**2) * mse_kappa

        # Store Cobb angle (amplitude of theta_IEC in degrees)
        cobb_angle = np.rad2deg(np.max(theta_IEC) - np.min(theta_IEC))

        D_geo = np.mean(np.abs(kappa_IEC - kappa_passive))

        results.append({
            "L": L,
            "P_counter": P_counter,
            "Cobb_angle": cobb_angle,
            "D_geo": D_geo
        })

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Calculate S_proprio reference S_0 at L_ref
    # Find P_counter at L closest to L_ref
    # We interpolate to get exact crossing value or just pick closest
    idx_ref = (np.abs(df['L'] - L_ref)).argmin()
    S_0 = df.loc[idx_ref, 'P_counter']

    # Compute S_proprio curves
    # S_proprio(L) = S_0 * (L / L_0)^alpha
    df['S_proprio_alpha05'] = S_0 * (df['L'] / L_ref)**0.5
    df['S_proprio_alpha10'] = S_0 * (df['L'] / L_ref)**1.0

    # Ensure output directories exist
    output_dir_cost = os.path.join(project_root, "outputs", "thermodynamic_cost")
    output_dir_figs = os.path.join(project_root, "outputs", "figures")
    os.makedirs(output_dir_cost, exist_ok=True)
    os.makedirs(output_dir_figs, exist_ok=True)

    # Save CSV
    csv_path = os.path.join(output_dir_cost, "energy_deficit_window.csv")
    df.to_csv(csv_path, index=False)
    print(f"Results saved to {csv_path}")

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(df['L'], df['P_counter'], 'r-', linewidth=2.5, label=r'$P_{counter} \sim L^2$ (Metabolic Demand)')
    plt.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=1.5, label=r'$S_{proprio} \sim L^{0.5}$ (Neural Supply)')
    plt.plot(df['L'], df['S_proprio_alpha10'], 'b:', linewidth=1.5, label=r'$S_{proprio} \sim L^{1.0}$')

    # Identify crossover for shading
    deficit_mask = df['P_counter'] > df['S_proprio_alpha05']
    if np.any(deficit_mask):
        plt.fill_between(df['L'], df['P_counter'], df['S_proprio_alpha05'],
                         where=deficit_mask, color='red', alpha=0.15, label='Energy Deficit Window')

        # Mark L_crit
        plt.axvline(x=L_ref, color='k', linestyle='-', alpha=0.3)
        plt.text(L_ref, plt.ylim()[1]*0.5, f' $L_{{crit}} \\approx {L_ref}m$', ha='right', rotation=90)

    plt.xlabel('Spinal Length L (m)', fontsize=12)
    plt.ylabel('Thermodynamic Cost (normalized)', fontsize=12)
    plt.title('The Energy Deficit Window: Isometric Growth', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    fig_path = os.path.join(output_dir_figs, "energy_deficit_window.png")
    plt.savefig(fig_path, dpi=300)
    print(f"Figure saved to {fig_path}")

if __name__ == "__main__":
    run_experiment()
