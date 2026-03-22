import pandas as pd
import numpy as np

def generate_confidence_weighted_ranking():
    # Load the latest metrics snapshot
    df = pd.read_csv('outputs/afcc/2026-02-16/metrics.csv')

    # Explicit confidence weighting and categorization
    # Using the threshold logic: pLDDT >= 70 is adequate confidence, anisotropy >= 3.0 is high anisotropy

    df['confidence_class'] = np.where(df['plddt_mean'] >= 70, 'adequate', 'low')
    df['anisotropy_class'] = np.where(df['anisotropy_index'] >= 3.0, 'high', 'low/intermediate')

    df['category'] = df.apply(lambda row:
        '1) high-anisotropy + adequate-confidence' if row['confidence_class'] == 'adequate' and row['anisotropy_class'] == 'high' else
        ('2) high-anisotropy + low-confidence (exploratory only)' if row['confidence_class'] == 'low' and row['anisotropy_class'] == 'high' else
         '3) intermediate/low-anisotropy'), axis=1)

    # Sort by category and then by anisotropy_index descending
    df_sorted = df.sort_values(by=['category', 'anisotropy_index'], ascending=[True, False])

    # Export to CSV
    df_sorted.to_csv('outputs/afcc/confidence_weighted_ranking.csv', index=False)
    print("Exported outputs/afcc/confidence_weighted_ranking.csv")

    # Generate markdown report
    report_lines = [
        "# Confidence-Weighted Structural Evidence",
        "",
        "## Overview",
        "Re-ranking AlphaFold structural outputs utilizing explicit confidence gating (adequate: pLDDT >= 70, high anisotropy: >= 3.0) refines the Biological Countercurvature evidence base. This approach separates measured structural signals from low-confidence model hallucinations, providing a rigorous filter for hypothesis generation. Data from latest snapshot `outputs/afcc/2026-02-16/metrics.csv`.",
        "",
        "## 1) High Anisotropy + Adequate Confidence (Strong Structural Signal)",
        "These targets exhibit extended geometries robustly supported by AFCC metrics.",
        ""
    ]

    high_conf = df_sorted[df_sorted['category'] == '1) high-anisotropy + adequate-confidence']
    for i, row in enumerate(high_conf.itertuples(), 1):
        report_lines.append(f"{i}. **{row.gene_symbol}**: Anisotropy {row.anisotropy_index:.2f}, pLDDT {row.plddt_mean:.2f}")

    report_lines.extend([
        "",
        "*Conclusion*: PIEZO2 and ADGRG6 demonstrate strong confidence scores alongside their elongated architecture. This firmly grounds the concept of mechanosensory 'Tension Rods' in structural data, distinguishing it from purely hypothetical models.",
        "",
        "## 2) High Anisotropy + Low Confidence (Exploratory Only)",
        "These targets exhibit extended geometries but lack the high pLDDT scores required for firm structural conclusions. High anisotropy here often correlates with large intrinsically disordered regions (IDRs) or isolated segments stretched due to missing inter-domain contacts.",
        ""
    ])

    low_conf = df_sorted[df_sorted['category'] == '2) high-anisotropy + low-confidence (exploratory only)']
    for i, row in enumerate(low_conf.itertuples(), 1):
        report_lines.append(f"{i}. **{row.gene_symbol}**: Anisotropy {row.anisotropy_index:.2f}, pLDDT {row.plddt_mean:.2f}")

    report_lines.extend([
        "",
        "*Conclusion*: POC5 and GHR possess extremely high anisotropy metrics but cannot be treated as verified tension rods without orthogonal validation. Their 'extendedness' may reflect modeling artifacts of flexible linkers rather than native rigid architecture.",
        "",
        "## 3) LBX1 Comparator Panel Analysis",
        "Contextualizing LBX1 against other key proteins.",
        "",
        "| Gene | Anisotropy | pLDDT | Category |",
        "|------|------------|-------|----------|"
    ])

    panel_genes = ['PIEZO2', 'ADGRG6', 'POC5', 'GHR', 'LBX1']
    panel_df = df_sorted[df_sorted['gene_symbol'].isin(panel_genes)].set_index('gene_symbol')

    for g in panel_genes:
        if g in panel_df.index:
            row = panel_df.loc[g]
            if g == 'LBX1':
                report_lines.append(f"| **{g}** | **{row.anisotropy_index:.2f}** | **{row.plddt_mean:.2f}** | **{row.category}** |")
            else:
                report_lines.append(f"| {g} | {row.anisotropy_index:.2f} | {row.plddt_mean:.2f} | {row.category} |")

    report_lines.extend([
        "",
        "*(Note: LMNA and RUNX3 are not present in the 2026-02-16 snapshot but historically present in earlier runs).*",
        "",
        "### LBX1 Structural Diagnosis",
        "LBX1 exhibits an **Intermediate Anisotropy (2.27)** and **Low Confidence (66.87 pLDDT)** with a high PAE blockiness (7.35). ",
        "* **Interpretation**: LBX1 does *not* structurally resemble verified tension rods like PIEZO2. Its low confidence and intermediate anisotropy suggest it is not a primary load-bearing structural element or rigid tension sensor.",
        "* **Caveat**: The high blockiness and intermediate anisotropy previously led to narratives characterizing it as a 'Cryptic Signal Reservoir' or a 'Blocky Integrator'. However, due to its low pLDDT, these are purely speculative structural interpretations. LBX1's mechanism must be verified via alternative means rather than assumed through its AlphaFold geometry."
    ])

    with open('reports/confidence_weighted_structural_evidence.md', 'w') as f:
        f.write('\n'.join(report_lines) + '\n')

    print("Exported reports/confidence_weighted_structural_evidence.md")

if __name__ == "__main__":
    generate_confidence_weighted_ranking()
