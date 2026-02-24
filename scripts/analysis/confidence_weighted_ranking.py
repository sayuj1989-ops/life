#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os

INPUT_FILE = "outputs/afcc/current_metrics.csv"
OUTPUT_FILE = "outputs/afcc/confidence_weighted_ranking.csv"

def normalize_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return df[c]
    return None

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    print(f"Reading metrics from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)

    # Normalize columns
    # We need: Identity (or gene_symbol), Anisotropy, pLDDT_mean, PAE_mean

    # Identity
    if 'Identity' in df.columns:
        df['Gene'] = df['Identity'].apply(lambda x: str(x).split()[0] if "(" in str(x) else str(x))
    elif 'gene_symbol' in df.columns:
        df['Gene'] = df['gene_symbol']
    else:
        print("Error: Could not find Identity/gene_symbol column.")
        return

    # Anisotropy
    aniso_col = normalize_col(df, ['Anisotropy', 'anisotropy_index'])
    if aniso_col is None:
        print("Error: Could not find Anisotropy column.")
        return
    df['Anisotropy_Val'] = pd.to_numeric(aniso_col, errors='coerce')

    # pLDDT (0-100, higher is better)
    plddt_col = normalize_col(df, ['pLDDT_mean', 'plddt_mean', 'mean_plddt'])
    if plddt_col is None:
        print("Error: Could not find pLDDT column.")
        return
    df['pLDDT_Val'] = pd.to_numeric(plddt_col, errors='coerce')

    # PAE (0-31, lower is better)
    pae_col = normalize_col(df, ['PAE_mean', 'pae_mean'])
    if pae_col is None:
        print("Warning: PAE column not found. Assuming PAE=0 (perfect) for ranking if missing? No, that's dangerous. Let's try to infer or skip.")
        # If PAE is missing, we can't fully compute the score as defined.
        # Let's see if we can use pLDDT as a proxy for PAE if PAE is missing (high pLDDT usually implies low PAE).
        # But strictly, let's mark as NaN.
        df['PAE_Val'] = np.nan
    else:
        df['PAE_Val'] = pd.to_numeric(pae_col, errors='coerce')

    # Calculate Confidence Score
    # Score = Anisotropy * (pLDDT/100) * (1 - PAE/31)
    # If PAE is missing, we might need a fallback.
    # Let's assume a default PAE if missing, but flag it? Or just drop?
    # Given the prompt emphasizes "confidence-weighted", missing PAE is a huge confidence hit.
    # Let's fill PAE with a conservative high value (e.g. 15 or 31) if missing?
    # Or just calc where possible.

    def calc_score(row):
        try:
            aniso = float(row['Anisotropy_Val'])
            plddt = float(row['pLDDT_Val'])
            pae = float(row['PAE_Val'])

            if np.isnan(aniso) or np.isnan(plddt):
                return 0.0

            if np.isnan(pae):
                # Fallback if PAE missing: heavily penalize or rely solely on pLDDT?
                # Let's penalize by assuming PAE is "average bad" (~15) or worse.
                # Actually, let's look at the data. Most have PAE.
                # If missing, let's use a proxy based on pLDDT: (100-pLDDT)/3 roughly?
                # Better: Treat missing PAE as 31 (worst case).
                pae = 31.0

            # Clamp PAE to 0-31 just in case
            pae = max(0, min(31, pae))

            # Confidence Factor 1: pLDDT (0-1)
            c1 = max(0, min(100, plddt)) / 100.0

            # Confidence Factor 2: PAE (1-0)
            c2 = 1.0 - (pae / 31.0)
            c2 = max(0, min(1, c2))

            return aniso * c1 * c2
        except:
            return 0.0

    df['Confidence_Score'] = df.apply(calc_score, axis=1)

    # Sort
    df_ranked = df.sort_values('Confidence_Score', ascending=False).reset_index(drop=True)
    df_ranked['Rank'] = df_ranked.index + 1

    # Select columns for output
    out_cols = ['Rank', 'Gene', 'Confidence_Score', 'Anisotropy_Val', 'pLDDT_Val', 'PAE_Val']
    # Add flags if available
    flag_col = normalize_col(df, ['Flags', 'flags', 'low_confidence_warning'])
    if flag_col is not None:
        df_ranked['Flags'] = flag_col
        out_cols.append('Flags')

    # Save
    print(f"Saving ranked list to {OUTPUT_FILE}...")
    df_ranked[out_cols].to_csv(OUTPUT_FILE, index=False)

    # Comparator Analysis
    targets = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    print("\n--- Comparator Analysis (LBX1 vs Targets) ---")

    comparators = df_ranked[df_ranked['Gene'].isin(targets)].copy()
    # Sort comparators by rank
    comparators = comparators.sort_values('Rank')

    print(f"{'Gene':<10} | {'Rank':<5} | {'Score':<6} | {'Aniso':<6} | {'pLDDT':<6} | {'PAE':<6}")
    print("-" * 60)
    for _, row in comparators.iterrows():
        print(f"{row['Gene']:<10} | {row['Rank']:<5} | {row['Confidence_Score']:.3f}  | {row['Anisotropy_Val']:.2f}   | {row['pLDDT_Val']:.1f}   | {row['PAE_Val']:.1f}")

    # LBX1 Analysis
    lbx1_row = df_ranked[df_ranked['Gene'] == 'LBX1']
    if not lbx1_row.empty:
        lbx1_rank = lbx1_row.iloc[0]['Rank']
        lbx1_score = lbx1_row.iloc[0]['Confidence_Score']
        total = len(df_ranked)
        print(f"\nLBX1 is ranked #{lbx1_rank} out of {total} candidates.")

        # Who is above?
        better = df_ranked[df_ranked['Rank'] < lbx1_rank]
        print(f"Candidates with stronger confidence-weighted evidence than LBX1: {len(better)}")
    else:
        print("\nLBX1 not found in metrics!")

if __name__ == "__main__":
    main()
