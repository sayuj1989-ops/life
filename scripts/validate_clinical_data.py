import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def main():
    print("Running Clinical Validation against published cohorts...")

    # Paths
    clinical_data_path = "data/clinical_cohort_targets.csv"
    simulation_data_path = "outputs/thermodynamic_cost/energy_deficit_window.csv"
    output_figure_path = "manuscript/figures/fig_clinical_validation.png"
    output_figure_pdf = "manuscript/figures/fig_clinical_validation.pdf"

    # Check inputs
    if not os.path.exists(clinical_data_path):
        print(f"Error: {clinical_data_path} not found.")
        sys.exit(1)

    if not os.path.exists(simulation_data_path):
        print(f"Error: {simulation_data_path} not found. Run experiment_energy_deficit_window.py first.")
        sys.exit(1)

    # Load Data
    try:
        df_clinical = pd.read_csv(clinical_data_path)
        df_sim = pd.read_csv(simulation_data_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    print(f"Loaded {len(df_clinical)} clinical points.")
    print(f"Loaded {len(df_sim)} simulation points.")

    # Transform Simulation Data: Map Length (L) to Age
    # Age = 10 + 40 * (L - 0.35)
    # L=0.35 -> Age 10
    # L=0.45 -> Age 14
    # L=0.55 -> Age 18
    df_sim['Simulated_Age'] = 10 + 40 * (df_sim['L'] - 0.35)

    # Plot
    plt.figure(figsize=(8, 6))

    # Plot Clinical Data (Scatter)
    # Filter by source for different markers/colors if needed, but for now just all points
    sources = df_clinical['source'].unique()
    markers = ['o', 's', '^', 'D']

    for i, source in enumerate(sources):
        subset = df_clinical[df_clinical['source'] == source]
        plt.scatter(subset['age'], subset['cobb_angle'],
                    label=f"Clinical: {source}",
                    marker=markers[i % len(markers)], alpha=0.7)

    # Plot Simulation Trajectory (Line)
    # Only plot for relevant age range (e.g., 10-18)
    mask = (df_sim['Simulated_Age'] >= 8) & (df_sim['Simulated_Age'] <= 20)
    plt.plot(df_sim.loc[mask, 'Simulated_Age'], df_sim.loc[mask, 'Cobb_angle'],
             'r-', linewidth=3, label='Model Prediction')

    # Formatting
    plt.xlabel('Age (Years)')
    plt.ylabel('Cobb Angle (Degrees)')
    plt.title('Clinical Validation: Model vs Published Cohorts')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Add metrics
    # Simple RMSE check on overlapping domains?
    # For now, just qualitative visual match is the goal of this step.

    # Save
    os.makedirs(os.path.dirname(output_figure_path), exist_ok=True)
    plt.savefig(output_figure_path, dpi=300, bbox_inches='tight')
    plt.savefig(output_figure_pdf, dpi=300, bbox_inches='tight')
    print(f"Saved validation figure to {output_figure_path}")
    print(f"Saved validation figure to {output_figure_pdf}")

if __name__ == "__main__":
    main()
