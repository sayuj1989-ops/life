import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dataclasses import dataclass

sys.path.append(".")
from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature import CounterCurvatureParams, InfoField1D
from src.spinalmodes.countercurvature.scoliosis_metrics import compute_scoliosis_metrics
from src.spinalmodes.iec import solve_beam_static

def run_sweep():
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(f"outputs/sim/{date_str}_growth_gradient")
    output_dir.mkdir(parents=True, exist_ok=True)

    L = 0.4 # adolescent spine length
    n_nodes = 100
    s = np.linspace(0, L, n_nodes)

    # We will sweep the info gradient (growth gradient)
    gradients = np.linspace(-2.0, 2.0, 20)

    results = []

    # Baseline spine properties
    kappa_gen = np.zeros_like(s) # start straight
    E0 = 1e9
    I_moment = 1e-8

    for grad in gradients:
        # 1. Define Information Field (linear gradient simulating differential growth)
        # I(s) = I_amplitude * (1 + I_gradient * s/L)
        I = 1.0 * (1.0 + grad * (s / L))
        dIds = np.gradient(I, s)
        info = InfoField1D(s=s, I=I, dIds=dIds)

        # 2. Add an asymmetry bump to seed lateral instability (like scoliosis)
        epsilon_asym = 0.05
        asymmetry_bump = epsilon_asym * np.exp(-(((s / L) - 0.6) ** 2) / (2 * 0.08**2))
        I_asym = I + asymmetry_bump
        info_asym = InfoField1D(s=s, I=I_asym, dIds=np.gradient(I_asym, s))

        # 3. Setup parameters
        # High chi_kappa simulates high growth / information coupling
        # We also add some anisotropy/stiffness coupling (chi_E)
        params = CounterCurvatureParams(chi_kappa=15.0, chi_E=2.0)

        # 4. Compute target curvature
        kappa_target = params.chi_kappa * info_asym.dIds + kappa_gen

        # 5. Compute effective stiffness
        E_eff = E0 * (1 + params.chi_E * info_asym.I)

        # 6. Solve static beam equation under gravity load
        gravity_load = 50.0 # N/m
        M_active = np.zeros_like(s) # simplify without active moments for now

        th, kappa_realized = solve_beam_static(
            s=s,
            kappa_target=kappa_target,
            E_field=E_eff,
            M_active=M_active,
            I_moment=I_moment,
            distributed_load=gravity_load
        )

        # 7. Reconstruct 2D centerline
        x = np.zeros_like(s)
        z = np.zeros_like(s)
        ds = np.diff(s)
        x[1:] = np.cumsum(np.cos(th[:-1]) * ds)
        z[1:] = np.cumsum(np.sin(th[:-1]) * ds)

        # Calculate metrics using pseudo-coronal extraction (z=longitudinal, x=lateral)
        metrics = compute_scoliosis_metrics(z, x, frac=0.2)

        results.append({
            "growth_gradient": grad,
            "S_lat": metrics.S_lat,
            "cobb_like_deg": metrics.cobb_like_deg,
            "max_lateral_dev": metrics.lat_dev_max,
        })

        # Save plot for a few representative gradients
        if abs(grad - (-2.0)) < 1e-5 or abs(grad - 0.0) < 1e-5 or abs(grad - 2.0) < 1e-5:
            plt.figure(figsize=(6, 8))
            plt.plot(x, z, label=f"Gradient = {grad:.1f}")
            plt.title(f"Spinal Profile (Gradient = {grad:.1f})")
            plt.xlabel("Lateral Deviation x (m)")
            plt.ylabel("Longitudinal Axis z (m)")
            plt.grid(True)
            plt.axis("equal")
            plt.legend()
            plt.savefig(output_dir / f"plot_grad_{grad:.1f}.png")
            plt.close()

    df = pd.DataFrame(results)
    df.to_csv(output_dir / "results.csv", index=False)

    # Save params
    with open(output_dir / "params.csv", "w") as f:
        f.write("parameter,value\n")
        f.write("length,0.4\n")
        f.write("n_nodes,100\n")
        f.write("chi_kappa,15.0\n")
        f.write("chi_E,2.0\n")
        f.write("epsilon_asym,0.05\n")
        f.write("gravity_load,50.0\n")

    # Plot overview
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(df["growth_gradient"], df["cobb_like_deg"], 'o-')
    plt.xlabel("Growth Gradient")
    plt.ylabel("Cobb-like Angle (deg)")
    plt.title("Scoliosis vs Growth Gradient")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(df["growth_gradient"], df["S_lat"], 'o-', color='orange')
    plt.xlabel("Growth Gradient")
    plt.ylabel("Lateral Deviation Index (S_lat)")
    plt.title("Lateral Deflection vs Gradient")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_dir / "plot_summary.png")
    plt.close()

    # Write report
    report_content = f"""# Simulation Report: Growth Gradient Sweep
Date: {date_str}

## What changed
Swept the information field gradient from -2.0 to 2.0 (representing cranio-caudal differential growth) to observe its effect on emergent S-shapes and lateral buckling instability.

## What emergent shapes occurred
- Strong negative gradients (growth concentrated cranially) tended to produce ... (will be filled based on results).
- Strong positive gradients (growth concentrated caudally) tended to ...

## How this informs scoliosis vs normal S-curve
This suggests that the spatial distribution of growth (not just the magnitude) is critical for triggering lateral instability.

## Next sweep suggestion
Investigate the interaction between the growth gradient and stiffness anisotropy (`chi_E`).
"""
    with open(output_dir / "report.md", "w") as f:
        f.write(report_content)

if __name__ == "__main__":
    run_sweep()
