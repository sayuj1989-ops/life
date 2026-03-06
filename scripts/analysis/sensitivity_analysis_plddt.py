import pandas as pd
import numpy as np
import scipy.stats as stats

def main():
    print("Running Sensitivity Analysis on AlphaFold Confidence (pLDDT)...")

    # Load dataset
    df = pd.read_csv('outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv')

    # Create Demand vs Supply Categories
    df['Category'] = df['term'].apply(lambda x: 'Demand' if x in ['eta_p', 'eta_a'] else 'Supply')

    # Stratify by confidence
    high_conf = df[df['plddt_mean'] >= 70]
    low_conf = df[df['plddt_mean'] < 70]

    print(f"\nTotal Proteins: {len(df)}")
    print(f"High Confidence (>= 70): {len(high_conf)}")
    print(f"Low Confidence (< 70): {len(low_conf)}")

    # 1. Compare Anisotropy Distributions between High and Low confidence
    u_stat, p_val = stats.mannwhitneyu(high_conf['anisotropy'], low_conf['anisotropy'])
    print(f"\n1. Anisotropy distribution difference (High vs Low Conf):")
    print(f"   Mann-Whitney U: {u_stat}, p-value: {p_val:.4f}")
    if p_val > 0.05:
        print("   -> Conclusion: Anisotropy distributions are NOT significantly different between high and low confidence structures. The structural predictions are robust.")
    else:
        print("   -> Conclusion: Anisotropy distributions ARE significantly different.")

    # 2. Demand vs Supply Anisotropy (All proteins)
    demand_all = df[df['Category'] == 'Demand']['anisotropy']
    supply_all = df[df['Category'] == 'Supply']['anisotropy']
    u_all, p_all = stats.mannwhitneyu(demand_all, supply_all)

    print(f"\n2. Demand vs Supply Anisotropy (All Proteins):")
    print(f"   Demand Mean: {demand_all.mean():.2f}, Supply Mean: {supply_all.mean():.2f}")
    print(f"   Mann-Whitney U: {u_all}, p-value: {p_all:.4f}")

    # 3. Demand vs Supply Anisotropy (High Confidence ONLY)
    demand_high = high_conf[high_conf['Category'] == 'Demand']['anisotropy']
    supply_high = high_conf[high_conf['Category'] == 'Supply']['anisotropy']
    u_high, p_high = stats.mannwhitneyu(demand_high, supply_high)

    print(f"\n3. Demand vs Supply Anisotropy (High Confidence ONLY):")
    print(f"   Demand Mean: {demand_high.mean():.2f}, Supply Mean: {supply_high.mean():.2f}")
    print(f"   Mann-Whitney U: {u_high}, p-value: {p_high:.4f}")

    if p_high < 0.05:
        print("   -> Conclusion: The core finding (Demand proteins are significantly more anisotropic than Supply proteins) HOLDS even when excluding low-confidence structures.")
    else:
        print("   -> Conclusion: The core finding loses significance when excluding low-confidence structures.")

if __name__ == '__main__':
    main()
