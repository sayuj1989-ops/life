import pandas as pd
import numpy as np
import scipy.stats as stats
import os

# Ensure output directory exists
os.makedirs('outputs/csv', exist_ok=True)

def main():
    # Attempt to load the dataset
    try:
        df = pd.read_csv('outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv')
    except FileNotFoundError:
        print("Dataset not found. Please run experiment_thermodynamic_cost_proteins.py first.")
        return

    # Check required columns
    required_cols = ['gene', 'term', 'anisotropy', 'plddt_mean', 'disorder_fraction']
    for col in required_cols:
        if col not in df.columns:
            print(f"Missing required column: {col}")
            return

    # Map categories based on text description in manuscript
    # Demand = eta_p and eta_a
    # Supply = Gamma_m
    df['Category'] = df['term'].apply(lambda x: 'Demand' if x in ['eta_p', 'eta_a'] else 'Supply')

    # Convert columns to numeric
    for col in ['anisotropy', 'plddt_mean', 'disorder_fraction']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['anisotropy', 'plddt_mean'])

    print("--- FULL DATASET (All proteins) ---")
    demand_full = df[df['Category'] == 'Demand']['anisotropy']
    supply_full = df[df['Category'] == 'Supply']['anisotropy']

    u_stat_full, p_val_full = stats.mannwhitneyu(demand_full, supply_full, alternative='two-sided')
    print(f"Demand (n={len(demand_full)}): mean={demand_full.mean():.2f}")
    print(f"Supply (n={len(supply_full)}): mean={supply_full.mean():.2f}")
    print(f"Mann-Whitney U: p = {p_val_full:.3e}")

    # Sensitivity Analysis: Exclude low confidence (pLDDT < 70)
    print("\n--- SENSITIVITY ANALYSIS (Excluding pLDDT < 70) ---")
    df_high = df[df['plddt_mean'] >= 70].copy()

    demand_high = df_high[df_high['Category'] == 'Demand']['anisotropy']
    supply_high = df_high[df_high['Category'] == 'Supply']['anisotropy']

    u_stat_high, p_val_high = stats.mannwhitneyu(demand_high, supply_high, alternative='two-sided')
    print(f"Demand High-Conf (n={len(demand_high)}): mean={demand_high.mean():.2f}")
    print(f"Supply High-Conf (n={len(supply_high)}): mean={supply_high.mean():.2f}")
    print(f"Mann-Whitney U: p = {p_val_high:.3e}")

    # Save the side-by-side results to CSV
    summary_data = [
        {"Analysis": "Full Dataset", "Group": "Demand", "N": len(demand_full), "Mean_Anisotropy": demand_full.mean()},
        {"Analysis": "Full Dataset", "Group": "Supply", "N": len(supply_full), "Mean_Anisotropy": supply_full.mean()},
        {"Analysis": "High Confidence Only", "Group": "Demand", "N": len(demand_high), "Mean_Anisotropy": demand_high.mean()},
        {"Analysis": "High Confidence Only", "Group": "Supply", "N": len(supply_high), "Mean_Anisotropy": supply_high.mean()},
    ]

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv('outputs/csv/sensitivity_analysis_summary.csv', index=False)
    print("\nSaved summary to outputs/csv/sensitivity_analysis_summary.csv")

if __name__ == "__main__":
    main()
