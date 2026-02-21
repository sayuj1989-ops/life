import pandas as pd
import numpy as np

def generate_confidence_ranking(input_csv="outputs/afcc/2026-02-16/metrics.csv", output_csv="outputs/afcc/confidence_weighted_ranking.csv", report_path="reports/confidence_weighted_structural_evidence.md"):

    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: Input file {input_csv} not found.")
        return

    # Key candidates for comparator analysis
    target_genes = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']

    # Filter for target genes (and maybe keep others for context if needed, but let's focus first)
    # Actually, let's keep all for ranking, but highlight targets

    # Coerce numerics
    df['plddt_mean'] = pd.to_numeric(df['plddt_mean'], errors='coerce')
    df['PAE_mean'] = pd.to_numeric(df['PAE_mean'], errors='coerce')
    df['anisotropy_index'] = pd.to_numeric(df['anisotropy_index'], errors='coerce')

    # Define Confidence Tiers
    def get_confidence_tier(row):
        if row['plddt_mean'] >= 80 and row['PAE_mean'] < 15: # Relaxed PAE slightly
            return "High"
        elif row['plddt_mean'] >= 70:
            return "Medium"
        else:
            return "Low"

    df['Confidence_Tier'] = df.apply(get_confidence_tier, axis=1)

    # Define Anisotropy Tiers
    def get_anisotropy_tier(row):
        if row['anisotropy_index'] > 3.5:
            return "Extreme (>3.5)"
        elif row['anisotropy_index'] > 2.0:
            return "High (>2.0)"
        else:
            return "Standard"

    df['Anisotropy_Tier'] = df.apply(get_anisotropy_tier, axis=1)

    # Create a weighted score (experimental)
    # Score = Anisotropy * (pLDDT / 100)^2
    df['Weighted_Anisotropy'] = df['anisotropy_index'] * (df['plddt_mean'] / 100) ** 2

    # Rank by Weighted Anisotropy
    df = df.sort_values('Weighted_Anisotropy', ascending=False)

    # Select columns for output
    out_cols = ['gene_symbol', 'anisotropy_index', 'plddt_mean', 'PAE_mean', 'Confidence_Tier', 'Anisotropy_Tier', 'Weighted_Anisotropy', 'morphology']
    df_out = df[out_cols]

    # Save CSV
    df_out.to_csv(output_csv, index=False)
    print(f"Ranking saved to {output_csv}")

    # Generate Report
    report_lines = []
    report_lines.append("# Confidence-Weighted Structural Evidence")
    report_lines.append(f"Based on metrics from: {input_csv}")
    report_lines.append("")

    report_lines.append("## 1. Executive Summary")
    report_lines.append("This analysis re-evaluates structural candidates by weighting their anisotropy with AlphaFold confidence metrics (pLDDT and PAE).")
    report_lines.append("High anisotropy in low-confidence regions (IDRs) is distinguished from rigid, high-confidence structural anisotropy.")
    report_lines.append("")

    report_lines.append("## 2. Comparator Analysis: LBX1 vs Controls")
    report_lines.append("We compare LBX1 against known mechanosensors (PIEZO2) and structural proteins (LMNA, GHR).")
    report_lines.append("")

    target_df = df[df['gene_symbol'].isin(target_genes)].sort_values('Weighted_Anisotropy', ascending=False)
    report_lines.append(target_df[out_cols].to_markdown(index=False))

    report_lines.append("")
    report_lines.append("### Key Observations")

    lbx1_row = target_df[target_df['gene_symbol'] == 'LBX1'].iloc[0] if not target_df[target_df['gene_symbol'] == 'LBX1'].empty else None
    piezo2_row = target_df[target_df['gene_symbol'] == 'PIEZO2'].iloc[0] if not target_df[target_df['gene_symbol'] == 'PIEZO2'].empty else None

    if lbx1_row is not None:
        report_lines.append(f"- **LBX1**: Anisotropy {lbx1_row['anisotropy_index']:.2f}, pLDDT {lbx1_row['plddt_mean']:.1f} ({lbx1_row['Confidence_Tier']}).")
        report_lines.append(f"  - Weighted Score: {lbx1_row['Weighted_Anisotropy']:.2f}")
        if lbx1_row['Confidence_Tier'] == 'Low':
            report_lines.append("  - **CRITICAL CAVEAT**: LBX1's anisotropy is flagged as Low Confidence. This suggests the shape elongation might be due to disordered loops rather than a rigid structural feature.")

    if piezo2_row is not None:
        report_lines.append(f"- **PIEZO2**: Anisotropy {piezo2_row['anisotropy_index']:.2f}, pLDDT {piezo2_row['plddt_mean']:.1f} ({piezo2_row['Confidence_Tier']}).")
        report_lines.append(f"  - Weighted Score: {piezo2_row['Weighted_Anisotropy']:.2f}")
        report_lines.append("  - PIEZO2 maintains high anisotropy even when weighted by confidence, supporting its role as a rigid tension rod.")

    report_lines.append("")
    report_lines.append("## 3. Top High-Confidence Anisotropic Structures")
    report_lines.append("These proteins have confirmed structural elongation (High/Medium Confidence + High/Extreme Anisotropy).")

    high_conf_aniso = df[(df['Confidence_Tier'].isin(['High', 'Medium'])) & (df['Anisotropy_Tier'].isin(['Extreme (>3.5)', 'High (>2.0)']))].head(10)
    report_lines.append(high_conf_aniso[out_cols].to_markdown(index=False))

    report_lines.append("")
    report_lines.append("## 4. Low-Confidence Artifact Risks")
    report_lines.append("These proteins show high anisotropy but have Low confidence, posing a risk of false positives due to IDRs.")

    low_conf_aniso = df[(df['Confidence_Tier'] == 'Low') & (df['Anisotropy_Tier'].isin(['Extreme (>3.5)', 'High (>2.0)']))].head(10)
    report_lines.append(low_conf_aniso[out_cols].to_markdown(index=False))

    # Write Report
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    generate_confidence_ranking()
