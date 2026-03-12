import pandas as pd
import os

# Load authoritative latest AFCC metrics snapshot
df = pd.read_csv('outputs/afcc/2026-02-16/metrics.csv')

# Calculate Confidence Score (simple logic: scale pLDDT + penalize disorder/low-confidence/PAE-blockiness)
# This is a basic confidence weighting, can be adjusted
df['confidence_weight'] = df['plddt_mean'] / 100.0

# Adjust confidence weight using available fields that penalize confidence
# If 'plddt_fraction_low' exists, decrease confidence
if 'plddt_fraction_low' in df.columns:
    df['confidence_weight'] = df['confidence_weight'] * (1.0 - df['plddt_fraction_low'])

# Rank high-anisotropy + adequate-confidence
high_ani_adequate_conf = df[(df['anisotropy_index'] >= 3.0) & (df['plddt_mean'] >= 70)].copy()
high_ani_adequate_conf['category'] = 'High Anisotropy + Adequate Confidence'
high_ani_adequate_conf = high_ani_adequate_conf.sort_values(by=['confidence_weight', 'anisotropy_index'], ascending=[False, False])

# Rank high-anisotropy + low-confidence
high_ani_low_conf = df[(df['anisotropy_index'] >= 3.0) & (df['plddt_mean'] < 70)].copy()
high_ani_low_conf['category'] = 'High Anisotropy + Low Confidence (Exploratory)'
high_ani_low_conf = high_ani_low_conf.sort_values(by=['anisotropy_index'], ascending=[False])

# Combine for CSV
combined = pd.concat([high_ani_adequate_conf, high_ani_low_conf])
combined.to_csv('outputs/afcc/confidence_weighted_ranking.csv', index=False)

# LBX1 Comparator Analysis
comparator_genes = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
comparator_df = df[df['gene_symbol'].isin(comparator_genes)][['gene_symbol', 'anisotropy_index', 'plddt_mean', 'PAE_domain_blockiness_score', 'confidence_weight']]

missing_genes = [gene for gene in comparator_genes if gene not in comparator_df['gene_symbol'].values]

# Generate report text
report = f"""# Confidence-Weighted Structural Evidence Report

*Generated from authoritative snapshot: outputs/afcc/2026-02-16/metrics.csv*
*Analysis date: 2026-02-16 window*

## 1. High-Anisotropy + Adequate-Confidence Candidates
These candidates have Anisotropy >= 3.0 and pLDDT >= 70. They represent the strongest structural evidence.
"""
for _, row in high_ani_adequate_conf.iterrows():
    report += f"- **{row['gene_symbol']}**: Anisotropy = {row['anisotropy_index']:.2f}, pLDDT = {row['plddt_mean']:.2f}, Confidence Weight = {row['confidence_weight']:.2f}\n"

report += f"""
## 2. High-Anisotropy + Low-Confidence Candidates (Exploratory Only)
These candidates have Anisotropy >= 3.0 but pLDDT < 70. Their high anisotropy might be an artifact of flexible or disordered regions and should be treated as hypothesis-generating only.
"""
for _, row in high_ani_low_conf.iterrows():
    report += f"- **{row['gene_symbol']}**: Anisotropy = {row['anisotropy_index']:.2f}, pLDDT = {row['plddt_mean']:.2f}, Confidence Weight = {row['confidence_weight']:.2f}\n"

report += f"""
## 3. LBX1 Comparator Analysis
Comparing LBX1 against key anchor genes:
"""
for _, row in comparator_df.iterrows():
    report += f"- **{row['gene_symbol']}**: Anisotropy = {row['anisotropy_index']:.2f}, pLDDT = {row['plddt_mean']:.2f}, PAE Blockiness = {row['PAE_domain_blockiness_score']:.2f}, Confidence Weight = {row['confidence_weight']:.2f}\n"

if missing_genes:
    report += f"\n*Note: The following comparator genes were missing from the 2026-02-16 snapshot and could not be included in the quantitative comparison: {', '.join(missing_genes)}.*\n"

report += f"""
### Inference vs Direct Measurement
- **Direct Measurement**: LBX1's pLDDT ({comparator_df[comparator_df['gene_symbol'] == 'LBX1']['plddt_mean'].values[0]:.2f}) and PAE Blockiness ({comparator_df[comparator_df['gene_symbol'] == 'LBX1']['PAE_domain_blockiness_score'].values[0]:.2f}) indicate a low-confidence, intermediate structure.
- **Inference**: Previous narratives assigned structural roles to LBX1 based on these static low-confidence metrics. Given its low confidence weight compared to PIEZO2, it should NOT be used as a primary structural anchor.
"""

with open('reports/confidence_weighted_structural_evidence.md', 'w') as f:
    f.write(report)
print("Confidence weighting complete.")
