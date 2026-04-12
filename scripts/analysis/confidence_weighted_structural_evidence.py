import pandas as pd
import os
import numpy as np
from datetime import datetime

def run_analysis():
    # Load latest metrics
    source_file = 'outputs/afcc/2026-02-16/metrics.csv'
    run_date = '2026-02-16'
    df = pd.read_csv(source_file)

    # Check what columns we have
    aniso_col = 'anisotropy_index' if 'anisotropy_index' in df.columns else 'anisotropy'
    plddt_col = 'plddt_mean' if 'plddt_mean' in df.columns else 'mean_plddt'
    pae_block_col = 'PAE_domain_blockiness_score' if 'PAE_domain_blockiness_score' in df.columns else 'pae_blockiness'

    # PAE-aware weighting: pLDDT (local confidence) multiplied by a function of PAE blockiness
    pae_penalty = np.clip(1.0 - (df[pae_block_col] / 20.0), 0.5, 1.0) # Penalty caps at 50% for extreme blockiness

    df['confidence_weight'] = (df[plddt_col] / 100.0) * pae_penalty
    df['weighted_anisotropy'] = df[aniso_col] * df['confidence_weight']

    # Group into categories
    df['confidence_class'] = df[plddt_col].apply(lambda x: 'Adequate/High' if x >= 70 else 'Low')
    df['structural_signal'] = 'Weak'

    for idx, row in df.iterrows():
        if row[aniso_col] >= 3.0:
            if row['confidence_class'] == 'Adequate/High':
                df.at[idx, 'structural_signal'] = 'High-anisotropy + adequate-confidence'
            else:
                df.at[idx, 'structural_signal'] = 'High-anisotropy + low-confidence (exploratory)'

    # Sort and rank
    df = df.sort_values(by='weighted_anisotropy', ascending=False)

    # Save the ranking CSV
    os.makedirs('outputs/afcc', exist_ok=True)
    df.to_csv('outputs/afcc/confidence_weighted_ranking.csv', index=False)

    # Generate the report
    with open('reports/confidence_weighted_structural_evidence.md', 'w') as f:
        f.write("# Confidence-Weighted Structural Evidence Report\n\n")
        f.write(f"**Date Generated:** {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"**Source Data:** `{source_file}` (Snapshot from {run_date})\n\n")
        f.write("## Overview\n")
        f.write("This report re-ranks candidates with explicit confidence weighting based on AlphaFold's pLDDT scores and PAE domain blockiness. It isolates strong signals from low-confidence exploratory narrative, penalizing highly blocky structures where global shape is less certain.\n\n")

        f.write("## 1. High-Anisotropy + Adequate-Confidence (>70 pLDDT)\n")
        f.write("These proteins are structurally confident to have an elongated or extended shape.\n\n")

        high_conf = df[df['structural_signal'] == 'High-anisotropy + adequate-confidence']
        f.write("| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Anisotropy | Morphology |\n")
        f.write("|------|------------|-------|----------------|---------------------|------------|\n")
        for _, row in high_conf.iterrows():
            f.write(f"| {row['gene_symbol']} | {row[aniso_col]:.2f} | {row[plddt_col]:.1f} | {row[pae_block_col]:.2f} | {row['weighted_anisotropy']:.2f} | {row['morphology']} |\n")

        f.write("\n## 2. High-Anisotropy + Low-Confidence (Exploratory Only)\n")
        f.write("These proteins exhibit high calculated anisotropy but lack structural confidence. Their \"shape\" may be an artifact of predicted disordered regions. Avoid strong mechanistic claims here until orthogonally verified.\n\n")

        low_conf = df[df['structural_signal'] == 'High-anisotropy + low-confidence (exploratory)']
        f.write("| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Anisotropy | Morphology |\n")
        f.write("|------|------------|-------|----------------|---------------------|------------|\n")
        for _, row in low_conf.iterrows():
            f.write(f"| {row['gene_symbol']} | {row[aniso_col]:.2f} | {row[plddt_col]:.1f} | {row[pae_block_col]:.2f} | {row['weighted_anisotropy']:.2f} | {row['morphology']} |\n")

        f.write("\n## 3. LBX1 Comparator Panel\n")
        f.write("Comparison of LBX1 against key anchor genes to contextualize its structural signal.\n\n")

        panel_genes = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
        f.write("| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Anisotropy | Confidence Class | Signal Status |\n")
        f.write("|------|------------|-------|----------------|---------------------|------------------|---------------|\n")

        for gene in panel_genes:
            gene_data = df[df['gene_symbol'] == gene]
            if len(gene_data) > 0:
                row = gene_data.iloc[0]
                f.write(f"| {gene} | {row[aniso_col]:.2f} | {row[plddt_col]:.1f} | {row[pae_block_col]:.2f} | {row['weighted_anisotropy']:.2f} | {row['confidence_class']} | {row['structural_signal']} |\n")
            else:
                f.write(f"| {gene} | N/A | N/A | N/A | N/A | N/A | Not in latest snapshot |\n")

if __name__ == '__main__':
    run_analysis()
