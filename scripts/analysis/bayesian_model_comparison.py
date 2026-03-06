import pandas as pd
import numpy as np

def compute_bic(rss, n, k):
    """Compute Bayesian Information Criterion (BIC)."""
    # Using the standard formulation for linear models: n * ln(RSS/n) + k * ln(n)
    return n * np.log(rss / n) + k * np.log(n)

def main():
    print("Running Bayesian Model Comparison (IEC vs Null Model)...")

    # We compare the cross-species allometric scaling
    # Model 1 (IEC): Bg = c * M^-0.25  (Theoretical metabolic scaling)
    # Model 2 (Null): Bg = constant (no scaling with mass)

    df = pd.read_csv('outputs/thermodynamic_cost/cross_species_scaling.csv')
    df = df.dropna(subset=['Bg', 'Mass_kg'])

    # 1. Null Model (Constant Bg)
    bg_mean = df['Bg'].mean()
    rss_null = np.sum((df['Bg'] - bg_mean)**2)
    k_null = 1 # 1 parameter: mean

    # 2. IEC Model (Power law: Bg = a * M^b)
    # We fit log(Bg) = log(a) + b*log(M)
    log_M = np.log(df['Mass_kg'])
    log_Bg = np.log(df['Bg'])
    p = np.polyfit(log_M, log_Bg, 1)

    # Predicted Bg under IEC
    bg_pred_iec = np.exp(p[1]) * df['Mass_kg']**p[0]
    rss_iec = np.sum((df['Bg'] - bg_pred_iec)**2)
    k_iec = 2 # 2 parameters: a, b

    n = len(df)

    bic_null = compute_bic(rss_null, n, k_null)
    bic_iec = compute_bic(rss_iec, n, k_iec)

    delta_bic = bic_null - bic_iec
    bayes_factor = np.exp(delta_bic / 2)

    print("\n--- Model Comparison Results ---")
    print(f"Sample Size (n): {n}")
    print(f"Null Model RSS: {rss_null:.6f}, BIC: {bic_null:.2f}")
    print(f"IEC Model RSS: {rss_iec:.6f}, BIC: {bic_iec:.2f}")
    print(f"Delta BIC (Null - IEC): {delta_bic:.2f}")
    print(f"Approximate Bayes Factor (K): {bayes_factor:.2f}")

    if delta_bic > 10:
        print("\nConclusion: Very strong evidence for the IEC (Allometric Scaling) model over the Null model.")
    elif delta_bic > 6:
        print("\nConclusion: Strong evidence for the IEC model over the Null model.")
    elif delta_bic > 2:
        print("\nConclusion: Positive evidence for the IEC model over the Null model.")
    else:
        print("\nConclusion: Weak or no evidence distinguishing the models.")

if __name__ == '__main__':
    main()
