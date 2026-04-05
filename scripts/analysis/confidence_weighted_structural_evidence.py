import pandas as pd
import os
import datetime

def main():
    metrics_file = "outputs/afcc/2026-02-16/metrics.csv"
    if not os.path.exists(metrics_file):
        print(f"Error: {metrics_file} not found.")
        return

    df = pd.read_csv(metrics_file)

    # Weight confidence based on plddt_mean and PAE blockiness
    df['confidence_class'] = df['plddt_mean'].apply(lambda x: 'Adequate' if x >= 70 else 'Low')

    # Separate groups
    high_aniso_adequate_conf = df[(df['anisotropy_index'] >= 3.0) & (df['confidence_class'] == 'Adequate')].copy()
    high_aniso_adequate_conf = high_aniso_adequate_conf.sort_values(by='anisotropy_index', ascending=False)

    high_aniso_low_conf = df[(df['anisotropy_index'] >= 3.0) & (df['confidence_class'] == 'Low')].copy()
    high_aniso_low_conf = high_aniso_low_conf.sort_values(by='anisotropy_index', ascending=False)

    # Comparator analysis
    target_genes = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    comparator_df = df[df['gene_symbol'].isin(target_genes)].copy()

    # Identify missing genes from the snapshot
    missing_genes = set(target_genes) - set(comparator_df['gene_symbol'])

    # Output to CSV
    os.makedirs("outputs/afcc", exist_ok=True)
    out_csv = "outputs/afcc/confidence_weighted_ranking.csv"

    df_sorted = df.sort_values(by=['confidence_class', 'anisotropy_index'], ascending=[True, False])
    df_sorted.to_csv(out_csv, index=False)

    # Output to Report
    report_lines = [
        "# Confidence-Weighted Structural Evidence",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Data Source: `{metrics_file}`",
        "",
        "## Overview",
        "This report re-ranks candidates with explicit confidence weighting based on pLDDT scores.",
        "Thresholds used: High Anisotropy >= 3.0, Adequate Confidence (pLDDT >= 70).",
        "",
        "## 1. High-Anisotropy + Adequate-Confidence (Strong Evidence)",
        "| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |",
        "|---|---|---|---|---|"
    ]
    for _, row in high_aniso_adequate_conf.iterrows():
        report_lines.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} | {row['morphology']} |")

    report_lines.extend([
        "",
        "## 2. High-Anisotropy + Low-Confidence (Exploratory Only)",
        "| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |",
        "|---|---|---|---|---|"
    ])
    for _, row in high_aniso_low_conf.iterrows():
        report_lines.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} | {row['morphology']} |")

    report_lines.extend([
        "",
        "## 3. LBX1 Comparator Analysis",
        "Comparing LBX1 to key structural anchors and outliers:",
        "| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence |",
        "|---|---|---|---|---|"
    ])

    for _, row in comparator_df.iterrows():
        report_lines.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} | {row['confidence_class']} |")

    for gene in missing_genes:
        report_lines.append(f"| {gene} | N/A | N/A | N/A | N/A (Missing from snapshot) |")

    os.makedirs("reports", exist_ok=True)
    with open("reports/confidence_weighted_structural_evidence.md", "w") as f:
        f.write("\n".join(report_lines))

if __name__ == "__main__":
    main()
