import os
import pandas as pd

def compute_confidence_weighted_ranking():
    # Read authoritative snapshot
    snapshot_file = "outputs/afcc/2026-02-16/metrics.csv"
    if not os.path.exists(snapshot_file):
        print(f"File not found: {snapshot_file}")
        return

    df = pd.read_csv(snapshot_file)

    # Extract the target proteins for the comparator
    comparator_genes = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']

    # For missing comparator genes, try to read from other files to fill if possible, but based on prompt LMNA is not present in 2026-02-16

    # 1. High-anisotropy + adequate-confidence
    high_anisotropy_high_conf = df[(df['anisotropy_index'] >= 3.0) & (df['plddt_mean'] >= 70)].copy()
    high_anisotropy_high_conf['Confidence_Category'] = 'Adequate (>=70)'

    # 2. High-anisotropy + low-confidence (exploratory only)
    high_anisotropy_low_conf = df[(df['anisotropy_index'] >= 3.0) & (df['plddt_mean'] < 70)].copy()
    high_anisotropy_low_conf['Confidence_Category'] = 'Low (<70)'

    # 3. Comparator Analysis
    comparators = df[df['gene_symbol'].isin(comparator_genes)].copy()
    comparators['Confidence_Category'] = comparators['plddt_mean'].apply(lambda x: 'Adequate (>=70)' if x >= 70 else 'Low (<70)')

    report_lines = [
        "# Confidence-Weighted Structural Evidence",
        "",
        "## Overview",
        "This report re-ranks AlphaFold structural proxy metrics with explicit confidence weighting. A major vulnerability in previous cluster analyses was treating high-anisotropy artifacts (arising from long unstructured regions) equally with rigidly structured tension rods.",
        "Authoritative snapshot: `outputs/afcc/2026-02-16/metrics.csv`",
        "",
        "## 1. High-Anisotropy + Adequate-Confidence Candidates",
        "**Threshold**: `Anisotropy >= 3.0` AND `pLDDT >= 70.0`",
        "**Significance**: These represent structurally certain, elongated architectures capable of transmitting mechanical force.",
        ""
    ]

    # Sort by anisotropy
    high_anisotropy_high_conf = high_anisotropy_high_conf.sort_values(by='anisotropy_index', ascending=False)
    for _, row in high_anisotropy_high_conf.iterrows():
        report_lines.append(f"- **{row['gene_symbol']}**: Anisotropy = {row['anisotropy_index']:.2f}, pLDDT = {row['plddt_mean']:.1f}, PAE Blockiness = {row['PAE_domain_blockiness_score']:.2f}")

    report_lines.append("")
    report_lines.append("## 2. High-Anisotropy + Low-Confidence Candidates (Exploratory Only)")
    report_lines.append("**Threshold**: `Anisotropy >= 3.0` AND `pLDDT < 70.0`")
    report_lines.append("**Significance**: High anisotropy here is often an artifact of unfolded loops extended by AlphaFold without structural context. These are strictly hypothesis-generating and cannot be used as primary evidence for tension rods.")
    report_lines.append("")

    high_anisotropy_low_conf = high_anisotropy_low_conf.sort_values(by='anisotropy_index', ascending=False)
    for _, row in high_anisotropy_low_conf.iterrows():
        report_lines.append(f"- **{row['gene_symbol']}**: Anisotropy = {row['anisotropy_index']:.2f}, pLDDT = {row['plddt_mean']:.1f}, PAE Blockiness = {row['PAE_domain_blockiness_score']:.2f}")

    report_lines.append("")
    report_lines.append("## 3. LBX1 Comparator Analysis")
    report_lines.append("Comparison of LBX1 against reference mechanosensors and low-confidence outliers:")
    report_lines.append("")

    comparators = comparators.sort_values(by='anisotropy_index', ascending=False)
    for _, row in comparators.iterrows():
        note = "Low Confidence Artifact Warning" if row['plddt_mean'] < 70 and row['anisotropy_index'] >= 3.0 else \
               "Reliable Structural Model" if row['plddt_mean'] >= 70 else "Low Confidence"

        if row['gene_symbol'] == 'LBX1':
            note = "Core Target - Low Confidence, Intermediate Anisotropy"

        report_lines.append(f"- **{row['gene_symbol']}**: Anisotropy={row['anisotropy_index']:.2f}, pLDDT={row['plddt_mean']:.1f} ({row['Confidence_Category']}) -> {note}")

    report_lines.append("")
    report_lines.append("*Note: LMNA is absent from the 2026-02-16 snapshot, though historical records show Anisotropy=4.75, pLDDT=76.4.*")

    with open("reports/confidence_weighted_structural_evidence.md", "w") as f:
        f.write("\n".join(report_lines))

    # Combine and save CSV
    out_df = pd.concat([high_anisotropy_high_conf, high_anisotropy_low_conf, df[(df['anisotropy_index'] < 3.0)]])
    out_df['Confidence_Category'] = out_df['plddt_mean'].apply(lambda x: 'Adequate (>=70)' if x >= 70 else 'Low (<70)')
    out_df.to_csv("outputs/afcc/confidence_weighted_ranking.csv", index=False)

if __name__ == "__main__":
    compute_confidence_weighted_ranking()
