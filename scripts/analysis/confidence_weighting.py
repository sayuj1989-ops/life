import pandas as pd
import numpy as np

def generate_confidence_weighted_ranking():
    # Authoritative snapshot
    input_file = "outputs/afcc/2026-02-16/metrics.csv"
    output_file = "outputs/afcc/confidence_weighted_ranking.csv"

    df = pd.read_csv(input_file, index_col=0)

    # Correct column name based on actual CSV
    plddt_col = 'plddt_mean' if 'plddt_mean' in df.columns else 'pLDDT_mean'

    # Identify high anisotropy + adequate confidence
    high_ani = df['anisotropy_index'] >= 3.0
    adequate_conf = df[plddt_col] >= 70.0

    df['confidence_class'] = np.where(adequate_conf, 'Adequate Confidence', 'Low Confidence')
    df['structural_signal'] = np.where(
        high_ani & adequate_conf, 'High Anisotropy + Adequate Confidence',
        np.where(high_ani & ~adequate_conf, 'High Anisotropy + Low Confidence (Exploratory)',
        np.where(~high_ani & adequate_conf, 'Low Anisotropy + Adequate Confidence', 'Low Anisotropy + Low Confidence'))
    )

    df = df.sort_values(by=['confidence_class', 'anisotropy_index'], ascending=[True, False]) # Adequate first

    # Save the CSV
    df.to_csv(output_file)

    # Generate the report
    report = f"""# Confidence-Weighted Structural Evidence

## Context
This report re-evaluates the structural candidates from the authoritative snapshot (`outputs/afcc/2026-02-16/metrics.csv`) using explicit confidence weighting to prevent the over-interpretation of poorly predicted architectures.

## Methodology
- **Authoritative Snapshot**: `outputs/afcc/2026-02-16/metrics.csv`
- **Adequate Confidence Threshold**: `{plddt_col} >= 70.0`
- **High Anisotropy Threshold**: `anisotropy_index >= 3.0`

## Ranked Evidence Tiers

### Tier 1: High Anisotropy + Adequate Confidence (Strongest Structural Signal)
*These candidates exhibit elongated, potentially load-bearing structures with sufficient AlphaFold prediction confidence to warrant mechanistic interpretation.*

"""
    tier1 = df[(df['anisotropy_index'] >= 3.0) & (df[plddt_col] >= 70.0)].sort_values(by='anisotropy_index', ascending=False)
    for index, row in tier1.iterrows():
        report += f"- **{index}**: Anisotropy = {row['anisotropy_index']:.2f}, pLDDT = {row[plddt_col]:.1f}, PAE Blockiness = {row['PAE_domain_blockiness_score']:.2f}\n"

    report += """
### Tier 2: High Anisotropy + Low Confidence (Exploratory Only)
*These candidates show high anisotropy, but their structures are poorly predicted (often highly disordered). Their geometry should NOT be used to infer precise mechanosensor architecture without orthogonal validation.*

"""
    tier2 = df[(df['anisotropy_index'] >= 3.0) & (df[plddt_col] < 70.0)].sort_values(by='anisotropy_index', ascending=False)
    for index, row in tier2.iterrows():
        report += f"- **{index}**: Anisotropy = {row['anisotropy_index']:.2f}, pLDDT = {row[plddt_col]:.1f}, PAE Blockiness = {row['PAE_domain_blockiness_score']:.2f}\n"

    # LBX1 Comparator Analysis
    comparators = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    report += """
## LBX1 Comparator Analysis
Comparing LBX1 to key putative mechanosensors and structural candidates.

| Gene | Anisotropy | pLDDT (Confidence) | PAE Blockiness | Confidence Class |
|---|---|---|---|---|
"""
    for comp in comparators:
        if comp in df.index:
            row = df.loc[comp]
            report += f"| {comp} | {row['anisotropy_index']:.2f} | {row[plddt_col]:.1f} | {row['PAE_domain_blockiness_score']:.2f} | {row['confidence_class']} |\n"
        else:
            report += f"| {comp} | N/A | N/A | N/A | Not in 2026-02-16 snapshot |\n"

    report += """
### Observations
- **LBX1 Weakness**: LBX1 remains in the "Low Confidence" tier with intermediate anisotropy (~2.27). Its high PAE blockiness (~7.35) suggests a modular architecture, but the low pLDDT prevents definitive geometric claims about its loaded state.
- **PIEZO2 Strength**: PIEZO2 serves as a positive control, showing both high anisotropy and adequate confidence, supporting its established mechanosensory role.
- **Outlier Caution**: While POC5 and GHR show extreme anisotropy, their low pLDDT scores mark them strictly as exploratory.
"""

    with open("reports/confidence_weighted_structural_evidence.md", "w") as f:
        f.write(report)

    print("Report written to reports/confidence_weighted_structural_evidence.md")

if __name__ == "__main__":
    generate_confidence_weighted_ranking()
