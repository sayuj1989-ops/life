import os
import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import csv

def generate_defect_field(x, y, defect_type=+0.5, core_radius=0.2):
    theta = defect_type * np.arctan2(y, x)
    r = np.sqrt(x**2 + y**2)
    S = 1.0 - np.exp(-(r / core_radius)**2)
    return theta, S

def calculate_active_force(X, Y, theta, S, zeta=1.0):
    Qxx = S * (np.cos(theta)**2 - 0.5)
    Qxy = S * (np.cos(theta) * np.sin(theta))
    Qyy = S * (np.sin(theta)**2 - 0.5)

    dx = X[0, 1] - X[0, 0]
    dy = Y[1, 0] - Y[0, 0]

    dQxx_dx = np.gradient(Qxx, dx, axis=1)
    dQxy_dy = np.gradient(Qxy, dy, axis=0)
    fx = -zeta * (dQxx_dx + dQxy_dy)

    dQyx_dx = np.gradient(Qxy, dx, axis=1)
    dQyy_dy = np.gradient(Qyy, dy, axis=0)
    fy = -zeta * (dQyx_dx + dQyy_dy)

    return fx, fy

def simulate_beam_deflection(force_profile, L=1.0, EI=1.0):
    N = len(force_profile)
    x = np.linspace(0, L, N)

    total_force = integrate.trapezoid(force_profile, x)
    moment_of_force = integrate.trapezoid(force_profile * x, x)
    R2 = moment_of_force / L
    R1 = total_force - R2

    V = R1 - integrate.cumulative_trapezoid(force_profile, x, initial=0)
    M = integrate.cumulative_trapezoid(V, x, initial=0)
    kappa = -M / EI
    slope = integrate.cumulative_trapezoid(kappa, x, initial=0)
    w = integrate.cumulative_trapezoid(slope, x, initial=0)

    w_corrected = w - w[-1] * (x / L)

    return x, w_corrected

def main():
    out_dir = "outputs/experiments/active_nematic"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs("outputs/figures", exist_ok=True)

    print("Simulating Active Nematic Defect...")

    L_tissue = 2.0
    x_grid = np.linspace(-L_tissue/2, L_tissue/2, 100)
    y_grid = np.linspace(-L_tissue/2, L_tissue/2, 100)
    X, Y = np.meshgrid(x_grid, y_grid)

    defect_type = 0.5
    core_radius = 0.15
    zeta_extensile = 5.0

    theta, S = generate_defect_field(X, Y, defect_type, core_radius)
    fx, fy = calculate_active_force(X, Y, theta, S, zeta_extensile)

    midline_idx = len(y_grid) // 2
    transverse_force = fx[midline_idx, :]

    L_spine = L_tissue
    EI_normal = 1.0

    spine_x, deflection = simulate_beam_deflection(transverse_force, L=L_spine, EI=EI_normal)
    max_deflection = np.max(np.abs(deflection))
    print(f"Max spine deflection: {max_deflection:.4f}")

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    st = 5
    axs[0].contourf(X, Y, S, cmap='viridis', alpha=0.5)
    axs[0].quiver(X[::st, ::st], Y[::st, ::st], np.cos(theta[::st, ::st]), np.sin(theta[::st, ::st]), pivot='mid', headlength=0, headaxislength=0)
    axs[0].set_title("+1/2 Topological Defect")
    axs[0].set_aspect('equal')

    axs[1].streamplot(X, Y, fx, fy, color=np.sqrt(fx**2 + fy**2), cmap='magma')
    axs[1].set_title("Active Force Field")
    axs[1].set_aspect('equal')

    axs[2].plot(spine_x - L_spine/2, transverse_force, 'r--', label='Transverse Force')
    axs[2].plot(spine_x - L_spine/2, deflection * 10, 'b-', linewidth=2, label='Spinal Deflection (x10)')
    axs[2].set_title("Resulting Spinal Curvature")
    axs[2].legend()
    axs[2].grid(True)

    plt.tight_layout()
    fig_path = "outputs/figures/nematic_defect_buckling.png"
    plt.savefig(fig_path, dpi=300)
    print(f"Saved figure to {fig_path}")

    csv_path = os.path.join(out_dir, "nematic_defect_results.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x_pos", "transverse_force", "deflection"])
        for xi, fi, wi in zip(spine_x, transverse_force, deflection):
            writer.writerow([xi, fi, wi])
    print(f"Saved numerical results to {csv_path}")

if __name__ == "__main__":
    main()
