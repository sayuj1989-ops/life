import csv
import os
import sys

import matplotlib.pyplot as plt

# Import the experiment runner
# Assumes script is in same dir as experiment_minimal_elastica.py
sys.path.append(os.path.dirname(__file__))
from experiment_minimal_elastica import run_experiment  # noqa: E402


def main():
    # Fixed date for this experiment cycle
    date_str = "2026-10-30"
    out_dir = f"outputs/sim/{date_str}"
    os.makedirs(out_dir, exist_ok=True)

    csv_path = os.path.join(out_dir, "results.csv")
    params_path = os.path.join(out_dir, "params.csv")

    # Define sweep
    # Testing "Growth Stability": Can high anisotropy (R=5.0) suppress
    # buckling across a full range of growth gains?
    anisotropies = [5.0]
    # chi_kappas = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
    chi_kappas = [5.0, 10.0, 15.0, 20.0]

    # Write params
    with open(params_path, "w") as f:
        f.write("parameter,values\n")
        f.write(f"anisotropies,{anisotropies}\n")
        f.write(f"chi_kappas,{chi_kappas}\n")
        f.write("fixed_params,BC=fixed, chi_tau=0.0\n")

    # Run
    # if os.path.exists(csv_path):
    #     os.remove(csv_path)

    print(f"Starting sweep: Growth {chi_kappas} at Anisotropy {anisotropies}...")
    run_experiment(
        out_file=csv_path,
        anisotropies=anisotropies,
        chi_kappas=chi_kappas,
        chi_taus=[0.0],
        boundary_condition="fixed",
        n_elements=30,
        final_time=1.0,
    )

    # Plotting
    plot_results(csv_path, out_dir)

    # Write Report Skeleton
    write_report_skeleton(out_dir, anisotropies, chi_kappas)


def plot_results(csv_path, out_dir):
    data = {"chi_kappa": [], "cobb": [], "max_curv": [], "s_lat": []}

    if not os.path.exists(csv_path):
        print("Error: Results file not found.")
        return

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                data["chi_kappa"].append(float(row["chi_kappa"]))
                data["cobb"].append(float(row["cobb_angle"]))
                data["max_curv"].append(float(row["max_curvature"]))
                data["s_lat"].append(float(row["s_lat"]))
            except ValueError:
                continue

    if not data["chi_kappa"]:
        print("No valid data found to plot.")
        return

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 3, 1)
    plt.plot(data["chi_kappa"], data["cobb"], "o-", color="blue")
    plt.xlabel("Growth Gain (chi_kappa)")
    plt.ylabel("Cobb Angle (deg)")
    plt.title("Growth vs Cobb Angle")
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(data["chi_kappa"], data["max_curv"], "s-", color="red")
    plt.xlabel("Growth Gain (chi_kappa)")
    plt.ylabel("Max Curvature (1/m)")
    plt.title("Growth vs Max Curvature")
    plt.grid(True)

    plt.subplot(1, 3, 3)
    plt.plot(data["chi_kappa"], data["s_lat"], "^-", color="green")
    plt.xlabel("Growth Gain (chi_kappa)")
    plt.ylabel("S_lat (Deviation Index)")
    plt.title("Growth vs Lateral Deviation")
    plt.grid(True)

    plt.tight_layout()
    plot_path = os.path.join(out_dir, "plot_growth_stability.png")
    plt.savefig(plot_path)
    print(f"Plots saved to {plot_path}")


def write_report_skeleton(out_dir, anisotropies, chi_kappas):
    report_path = os.path.join(out_dir, "report.md")
    if os.path.exists(report_path):
        print("Report already exists, skipping skeleton generation.")
        return

    with open(report_path, "w") as f:
        f.write("# Simulation Report: Growth Stability Sweep\n\n")
        f.write(f"**Date**: {os.path.basename(out_dir)}\n\n")
        f.write("## Hypothesis\n")
        f.write(
            "Testing the limits of 'Vector Chain' stability: "
            "At what growth gain (chi_kappa) does a highly anisotropic "
            "spine (R=5.0) buckle into an S-shape?\n\n"
        )
        f.write("## Parameters\n")
        f.write(f"- **Anisotropy**: {anisotropies}\n")
        f.write(f"- **Growth Gain (chi_kappa)**: {chi_kappas}\n")
        f.write("- **Boundary Condition**: Fixed\n\n")
        f.write("## Results\n")
        f.write("See attached `plot_growth_stability.png`.\n\n")
        f.write("### Quantitative Summary\n")
        f.write("| Chi_Kappa | Cobb Angle | Max Curvature | S_lat |\n")
        f.write("|-----------|------------|---------------|-------|\n")
        f.write("<!-- To be filled -->\n\n")
        f.write("## Observations\n")
        f.write("- [Observation 1]\n")
        f.write("- [Observation 2]\n\n")
        f.write("## Next Steps\n")
        f.write("- [Suggestion]\n")


if __name__ == "__main__":
    main()
