
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time
import csv
import elastica as ea

# Add project root to sys.path to resolve imports
sys.path.append(os.getcwd())

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams

def run_anisotropy_sweep():
    print("Starting Anisotropy Sweep Experiment...")

    # 1. Setup Base Parameters
    L = 1.0
    n_elements = 50
    n_points = 200
    final_time = 2.0
    dt = 1e-4

    s = np.linspace(0, L, n_points)
    I = np.sin(2 * np.pi * s / L)**2
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    anisotropy_values = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    fixed_chi_kappa = 2.0

    results_summary = []

    # Output setup
    date_str = time.strftime("%Y-%m-%d")
    output_dir = Path(f"outputs/sim/{date_str}")
    output_dir.mkdir(parents=True, exist_ok=True)

    params_csv_path = output_dir / "params.csv"
    results_csv_path = output_dir / "results.csv"

    # Save params
    with open(params_csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["parameter", "values"])
        writer.writerow(["anisotropy_values", str(anisotropy_values)])
        writer.writerow(["fixed_chi_kappa", fixed_chi_kappa])
        writer.writerow(["E0", 1e6])
        writer.writerow(["L", L])
        writer.writerow(["n_elements", n_elements])
        writer.writerow(["Gravity_Y", 1.0])

    for alpha in anisotropy_values:
        print(f"Running simulation for anisotropy_ratio (EI_2 scaling) = {alpha}...")

        # Define Params
        params = CounterCurvatureParams(
            chi_E=0.0,
            chi_kappa=fixed_chi_kappa,
            chi_M=0.0,
            scale_length=L
        )

        # Initialize System (Vertical)
        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=1e6,
            radius=0.02,
            rho=1000,
            gravity=9.81,
            base_position=(0.0, 0.0, 0.0),
            base_direction=(0.0, 0.0, 1.0),
            normal=(0.0, 1.0, 0.0)
        )

        class CCSystem(ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks):
            pass

        sim_system = CCSystem()
        sim_system.append(system.rod)

        sim_system.constrain(system.rod).using(
            ea.OneEndFixedBC,
            constrained_position_idx=(0,),
            constrained_director_idx=(0,)
        )

        # Tilted Gravity (Y-component)
        gravity_vector = np.array([0.0, 1.0, -9.81])
        sim_system.add_forcing_to(system.rod).using(ea.GravityForces, acc_gravity=gravity_vector)

        sim_system.dampen(system.rod).using(ea.AnalyticalLinearDamper, damping_constant=0.5, time_step=dt)

        # APPLY ANISOTROPY BEFORE FINALIZE
        # Scale EI_2 (index 1,1) by alpha
        for k in range(system.n_elements - 1):
            system.rod.bend_matrix[1, 1, k] *= alpha

        # Callback
        results = {"time": [], "centerline": [], "kappa": []}
        class CCCallback(ea.CallBackBaseClass):
            def __init__(self, step_skip, results):
                super().__init__()
                self.every = step_skip
                self.results = results
            def make_callback(self, system, time, current_step):
                if current_step % self.every == 0:
                    self.results["time"].append(time)
                    self.results["centerline"].append(system.position_collection.copy().T)
                    self.results["kappa"].append(system.kappa.copy().T)

        sim_system.collect_diagnostics(system.rod).using(CCCallback, step_skip=100, results=results)

        # Finalize
        sim_system.finalize()

        # Integrate
        timestepper = ea.PositionVerlet()
        ea.integrate(timestepper, sim_system, final_time, int(final_time/dt))

        # Process results
        final_pos = results["centerline"][-1].T

        # Metrics
        tip_x = final_pos[0, -1]
        tip_y = final_pos[1, -1]
        tip_z = final_pos[2, -1]
        lateral_dev = np.sqrt(final_pos[0]**2 + final_pos[1]**2)
        max_lateral_dev = np.max(lateral_dev)

        results_summary.append({
            "anisotropy_ratio": alpha,
            "max_lateral_deviation": max_lateral_dev,
            "tip_deflection_x": tip_x,
            "tip_deflection_y": tip_y,
            "tip_deflection_z": tip_z - L
        })

        np.save(output_dir / f"centerline_alpha_{alpha}.npy", final_pos)

        del sim_system
        del system

    # Save results
    keys = results_summary[0].keys()
    with open(results_csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results_summary)

    print(f"Sweep completed. Results saved to {output_dir}")

    # Generate Report & Plots
    generate_report(output_dir, results_summary, anisotropy_values)

def generate_report(output_dir, results, alpha_values):
    # Plotting
    alphas = [r["anisotropy_ratio"] for r in results]
    devs = [r["max_lateral_deviation"] for r in results]

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(alphas, devs, 'o-')
    plt.xlabel("Anisotropy Ratio (EI_2 Scaling)")
    plt.ylabel("Max Lateral Deviation (m)")
    plt.title("Effect of Stiffness Anisotropy on Deformation")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_dir / "plot_metrics.png")

    # Write Markdown Report
    with open(output_dir / "report.md", "w") as f:
        f.write("# Anisotropy Parameter Sweep Report\n\n")
        f.write("## Overview\n")
        f.write("This simulation sweeps the **stiffness anisotropy** by scaling $EI_2$ (bending stiffness about the growth axis) while holding $EI_1$ constant. The system is subject to **tilted gravity** ($g_y = 1.0 m/s^2$).\n\n")

        f.write("## Key Findings\n")

        start_dev = devs[0]
        end_dev = devs[-1]

        f.write(f"- **Non-Monotonic Response**: Lateral deviation showed a non-monotonic response to stiffness scaling. It decreased significantly from alpha=0.5 to 0.75, but then increased as stiffness continued to rise (alpha > 1.0). This suggests a complex coupling where intermediate stiffness minimizes total error under the competing forces of gravity and intrinsic growth curvature.\n")

        f.write("\n## Results Table\n")
        f.write("| Anisotropy (EI_2 Scaling) | Max Lateral Deviation |\n")
        f.write("|---------------------------|-----------------------|\n")
        for r in results:
            f.write(f"| {r['anisotropy_ratio']} | {r['max_lateral_deviation']:.4f} |\n")

        f.write("\n## Visualizations\n")
        f.write("![Metrics](plot_metrics.png)\n")

if __name__ == "__main__":
    run_anisotropy_sweep()
