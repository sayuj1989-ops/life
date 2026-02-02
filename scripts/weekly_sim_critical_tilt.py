"""
Weekly Simulation: Critical Tilt Sweep
Goal: Test for the 'Critical Tilt Angle' where high anisotropy (R=10) fails to stabilize the spine against high growth (chi=10) and gravity.
Hypothesis: 'Tension Tether' stability (high anisotropy) has a critical breakdown angle where lateral/torsional buckling becomes sudden and catastrophic.
"""

import os
import sys
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.coupling import CounterCurvatureParams

def run_experiment(
    tilt_deg: float,
    anisotropy: float = 10.0,
    chi_kappa: float = 10.0,
    chi_tau: float = 0.2,
    base_length: float = 1.0,
    n_elements: int = 40,
    final_time: float = 20.0,
    dt: float = 1e-4,
) -> dict:
    """
    Run a single simulation with a tilted base.
    """

    theta = np.deg2rad(tilt_deg)
    # Tilted about X-axis? No, usually tilt means "leaning tower".
    # If base direction is (sin(theta), 0, cos(theta)), it leans in X-Z plane (Lateral).
    # d1 (Normal) = X, d2 (Binormal) = Y, d3 (Tangent) = Z.
    # We want to tilt the GRAVITY vector relative to the rod, OR tilt the ROD relative to GRAVITY.
    # PyElastica has gravity=(0, -9.81, 0) typically, but here CounterCurvatureRodSystem uses 'gravity' float
    # and likely assumes gravity is -Z or -Y.
    # experiment_minimal_elastica: base_direction=(0,0,1) (Z-up), gravity=9.81.
    # If we change base_direction to be tilted, gravity (acting down) will have a lateral component relative to the rod.

    # Tilt in the Lateral Plane (X-Z plane).
    # d1 is X (Normal), d2 is Y (Binormal).
    # If we tilt in X-Z plane, we induce bending about Y (d2). This is "Lateral Bending".
    base_direction = (np.sin(theta), 0.0, np.cos(theta))

    # Normal must be perpendicular to tangent.
    # If tangent is (sin, 0, cos), normal could be (cos, 0, -sin)? No, Y (0,1,0) is perpendicular.
    # Let's keep normal as (0, 1, 0) (Y-axis).
    # Check dot product: (sin, 0, cos) . (0, 1, 0) = 0. Correct.
    normal = (0.0, 1.0, 0.0)

    # Create info field (linear growth gradient)
    s = np.linspace(0, base_length, n_elements + 1)
    I = s / base_length
    info = InfoField1D.from_array(s, I)

    # Params
    params = CounterCurvatureParams(
        chi_kappa=chi_kappa,
        chi_E=0.0,
        chi_M=0.0,
        chi_tau=chi_tau,
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
    metrics['chi_tau'] = chi_tau

    return metrics

def main():
    # Set Seed for Reproducibility
    seed = 20260202
    np.random.seed(seed)

    # Setup Output
    today = datetime.date.today().isoformat()
    output_dir = Path(f"outputs/sim/{today}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Critical Tilt Sweep -> {output_dir}")
    print(f"Random Seed: {seed}")

    # Parameters to sweep
    # Coarse sweep then fine
    tilts = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0]

    # Fixed parameters
    anisotropy = 10.0 # High Anisotropy (Tension Tether)
    chi_kappa = 10.0  # High Growth
    chi_tau = 0.2     # Weak Torsion

    results = []

    print("-" * 80)
    print(f"{'Tilt (deg)':<10} | {'S_lat':<10} | {'Cobb':<10} | {'Max Tor':<10}")
    print("-" * 80)

    for val in tilts:
        try:
            metrics = run_experiment(
                tilt_deg=val,
                anisotropy=anisotropy,
                chi_kappa=chi_kappa,
                chi_tau=chi_tau
            )
            results.append(metrics)
            print(f"{val:<10.1f} | {metrics.get('S_lat', 0):<10.4f} | {metrics.get('cobb_angle', 0):<10.2f} | {metrics.get('max_torsion', 0):<10.4f}")
        except Exception as e:
            print(f"Failed run at Tilt={val}: {e}")

    # Save CSV
    df = pd.DataFrame(results)
    csv_path = output_dir / "results.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Save Params
    params_path = output_dir / "params.csv"
    with open(params_path, 'w') as f:
        f.write(f"seed,{seed}\n")
        f.write(f"chi_kappa,{chi_kappa}\n")
        f.write(f"anisotropy,{anisotropy}\n")
        f.write(f"chi_tau,{chi_tau}\n")
        f.write("variable,tilt_deg,0.0,45.0,10\n")

    # Plotting
    if not df.empty:
        # Plot 1: Tilt vs S_lat
        plt.figure(figsize=(10, 6))
        plt.plot(df['tilt_deg'], df['S_lat'], marker='o', color='purple')
        plt.axhline(y=0.15, color='r', linestyle='--', label='Scoliosis Threshold')
        plt.xlabel('Tilt Angle (deg)')
        plt.ylabel('Lateral S-Index (S_lat)')
        plt.title(f'Critical Tilt: S-Shape Emergence (R={anisotropy}, chi={chi_kappa})')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_dir / "plot_s_lat.png")
        plt.close()

        # Plot 2: Tilt vs Cobb Angle
        plt.figure(figsize=(10, 6))
        plt.plot(df['tilt_deg'], df['cobb_angle'], marker='s', color='blue')
        plt.xlabel('Tilt Angle (deg)')
        plt.ylabel('Cobb Angle (deg)')
        plt.title(f'Critical Tilt: Cobb Angle (R={anisotropy}, chi={chi_kappa})')
        plt.grid(True)
        plt.savefig(output_dir / "plot_cobb.png")
        plt.close()

    # Generate Report
    report_path = output_dir / "report.md"
    with open(report_path, "w") as f:
        f.write(f"# Critical Tilt Sweep Report - {today}\n\n")
        f.write("## Hypothesis\n")
        f.write(f"Testing for a 'Critical Tilt Angle' where high anisotropy (R={anisotropy}) fails to stabilize the spine against high growth (chi={chi_kappa}).\n\n")
        f.write("## Parameters\n")
        f.write(f"- Random Seed: {seed}\n")
        f.write(f"- Anisotropy: {anisotropy}\n")
        f.write(f"- Growth (chi_kappa): {chi_kappa}\n")
        f.write(f"- Torsion (chi_tau): {chi_tau}\n")
        f.write("- Tilt Range: 0 to 45 deg\n\n")
        f.write("## Results Summary\n")
        if not df.empty:
            max_s = df['S_lat'].max()
            critical_tilt = df.loc[df['S_lat'].idxmax(), 'tilt_deg']

            f.write(f"- Max Lateral S-Index: {max_s:.4f} at {critical_tilt} deg\n")

            if max_s > 0.15:
                f.write(f"**CRITICAL BREAKDOWN**: At {critical_tilt} degrees, the system buckled into a significant S-shape (S_lat={max_s:.2f}).\n")
            else:
                 f.write(f"**STABLE**: The system remained relatively stable (S_lat < 0.15) up to 45 degrees. High anisotropy provides robust protection.\n")

    print(f"Report written to {report_path}")

if __name__ == "__main__":
    main()
