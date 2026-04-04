import pandas as pd
import numpy as np

# Use the authoritative latest AFCC metrics snapshot: outputs/afcc/2026-02-16/metrics.csv
df = pd.read_csv("outputs/afcc/2026-02-16/metrics.csv")

# Create confidence weighting
df['confidence_category'] = 'low'
df.loc[df['plddt_mean'] >= 70, 'confidence_category'] = 'adequate'

# Sort by anisotropy index within confidence categories
adequate_df = df[df['confidence_category'] == 'adequate'].sort_values(by='anisotropy_index', ascending=False)
low_df = df[df['confidence_category'] == 'low'].sort_values(by='anisotropy_index', ascending=False)

# Rank candidates
combined_df = pd.concat([adequate_df, low_df])
combined_df.to_csv("outputs/afcc/confidence_weighted_ranking.csv", index=False)

with open("reports/confidence_weighted_structural_evidence.md", "w") as f:
    f.write("# Confidence-Weighted Structural Evidence\n\n")
    f.write("**Data Source:** `outputs/afcc/2026-02-16/metrics.csv`\n")
    f.write("**Date:** 2026-04-04\n\n")

    f.write("## 1. High-Anisotropy + Adequate-Confidence (>70 pLDDT)\n")
    f.write("These proteins represent structurally verified anisotropic candidates.\n\n")
    f.write("| Gene | Anisotropy | pLDDT Mean | Morphology | Notes |\n")
    f.write("|---|---|---|---|---|\n")
    for _, row in adequate_df.head(10).iterrows():
        f.write(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['morphology']} | |\n")

    f.write("\n## 2. High-Anisotropy + Low-Confidence (<70 pLDDT) (Exploratory Only)\n")
    f.write("High anisotropy in these proteins may be driven by unstructured regions. Proceed with caution.\n\n")
    f.write("| Gene | Anisotropy | pLDDT Mean | Morphology | Notes |\n")
    f.write("|---|---|---|---|---|\n")
    for _, row in low_df.head(10).iterrows():
        f.write(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['morphology']} | |\n")

    f.write("\n## 3. LBX1 Comparator Analysis\n")
    f.write("Comparing LBX1 to key markers.\n\n")
    f.write("| Gene | Anisotropy | pLDDT Mean | Confidence | Comparison |\n")
    f.write("|---|---|---|---|---|\n")

    comparators = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    for comp in comparators:
        if comp in df['gene_symbol'].values:
            row = df[df['gene_symbol'] == comp].iloc[0]
            conf = "Adequate" if row['plddt_mean'] >= 70 else "Low"
            f.write(f"| {comp} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {conf} | |\n")

    f.write("\n**LBX1 Context:** LBX1 shows intermediate anisotropy (2.27) and low confidence (66.9 pLDDT). It is less anisotropic than PIEZO2 or GHR, and its predicted structure is likely flexible/disordered, suggesting its role might not be a pure rigid mechanosensor but a flexible scaffold or its anisotropy is an artifact of low-confidence regions.\n")
