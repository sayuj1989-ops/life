
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure src is in path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_root, "src"))

from spinalmodes.iec import IECParameters, apply_iec_coupling

def solve_beam_column(L, A, I, E0, rho, iec_params, n_nodes=100):
    """
    Solves the linearized beam-column equation with intrinsic curvature and axial gravity load:
    (EI * (theta' - kappa_target))' - N(s) * theta = 0
    or:
    (EI * theta')' - N(s) * theta = (EI * kappa_target)'

    Boundary Conditions:
    theta(0) = 0 (Clamped base)
    theta'(L) = kappa_target(L) (Free top, zero moment M(L) = EI(theta'(L) - kappa_target(L)) = 0)

    Args:
        L: Length (m)
        A: Cross-sectional area (m^2)
        I: Second moment of area (m^4)
        E0: Young's modulus (Pa)
        rho: Density (kg/m^3)
        iec_params: IECParameters object
        n_nodes: Number of nodes

    Returns:
        s: spatial coordinate array
        kappa: curvature array (theta')
        theta: angle array
    """
    s = np.linspace(0, L, n_nodes)
    h = s[1] - s[0]

    # Get IEC fields
    # We update length in params to match current L
    iec_params.length = L
    iec_params.n_nodes = n_nodes

    # Get kappa_target and E_field
    # Note: apply_iec_coupling uses iec_params.length internally for normalized coords
    kappa_target, E_field, _, _ = apply_iec_coupling(s, iec_params)

    # Calculate EI array
    EI = E_field * I

    # Calculate Axial Load N(s) = rho * A * g * (L - s)
    g = 9.81
    N_axial = rho * A * g * (L - s)

    # Build Finite Difference Matrix
    # Unknowns: theta_0, theta_1, ..., theta_{n-1}
    # However, theta_0 is fixed to 0 by BC. So solve for theta_1 ... theta_{n-1}.
    # Number of unknowns = n_nodes - 1.

    dim = n_nodes - 1
    Mat = np.zeros((dim, dim))
    RHS = np.zeros(dim)

    # Precompute EI midpoints
    EI_mid = 0.5 * (EI[:-1] + EI[1:])

    # Discretization for interior nodes i (corresponding to s[i])
    # Equation at node i:
    # [ EI_{i+1/2} (theta_{i+1} - theta_i)/h - EI_{i-1/2} (theta_i - theta_{i-1})/h ] / h - N_i * theta_i = RHS_i
    # RHS comes from (EI * kappa_target)' term.
    # Term (EI * kappa_target)' at node i approx:
    # [ (EI * kappa_target)_{i+1/2} - (EI * kappa_target)_{i-1/2} ] / h

    EI_kappa_t = EI * kappa_target
    EI_kappa_t_mid = 0.5 * (EI_kappa_t[:-1] + EI_kappa_t[1:])

    # Mapping: unknowns index k corresponds to s[k+1].
    # k=0 -> s[1], k=1 -> s[2], ..., k=dim-1 -> s[n-1] (top)

    for k in range(dim):
        i = k + 1  # Actual node index

        # Coefficients for theta_{i-1}, theta_i, theta_{i+1}
        # Be careful with h^2 scaling

        # Term 1: EI_{i+1/2} / h^2 * theta_{i+1}
        # Term 2: -(EI_{i+1/2} + EI_{i-1/2}) / h^2 * theta_i
        # Term 3: EI_{i-1/2} / h^2 * theta_{i-1}
        # Term 4: -N_i * theta_i

        if k < dim - 1: # Normal interior node
            # Combined coeff for theta_i:
            coeff_i = -(EI_mid[i] + EI_mid[i-1]) / h**2 - N_axial[i]

            # Coeff for theta_{i+1}:
            coeff_ip1 = EI_mid[i] / h**2

            # Coeff for theta_{i-1}:
            coeff_im1 = EI_mid[i-1] / h**2

            # RHS term: ( (EI*kt)_{i+1/2} - (EI*kt)_{i-1/2} ) / h
            rhs_val = (EI_kappa_t_mid[i] - EI_kappa_t_mid[i-1]) / h

            # Fill Matrix
            Mat[k, k] = coeff_i

            if k > 0: # theta_{i-1} is unknown (i-1 >= 1)
                Mat[k, k-1] = coeff_im1
            else:
                # theta_{i-1} is theta_0 which is 0. Term vanishes.
                pass

            Mat[k, k+1] = coeff_ip1

        else:
            # Boundary Condition at Top (i = n_nodes-1 = L)
            # Row k=dim-1 corresponds to node n_nodes-1.
            # Equation: theta_{n_nodes-1} - theta_{n_nodes-2} = h * kappa_target[n_nodes-1]

            Mat[k, k] = 1.0
            Mat[k, k-1] = -1.0
            rhs_val = h * kappa_target[n_nodes-1]

        RHS[k] = rhs_val

    # Solve
    theta_interior = np.linalg.solve(Mat, RHS)

    theta = np.zeros(n_nodes)
    theta[1:] = theta_interior

    # Compute curvature kappa = theta'
    # Centered difference
    kappa = np.zeros(n_nodes)
    kappa[1:-1] = (theta[2:] - theta[:-2]) / (2*h)
    kappa[0] = (theta[1] - theta[0]) / h # Forward
    kappa[-1] = (theta[-1] - theta[-2]) / h # Backward (consistent with BC)

    return s, kappa, theta


def run_experiment():
    # Parameters
    L_start = 0.25
    L_end = 0.55
    steps = 30
    Ls = np.linspace(L_start, L_end, steps)

    # Reference values for isometric scaling
    L_ref = 0.40 # Standard length
    A_ref = 0.001
    # Circular approx for I: A = pi * r^2 => r = sqrt(A/pi). I = pi * r^4 / 4 = A^2 / (4pi)
    I_ref = (A_ref**2) / (4 * np.pi)

    # Material Props
    E0 = 1.0e9
    rho = 1100.0

    # Information Field Params (Standard from Manuscript)
    # Bimodal Gaussian
    # A_c=0.5, s_c=0.80, sigma_c=0.08, A_l=0.7, s_l=0.25, sigma_l=0.10, I_0=0.3
    # Note: s_c, s_l are normalized (0..1) in IECParameters?
    # iec.py says:
    # I_mode="gaussian" only supports one bump.
    # But generate_coherence_field checks mode.
    # We might need to subclass or modify if "bimodal" is not supported directly in minimal iec.py.
    # Let's check iec.py content again.
    # It has "gaussian" mode: return params.I_amplitude * np.exp(-((s_norm - params.I_center) ** 2) / (2 * params.I_width**2))
    # It doesn't seem to support bimodal sum directly via params unless we supply "file" or extend it.
    # However, the prompt says "Information field: bimodal Gaussian ...".
    # And "Uses the existing IEC beam solver ... (or the simpler src/spinalmodes/iec.py)".
    # If the simpler iec.py doesn't support bimodal, I should probably implement the field generation locally
    # and pass it, OR extend iec.py, OR use a custom mode if available.
    # Looking at iec.py, it calculates I_field inside apply_iec_coupling using generate_coherence_field.
    # I cannot inject a custom field easily without modifying iec.py or subclassing.
    # Wait, I can monkey-patch `generate_coherence_field` in this script!

    def bimodal_gaussian_field(s, params):
        s_norm = s / params.length
        # A_c=0.5, s_c=0.80, sigma_c=0.08
        I_c = 0.5 * np.exp(-((s_norm - 0.80)**2) / (2 * 0.08**2))
        # A_l=0.7, s_l=0.25, sigma_l=0.10
        I_l = 0.7 * np.exp(-((s_norm - 0.25)**2) / (2 * 0.10**2))
        # I_0=0.3
        I_base = 0.3
        return I_base + I_c + I_l

    # Monkey patch
    import spinalmodes.iec
    spinalmodes.iec.generate_coherence_field = bimodal_gaussian_field

    # IEC Params Base
    iec_params_active = IECParameters(
        chi_kappa=0.05,
        E0=E0,
        C0=1e6, # Not used for static
        length=L_ref, # Will be updated in loop
        I_mode="custom_bimodal" # Dummy, since we patched the function
    )

    iec_params_passive = IECParameters(
        chi_kappa=0.0,
        E0=E0,
        C0=1e6,
        length=L_ref,
        I_mode="custom_bimodal"
    )

    results = []

    # Supply curve params
    L0_supply = 0.35
    alpha_vals = [0.5, 1.0]

    # First pass to compute P_counter(L)
    P_counters = []

    for L in Ls:
        # Isometric Scaling
        scale = L / L_ref
        A = A_ref * scale**2
        I = I_ref * scale**4

        # Solve IEC
        s, kappa_iec, _ = solve_beam_column(L, A, I, E0, rho, iec_params_active)

        # Solve Passive
        _, kappa_passive, _ = solve_beam_column(L, A, I, E0, rho, iec_params_passive)

        # Compute Cost
        # P_counter ~ eta * rho * A * g * L^2 * mean(|kappa_iec - kappa_passive|^2)
        # eta = 1.0
        g = 9.81
        mse_kappa = np.mean((kappa_iec - kappa_passive)**2)
        P = 1.0 * rho * A * g * (L**2) * mse_kappa

        P_counters.append(P)

    P_counters = np.array(P_counters)

    # Re-run loop to compute auxiliary metrics efficiently or store them above.
    # We can't efficiently re-run, so let's modify the loop to store them.
    # Wait, I can't easily modify the loop above with a small diff because I need to initialize lists.
    # I'll just re-run the loop? It's cheap. Or recalculate.

    # Let's recalculate auxiliary metrics in a second pass or modify the loop structure.
    # Modifying the loop structure is better but requires larger context.
    # I'll just re-calculate for simplicity since N=30 is tiny.

    Cobb_angles = []
    D_geos = []

    for L in Ls:
        # Isometric Scaling
        scale = L / L_ref
        A = A_ref * scale**2
        I = I_ref * scale**4

        # Solve IEC
        s, kappa_iec, theta_iec = solve_beam_column(L, A, I, E0, rho, iec_params_active)

        # Solve Passive
        _, kappa_passive, _ = solve_beam_column(L, A, I, E0, rho, iec_params_passive)

        # Cobb Angle (deg)
        cobb = np.rad2deg(np.max(theta_iec) - np.min(theta_iec))
        Cobb_angles.append(cobb)

        # D_geo (RMS curvature deviation)
        d_geo = np.sqrt(np.mean((kappa_iec - kappa_passive)**2))
        D_geos.append(d_geo)

    Cobb_angles = np.array(Cobb_angles)
    D_geos = np.array(D_geos)

    # Calculate Supply Curves
    # Find P_counter at L0_supply (0.35)
    P_ref = np.interp(L0_supply, Ls, P_counters)

    S_proprio_05 = P_ref * (Ls / L0_supply)**0.5
    S_proprio_10 = P_ref * (Ls / L0_supply)**1.0

    # Identify Crossings (L_crit)
    # Where P_counter > S_proprio
    # We look for the first index where P > S after being < S?
    # Or just intersection.
    # Assuming P grows faster than S.

    L_crit_05 = None
    # Find intersection using interpolation
    diff_05 = P_counters - S_proprio_05
    # Find zero crossing
    for i in range(len(diff_05)-1):
        if diff_05[i] <= 0 and diff_05[i+1] > 0:
            # Linear interp
            frac = -diff_05[i] / (diff_05[i+1] - diff_05[i])
            L_crit_05 = Ls[i] + frac * (Ls[i+1] - Ls[i])
            break

    # Save Data
    df = pd.DataFrame({
        'L': Ls,
        'P_counter': P_counters,
        'S_proprio_alpha05': S_proprio_05,
        'S_proprio_alpha10': S_proprio_10,
        'Cobb_angle': Cobb_angles,
        'D_geo': D_geos
    })

    out_dir = "outputs/thermodynamic_cost"
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "energy_deficit_window.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved data to {csv_path}")

    if L_crit_05:
        print(f"L_crit (alpha=0.5) found at {L_crit_05:.4f} m")
    else:
        print("No L_crit found in range")

    # Plot
    fig_dir = "outputs/figures"
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "energy_deficit_window.png")

    plt.figure(figsize=(8, 6))
    plt.plot(Ls, P_counters, 'r-', linewidth=2, label=r'$P_{counter}$ (Thermodynamic Cost)')
    plt.plot(Ls, S_proprio_05, 'b--', linewidth=2, label=r'$S_{proprio}$ ($\alpha=0.5$)')
    plt.plot(Ls, S_proprio_10, 'g:', linewidth=2, label=r'$S_{proprio}$ ($\alpha=1.0$)')

    if L_crit_05:
        plt.axvline(L_crit_05, color='k', linestyle='--', alpha=0.5, label=f'$L_{{crit}} \\approx {L_crit_05:.2f}$ m')
        # Shade region
        plt.fill_between(Ls, P_counters, S_proprio_05, where=(Ls >= L_crit_05), color='red', alpha=0.1, label='Energy Deficit')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Power (Normalized)')
    plt.title('Thermodynamic Cost vs Proprioceptive Supply')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_path)
    print(f"Saved figure to {fig_path}")

if __name__ == "__main__":
    run_experiment()
