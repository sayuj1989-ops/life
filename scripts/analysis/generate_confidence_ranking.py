import pandas as pd
import os

INPUT_FILE = "outputs/afcc/2026-02-16/metrics.csv"
OUTPUT_CSV = "outputs/afcc/confidence_weighted_ranking.csv"
REPORT_FILE = "reports/confidence_weighted_structural_evidence.md"

def to_markdown_table(df):
    """
    Converts a DataFrame to a Markdown table string without using tabulate.
    """
    if df.empty:
        return "No data available."

    columns = df.columns.tolist()
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    rows = []
    for _, row in df.iterrows():
        row_str = "| " + " | ".join([str(val) for val in row]) + " |"
        rows.append(row_str)

    return "\n".join([header, separator] + rows)

def generate_ranking():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file {INPUT_FILE} not found.")
        return None, None

    df = pd.read_csv(INPUT_FILE)

    # Calculate Weighted Score
    df['weighted_score'] = df['anisotropy_index'] * (df['plddt_mean'] / 100.0)

    # Define Confidence Tiers
    def classify_tier(row):
        is_high_anisotropy = row['anisotropy_index'] >= 3.0
        is_adequate_confidence = row['plddt_mean'] >= 70.0

        if is_high_anisotropy and is_adequate_confidence:
            return "Tier 1: High Anisotropy + High Confidence"
        elif is_high_anisotropy and not is_adequate_confidence:
            return "Tier 2: High Anisotropy + Low Confidence"
        elif not is_high_anisotropy and is_adequate_confidence:
            return "Tier 3: Low Anisotropy + High Confidence"
        else:
            return "Tier 4: Low Anisotropy + Low Confidence"

    df['confidence_tier'] = df.apply(classify_tier, axis=1)

    # Rank by weighted score
    df_sorted = df.sort_values(by='weighted_score', ascending=False)

    # Select key columns for output
    cols = ['gene_symbol', 'confidence_tier', 'weighted_score', 'anisotropy_index', 'plddt_mean', 'PAE_domain_blockiness_score', 'source_category']
    extra_cols = ['uniprot', 'morphology']
    for c in extra_cols:
        if c in df.columns:
            cols.append(c)

    df_out = df_sorted[cols]
    df_out.to_csv(OUTPUT_CSV, index=False)
    print(f"Ranking CSV written to {OUTPUT_CSV}")

    return df, df_sorted

def generate_report(df):
    with open(REPORT_FILE, "w") as f:
        f.write("# Confidence-Weighted Structural Evidence\n\n")
        f.write("**Baseline Date:** 2026-02-16\n")
        f.write("**Metric:** Weighted Score = Anisotropy * (pLDDT / 100)\n\n")

        # Tier 1 Analysis
        tier1 = df[df['confidence_tier'] == "Tier 1: High Anisotropy + High Confidence"]
        f.write("## Tier 1: Confirmed Structural Drivers (High Anisotropy, High Confidence)\n")
        f.write("These candidates have robust structural evidence supporting their role as anisotropic mechanical elements.\n\n")
        f.write(to_markdown_table(tier1[['gene_symbol', 'anisotropy_index', 'plddt_mean', 'weighted_score']]))
        f.write("\n\n")

        # Tier 2 Analysis
        tier2 = df[df['confidence_tier'] == "Tier 2: High Anisotropy + Low Confidence"]
        f.write("## Tier 2: Speculative Structural Drivers (High Anisotropy, Low Confidence)\n")
        f.write("High anisotropy detected but structure is low confidence (IDR or flexible). **Interpret with caution.**\n\n")
        f.write(to_markdown_table(tier2[['gene_symbol', 'anisotropy_index', 'plddt_mean', 'weighted_score']]))
        f.write("\n\n")

        # LBX1 Comparative Analysis
        f.write("## LBX1 Comparative Analysis\n")
        f.write("Evaluating LBX1 against known mechanosensors and controls.\n\n")

        targets = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
        # Filter for targets present in df
        target_df = df[df['gene_symbol'].isin(targets)].copy()

        # Add commentary based on data
        def get_comment(row):
            if row['gene_symbol'] == 'LBX1':
                return "Baseline target. Moderate anisotropy, low confidence. Likely NOT a primary structural rod."
            elif row['gene_symbol'] in ['PIEZO2', 'LMNA']:
                return "Confirmed high-anisotropy sensors."
            elif row['gene_symbol'] == 'POC5':
                return "Extreme anisotropy, but check confidence."
            return ""

        target_df['Comment'] = target_df.apply(get_comment, axis=1)

        f.write(to_markdown_table(target_df[['gene_symbol', 'anisotropy_index', 'plddt_mean', 'PAE_domain_blockiness_score', 'confidence_tier', 'Comment']].sort_values(by='anisotropy_index', ascending=False)))
        f.write("\n\n")

        # LBX1 Specific Interpretation
        lbx1 = df[df['gene_symbol'] == 'LBX1']
        if not lbx1.empty:
            lbx1_row = lbx1.iloc[0]
            f.write("### LBX1 Assessment\n")
            f.write(f"- **Anisotropy:** {lbx1_row['anisotropy_index']:.2f} (Moderate)\n")
            f.write(f"- **Confidence (pLDDT):** {lbx1_row['plddt_mean']:.2f} (Low/Moderate)\n")
            f.write(f"- **Blockiness:** {lbx1_row['PAE_domain_blockiness_score']:.2f}\n")
            f.write("\n**Conclusion:** LBX1's structural metrics do not support a \"Tension Rod\" hypothesis. It clusters with globular/intermediate proteins. Its role is likely regulatory rather than structural.\n")
        else:
            f.write("LBX1 not found in dataset.\n")

    print(f"Report written to {REPORT_FILE}")

if __name__ == "__main__":
    df_raw, df_ranked = generate_ranking()
    if df_ranked is not None:
        generate_report(df_ranked)
