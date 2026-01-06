
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import time
from datetime import datetime

# Ensure root is in path for imports
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.scoliosis_metrics import compute_scoliosis_metrics

def run_single_sim(chi_kappa, output_dir):
    """Run a single simulation for a given chi_kappa."""

    L = 1.0
    n_points = 200
    s = np.linspace(0, L, n_points)

    # Sinusoidal information field: I = sin^2(2*pi*s/L)
    # This creates a periodic gradient field dI/ds
    I = np.sin(2 * np.pi * s / L)**2
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    # Parameters
    params = CounterCurvatureParams(
        chi_E=0.5,         # Fixed stiffness modulation
        chi_kappa=chi_kappa, # Variable being swept
        chi_M=0.0,
        scale_length=L
    )

    n_elements = 50
    final_time = 2.0
    dt = 1e-4

    # Setup System
    # Horizontal initial state to test gravity vs programmed shape
    # Gravity in -z
    system = CounterCurvatureRodSystem.from_iec(
        info=info,
        params=params,
        length=L,
        n_elements=n_elements,
        E0=1e6,
        radius=0.02,
        rho=1000,
        gravity=9.81,
        base_direction=(1.0, 0.0, 0.0),
        normal=(0.0, 1.0, 0.0)
    )

    # Run
    result = system.run_simulation(final_time=final_time, dt=dt, save_every=100)

    # Analyze
    # Result centerline shape: (time, n_nodes, 3)
    final_centerline = result.centerline[-1] # (n_nodes, 3)
    final_curvature = result.curvature[-1] # (n_elems-1,)

    x = final_centerline[:, 0] # Longitudinal (approx)
    y = final_centerline[:, 1] # Coronal / Lateral
    z = final_centerline[:, 2] # Sagittal / Vertical

    # Debug print ranges
    print(f"    Range X: {x.min():.3f} to {x.max():.3f}")
    print(f"    Range Y: {y.min():.3f} to {y.max():.3f}")
    print(f"    Range Z: {z.min():.3f} to {z.max():.3f}")

    if (x.max() - x.min()) < 1e-6:
        print("    WARNING: X range too small, skipping metrics.")
        return {
            "chi_kappa": chi_kappa,
            "avg_curvature": np.mean(np.abs(final_curvature)),
            "S_lat_sagittal": np.nan,
            "max_deflection_z": np.max(np.abs(z)),
            "final_centerline": final_centerline,
            "final_curvature": final_curvature
        }

    # Sagittal plane metrics (X, Z) - this is where gravity and 'primary' curvature happen
    # Note: compute_scoliosis_metrics expects (z, y) as (longitudinal, lateral)
    sagittal_metrics = compute_scoliosis_metrics(z=x, y=z)

    # Coronal plane metrics (X, Y) - usually zero unless instability
    coronal_metrics = compute_scoliosis_metrics(z=x, y=y)

    avg_curvature = np.mean(np.abs(final_curvature))
    max_deflection_z = np.max(np.abs(z))

    return {
        "chi_kappa": chi_kappa,
        "avg_curvature": avg_curvature,
        "S_lat_sagittal": sagittal_metrics.S_lat,
        "max_deflection_z": max_deflection_z,
        "final_centerline": final_centerline,
        "final_curvature": final_curvature
    }

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_base = Path("outputs/sim") / date_str
    output_base.mkdir(parents=True, exist_ok=True)

    print(f"Running chi_kappa parameter sweep. Output: {output_base}")

    # Sweep Parameters
    chi_kappa_values = np.linspace(0.0, 20.0, 11) # 0 to 20, 11 steps
    results = []

    # Store representative shapes for plotting
    shapes = {}

    for val in chi_kappa_values:
        print(f"  Running chi_kappa = {val:.2f}...")
        res = run_single_sim(val, output_base)
        results.append(res)
        shapes[val] = (res["final_centerline"], res["final_curvature"])

    # Create DataFrame
    df = pd.DataFrame([{k: v for k, v in r.items() if "final" not in k} for r in results])
    df.to_csv(output_base / "results.csv", index=False)

    # Save Params
    with open(output_base / "params.csv", "w") as f:
        f.write("parameter,values\n")
        f.write(f"chi_kappa,{list(chi_kappa_values)}\n")
        f.write("fixed_params,chi_E=0.5;chi_M=0.0;L=1.0;info=sin^2\n")

    # Plotting
    # 1. Metrics vs chi_kappa
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(df["chi_kappa"], df["S_lat_sagittal"], 'o-')
    plt.xlabel(r"$\chi_\kappa$ (Countercurvature Gain)")
    plt.ylabel(r"$S_{lat}$ (Sagittal S-Shape Index)")
    plt.title("S-Shape Emergence")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(df["chi_kappa"], df["max_deflection_z"], 's-', color='orange')
    plt.xlabel(r"$\chi_\kappa$")
    plt.ylabel("Max Vertical Deflection (m)")
    plt.title("Gravity Resistance")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_base / "plot_metrics.png")
    plt.close()

    # 2. Shape Evolution
    plt.figure(figsize=(12, 6))

    # Select subset to plot
    subset_indices = [0, 5, 10] # Low, Mid, High
    subset_vals = [chi_kappa_values[i] for i in subset_indices]

    for val in subset_vals:
        centerline, _ = shapes[val]
        x = centerline[:, 0]
        z = centerline[:, 2]
        plt.plot(x, z, label=r"$\chi_\kappa$=" + f"{val:.1f}")

    plt.plot([0, 1], [0, 0], 'k--', alpha=0.3, label="Rest (Gravity-Free)")
    plt.xlabel("X (m)")
    plt.ylabel("Z (m) [Gravity Down]")
    plt.title("Spinal Profile under Gravity vs Countercurvature")
    plt.legend()
    plt.axis('equal')
    plt.savefig(output_base / "plot_shapes.png")
    plt.close()

    print("Sweep complete.")

if __name__ == "__main__":
    main()
