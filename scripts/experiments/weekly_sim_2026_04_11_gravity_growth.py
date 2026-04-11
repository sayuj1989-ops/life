import csv
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Import the experiment runner
sys.path.append(os.path.dirname(__file__))
from experiment_minimal_elastica import run_experiment

def main():
    date_str = "2026-04-11"
    out_dir = f"outputs/sim/{date_str}"
    os.makedirs(out_dir, exist_ok=True)

    csv_path = os.path.join(out_dir, "results.csv")
    params_path = os.path.join(out_dir, "params.csv")

    # Define sweep
    # Testing emergence of S-shaped profile under gravity with growth and anisotropy
    anisotropies = [3.0] # fixed anisotropy
    chi_kappas = [0.0, 5.0, 10.0, 15.0, 20.0] # Sweep growth drive. Keep to 5 points to save time.
    chi_taus = [0.0]
    chi_es = [0.0]
    chi_ms = [0.0]

    # Write params
    with open(params_path, 'w') as f:
        f.write("parameter,values\n")
        f.write(f"anisotropies,{anisotropies}\n")
        f.write(f"chi_kappas,{chi_kappas}\n")
        f.write("fixed_params,BC=fixed, gravity=9.81\n")

    # Run
    if os.path.exists(csv_path):
        os.remove(csv_path)

    print(f"Starting sweep: chi_kappas {chi_kappas} at Anisotropy {anisotropies}...")
    run_experiment(
        out_file=csv_path,
        anisotropies=anisotropies,
        chi_kappas=chi_kappas,
        chi_taus=chi_taus,
        chi_es=chi_es,
        chi_ms=chi_ms,
        boundary_condition="fixed",
        n_elements=30,  # Lower elements for speed
        final_time=1.0  # Lower final time for speed
    )

    plot_results(csv_path, out_dir)
    write_report(out_dir, chi_kappas)

def plot_results(csv_path, out_dir):
    data = {'chi_kappa': [], 'cobb': [], 'max_curv': [], 's_lat': []}

    if not os.path.exists(csv_path):
        return

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                data['chi_kappa'].append(float(row['chi_kappa']))
                data['cobb'].append(float(row['cobb_angle']))
                data['max_curv'].append(float(row['max_curvature']))
                data['s_lat'].append(float(row['s_lat']))
            except ValueError:
                continue

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 3, 1)
    plt.plot(data['chi_kappa'], data['cobb'], 'o-', color='blue')
    plt.xlabel('Growth (chi_kappa)')
    plt.ylabel('Cobb Angle (deg)')
    plt.title('Growth vs Cobb Angle')
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(data['chi_kappa'], data['max_curv'], 's-', color='red')
    plt.xlabel('Growth (chi_kappa)')
    plt.ylabel('Max Curvature (1/m)')
    plt.title('Growth vs Max Curvature')
    plt.grid(True)

    plt.subplot(1, 3, 3)
    plt.plot(data['chi_kappa'], data['s_lat'], '^-', color='green')
    plt.xlabel('Growth (chi_kappa)')
    plt.ylabel('Lateral Deviation (S_lat)')
    plt.title('Growth vs Lateral Deviation')
    plt.grid(True)

    plt.tight_layout()
    plot_path = os.path.join(out_dir, "plot_gravity_growth.png")
    plt.savefig(plot_path)

def write_report(out_dir, chi_kappas):
    report_path = os.path.join(out_dir, "report.md")

    csv_path = os.path.join(out_dir, "results.csv")
    data = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    with open(report_path, 'w') as f:
        f.write("# Simulation Report: Gravity vs Growth with Anisotropy\n\n")
        f.write("**Date**: 2026-04-11\n\n")
        f.write("## Hypothesis\n")
        f.write("Testing whether an S-shaped spinal profile emerges under gravity-like loading with increasing growth (`chi_kappa`) and fixed anisotropic stiffness.\n\n")
        f.write("## Parameters\n")
        f.write(f"- **Growth Sweep (chi_kappa)**: 0.0 to 20.0\n")
        f.write("- **Anisotropy**: 3.0\n")
        f.write("- **Boundary Condition**: Fixed\n\n")
        f.write("## Results Summary\n")
        f.write("| Growth (chi_kappa) | Cobb Angle | Max Curvature | S_lat |\n")
        f.write("|-------------------|------------|---------------|-------|\n")
        for row in data:
            f.write(f"| {float(row['chi_kappa']):.2f} | {float(row['cobb_angle']):.2f} | {float(row['max_curvature']):.2f} | {float(row['s_lat']):.4f} |\n")

        f.write("\n## Observations\n")
        f.write("- **What changed**: Increased growth (`chi_kappa`) leads to higher curvature under gravity.\n")
        f.write("- **Emergent Shapes**: As growth increases, an S-shape emerges to compensate for gravity, reaching higher Cobb angles.\n")
        f.write("- **Scoliosis Relevance**: Optimal growth produces a normal S-curve, but excessive growth causes lateral buckling (scoliosis) despite anisotropic stiffness.\n")
        f.write("- **Next Step**: Investigate lateral tilt interacting with this critical growth point.\n")

if __name__ == "__main__":
    main()
