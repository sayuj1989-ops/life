import os
import pandas as pd
import glob
from datetime import datetime
import numpy as np

OUTPUT_DIR = "outputs/afcc"
REPORT_FILE = "reports/evidence_freshness_audit.md"

def get_metrics_files():
    files = glob.glob(os.path.join(OUTPUT_DIR, "*", "metrics.csv"))
    files.sort()
    return files

def audit_files():
    files = get_metrics_files()
    if not files:
        print("No metrics.csv files found.")
        return

    report_lines = []
    report_lines.append("# AFCC Evidence Freshness Audit")
    report_lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    report_lines.append("")

    previous_df = None
    previous_date = None

    for file_path in files:
        date_dir = os.path.dirname(file_path)
        date_str = os.path.basename(date_dir)

        # Check for summary.md
        summary_path = os.path.join(date_dir, "summary.md")
        has_summary = os.path.exists(summary_path)

        report_lines.append(f"## Run: {date_str}")
        report_lines.append(f"- **Metrics File:** `{file_path}`")
        report_lines.append(f"- **Summary Report:** {'`Found`' if has_summary else '**MISSING**'}")

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            report_lines.append(f"- **Error:** Could not read CSV: {e}")
            continue

        if previous_df is not None:
            # Schema Drift
            curr_cols = set(df.columns)
            prev_cols = set(previous_df.columns)
            added = curr_cols - prev_cols
            removed = prev_cols - curr_cols

            if added or removed:
                report_lines.append(f"- **Schema Drift:**")
                if added: report_lines.append(f"  - Added: {', '.join(added)}")
                if removed: report_lines.append(f"  - Removed: {', '.join(removed)}")
            else:
                report_lines.append("- **Schema:** Stable")

            # Identical Vectors
            # We compare common columns for common genes
            common_genes = set(df['gene_symbol']).intersection(set(previous_df['gene_symbol']))
            if common_genes:
                identical_genes = []
                for gene in common_genes:
                    curr_row = df[df['gene_symbol'] == gene].iloc[0]
                    prev_row = previous_df[previous_df['gene_symbol'] == gene].iloc[0]

                    # Compare float columns with tolerance
                    is_diff = False
                    for col in curr_cols.intersection(prev_cols):
                        if col == 'gene_symbol': continue

                        val_curr = curr_row[col]
                        val_prev = prev_row[col]

                        # Check for boolean
                        if isinstance(val_curr, (bool, np.bool_)) or isinstance(val_prev, (bool, np.bool_)):
                            if val_curr != val_prev:
                                is_diff = True
                                break
                            continue

                        # Check for numeric
                        is_numeric = pd.api.types.is_numeric_dtype(type(val_curr))

                        if is_numeric and not isinstance(val_curr, (bool, np.bool_)):
                             if not pd.isna(val_curr) and not pd.isna(val_prev):
                                try:
                                    if abs(val_curr - val_prev) > 1e-6:
                                        is_diff = True
                                        break
                                except TypeError:
                                    # Fallback for non-substractable types
                                    if val_curr != val_prev:
                                        is_diff = True
                                        break
                             elif pd.isna(val_curr) != pd.isna(val_prev):
                                is_diff = True
                                break
                        else:
                            # String or other
                            if val_curr != val_prev:
                                is_diff = True
                                break

                    if not is_diff:
                        identical_genes.append(gene)

                if identical_genes:
                    report_lines.append(f"- **Stale Data Warning:** {len(identical_genes)}/{len(common_genes)} genes have IDENTICAL metrics to previous run.")
                    if len(identical_genes) == len(common_genes):
                         report_lines.append("  - **CRITICAL:** Entire dataset appears to be a copy of the previous run.")
                else:
                    report_lines.append(f"- **Freshness:** All {len(common_genes)} common genes show updates.")
            else:
                report_lines.append("- **Freshness:** No common genes to compare.")

        previous_df = df
        previous_date = date_str
        report_lines.append("")

    with open(REPORT_FILE, "w") as f:
        f.write("\n".join(report_lines))

    print(f"Audit report written to {REPORT_FILE}")

if __name__ == "__main__":
    audit_files()
