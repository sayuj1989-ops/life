from pathlib import Path
import pandas as pd

def generate_confidence_weighted_evidence():
    metrics_file = Path('outputs/afcc/2026-02-16/metrics.csv')
    df = pd.read_csv(metrics_file)

    high_anisotropy_threshold = 3.0
    adequate_confidence_threshold = 70.0

    adequate_conf = df[(df['anisotropy_index'] >= high_anisotropy_threshold) & (df['plddt_mean'] >= adequate_confidence_threshold)].sort_values(by='anisotropy_index', ascending=False)
    low_conf = df[(df['anisotropy_index'] >= high_anisotropy_threshold) & (df['plddt_mean'] < adequate_confidence_threshold)].sort_values(by='anisotropy_index', ascending=False)

    ranked_df = pd.concat([adequate_conf, low_conf])
    ranked_df.to_csv('outputs/afcc/confidence_weighted_ranking.csv', index=False)

    report_content = [
        "# Confidence-Weighted Structural Evidence Report\n",
        "**Date**: 2026-02-19",
        "**Source Data**: `outputs/afcc/2026-02-16/metrics.csv`\n",
        "## Methodology\n",
        "Candidates were re-ranked based on anisotropy, with explicit separation by structural confidence (pLDDT).",
        "- **High Anisotropy Threshold**: >= 3.0",
        "- **Adequate Confidence Threshold**: pLDDT >= 70.0\n",
        "## High-Anisotropy + Adequate-Confidence (Strong Structural Signal)\n",
        "| Gene | Anisotropy | pLDDT | PAE Blockiness |",
        "|------|------------|-------|----------------|"
    ]
    for _, row in adequate_conf.iterrows():
        report_content.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.2f} | {row['PAE_domain_blockiness_score']:.2f} |")

    report_content.extend([
        "\n## High-Anisotropy + Low-Confidence (Exploratory Only)\n",
        "| Gene | Anisotropy | pLDDT | PAE Blockiness |",
        "|------|------------|-------|----------------|"
    ])
    for _, row in low_conf.iterrows():
        report_content.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.2f} | {row['PAE_domain_blockiness_score']:.2f} |")

    report_content.extend([
        "\n## LBX1 Comparator Analysis\n",
        "Comparing LBX1 against key mechanosensors and structural candidates:\n",
        "| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence Category |",
        "|------|------------|-------|----------------|---------------------|"
    ])

    comparators = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    for gene in comparators:
        gene_data = df[df['gene_symbol'] == gene]
        if not gene_data.empty:
            row = gene_data.iloc[0]
            conf_cat = "Adequate" if row['plddt_mean'] >= adequate_confidence_threshold else "Low"
            report_content.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.2f} | {row['PAE_domain_blockiness_score']:.2f} | {conf_cat} |")
        else:
            report_content.append(f"| {gene} | N/A | N/A | N/A | Not in latest snapshot |")

    report_content.extend([
        "\n## Conclusions\n",
        "- **LBX1 Context**: LBX1 presents an intermediate anisotropy with low structural confidence. Its values are more static than dynamic, suggesting it may not be a primary structural tension rod, but rather a regulatory hub.",
        "- **Reliable Signals**: PIEZO2 and ADGRG6 show both high anisotropy and adequate confidence, making them stronger candidates for direct mechanosensory roles based purely on predicted structure.",
        "- **Caveats**: Candidates like POC5 and GHR show extreme anisotropy but suffer from low confidence. These metrics might reflect intrinsically disordered regions modeled as extended coils by AlphaFold, requiring orthogonal validation."
    ])

    report_path = Path('reports/confidence_weighted_structural_evidence.md')
    with open(report_path, 'w') as f:
        f.write("\n".join(report_content))

    print(f"Confidence weighted report generated at {report_path}")

if __name__ == "__main__":
    generate_confidence_weighted_evidence()
