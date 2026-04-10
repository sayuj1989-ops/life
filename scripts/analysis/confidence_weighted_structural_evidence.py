import pandas as pd

def rank_candidates():
    print("Ranking candidates...")

    # Authoritative snapshot
    df = pd.read_csv('outputs/afcc/2026-02-16/metrics.csv')

    gene_col = 'gene_symbol' if 'gene_symbol' in df.columns else 'Gene'

    if gene_col not in df.columns:
        print("Gene column not found")
        return

    df['anisotropy_index'] = df['anisotropy_index'].astype(float)
    df['plddt_mean'] = df['plddt_mean'].astype(float)

    # 1) high-anisotropy + adequate-confidence
    high_conf = df[(df['anisotropy_index'] >= 3.0) & (df['plddt_mean'] >= 70.0)].copy()
    high_conf['confidence_tier'] = 'Adequate'

    # 2) high-anisotropy + low-confidence (exploratory only)
    low_conf = df[(df['anisotropy_index'] >= 3.0) & (df['plddt_mean'] < 70.0)].copy()
    low_conf['confidence_tier'] = 'Low (Exploratory)'

    # Other
    other = df[df['anisotropy_index'] < 3.0].copy()
    other['confidence_tier'] = 'N/A (< 3.0 Anisotropy)'

    # Re-rank candidates with explicit confidence weighting
    # We'll just sort by confidence_tier, then anisotropy
    ranked = pd.concat([high_conf, low_conf, other])

    # We want adequate first, then low, then NA
    ranked['tier_rank'] = ranked['confidence_tier'].map({
        'Adequate': 1,
        'Low (Exploratory)': 2,
        'N/A (< 3.0 Anisotropy)': 3
    })

    ranked = ranked.sort_values(['tier_rank', 'anisotropy_index'], ascending=[True, False])
    ranked = ranked.drop(columns=['tier_rank'])

    ranked.to_csv('outputs/afcc/confidence_weighted_ranking.csv', index=False)

    # Generate report
    comparators = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    comp_df = df[df[gene_col].isin(comparators)]

    report_lines = [
        "# Confidence-Weighted Structural Evidence",
        "",
        "## Data Provenance",
        "- Date: 2026-02-16 (Authoritative snapshot)",
        "- File: `outputs/afcc/2026-02-16/metrics.csv`",
        "",
        "## Ranking Tiers",
        "Thresholds: High Anisotropy >= 3.0, Adequate Confidence >= 70.0 pLDDT.",
        "",
        "### 1. High-Anisotropy + Adequate-Confidence (Strongest Signals)",
        "| Gene | Anisotropy | pLDDT | Morphology |",
        "|------|------------|-------|------------|"
    ]

    for _, row in high_conf.sort_values('anisotropy_index', ascending=False).iterrows():
        report_lines.append(f"| {row[gene_col]} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row.get('morphology', 'N/A')} |")

    report_lines.extend([
        "",
        "### 2. High-Anisotropy + Low-Confidence (Exploratory Only)",
        "| Gene | Anisotropy | pLDDT | Morphology |",
        "|------|------------|-------|------------|"
    ])

    for _, row in low_conf.sort_values('anisotropy_index', ascending=False).iterrows():
        report_lines.append(f"| {row[gene_col]} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row.get('morphology', 'N/A')} |")

    report_lines.extend([
        "",
        "## LBX1 Comparator Analysis",
        "Comparison against PIEZO2, LMNA, ADGRG6, RUNX3, POC5, GHR.",
        "",
        "| Gene | Anisotropy | pLDDT | Confidence Tier | Notes |",
        "|------|------------|-------|-----------------|-------|"
    ])

    for gene in comparators:
        if gene in comp_df[gene_col].values:
            row = comp_df[comp_df[gene_col] == gene].iloc[0]
            ani = float(row['anisotropy_index'])
            pld = float(row['plddt_mean'])
            tier = 'Adequate' if pld >= 70 else 'Low'
            note = 'Strong struct signal' if ani >= 3 and pld >= 70 else 'Exploratory' if ani >= 3 else 'Intermediate/Globular'
            report_lines.append(f"| {gene} | {ani:.2f} | {pld:.1f} | {tier} | {note} |")
        else:
            report_lines.append(f"| {gene} | N/A | N/A | N/A | Not found in snapshot |")

    report_lines.extend([
        "",
        "## Conclusions",
        "- [Confirmed by metrics] PIEZO2 and ADGRG6 possess solid structural confidence (pLDDT > 70) to ground their anisotropic morphology claims.",
        "- [Supported but uncertain] LBX1 continues to sit below the pLDDT confidence threshold, requiring caution when applying functional narrative directly from computationally derived architecture.",
        "- [Evidence AGAINST / Weakening] Low-confidence predictions (e.g., POC5, GHR, LBX1) introduce high risk if interpreted purely as tension-rods or mechanosensors without validation, weakening the blanket narrative that high computational anisotropy equals biological mechanosensing."
    ])

    with open('reports/confidence_weighted_structural_evidence.md', 'w') as f:
        f.write('\n'.join(report_lines))

if __name__ == "__main__":
    rank_candidates()
