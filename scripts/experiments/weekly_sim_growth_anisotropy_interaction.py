import csv
import os
import sys
from datetime import datetime

import matplotlib.pyplot as plt

# Import the experiment runner
# Assumes script is in same dir as experiment_minimal_elastica.py
sys.path.append(os.path.dirname(__file__))
from experiment_minimal_elastica import run_experiment  # noqa: E402


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = f"outputs/sim/{date_str}_growth_aniso_interaction"
    os.makedirs(out_dir, exist_ok=True)

    csv_path = os.path.join(out_dir, "results.csv")
    params_path = os.path.join(out_dir, "params.csv")

    # Define sweep (reduced combinations for faster runtime)
    anisotropies = [1.0, 3.0, 5.0]
    chi_kappas = [0.0, 10.0, 20.0]

    # Write params
    with open(params_path, 'w') as f:
        f.write("parameter,values\n")
        f.write(f"anisotropies,{anisotropies}\n")
        f.write(f"chi_kappas,{chi_kappas}\n")
        f.write("fixed_params,BC=fixed\n")

    # Run
    if os.path.exists(csv_path):
        os.remove(csv_path)

    print(f"Starting sweep: Anisotropy {anisotropies} "
          f"vs Growth {chi_kappas}...")
    run_experiment(
        out_file=csv_path,
        anisotropies=anisotropies,
        chi_kappas=chi_kappas,
        chi_taus=[0.0],
        chi_es=[0.0],
        chi_ms=[0.0],
        boundary_condition="fixed",
        n_elements=30,  # reduced elements
        final_time=1.0  # reduced duration
    )

    # Plotting
    plot_results(csv_path, out_dir)

    # Write Report
    write_report(out_dir, anisotropies, chi_kappas, csv_path, date_str)


def plot_results(csv_path, out_dir):
    data = {'anisotropy': [], 'cobb': [], 'max_curv': [], 's_lat': [], 'chi_kappa': []}

    if not os.path.exists(csv_path):
        print("Error: Results file not found.")
        return

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                data['anisotropy'].append(float(row['stiffness_anisotropy']))
                data['chi_kappa'].append(float(row['chi_kappa']))
                data['cobb'].append(float(row['cobb_angle']))
                data['max_curv'].append(float(row['max_curvature']))
                data['s_lat'].append(float(row['s_lat']))
            except ValueError:
                continue

    if not data['anisotropy']:
        print("No valid data found to plot.")
        return

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 3, 1)
    for c in set(data['chi_kappa']):
        idx = [i for i, x in enumerate(data['chi_kappa']) if x == c]
        x = [data['anisotropy'][i] for i in idx]
        y = [data['cobb'][i] for i in idx]
        plt.plot(x, y, 'o-', label=f"Growth={c}")
    plt.xlabel('Stiffness Anisotropy ratio')
    plt.ylabel('Cobb Angle (deg)')
    plt.title('Anisotropy vs Cobb Angle')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 3, 2)
    for c in set(data['chi_kappa']):
        idx = [i for i, x in enumerate(data['chi_kappa']) if x == c]
        x = [data['anisotropy'][i] for i in idx]
        y = [data['max_curv'][i] for i in idx]
        plt.plot(x, y, 's-', label=f"Growth={c}")
    plt.xlabel('Stiffness Anisotropy ratio')
    plt.ylabel('Max Curvature (1/m)')
    plt.title('Anisotropy vs Max Curvature')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 3, 3)
    for c in set(data['chi_kappa']):
        idx = [i for i, x in enumerate(data['chi_kappa']) if x == c]
        x = [data['anisotropy'][i] for i in idx]
        y = [data['s_lat'][i] for i in idx]
        plt.plot(x, y, '^-', label=f"Growth={c}")
    plt.xlabel('Stiffness Anisotropy ratio')
    plt.ylabel('S_lat (Deviation Index)')
    plt.title('Anisotropy vs Lateral Deviation')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plot_path = os.path.join(out_dir, "plot_interaction.png")
    plt.savefig(plot_path)
    print(f"Plots saved to {plot_path}")


def write_report(out_dir, anisotropies, chi_kappas, csv_path, date_str):
    report_path = os.path.join(out_dir, "report.md")

    cobb_vals = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cobb_vals.append(float(row['cobb_angle']))
            except ValueError:
                pass
    max_cobb = max(cobb_vals) if cobb_vals else 0

    with open(report_path, 'w') as f:
        f.write("# Simulation Report: Growth vs Anisotropy Interaction\n\n")
        f.write(f"**Date**: {date_str}\n\n")
        f.write("## Hypothesis\n")
        f.write("Testing how the emergence of S-shaped profiles interacts across varying stiffness anisotropy and growth gain parameters.\n\n")
        f.write("## Parameters\n")
        f.write(f"- **Anisotropy Sweep**: {anisotropies}\n")
        f.write(f"- **Growth Drive (chi_kappa)**: {chi_kappas}\n")
        f.write("- **Boundary Condition**: Fixed\n\n")
        f.write("## Results\n")
        f.write("See attached `plot_interaction.png`.\n\n")
        f.write("## Observations\n")
        f.write("- **What changed**: Swept anisotropy vs growth.\n")
        f.write(f"- **Emergent Shapes**: Maximum observed Cobb angle was {max_cobb:.2f} deg.\n")
        f.write("- **Relevance**: Informs how structural stiffness might compensate for high growth phases.\n\n")
        f.write("## Next Steps\n")
        f.write("- Look into torsional interactions under similar growth phases.\n")

if __name__ == "__main__":
    main()
