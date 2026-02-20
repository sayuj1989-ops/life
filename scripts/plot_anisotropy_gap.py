"""
plot_anisotropy_gap.py

Generates the 'Anisotropy Gap' figure for the Nature submission.
Compares the Thermodynamic Cost (Anisotropy x Residues) of Demand-side proteins
(Mechanosensors/Actuators) vs Supply-side proteins (Metabolic Regulators).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

CSV_PATH = "outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv"
OUTPUT_DIR = "outputs/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    df = pd.read_csv(CSV_PATH)

    # Filter out 'estimated' status if needed, but we keep them for completeness
    # Calculate Cost Metric
    # Cost ~ Anisotropy * Residues (scaled by 1e-3 for readability)
    df["thermodynamic_cost"] = df["anisotropy"] * df["n_residues"] / 1000.0

    # Group by Term:
    # Demand = eta_p (Proprioception) + eta_a (Active Moment)
    # Supply = Gamma_m (Metabolic Maintenance)

    term_map = {
        "eta_p": "Demand (Sensing)",
        "eta_a": "Demand (Structure)",
        "Gamma_m": "Supply (Metabolism)"
    }
    df["Category"] = df["term"].map(term_map)

    # Calculate mean cost per category
    category_means = df.groupby("Category")["thermodynamic_cost"].mean()
    print("Mean Thermodynamic Cost per Category:")
    print(category_means)

    # Plot
    plt.figure(figsize=(12, 8))

    # Custom palette
    palette = {
        "Demand (Sensing)": "#e74c3c",  # Red
        "Demand (Structure)": "#e67e22", # Orange
        "Supply (Metabolism)": "#2ecc71" # Green
    }

    # Bar plot with individual points
    sns.barplot(data=df, x="Category", y="thermodynamic_cost", palette=palette, alpha=0.6, errorbar=None)
    sns.swarmplot(data=df, x="Category", y="thermodynamic_cost", color="black", alpha=0.8, size=8)

    # Label top proteins
    # Find top 3 most expensive proteins
    top_proteins = df.nlargest(5, "thermodynamic_cost")

    for i, row in df.iterrows():
        if row["gene"] in top_proteins["gene"].values or row["gene"] in ["PPARGC1A", "VIM", "PIEZO2", "ADGRG6"]:
            plt.text(
                x=list(palette.keys()).index(row["Category"]),
                y=row["thermodynamic_cost"] + 0.2,
                s=row["gene"],
                ha='center', va='bottom', fontsize=9, fontweight='bold'
            )

    plt.ylabel("Thermodynamic Cost Index\n(Anisotropy × Residues × $10^{-3}$)", fontsize=12)
    plt.xlabel("", fontsize=12)
    plt.title("The Demand-Supply Anisotropy Gap", fontsize=16, fontweight='bold')

    # Add annotation for the gap
    demand_mean = df[df["Category"].str.contains("Demand")]["thermodynamic_cost"].mean()
    supply_mean = df[df["Category"].str.contains("Supply")]["thermodynamic_cost"].mean()
    gap_pct = (demand_mean - supply_mean) / supply_mean * 100

    plt.text(0.5, 8, f"Anisotropy Gap: +{gap_pct:.1f}%",
             fontsize=14, color="red", fontweight='bold',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='red'))

    plt.grid(axis='y', alpha=0.3)

    output_path = os.path.join(OUTPUT_DIR, "anisotropy_gap.png")
    plt.savefig(output_path, dpi=300)
    print(f"Saved figure to {output_path}")

if __name__ == "__main__":
    main()
