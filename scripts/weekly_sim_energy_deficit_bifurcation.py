"""
Weekly Simulation: Energy Deficit Bifurcation.

Performs a 2D parameter sweep of the Energy Deficit Window across (chi_kappa, L) space.
Generates a phase diagram showing where AIS vulnerability is highest (R_deficit > 1)
and where lateral instability (Cobb angle) emerges due to the P-delta effect.

Parameters:
- chi_kappa: IEC coupling strength (0.01 - 0.10)
- L: Spinal length (0.25 - 0.55 m)
"""

import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Ensure src is in python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    # Fallback if running from scripts dir
    sys.path.append('../src')
    from spinalmodes.iec import solve_beam_static

def generate_bimodal_gaussian_field(s, L):
    """
    Generate the bimodal Gaussian information field I(s).
    I(s) = A_c * exp(-((s/L - s_c)^2)/(2*sigma_c^2)) +
           A_l * exp(-((s/L - s_l)^2)/(2*sigma_l^2)) + I_0
    """
    if L == 0:
        return np.full_like(s, 0.3)

    s_norm = s / L

    # Parameters from manuscript/sections/methods.tex
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08

    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10

    I_0 = 0.3

    term_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    term_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

    return term_c + term_l + I_0

class BeamColumnSolver:
    """
    Iterative solver for lateral beam-column instability (P-delta effect).
    Uses solve_beam_static for the linear step and updates the moment
    distribution based on axial load P(s) and deflection w(s).
    """
    def __init__(self, rho, A, g, E0, I_moment, max_iter=20, tol=1e-4):
        self.rho = rho
        self.A = A
        self.g = g
        self.E0 = E0
        self.I_moment = I_moment
        self.max_iter = max_iter
        self.tol = tol

    def solve_lateral_cobb(self, s, L, kappa_pert_mag):
        """
        Solve for lateral deflection under gravity and perturbation.

        Args:
            s: spatial array
            L: length
            kappa_pert_mag: Magnitude of lateral curvature perturbation (1/m)

        Returns:
            cobb_angle (deg)
        """
        # Initial guess: 0 deflection
        theta = np.zeros_like(s)
        w = np.zeros_like(s) # deflection

        # Perturbation moment (assuming constant curvature bias -> constant moment bias EI*kappa)
        # Or better: treat perturbation as a target curvature kappa_target
        # M_pert = EI * kappa_pert
        # We can pass kappa_target to solve_beam_static directly.

        kappa_target_pert = np.full_like(s, kappa_pert_mag)

        # Axial Load P(s) = rho * A * g * (L - s)
        # This is compressive load.
        # In solve_beam_static, we solve: EI(k - k_target) = M_ext
        # M_ext = M_transverse + M_P_delta
        # M_P_delta(s) = Integral_s^L P(x) * w'(x) dx ? No.
        # Moment at s due to axial load P acting on deflected shape:
        # M_P(s) = P(s) * (w(L) - w(s)) ?
        # For a column, the moment is M(s) = P * (delta - w(s)).
        # With distributed load P(s), it's more complex.
        # M_P(s) = Integral_x=s^L (rho A g dx) * (w(x) - w(s))

        # We will iterate.

        # Stiffness (Lateral). Assume isotropic for this solver or scaled.
        # If we assume lateral stiffness is E0 * I (no IEC scaling for lateral unless specified)
        E_field = np.full_like(s, self.E0)

        for i in range(self.max_iter):
            # 1. Calculate P-delta moment from current w
            M_P_delta = np.zeros_like(s)

            # Discrete integral for M_P_delta
            # M_P_delta[i] = Sum_{j=i}^{N} rho*A*g*ds * (w[j] - w[i])
            ds = s[1] - s[0]
            load_element = self.rho * self.A * self.g * ds

            # Vectorized calculation?
            # M[i] = Sum_{j=i} P_elem * (w[j] - w[i])
            #      = Sum_{j=i} P_elem * w[j] - w[i] * Sum_{j=i} P_elem
            # Let P_sum[i] = Sum_{j=i} P_elem (Total load above i)
            # Let Pw_sum[i] = Sum_{j=i} P_elem * w[j]
            # M[i] = Pw_sum[i] - w[i] * P_sum[i]

            P_elem = np.full_like(s, load_element)
            P_sum = np.cumsum(P_elem[::-1])[::-1] # Cumulative sum from end
            Pw_sum = np.cumsum((P_elem * w)[::-1])[::-1]

            M_P_delta = Pw_sum - w * P_sum

            # 2. Solve beam with effective moment
            # solve_beam_static solves: EI(k - k_target) = M_ext - M_active
            # We want EI * k = EI * k_target + M_ext
            # Here M_ext includes M_P_delta.
            # But solve_beam_static computes M_ext internally from P_load and distributed_load (Transverse).
            # We treat M_P_delta as an "Active Moment" (negative) or modify M_ext.
            # Actually, `solve_beam_static` takes `M_active`.
            # Equation: EI(k - k_t) = M_ext_transverse - M_active
            # We want: EI(k - k_t) = M_ext_transverse + M_P_delta
            # So we can pass M_active = -M_P_delta

            theta_new, kappa_new = solve_beam_static(
                s=s,
                kappa_target=kappa_target_pert,
                E_field=E_field,
                M_active=-M_P_delta, # Invert sign to add it
                I_moment=self.I_moment,
                P_load=0.0,
                distributed_load=0.0 # No transverse gravity in lateral plane (assuming upright)
            )

            # 3. Integrate theta to get w
            w_new = np.zeros_like(s)
            w_new[1:] = np.cumsum(0.5 * (theta_new[1:] + theta_new[:-1]) * ds)

            # 4. Check convergence
            diff = np.max(np.abs(w_new - w))
            if diff < self.tol:
                w = w_new
                theta = theta_new
                break

            w = w_new
            theta = theta_new

        # Calculate Cobb Angle (Range of Theta in Degrees)
        cobb = np.rad2deg(np.max(theta) - np.min(theta))
        return cobb

def run_simulation():
    print("Running Energy Deficit Bifurcation Sweep...")

    # Setup Output
    output_dir_data = Path("outputs/thermodynamic_cost")
    output_dir_figs = Path("outputs/figures")
    output_dir_data.mkdir(parents=True, exist_ok=True)
    output_dir_figs.mkdir(parents=True, exist_ok=True)

    # Sweep Parameters
    chi_vals = np.linspace(0.01, 0.10, 20)
    L_vals = np.linspace(0.25, 0.55, 20)

    # Fixed Parameters
    rho = 1100.0
    A = 0.001
    g = 9.81
    E0 = 1.0e9
    I_moment = 1.0e-8
    chi_E = 0.10 # Stiffness modulation
    eta_a = 1.0 # Cost scaling

    # Lateral Asymmetry
    epsilon_asym = 0.03

    results = []

    # Solver for Lateral Cobb
    lateral_solver = BeamColumnSolver(rho, A, g, E0, I_moment)

    # Pre-calculate Supply Reference S0
    # At L=0.35, chi=0.05
    ref_L = 0.35
    ref_chi = 0.05

    # Compute P_counter for reference
    ref_s = np.linspace(0, ref_L, 100)
    ref_I = generate_bimodal_gaussian_field(ref_s, ref_L)
    ref_grad_I = np.gradient(ref_I, ref_s)
    ref_E = E0 * (1.0 + chi_E * ref_I)

    # Reference IEC
    ref_kappa_t = ref_chi * ref_grad_I
    ref_theta, ref_kappa = solve_beam_static(
        s=ref_s, kappa_target=ref_kappa_t, E_field=ref_E,
        M_active=np.zeros_like(ref_s), I_moment=I_moment,
        P_load=0.0, distributed_load=rho*A*g
    )
    # Reference Passive
    ref_theta_p, ref_kappa_p = solve_beam_static(
        s=ref_s, kappa_target=np.zeros_like(ref_s), E_field=ref_E,
        M_active=np.zeros_like(ref_s), I_moment=I_moment,
        P_load=0.0, distributed_load=rho*A*g
    )

    ref_diff_sq = (ref_kappa - ref_kappa_p)**2
    S0 = eta_a * rho * A * g * (ref_L**2) * np.mean(ref_diff_sq)
    print(f"Reference S0 calculated: {S0:.6f} at L={ref_L}, chi={ref_chi}")

    # Main Sweep
    # Grid for plotting
    Cobb_grid = np.zeros((len(chi_vals), len(L_vals)))
    R_grid = np.zeros((len(chi_vals), len(L_vals)))

    for i, chi in enumerate(chi_vals):
        for j, L in enumerate(L_vals):
            n_nodes = 100
            s = np.linspace(0, L, n_nodes)

            # --- 1. Sagittal (Counter-Curvature) Analysis ---
            I_field = generate_bimodal_gaussian_field(s, L)
            grad_I = np.gradient(I_field, s)
            E_field = E0 * (1.0 + chi_E * I_field)

            # IEC State
            kappa_t_iec = chi * grad_I
            _, kappa_iec = solve_beam_static(
                s=s, kappa_target=kappa_t_iec, E_field=E_field,
                M_active=np.zeros_like(s), I_moment=I_moment,
                P_load=0.0, distributed_load=rho*A*g
            )

            # Passive State
            _, kappa_pass = solve_beam_static(
                s=s, kappa_target=np.zeros_like(s), E_field=E_field,
                M_active=np.zeros_like(s), I_moment=I_moment,
                P_load=0.0, distributed_load=rho*A*g
            )

            # Cost
            diff_sq = (kappa_iec - kappa_pass)**2
            P_counter = eta_a * rho * A * g * (L**2) * np.mean(diff_sq)

            # Supply & Ratio
            S_proprio = S0 * (L / ref_L)**0.7
            R_deficit = P_counter / S_proprio

            # --- 2. Lateral (Cobb) Analysis ---
            # Perturbation: epsilon_asym = 0.03
            # We assume this corresponds to a curvature perturbation scaled by length?
            # or constant? Let's use kappa_pert = 0.03 / L (dimensionless 0.03)
            kappa_pert = epsilon_asym / L
            cobb_angle = lateral_solver.solve_lateral_cobb(s, L, kappa_pert)

            results.append({
                "chi_kappa": chi,
                "L": L,
                "P_counter": P_counter,
                "S_proprio": S_proprio,
                "R_deficit": R_deficit,
                "cobb_angle": cobb_angle
            })

            Cobb_grid[i, j] = cobb_angle
            R_grid[i, j] = R_deficit

    # Save CSV
    df = pd.DataFrame(results)
    csv_path = output_dir_data / "phase_diagram_energy_deficit.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Plot 1: R_deficit Heatmap
    plt.figure(figsize=(10, 8))
    X, Y = np.meshgrid(L_vals, chi_vals) # L on X, chi on Y
    # Note: meshgrid returns (rows, cols), so need to match grid shape
    # Grid is (len(chi), len(L)).

    cp = plt.contourf(X, Y, R_grid, levels=20, cmap='RdYlBu_r') # Red for high deficit
    plt.colorbar(cp, label='Energy Deficit Ratio (R_deficit)')

    # Contour line at R=1
    cs = plt.contour(X, Y, R_grid, levels=[1.0], colors='k', linewidths=2, linestyles='--')
    plt.clabel(cs, inline=1, fontsize=10, fmt='R=1.0')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('IEC Coupling Strength (chi_kappa)')
    plt.title('Energy Deficit Phase Diagram')
    plt.grid(True, alpha=0.3)

    fig_path1 = output_dir_figs / "phase_diagram_energy_deficit.png"
    plt.savefig(fig_path1, dpi=300)
    plt.close()

    # Plot 2: Cobb Angle Heatmap
    plt.figure(figsize=(10, 8))
    cp2 = plt.contourf(X, Y, Cobb_grid, levels=20, cmap='viridis')
    plt.colorbar(cp2, label='Cobb Angle (deg)')

    # Overlay R=1 line
    plt.contour(X, Y, R_grid, levels=[1.0], colors='r', linewidths=2, linestyles='--')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('IEC Coupling Strength (chi_kappa)')
    plt.title('Cobb Angle Phase Diagram')
    plt.grid(True, alpha=0.3)

    fig_path2 = output_dir_figs / "phase_diagram_energy_deficit_cobb.png"
    plt.savefig(fig_path2, dpi=300)
    plt.close()

    print("Figures saved.")

if __name__ == "__main__":
    run_simulation()
