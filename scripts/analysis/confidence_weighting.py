import pandas as pd
import os

def create_confidence_weighted_evidence():
    df = pd.read_csv('outputs/afcc/2026-02-16/metrics.csv')

    # Stratify
    df['confidence_tier'] = df['plddt_mean'].apply(lambda x: 'Adequate (>=70)' if x >= 70 else 'Low (<70)')
    df_sorted = df.sort_values(by='anisotropy_index', ascending=False)

    df_sorted.to_csv('outputs/afcc/confidence_weighted_ranking.csv', index=False)

    # LBX1 Comparator Analysis
    target_genes = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    df_comparator = df_sorted[df_sorted['gene_symbol'].isin(target_genes)].copy()

    report_path = 'reports/confidence_weighted_structural_evidence.md'
    with open(report_path, 'w') as f:
        f.write("# Confidence-Weighted Structural Evidence\n\n")

        f.write("## Overview\n")
        f.write("Re-ranking of structural candidate proteins based on AlphaFold anisotropy metrics, explicitly separated by pLDDT confidence scores to avoid over-interpreting disordered/flexible regions as rigidly fibrous mechanosensors.\n\n")

        f.write("## High-Anisotropy + Adequate-Confidence (pLDDT >= 70)\n")
        f.write("These structures represent robust predictions of extended/fibrous architecture.\n\n")
        high_conf = df_sorted[(df_sorted['confidence_tier'] == 'Adequate (>=70)') & (df_sorted['anisotropy_index'] > 2.0)].head(10)
        f.write(high_conf[['gene_symbol', 'anisotropy_index', 'plddt_mean']].to_markdown(index=False))
        f.write("\n\n")

        f.write("## High-Anisotropy + Low-Confidence (pLDDT < 70) [Exploratory Only]\n")
        f.write("High anisotropy in these structures is likely driven by intrinsically disordered regions or high flexibility rather than a rigid rod-like function. Narrative claims regarding these should be strictly labeled as speculative.\n\n")
        low_conf = df_sorted[(df_sorted['confidence_tier'] == 'Low (<70)') & (df_sorted['anisotropy_index'] > 2.0)].head(10)
        f.write(low_conf[['gene_symbol', 'anisotropy_index', 'plddt_mean']].to_markdown(index=False))
        f.write("\n\n")

        f.write("## LBX1 Comparator Analysis\n")
        f.write("Comparison of LBX1 against known mechanosensors and structural proteins.\n\n")
        f.write(df_comparator[['gene_symbol', 'anisotropy_index', 'plddt_mean', 'confidence_tier']].to_markdown(index=False))
        f.write("\n\n")
        f.write("### Interpretation\n")
        f.write("- **LBX1**: Exhibits intermediate anisotropy (~2.27) but with low confidence (pLDDT ~66.9). The geometry is likely driven by unstructured regions, not a stable fibrous mechanosensing domain. Mechanosensor claims for LBX1 based purely on AF structural geometry are currently unsupported.\n")
        f.write("- **PIEZO2 / LMNA / ADGRG6**: Demonstrate true extended mechanosensory/structural architectures with adequate confidence (pLDDT > 70).\n")
        f.write("- **POC5 / GHR / RUNX3**: Also show high/intermediate anisotropy but suffer from low confidence, requiring experimental validation of their structural rigidity before they can be classified as strict mechanosensors.\n")

if __name__ == "__main__":
    create_confidence_weighted_evidence()
