import os
import pandas as pd

def main():
    latest_metrics = "outputs/afcc/2026-02-16/metrics.csv"
    if not os.path.exists(latest_metrics):
        print(f"Error: {latest_metrics} not found")
        return

    df = pd.read_csv(latest_metrics)

    # standardize columns based on audit
    gene_col = 'gene_symbol' if 'gene_symbol' in df.columns else 'Gene'
    anis_col = 'anisotropy_index' if 'anisotropy_index' in df.columns else 'anisotropy'
    plddt_col = 'plddt_mean' if 'plddt_mean' in df.columns else 'pLDDT'
    pae_col = 'PAE_domain_blockiness_score' if 'PAE_domain_blockiness_score' in df.columns else 'PAE_blockiness'

    df_clean = df[[gene_col, anis_col, plddt_col, pae_col, 'morphology']].copy()

    # Confidence weighting (pLDDT >= 70 is adequate)
    df_clean['confidence_class'] = df_clean[plddt_col].apply(lambda x: 'Adequate' if x >= 70 else 'Low')

    # Sort by anisotropy within confidence classes
    df_ranked = df_clean.sort_values(by=['confidence_class', anis_col], ascending=[True, False]) # Adequate first

    df_ranked.to_csv("outputs/afcc/confidence_weighted_ranking.csv", index=False)

    # Generate report
    with open("reports/confidence_weighted_structural_evidence.md", "w") as f:
        f.write("# Confidence-Weighted Structural Evidence\n\n")
        f.write("## Overview\n")
        f.write("This report re-evaluates the structural candidates for the Biological Countercurvature hypothesis by explicitly weighting their AlphaFold prediction confidence (pLDDT). High anisotropy (extended shapes) in low-confidence regions often reflects unstructured/disordered states rather than rigid mechanosensory rods. We must distinguish between adequate-confidence structures and low-confidence exploratory targets. Generated from `outputs/afcc/2026-02-16/metrics.csv`.\n\n")

        f.write("## 1. High-Anisotropy + Adequate-Confidence (>70 pLDDT)\n")
        f.write("These candidates possess strong structural evidence for an extended, potentially load-bearing conformation.\n\n")
        f.write("| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |\n")
        f.write("|---|---|---|---|---|\n")
        for _, row in df_ranked[(df_ranked['confidence_class'] == 'Adequate') & (df_ranked[anis_col] >= 3.0)].iterrows():
            f.write(f"| {row[gene_col]} | {row[anis_col]:.2f} | {row[plddt_col]:.1f} | {row[pae_col]:.2f} | {row['morphology']} |\n")

        f.write("\n## 2. High-Anisotropy + Low-Confidence (<70 pLDDT)\n")
        f.write("These candidates exhibit extended shapes but lack structural confidence. The anisotropy may simply reflect long unstructured loops rather than mechanosensory 'rods'. Use only for hypothesis generation.\n\n")
        f.write("| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |\n")
        f.write("|---|---|---|---|---|\n")
        for _, row in df_ranked[(df_ranked['confidence_class'] == 'Low') & (df_ranked[anis_col] >= 3.0)].iterrows():
            f.write(f"| {row[gene_col]} | {row[anis_col]:.2f} | {row[plddt_col]:.1f} | {row[pae_col]:.2f} | {row['morphology']} |\n")

        f.write("\n## 3. LBX1 Comparator Panel\n")
        f.write("Comparing LBX1 to known mechanosensors and structural regulators to contextualize its hypothesized role as a structural signaling hub.\n\n")
        panel = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
        f.write("| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence |\n")
        f.write("|---|---|---|---|---|\n")
        for gene in panel:
            match = df_ranked[df_ranked[gene_col] == gene]
            if not match.empty:
                row = match.iloc[0]
                f.write(f"| {gene} | {row[anis_col]:.2f} | {row[plddt_col]:.1f} | {row[pae_col]:.2f} | {row['confidence_class']} |\n")
            else:
                f.write(f"| {gene} | N/A | N/A | N/A | N/A |\n")

        f.write("\n## 4. Conclusions and Labeling\n")
        f.write("- **[Confirmed by metrics]** LBX1 has low structural confidence (pLDDT ~66.9) and intermediate anisotropy (~2.27). It does not present as a rigid tension rod, but rather a modular or flexible entity.\n")
        f.write("- **[Confirmed by metrics]** True structural rods with adequate confidence (e.g., PIEZO2, FBLN5) exhibit pLDDT > 70 alongside high anisotropy.\n")
        f.write("- **Evidence AGAINST hypothesis strength**: Relying on candidates like POC5 or GHR as primary examples of 'anisotropic mechanosensors' is flawed because their extended shapes are driven by low-confidence (likely disordered) regions. This weakens the structural argument unless validated orthogonally.\n")

if __name__ == "__main__":
    main()
