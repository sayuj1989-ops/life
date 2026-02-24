import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from pathlib import Path

def run_experiment():
    print("Running experiment_energy_deficit_window.py to ensure fresh data...")
    subprocess.run(["python3", "scripts/experiment_energy_deficit_window.py"], check=True)

def plot_clinical_validation():
    print("Plotting Clinical Validation Figure...")

    # Load Clinical Data
    clinical_path = Path("data/clinical_cohort_targets.csv")
    if not clinical_path.exists():
        print(f"Error: {clinical_path} not found.")
        return

    clinical_df = pd.read_csv(clinical_path)

    # Load Simulation Data
    sim_path = Path("outputs/thermodynamic_cost/energy_deficit_window.csv")
    if not sim_path.exists():
        print(f"Error: {sim_path} not found. Did the experiment run?")
        return

    sim_df = pd.read_csv(sim_path)

    # Map Simulation Length L to Approximate Age
    # Assumption: Growth spurt from L=0.35m (Age 10) to L=0.45m (Age 14)
    # Age = 10 + (L - 0.35) / (0.45 - 0.35) * 4
    # Age = 10 + (L - 0.35) * 40

    sim_df['Approx_Age'] = 10 + (sim_df['L'] - 0.35) * 40

    # Filter valid age range for plot (e.g., 10-16)
    plot_df = sim_df[(sim_df['Approx_Age'] >= 9) & (sim_df['Approx_Age'] <= 16)]

    plt.figure(figsize=(10, 6))

    # Plot Simulation Curve
    plt.plot(plot_df['Approx_Age'], plot_df['Cobb_angle'], 'r-', linewidth=2, label='IEC Model Prediction (Energy Deficit)')

    # Plot Clinical Data Points
    # Group by source to have separate markers
    sources = clinical_df['source'].unique()
    markers = {'Weinstein_1983': 'o', 'Lonstein_1984': 's'}
    colors = {'Weinstein_1983': 'blue', 'Lonstein_1984': 'green'}

    for source in sources:
        subset = clinical_df[clinical_df['source'] == source]
        plt.scatter(subset['age'], subset['cobb_angle'],
                    label=f'Clinical: {source}',
                    marker=markers.get(source, 'o'),
                    color=colors.get(source, 'black'),
                    s=60, alpha=0.8, zorder=5)

    plt.xlabel('Age (Years) [Mapped from Spinal Length L]')
    plt.ylabel('Cobb Angle (Degrees)')
    plt.title('Clinical Validation: Predicted vs Observed Scoliosis Progression')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Add Critical Threshold Annotation
    # L_crit approx 0.35m -> Age 10
    plt.axvline(x=10, color='gray', linestyle='--', alpha=0.5, label='Onset of Growth Spurt')

    output_path = Path("manuscript/figures/fig_clinical_validation.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    print(f"Saved figure to {output_path}")

if __name__ == "__main__":
    run_experiment()
    plot_clinical_validation()
