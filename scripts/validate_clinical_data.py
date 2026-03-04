import os
import sys

import matplotlib.pyplot as plt
import pandas as pd


def main():
    print("Running Clinical Validation against published cohorts...")
    data_path = "data/clinical_cohort_targets.csv"
    output_dir = "manuscript/figures"
    output_path = os.path.join(output_dir, "fig_clinical_cohort_data.png")

    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        sys.exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    print(f"Loaded {len(df)} data points from {data_path}.")
    print("\nSample Data:")
    print(df.head())

    # Create Scatter Plot
    plt.figure(figsize=(10, 6))

    # Iterate through unique sources and plot each with a different label
    for source in df['source'].unique():
        subset = df[df['source'] == source]
        plt.scatter(subset['age'], subset['cobb_angle'], label=source, s=100, alpha=0.7)

    plt.xlabel("Age (years)")
    plt.ylabel("Cobb Angle (degrees)")
    plt.title("Clinical Cohort Data: Age vs Cobb Angle")
    plt.grid(True, alpha=0.3)
    plt.legend()

    try:
        plt.savefig(output_path, dpi=300)
        print(f"\nSuccessfully generated plot: {output_path}")
    except Exception as e:
        print(f"\nError saving plot: {e}")
        sys.exit(1)

    # Placeholder for validation logic (future work)
    print("Validation Status: PLOT GENERATED")
    print("TODO: Compare simulation trajectories against these clinical points.")

if __name__ == "__main__":
    main()
