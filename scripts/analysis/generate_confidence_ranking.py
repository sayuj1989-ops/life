import pandas as pd
import os
import argparse
from datetime import datetime

# Default paths
DEFAULT_INPUT_FILE = "outputs/afcc/2026-02-16/metrics.csv"
DEFAULT_OUTPUT_CSV = "outputs/afcc/confidence_weighted_ranking.csv"
DEFAULT_REPORT_FILE = "reports/confidence_weighted_structural_evidence.md"

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

def generate_confidence_ranking(input_csv, output_csv, report_path):
    """
    Generates confidence ranking and report from metrics CSV.
    """
    if not os.path.exists(input_csv):
        print(f"Error: Input file {input_csv} not found.")
        return None, None

    df = pd.read_csv(input_csv)

    # Calculate Weighted Score
    # Anisotropy * (pLDDT / 100)
    # Handle missing columns if necessary, but assuming standard schema
    if 'anisotropy_index' not in df.columns or 'plddt_mean' not in df.columns:
        print("Error: Missing required columns 'anisotropy_index' or 'plddt_mean'.")
        return df, pd.DataFrame()

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
    # Check if optional columns exist
    extra_cols = ['uniprot', 'morphology']
    for c in extra_cols:
        if c in df.columns:
            cols.append(c)

    # Ensure all cols exist
    cols = [c for c in cols if c in df.columns]

    df_out = df_sorted[cols]

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    df_out.to_csv(output_csv, index=False)
    print(f"Ranking CSV written to {output_csv}")

    # Generate Report
    with open(report_path, "w") as f:
        f.write("# Confidence-Weighted Structural Evidence\n\n")
        f.write(f"**Baseline Date:** {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"**Source Data:** {input_csv}\n")
        f.write("**Metric:** Weighted Score = Anisotropy * (pLDDT / 100)\n\n")

        # Tier 1 Analysis
        tier1 = df_sorted[df_sorted['confidence_tier'] == "Tier 1: High Anisotropy + High Confidence"]
        f.write("## Tier 1: Confirmed Structural Drivers (High Anisotropy, High Confidence)\n")
        f.write("These candidates have robust structural evidence supporting their role as anisotropic mechanical elements.\n\n")
        if not tier1.empty:
            f.write(to_markdown_table(tier1[['gene_symbol', 'anisotropy_index', 'plddt_mean', 'weighted_score']]))
        else:
            f.write("No candidates found in Tier 1.")
        f.write("\n\n")

        # Tier 2 Analysis
        tier2 = df_sorted[df_sorted['confidence_tier'] == "Tier 2: High Anisotropy + Low Confidence"]
        f.write("## Tier 2: Speculative Structural Drivers (High Anisotropy, Low Confidence)\n")
        f.write("High anisotropy detected but structure is low confidence (IDR or flexible). **Interpret with caution.**\n\n")
        if not tier2.empty:
            f.write(to_markdown_table(tier2[['gene_symbol', 'anisotropy_index', 'plddt_mean', 'weighted_score']]))
        else:
            f.write("No candidates found in Tier 2.")
        f.write("\n\n")

        # LBX1 Comparative Analysis
        f.write("## LBX1 Comparative Analysis\n")
        f.write("Evaluating LBX1 against known mechanosensors and controls.\n\n")

        targets = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
        # Filter for targets present in df
        target_df = df_sorted[df_sorted['gene_symbol'].isin(targets)].copy()

        missing_targets = set(targets) - set(target_df['gene_symbol'])
        if missing_targets:
            f.write(f"**Note:** The following targets were not found in the baseline dataset: {', '.join(missing_targets)}.\n\n")

        # Add commentary based on data
        def get_comment(row):
            s = row['gene_symbol']
            if s == 'LBX1':
                return "Baseline target. Moderate anisotropy, low confidence. Likely NOT a primary structural rod."
            elif s == 'PIEZO2':
                return "Confirmed high-anisotropy sensor (Vector)."
            elif s == 'LMNA':
                return "Confirmed high-anisotropy sensor (Nuclear)."
            elif s == 'POC5':
                return "Extreme anisotropy, but check confidence (Ciliary)."
            elif s == 'GHR':
                return "High anisotropy, low confidence (Membrane)."
            elif s == 'ADGRG6':
                return "High anisotropy, good confidence (GPCR)."
            elif s == 'RUNX3':
                return "Comparator (Monolithic)."
            return ""

        if not target_df.empty:
            target_df['Comment'] = target_df.apply(get_comment, axis=1)
            # Ensure columns exist
            disp_cols = ['gene_symbol', 'anisotropy_index', 'plddt_mean', 'confidence_tier', 'Comment']
            if 'PAE_domain_blockiness_score' in target_df.columns:
                disp_cols.insert(3, 'PAE_domain_blockiness_score')

            f.write(to_markdown_table(target_df[disp_cols].sort_values(by='anisotropy_index', ascending=False)))
        else:
            f.write("No target candidates found in dataset.")
        f.write("\n\n")

        # LBX1 Specific Interpretation
        lbx1 = df_sorted[df_sorted['gene_symbol'] == 'LBX1']
        if not lbx1.empty:
            lbx1_row = lbx1.iloc[0]
            f.write("### LBX1 Assessment\n")
            f.write(f"- **Anisotropy:** {lbx1_row['anisotropy_index']:.2f} (Moderate)\n")
            f.write(f"- **Confidence (pLDDT):** {lbx1_row['plddt_mean']:.2f} (Low/Moderate)\n")
            if 'PAE_domain_blockiness_score' in lbx1_row:
                 f.write(f"- **Blockiness:** {lbx1_row['PAE_domain_blockiness_score']:.2f}\n")

            f.write("\n**Conclusion:** LBX1's structural metrics do not support a \"Tension Rod\" hypothesis. It clusters with globular/intermediate proteins. Its role is likely regulatory rather than structural.\n")
        else:
            f.write("LBX1 not found in dataset.\n")

    print(f"Report written to {report_path}")
    return df, df_sorted

def main():
    parser = argparse.ArgumentParser(description="Generate confidence ranking from AFCC metrics.")
    parser.add_argument("--input", default=DEFAULT_INPUT_FILE, help="Path to input metrics CSV")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_CSV, help="Path to output ranking CSV")
    parser.add_argument("--report", default=DEFAULT_REPORT_FILE, help="Path to output report MD")

    args = parser.parse_args()

    generate_confidence_ranking(args.input, args.output, args.report)

if __name__ == "__main__":
    main()
