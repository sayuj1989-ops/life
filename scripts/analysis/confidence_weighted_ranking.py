import pandas as pd
from pathlib import Path

def generate_confidence_weighted_ranking():
    metrics_file = Path('outputs/afcc/2026-02-16/metrics.csv')
    if not metrics_file.exists():
        print(f"Metrics file not found: {metrics_file}")
        return

    df = pd.read_csv(metrics_file)

    # Calculate a composite score: anisotropy * (pLDDT / 100)
    # We add a small penalty for high PAE blockiness for structurally uncertain regions
    # Replace NaN with 0 for PAE to avoid dropping rows without PAE
    df['PAE_domain_blockiness_score'] = df['PAE_domain_blockiness_score'].fillna(0)

    # Scale PAE blockiness: max observed is ~10, so we use a gentle penalty term: 1 / (1 + PAE/10)
    pae_penalty = 1.0 / (1.0 + df['PAE_domain_blockiness_score'] / 10.0)

    df['confidence_weighted_score'] = df['anisotropy_index'] * (df['plddt_mean'] / 100.0) * pae_penalty

    # Separate into high-anisotropy + adequate-confidence vs low-confidence
    high_anisotropy_mask = df['anisotropy_index'] >= 3.0
    adequate_confidence_mask = df['plddt_mean'] >= 70.0

    high_conf = df[high_anisotropy_mask & adequate_confidence_mask].copy()
    low_conf = df[high_anisotropy_mask & ~adequate_confidence_mask].copy()

    high_conf.sort_values('confidence_weighted_score', ascending=False, inplace=True)
    low_conf.sort_values('confidence_weighted_score', ascending=False, inplace=True)

    # Save to CSV
    output_csv = Path('outputs/afcc/confidence_weighted_ranking.csv')
    df.sort_values('confidence_weighted_score', ascending=False).to_csv(output_csv, index=False)

    # LBX1 Comparator Analysis
    comparators = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    comp_df = df[df['gene_symbol'].isin(comparators)].copy()

    # Generate Report
    report = [
        "# Confidence-Weighted Structural Evidence",
        "\nData snapshot: outputs/afcc/2026-02-16/metrics.csv",
        "\n## High-Anisotropy + Adequate-Confidence (pLDDT >= 70)",
        "| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Score |",
        "|------|------------|-------|----------------|----------------|"
    ]

    for _, row in high_conf.iterrows():
        pae = row.get('PAE_domain_blockiness_score', 0.0)
        report.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {pae:.2f} | {row['confidence_weighted_score']:.2f} |")

    report.extend([
        "\n## High-Anisotropy + Low-Confidence (Exploratory Only)",
        "| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Score |",
        "|------|------------|-------|----------------|----------------|"
    ])

    for _, row in low_conf.iterrows():
        pae = row.get('PAE_domain_blockiness_score', 0.0)
        report.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {pae:.2f} | {row['confidence_weighted_score']:.2f} |")

    report.extend([
        "\n## LBX1 Comparator Analysis",
        "Comparison of LBX1 against key anchors (PIEZO2, LMNA, ADGRG6) and low-confidence outliers (POC5, GHR).",
        "\n| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence |",
        "|------|------------|-------|----------------|------------|"
    ])

    for _, row in comp_df.iterrows():
        conf_level = "Adequate" if row['plddt_mean'] >= 70 else "Low"
        pae = row.get('PAE_domain_blockiness_score', 'N/A')
        if isinstance(pae, float):
            pae = f"{pae:.2f}"
        report.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {pae} | {conf_level} |")

    report.extend([
        "\n### Interpretation",
        "- **LBX1 Weakness**: LBX1 remains low confidence (pLDDT < 70) and is structurally intermediate. Its link to mechanosensing via pure geometry is weaker than PIEZO2 or ADGRG6.",
        "- **Strongest Geometries**: CNNM2, FBLN5, and PIEZO2 present the most robust evidence for extended structural mechanosensors based on current modeling."
    ])

    report_path = Path('reports/confidence_weighted_structural_evidence.md')
    with open(report_path, 'w') as f:
        f.write("\n".join(report))

    print(f"Generated {report_path} and {output_csv}")

if __name__ == "__main__":
    generate_confidence_weighted_ranking()
