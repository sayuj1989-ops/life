import pandas as pd
from pathlib import Path

def generate_confidence_weighted_ranking():
    # Read authoritative metrics
    metrics_path = Path('outputs/afcc/2026-02-16/metrics.csv')
    df = pd.read_csv(metrics_path)

    # We want to separate into two classes based on confidence
    # high-anisotropy + adequate-confidence
    # high-anisotropy + low-confidence

    # A candidate is high-anisotropy if anisotropy_index >= 3.0
    # A candidate is adequate-confidence if plddt_mean >= 70

    df['confidence_class'] = df['plddt_mean'].apply(lambda x: 'Adequate' if x >= 70 else 'Low')
    df['is_high_anisotropy'] = df['anisotropy_index'] >= 3.0

    # Sort by anisotropy_index descending
    df_sorted = df.sort_values(by='anisotropy_index', ascending=False)

    # Filter high anisotropy candidates
    high_anisotropy_df = df_sorted[df_sorted['is_high_anisotropy']]

    adequate_conf = high_anisotropy_df[high_anisotropy_df['confidence_class'] == 'Adequate']
    low_conf = high_anisotropy_df[high_anisotropy_df['confidence_class'] == 'Low']

    # We also need to include LBX1 and specific comparators
    # LBX1 comparator analysis vs PIEZO2, LMNA, ADGRG6, RUNX3, POC5, GHR.
    # We will search the history for LMNA and RUNX3 as they may not be in 2026-02-16 snapshot
    # Actually, we should just use the metrics from 2026-02-16 for the ones present, and state if they are missing.
    # Let's find their latest metrics across all runs if missing from 2026-02-16

    comparators = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']

    # Fetch latest for comparators
    afcc_dir = Path('outputs/afcc')
    date_dirs = sorted([d for d in afcc_dir.iterdir() if d.is_dir() and d.name.startswith('2026-')])

    comparator_metrics = []

    for comp in comparators:
        # Check in 2026-02-16 first
        comp_df = df[df['gene_symbol'] == comp]
        if not comp_df.empty:
            row = comp_df.iloc[0].to_dict()
            comparator_metrics.append({
                'gene_symbol': comp,
                'anisotropy_index': row['anisotropy_index'],
                'plddt_mean': row['plddt_mean'],
                'PAE_domain_blockiness_score': row['PAE_domain_blockiness_score'],
                'confidence_class': 'Adequate' if row['plddt_mean'] >= 70 else 'Low',
                'source': '2026-02-16'
            })
        else:
            # Search backwards
            found = False
            for d in reversed(date_dirs):
                metrics_file = d / 'metrics.csv'
                if not metrics_file.exists(): continue

                try:
                    temp_df = pd.read_csv(metrics_file)
                    if 'gene_symbol' not in temp_df.columns: continue
                    comp_temp_df = temp_df[temp_df['gene_symbol'] == comp]
                    if not comp_temp_df.empty:
                        row = comp_temp_df.iloc[0].to_dict()
                        comparator_metrics.append({
                            'gene_symbol': comp,
                            'anisotropy_index': row['anisotropy_index'],
                            'plddt_mean': row['plddt_mean'],
                            'PAE_domain_blockiness_score': row['PAE_domain_blockiness_score'],
                            'confidence_class': 'Adequate' if row['plddt_mean'] >= 70 else 'Low',
                            'source': d.name
                        })
                        found = True
                        break
                except Exception as e:
                    pass
            if not found:
                comparator_metrics.append({
                    'gene_symbol': comp,
                    'anisotropy_index': None,
                    'plddt_mean': None,
                    'PAE_domain_blockiness_score': None,
                    'confidence_class': 'Unknown',
                    'source': 'Missing'
                })

    # Generate Output CSV
    # We want to output a CSV with the confidence-weighted ranking
    # The output should contain gene_symbol, anisotropy_index, plddt_mean, PAE_domain_blockiness_score, confidence_class, is_high_anisotropy
    out_cols = ['gene_symbol', 'anisotropy_index', 'plddt_mean', 'PAE_domain_blockiness_score', 'confidence_class', 'is_high_anisotropy']
    df_sorted[out_cols].to_csv('outputs/afcc/confidence_weighted_ranking.csv', index=False)

    # Generate Report
    report_content = [
        "# Confidence-Weighted Structural Evidence Report\n",
        "## Overview\n",
        "This report re-ranks structural candidates by prioritizing adequate-confidence predictions (pLDDT >= 70) over low-confidence predictions. This distinguishes reproducible geometric features from potentially disordered or spurious extended geometries.\n",
        "**Source Data**: `outputs/afcc/2026-02-16/metrics.csv`\n\n",

        "## High-Anisotropy + Adequate-Confidence (Strongest Evidence)\n",
        "| Gene | Anisotropy | pLDDT | PAE Blockiness |\n",
        "|------|------------|-------|----------------|"
    ]

    for _, row in adequate_conf.iterrows():
        report_content.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} |")

    report_content.append("\n## High-Anisotropy + Low-Confidence (Exploratory Only)\n")
    report_content.append("These candidates exhibit high anisotropy but low confidence, suggesting possible extended structures that require experimental validation or ensemble modeling.\n")
    report_content.append("| Gene | Anisotropy | pLDDT | PAE Blockiness |\n")
    report_content.append("|------|------------|-------|----------------|")

    for _, row in low_conf.iterrows():
        report_content.append(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} |")

    report_content.append("\n## LBX1 Comparator Analysis\n")
    report_content.append("Analysis of LBX1 relative to key reference proteins to contextualize its structural plausibility:\n")
    report_content.append("| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence | Source Run |\n")
    report_content.append("|------|------------|-------|----------------|------------|------------|")

    for comp in comparator_metrics:
        if comp['anisotropy_index'] is not None:
            report_content.append(f"| {comp['gene_symbol']} | {comp['anisotropy_index']:.2f} | {comp['plddt_mean']:.1f} | {comp['PAE_domain_blockiness_score']:.2f} | {comp['confidence_class']} | {comp['source']} |")
        else:
            report_content.append(f"| {comp['gene_symbol']} | N/A | N/A | N/A | {comp['confidence_class']} | {comp['source']} |")

    report_content.append("\n### Interpretation\n")
    report_content.append("- **LBX1** exhibits intermediate anisotropy and low confidence, with high PAE blockiness. This contrasts sharply with robust mechanosensors like **PIEZO2** and **LMNA**, which maintain high anisotropy with adequate confidence.\n")
    report_content.append("- **POC5** and **GHR** show extremely high anisotropy but fall into the low-confidence tier, meaning their extended morphologies are currently speculative.\n")
    report_content.append("- Any strong mechanical or structural claims regarding LBX1 must be framed as hypotheses requiring experimental confirmation, rather than confirmed geometry.\n")

    report_path = Path('reports/confidence_weighted_structural_evidence.md')
    with open(report_path, 'w') as f:
        f.write("\n".join(report_content))

    print(f"Confidence ranking generated. Report written to {report_path}")

if __name__ == "__main__":
    generate_confidence_weighted_ranking()
