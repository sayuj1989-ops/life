import csv
import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Ensure scripts directory is in path to import experiment_minimal_elastica
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from experiment_minimal_elastica import run_experiment
from spinalmodes.utils.seeds import set_seed

def main():
    # Set seed for reproducibility
    seed = 42
    set_seed(seed)

    # Setup Date and Output Directory
    today = datetime.date.today().isoformat()
    out_dir = f"outputs/sim/{today}"
    os.makedirs(out_dir, exist_ok=True)

    csv_path = os.path.join(out_dir, "results.csv")
    params_path = os.path.join(out_dir, "params.csv")
    report_path = os.path.join(out_dir, "report.md")

    # Define Sweep Parameters
    # Anisotropy: 0.1 (Isotropic/Flat) to 10.0 (Highly Anisotropic/Tall)
    # Reduced set for speed
    anisotropies = [0.5, 1.0, 5.0, 10.0]

    # Growth Amplitude (chi_kappa): 0 (None) to 20 (Strong)
    # Reduced set for speed
    chi_kappas = [0.0, 10.0, 20.0]

    # Fixed parameters
    boundary_condition = "fixed"
    chi_taus = [0.0] # No torsion coupling for this 2D map

    # Save Parameters
    with open(params_path, 'w') as f:
        f.write("parameter,values\n")
        f.write(f"seed,{seed}\n")
        f.write(f"anisotropies,{anisotropies}\n")
        f.write(f"chi_kappas,{chi_kappas}\n")
        f.write(f"chi_taus,{chi_taus}\n")
        f.write(f"boundary_condition,{boundary_condition}\n")

    # Remove existing results if any to avoid duplicates
    if os.path.exists(csv_path):
        os.remove(csv_path)

    print(f"Starting 2D Sweep: Anisotropy vs Growth -> {out_dir}")
    print(f"Anisotropies: {anisotropies}")
    print(f"Growth (chi_kappa): {chi_kappas}")

    # Run Experiment
    run_experiment(
        out_file=csv_path,
        anisotropies=anisotropies,
        chi_kappas=chi_kappas,
        chi_taus=chi_taus,
        boundary_condition=boundary_condition,
        n_elements=30, # Reduced elements
        final_time=1.0 # Reduced time
    )

    # Analyze and Plot
    analyze_results(csv_path, out_dir, anisotropies, chi_kappas)

def analyze_results(csv_path, out_dir, anisotropies, chi_kappas):
    if not os.path.exists(csv_path):
        print("Error: No results file found.")
        return

    df = pd.read_csv(csv_path)

    # Pivot for Heatmaps
    # We want Anisotropy (X) vs Growth (Y) -> Color = Cobb Angle or S_lat

    try:
        pivot_cobb = df.pivot(index="chi_kappa", columns="stiffness_anisotropy", values="cobb_angle")
        pivot_slat = df.pivot(index="chi_kappa", columns="stiffness_anisotropy", values="s_lat")
    except Exception as e:
        print(f"Error creating pivot tables: {e}")
        return

    # Plot 1: Cobb Angle Heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(pivot_cobb, aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(label='Cobb Angle (deg)')
    plt.xticks(range(len(anisotropies)), anisotropies)
    plt.yticks(range(len(chi_kappas)), chi_kappas)
    plt.xlabel('Stiffness Anisotropy (R)')
    plt.ylabel('Growth Amplitude (chi_kappa)')
    plt.title('Cobb Angle Landscape: Anisotropy vs Growth')
    plt.savefig(os.path.join(out_dir, "plot_heatmap_cobb.png"))
    plt.close()

    # Plot 2: S_lat Heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(pivot_slat, aspect='auto', origin='lower', cmap='plasma')
    plt.colorbar(label='Lateral Deviation Index (S_lat)')
    plt.xticks(range(len(anisotropies)), anisotropies)
    plt.yticks(range(len(chi_kappas)), chi_kappas)
    plt.xlabel('Stiffness Anisotropy (R)')
    plt.ylabel('Growth Amplitude (chi_kappa)')
    plt.title('S-Shape Emergence (S_lat): Anisotropy vs Growth')
    plt.savefig(os.path.join(out_dir, "plot_heatmap_slat.png"))
    plt.close()

    # Generate Report
    generate_report(df, out_dir)

def generate_report(df, out_dir):
    report_path = os.path.join(out_dir, "report.md")

    max_cobb = df['cobb_angle'].max()
    max_slat = df['s_lat'].max()

    # Find parameters for max values
    row_max_cobb = df.loc[df['cobb_angle'].idxmax()]
    row_max_slat = df.loc[df['s_lat'].idxmax()]

    with open(report_path, 'w') as f:
        f.write(f"# Simulation Report: Anisotropy vs Growth 2D Sweep\n\n")
        f.write(f"**Date**: {datetime.date.today().isoformat()}\n\n")

        f.write("## Hypothesis\n")
        f.write("We investigate whether increasing Stiffness Anisotropy (e.g., Piezo2-mediated alignment) stabilizes or destabilizes "
                "the spine under increasing Growth loads. We specifically look for the emergence of S-shaped profiles (S_lat).\n\n")

        f.write("## Key Findings\n")
        f.write(f"- **Max Cobb Angle**: {max_cobb:.2f} deg (at R={row_max_cobb['stiffness_anisotropy']}, chi_kappa={row_max_cobb['chi_kappa']})\n")
        f.write(f"- **Max Lateral S-Index (S_lat)**: {max_slat:.4f} (at R={row_max_slat['stiffness_anisotropy']}, chi_kappa={row_max_slat['chi_kappa']})\n\n")

        f.write("## Visualizations\n")
        f.write("![Cobb Heatmap](plot_heatmap_cobb.png)\n")
        f.write("![S_lat Heatmap](plot_heatmap_slat.png)\n\n")

        f.write("## Interpretation\n")
        if max_slat > 0.1:
            f.write("Significant lateral buckling (S-shape) emerged. ")
            if row_max_slat['stiffness_anisotropy'] > 1.0:
                f.write("Interestingly, high anisotropy (R>1) seems to facilitate this mode under high growth.\n")
            else:
                f.write("Low anisotropy (R<=1) seems more susceptible to this instability.\n")
        else:
            f.write("No significant S-shape emerged (S_lat < 0.1). The system likely remained in a planar C-curve or stable state.\n")

        f.write("\n## Next Steps\n")
        f.write("- Consider adding Torsional Coupling (chi_tau) to this map to see if it breaks planar symmetry further.\n")

if __name__ == "__main__":
    main()
