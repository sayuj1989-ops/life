import pandas as pd
import glob
import os

def generate_confidence_ranking():
    # Load authoritative metrics
    df = pd.read_csv('outputs/afcc/2026-02-16/metrics.csv')

    # 1. High-anisotropy + adequate-confidence
    high_conf = df[(df['anisotropy_index'] >= 3.0) & (df['plddt_mean'] >= 70.0)].copy()
    high_conf = high_conf.sort_values(by='anisotropy_index', ascending=False)
    high_conf['confidence_tier'] = 'Adequate (pLDDT >= 70)'

    # 2. High-anisotropy + low-confidence
    low_conf = df[(df['anisotropy_index'] >= 3.0) & (df['plddt_mean'] < 70.0)].copy()
    low_conf = low_conf.sort_values(by='anisotropy_index', ascending=False)
    low_conf['confidence_tier'] = 'Low (pLDDT < 70) - Exploratory'

    # Rest of the candidates (below threshold)
    other = df[df['anisotropy_index'] < 3.0].copy()
    other['confidence_tier'] = other['plddt_mean'].apply(lambda x: 'Adequate (pLDDT >= 70)' if x >= 70 else 'Low (pLDDT < 70) - Exploratory')
    other = other.sort_values(by='anisotropy_index', ascending=False)

    # Combine
    combined = pd.concat([high_conf, low_conf, other])

    # Output CSV
    cols = ['gene_symbol', 'confidence_tier', 'anisotropy_index', 'plddt_mean', 'PAE_domain_blockiness_score', 'morphology']
    combined[cols].to_csv('outputs/afcc/confidence_weighted_ranking.csv', index=False)

    # Generate LBX1 Comparator Table
    comparators = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    comp_df = df[df['gene_symbol'].isin(comparators)].copy()

    # Some genes might not be in the snapshot, find them
    found = comp_df['gene_symbol'].tolist()
    missing = [c for c in comparators if c not in found]

    if missing:
        # Check other recent files
        other_files = sorted(glob.glob('outputs/afcc/*/metrics.csv'), reverse=True)
        for c in missing:
            for f in other_files:
                if '2026-02-16' in f: continue
                try:
                    temp_df = pd.read_csv(f)
                    if c in temp_df['gene_symbol'].values:
                        row = temp_df[temp_df['gene_symbol'] == c].iloc[[0]]
                        comp_df = pd.concat([comp_df, row])
                        break
                except:
                    pass

    comp_df = comp_df.sort_values(by='anisotropy_index', ascending=False)

    # Generate Markdown Report
    report = f"""# Confidence-Weighted Structural Evidence

## Methodology
To prevent over-interpretation of intrinsically disordered or highly flexible regions, candidates are stratified by their structural confidence (pLDDT mean). High-anisotropy values computed on low-confidence regions reflect extended random coils rather than rigid mechanical sensors.

## 1. High-Anisotropy, Adequate Confidence (Mechanosensor Candidates)
These proteins exhibit both extended shapes and rigid structural predictions, making them the most defensible candidates for load-bearing or geometric sensing roles.
Threshold: Anisotropy >= 3.0, pLDDT >= 70.0

| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |
|------|------------|-------|----------------|------------|
"""
    for _, row in high_conf.iterrows():
        report += f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} | {row['morphology']} |\n"

    report += """
## 2. High-Anisotropy, Low Confidence (Exploratory Only)
These proteins have extended predictions but low structural confidence. Their high anisotropy likely reflects disordered states, unfoldase activity, or missing binding partners. Structural inferences here are strictly hypothesis-generating.
Threshold: Anisotropy >= 3.0, pLDDT < 70.0

| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |
|------|------------|-------|----------------|------------|
"""
    for _, row in low_conf.iterrows():
        report += f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} | {row['morphology']} |\n"

    report += """
## LBX1 Comparator Analysis
LBX1's predicted structure is contextualized against known mechanosensors and other candidates to evaluate its plausibility as a purely geometric driver.

| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology | Role in Context |
|------|------------|-------|----------------|------------|-----------------|
"""
    for _, row in comp_df.iterrows():
        gene = row['gene_symbol']
        role = "Target of interest; intermediate shape, low confidence." if gene == 'LBX1' else \
               "Validated mechanosensor; extended, high confidence." if gene == 'PIEZO2' else \
               "Nuclear tension element; extended, high confidence." if gene == 'LMNA' else \
               "Scoliosis-linked receptor; extended, adequate confidence." if gene == 'ADGRG6' else \
               "Transcription factor; globular/intermediate, low confidence." if gene == 'RUNX3' else \
               "Centriolar scaffold; extreme anisotropy, low confidence (disordered)." if gene == 'POC5' else \
               "Growth receptor; high anisotropy, low confidence." if gene == 'GHR' else "Comparator"

        report += f"| {gene} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} | {row['morphology']} | {role} |\n"

    report += """
### Conclusion on LBX1
Based on explicit confidence weighting:
- **LBX1 is not an extended mechanosensor**: Its anisotropy (2.27) falls below the threshold for tension rods, and its low pLDDT (66.9) suggests flexibility rather than a rigid structural element.
- **LBX1 vs Known Sensors**: Unlike `PIEZO2` or `LMNA`, which maintain high confidence across their extended geometries, LBX1 resembles flexible transcription factors (`RUNX3`).
- **Path Forward**: LBX1's high PAE blockiness (7.35) remains its most distinctive feature, suggesting a 'beads-on-a-string' multi-domain architecture. Its role in scoliosis is more likely related to complex assembly or tension-modulated binding rather than intrinsic cytoskeletal strut function.
"""
    with open('reports/confidence_weighted_structural_evidence.md', 'w') as f:
        f.write(report)

    print("Report written to reports/confidence_weighted_structural_evidence.md")
    print("CSV written to outputs/afcc/confidence_weighted_ranking.csv")

if __name__ == '__main__':
    generate_confidence_ranking()
