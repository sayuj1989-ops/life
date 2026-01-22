
import os
import sys
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem, SimulationResult
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.coupling import CounterCurvatureParams

def run_simulation_case(
    anisotropy: float,
    tilt_deg: float = 15.0,
    chi_kappa: float = 10.0,
    base_length: float = 1.0,
    n_elements: int = 40,
    final_time: float = 10.0,
    dt: float = 1e-4,
) -> dict:
    """
    Run a single simulation with specific anisotropy and fixed tilt.
    """

    theta = np.deg2rad(tilt_deg)
    base_direction = (np.sin(theta), 0.0, np.cos(theta))
    normal = (0.0, 1.0, 0.0) # Normal stays along Y

    # Create info field (linear growth gradient)
    # I(s) = s / L (linear increase from 0 to 1)
    s = np.linspace(0, base_length, n_elements + 1)
    I = s / base_length
    info = InfoField1D.from_array(s, I)

    # Params
    params = CounterCurvatureParams(
        chi_kappa=chi_kappa,
        chi_E=0.0,
        chi_M=0.0,
        chi_tau=0.0,
        scale_length=1.0
    )

    # Create System
    system = CounterCurvatureRodSystem.from_iec(
        info=info,
        params=params,
        length=base_length,
        n_elements=n_elements,
        radius=0.02,
        E0=1e6,
        rho=1000.0,
        base_direction=base_direction,
        normal=normal,
        stiffness_anisotropy=anisotropy,
    )

    # Run
    # Use 'fixed' boundary condition (cantilever)
    res = system.run_simulation(
        final_time=final_time,
        dt=dt,
        save_every=int(final_time/dt/100), # 100 frames total
        boundary_condition="fixed"
    )

    metrics = res.compute_final_metrics()
    metrics['tilt_deg'] = tilt_deg
    metrics['chi_kappa'] = chi_kappa
    metrics['anisotropy'] = anisotropy

    return metrics

def main():
    # Set Seed for Reproducibility
    seed = 42
    np.random.seed(seed)

    # Setup Output
    today = datetime.date.today().isoformat()
    output_dir = Path(f"outputs/sim/{today}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Anisotropy Stability Sweep -> {output_dir}")
    print(f"Random Seed: {seed}")

    # Parameters to sweep
    # Anisotropy < 1: Weaker lateral stiffness (Unstable?)
    # Anisotropy = 1: Isotropic
    # Anisotropy > 1: Stiffer lateral stiffness (Stable?)
    anisotropies = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 5.0, 10.0]

    fixed_tilt = 15.0
    fixed_chi_kappa = 10.0

    results = []

    for aniso in anisotropies:
        print(f"Running Anisotropy = {aniso}...")
        try:
            metrics = run_simulation_case(aniso, tilt_deg=fixed_tilt, chi_kappa=fixed_chi_kappa)
            results.append(metrics)
        except Exception as e:
            print(f"Failed run at anisotropy {aniso}: {e}")

    # Save CSV
    df = pd.DataFrame(results)
    csv_path = output_dir / "results.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Save Params
    params_path = output_dir / "params.csv"
    with open(params_path, 'w') as f:
        f.write(f"seed,{seed}\n")
        f.write(f"chi_kappa,{fixed_chi_kappa}\n")
        f.write(f"tilt_deg,{fixed_tilt}\n")
        f.write(f"variable,anisotropy,{min(anisotropies)},{max(anisotropies)},{len(anisotropies)}\n")

    # Plotting
    if not df.empty:
        # Plot 1: S_lat vs Anisotropy
        plt.figure(figsize=(10, 6))
        plt.plot(df['anisotropy'], df['S_lat'], marker='o', color='purple')
        plt.xscale('log')
        plt.xlabel('Stiffness Anisotropy (Log Scale)')
        plt.ylabel('Lateral S-Index (S_lat)')
        plt.title(f'Scoliosis Index vs Anisotropy (Tilt={fixed_tilt} deg)')
        plt.grid(True, which="both", ls="-")
        plt.savefig(output_dir / "plot_s_lat_vs_anisotropy.png")
        plt.close()

        # Plot 2: Tip Deflection Components
        plt.figure(figsize=(10, 6))
        plt.plot(df['anisotropy'], df['x_tip'], marker='o', label='Lateral Tip (X)')
        plt.plot(df['anisotropy'], df['y_tip'], marker='^', label='Sagittal Tip (Y)')
        plt.xscale('log')
        plt.xlabel('Stiffness Anisotropy (Log Scale)')
        plt.ylabel('Tip Position (m)')
        plt.title('Tip Deflection vs Anisotropy')
        plt.legend()
        plt.grid(True, which="both", ls="-")
        plt.savefig(output_dir / "plot_tip_components.png")
        plt.close()

        # Plot 3: Cobb Angle
        plt.figure(figsize=(10, 6))
        plt.plot(df['anisotropy'], df['cobb_angle'], marker='s', color='red')
        plt.xscale('log')
        plt.xlabel('Stiffness Anisotropy (Log Scale)')
        plt.ylabel('Cobb Angle (deg)')
        plt.title('Cobb Angle vs Anisotropy')
        plt.grid(True, which="both", ls="-")
        plt.savefig(output_dir / "plot_cobb_angle.png")
        plt.close()

    # Generate Report
    report_path = output_dir / "report.md"
    with open(report_path, "w") as f:
        f.write(f"# Anisotropy Stability Sweep Report - {today}\n\n")
        f.write("## Hypothesis\n")
        f.write("Testing if increasing lateral stiffness (Anisotropy > 1.0) can rescue the spine from S-shape formation induced by lateral tilt (15 deg) and growth.\n\n")
        f.write("## Parameters\n")
        f.write(f"- Random Seed: {seed}\n")
        f.write(f"- Growth Gradient (chi_kappa): {fixed_chi_kappa}\n")
        f.write(f"- Base Tilt: {fixed_tilt} deg (Lateral X-Z plane)\n")
        f.write(f"- Stiffness Anisotropy Sweep: {anisotropies}\n\n")
        f.write("## Results Summary\n")
        if not df.empty:
            # Find anisotropy where S_lat is minimized vs maximized
            row_max = df.loc[df['S_lat'].idxmax()]
            row_min = df.loc[df['S_lat'].idxmin()]

            f.write(f"- **Max S-Index**: {row_max['S_lat']:.4f} at Anisotropy={row_max['anisotropy']}\n")
            f.write(f"- **Min S-Index**: {row_min['S_lat']:.4f} at Anisotropy={row_min['anisotropy']}\n")
            f.write(f"- **Max Cobb Angle**: {df['cobb_angle'].max():.2f} deg\n\n")

            f.write("## Interpretation\n")

            # Simple heuristic analysis
            low_aniso = df[df['anisotropy'] < 1.0]['S_lat'].mean()
            high_aniso = df[df['anisotropy'] > 1.0]['S_lat'].mean()

            f.write(f"Average S-Index for Anisotropy < 1.0: {low_aniso:.4f}\n")
            f.write(f"Average S-Index for Anisotropy > 1.0: {high_aniso:.4f}\n\n")

            if high_aniso < low_aniso:
                 f.write("Increasing lateral stiffness (Anisotropy > 1) successfully reduces lateral deviation and S-shape formation, confirming the stabilizing role of lateral stiffness.\n")
            else:
                 f.write("Increasing lateral stiffness did not clearly suppress S-shape formation in this regime.\n")

        else:
            f.write("No results generated.\n")

    print(f"Report written to {report_path}")

if __name__ == "__main__":
    main()
