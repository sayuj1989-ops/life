import os
import pandas as pd
import glob
from datetime import datetime

OUTPUT_DIR = "outputs/afcc"
REPORT_FILE = "reports/evidence_freshness_audit.md"

def get_metrics_files():
    files = glob.glob(os.path.join(OUTPUT_DIR, "*", "metrics.csv"))
    files.sort()  # Sort by date
    return files

def audit_files():
    files = get_metrics_files()
    if not files:
        print("No metrics.csv files found in outputs/afcc/")
        return

    print(f"Found {len(files)} metrics.csv files.")

    previous_df = None
    previous_date = None

    findings = []

    for file_path in files:
        date_str = os.path.basename(os.path.dirname(file_path))
        print(f"Analyzing {date_str}...")

        try:
            current_df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

        if previous_df is not None:
            # Check for schema drift
            added_cols = set(current_df.columns) - set(previous_df.columns)
            removed_cols = set(previous_df.columns) - set(current_df.columns)

            if added_cols:
                findings.append(f"- **{date_str}**: Schema drift: Added columns {added_cols}")
            if removed_cols:
                findings.append(f"- **{date_str}**: Schema drift: Removed columns {removed_cols}")

            # Check for identical values
            # Compare rows by gene_symbol or uniprot if available
            key_col = 'gene_symbol' if 'gene_symbol' in current_df.columns else ('Identity' if 'Identity' in current_df.columns else None)

            if key_col:
                common_genes = set(current_df[key_col]).intersection(set(previous_df[key_col]))
                identical_count = 0
                changed_count = 0

                for gene in common_genes:
                    curr_row = current_df[current_df[key_col] == gene].iloc[0]
                    prev_row = previous_df[previous_df[key_col] == gene].iloc[0]

                    # Compare specific metrics like anisotropy, pLDDT
                    # Handle different column names if schema changed
                    # For now, simplistic comparison of common columns
                    common_cols = set(curr_row.index).intersection(set(prev_row.index))
                    common_cols.discard(key_col) # Don't compare key

                    is_identical = True
                    for col in common_cols:
                        if pd.isna(curr_row[col]) and pd.isna(prev_row[col]):
                            continue
                        if curr_row[col] != prev_row[col]:
                            is_identical = False
                            break

                    if is_identical:
                        identical_count += 1
                    else:
                        changed_count += 1

                findings.append(f"- **{date_str}**: {identical_count} identical genes, {changed_count} changed genes vs {previous_date}")
                if identical_count > 0 and changed_count == 0:
                     findings.append(f"  - WARNING: All common genes are identical to previous run!")

            else:
                findings.append(f"- **{date_str}**: Could not identify key column for comparison (tried gene_symbol, Identity)")

        previous_df = current_df
        previous_date = date_str

    # Generate Report
    with open(REPORT_FILE, "w") as f:
        f.write("# AFCC Evidence Freshness Audit\n\n")
        f.write(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Findings\n\n")
        for finding in findings:
            f.write(f"{finding}\n")

        f.write("\n## Summary\n")
        f.write(f"- Total files analyzed: {len(files)}\n")
        f.write(f"- Date range: {os.path.basename(os.path.dirname(files[0]))} to {os.path.basename(os.path.dirname(files[-1]))}\n")

    print(f"Audit complete. Report written to {REPORT_FILE}")

if __name__ == "__main__":
    audit_files()
