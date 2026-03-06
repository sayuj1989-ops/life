import pandas as pd
import os
from datetime import datetime

def generate_confidence_weighted_ranking():
    metrics_path = "outputs/afcc/2026-02-16/metrics.csv"
    if not os.path.exists(metrics_path):
        print(f"Error: {metrics_path} not found.")
        return

    df = pd.read_csv(metrics_path)

    # Define thresholds
    ANISOTROPY_THRESHOLD = 3.0
    PLDDT_THRESHOLD = 70.0

    # 1. High-anisotropy + adequate-confidence
    high_aniso_high_conf = df[(df['anisotropy_index'] >= ANISOTROPY_THRESHOLD) & (df['plddt_mean'] >= PLDDT_THRESHOLD)].copy()
    high_aniso_high_conf['confidence_tier'] = 'Adequate'

    # 2. High-anisotropy + low-confidence
    high_aniso_low_conf = df[(df['anisotropy_index'] >= ANISOTROPY_THRESHOLD) & (df['plddt_mean'] < PLDDT_THRESHOLD)].copy()
    high_aniso_low_conf['confidence_tier'] = 'Low (Exploratory)'

    # Combine and sort
    combined_ranked = pd.concat([high_aniso_high_conf, high_aniso_low_conf])
    combined_ranked = combined_ranked.sort_values(by=['confidence_tier', 'anisotropy_index'], ascending=[True, False])

    # Save CSV
    out_csv = "outputs/afcc/confidence_weighted_ranking.csv"
    combined_ranked.to_csv(out_csv, index=False)
    print(f"Saved ranking to {out_csv}")

    # Comparator analysis
    comparators = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    comp_df = df[df['gene_symbol'].isin(comparators)].copy()

    # Note: LMNA and RUNX3 might not be in the 2026-02-16 snapshot
    found_comparators = comp_df['gene_symbol'].tolist()
    missing_comparators = [g for g in comparators if g not in found_comparators]

    report_out = "reports/confidence_weighted_structural_evidence.md"
    with open(report_out, 'w') as f:
        f.write("# Confidence-Weighted Structural Evidence Report\n\n")
        f.write(f"**Source Data:** `outputs/afcc/2026-02-16/metrics.csv`\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## 1. High-Anisotropy + Adequate-Confidence (Strong Signal)\n")
        f.write("Thresholds: Anisotropy >= 3.0, pLDDT >= 70.0\n\n")
        f.write("| Gene | Anisotropy | pLDDT | Morphology |\n")
        f.write("|---|---|---|---|\n")
        for _, row in high_aniso_high_conf.sort_values(by='anisotropy_index', ascending=False).iterrows():
            f.write(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.2f} | {row['morphology']} |\n")

        f.write("\n## 2. High-Anisotropy + Low-Confidence (Exploratory Only)\n")
        f.write("Thresholds: Anisotropy >= 3.0, pLDDT < 70.0. *These candidates require orthogonal validation.*\n\n")
        f.write("| Gene | Anisotropy | pLDDT | Morphology |\n")
        f.write("|---|---|---|---|\n")
        for _, row in high_aniso_low_conf.sort_values(by='anisotropy_index', ascending=False).iterrows():
            f.write(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.2f} | {row['morphology']} |\n")

        f.write("\n## 3. LBX1 Comparator Analysis\n")
        f.write("Comparing LBX1 metrics against anchor mechanosensors and other highly anisotropic targets.\n\n")
        f.write("| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence Tier |\n")
        f.write("|---|---|---|---|---|\n")
        for _, row in comp_df.iterrows():
            tier = "Adequate" if row['plddt_mean'] >= 70 else "Low"
            f.write(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.2f} | {row.get('PAE_domain_blockiness_score', 0):.2f} | {tier} |\n")

        if missing_comparators:
            f.write(f"\n*Note: The following comparators were absent from the 2026-02-16 snapshot: {', '.join(missing_comparators)}*\n")

        f.write("\n### Comparator Interpretation\n")
        f.write("- **LBX1** remains an intermediate-anisotropy candidate with low confidence and high blockiness, distinguishing it from rigid structural rods like PIEZO2.\n")
        f.write("- **PIEZO2** and **ADGRG6** represent true adequate-confidence mechanosensors, showing high anisotropy and acceptable pLDDT.\n")
        f.write("- **POC5** and **GHR** show extreme anisotropy but are structurally low-confidence, meaning they are exploratory and their geometry could be an artifact of intrinsic disorder.\n")

    print(f"Report saved to {report_out}")

if __name__ == "__main__":
    generate_confidence_weighted_ranking()
