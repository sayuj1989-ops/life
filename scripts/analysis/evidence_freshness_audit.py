import os
import pandas as pd
import numpy as np
import glob
from pathlib import Path
import datetime

def audit_freshness(base_dir="outputs/afcc"):
    report_lines = []
    report_lines.append("# Evidence Freshness Audit Report")
    report_lines.append(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    metrics_files = sorted(glob.glob(os.path.join(base_dir, "*", "metrics.csv")))

    if not metrics_files:
        report_lines.append("No metrics.csv files found.")
        print("\n".join(report_lines))
        return

    all_data = []
    for f in metrics_files:
        try:
            df = pd.read_csv(f)
            # Extract date from path
            path_parts = Path(f).parts
            run_date = path_parts[-2] # Assuming outputs/afcc/DATE/metrics.csv

            # Check if date is valid format (YYYY-MM-DD)
            try:
                datetime.datetime.strptime(run_date, '%Y-%m-%d')
            except ValueError:
                continue # Skip non-date directories like 'manual_metabolic_update'

            df['run_date'] = run_date
            all_data.append(df)
        except Exception as e:
            report_lines.append(f"- Error reading {f}: {e}")

    if not all_data:
        report_lines.append("No valid date-stamped metrics files found.")
        print("\n".join(report_lines))
        return

    combined_df = pd.concat(all_data, ignore_index=True)

    # Check for identical runs (file hash or content equality)
    # Group by run_date and check if content is identical to previous run
    run_dates = sorted(combined_df['run_date'].unique())

    report_lines.append("## Run-to-Run Consistency Check")
    report_lines.append("| Date | Rows | Columns | Identical to Prev? | Changes |")
    report_lines.append("|---|---|---|---|---|")

    prev_df = None
    prev_date = None

    for date in run_dates:
        current_df = combined_df[combined_df['run_date'] == date].drop(columns=['run_date']).reset_index(drop=True)
        # Sort by gene_symbol to ensure order doesn't affect equality
        if 'gene_symbol' in current_df.columns:
            current_df = current_df.sort_values('gene_symbol').reset_index(drop=True)

        is_identical = False
        changes = "N/A"

        if prev_df is not None:
            # Check if columns are the same
            if set(current_df.columns) != set(prev_df.columns):
                changes = "Schema Drift"
            else:
                # Check if content is identical
                try:
                    pd.testing.assert_frame_equal(current_df, prev_df, check_dtype=False)
                    is_identical = True
                    changes = "None"
                except AssertionError:
                    is_identical = False
                    # Identify what changed
                    # Simple check: number of rows
                    if len(current_df) != len(prev_df):
                        changes = f"Row count: {len(prev_df)} -> {len(current_df)}"
                    else:
                        # Check specific columns for changes
                        diff_cols = []
                        for col in current_df.columns:
                            if not current_df[col].equals(prev_df[col]):
                                diff_cols.append(col)
                        changes = f"Changed cols: {', '.join(diff_cols[:3])}..." if diff_cols else "Value changes"

        report_lines.append(f"| {date} | {len(current_df)} | {len(current_df.columns)} | {is_identical} | {changes} |")

        prev_df = current_df
        prev_date = date

    report_lines.append("")

    # Check for static genes across all runs
    report_lines.append("## Gene-Level Freshness")
    report_lines.append("Checking for genes that have static metrics across multiple runs (indicating potential reuse or lack of update).")

    gene_stats = []

    # Coerce numeric columns to ensure correct min/max calculation
    combined_df['anisotropy_index'] = pd.to_numeric(combined_df['anisotropy_index'], errors='coerce')
    combined_df['plddt_mean'] = pd.to_numeric(combined_df['plddt_mean'], errors='coerce')

    genes = combined_df['gene_symbol'].unique()
    for gene in genes:
        gene_df = combined_df[combined_df['gene_symbol'] == gene].sort_values('run_date')
        if len(gene_df) > 1:
            # Check if anisotropy_index is static (ignoring NaNs for static check if desired, or treating as value)
            # Using dropna() for values to check range
            aniso_vals = gene_df['anisotropy_index'].dropna().unique()
            plddt_vals = gene_df['plddt_mean'].dropna().unique()

            # If after dropna we have values, check if they are all close (float comparison)
            is_static_aniso = False
            if len(aniso_vals) == 0:
                is_static_aniso = True # All NaNs
            elif len(aniso_vals) == 1:
                is_static_aniso = True
            else:
                # Check if all values are close
                if np.allclose(aniso_vals, aniso_vals[0]):
                    is_static_aniso = True

            is_static_plddt = False
            if len(plddt_vals) == 0:
                is_static_plddt = True
            elif len(plddt_vals) == 1:
                is_static_plddt = True
            else:
                 if np.allclose(plddt_vals, plddt_vals[0]):
                    is_static_plddt = True

            status = "Dynamic"
            if is_static_aniso and is_static_plddt:
                status = "Static"

            # Format range
            if len(aniso_vals) > 0:
                aniso_range = f"{min(aniso_vals):.2f}-{max(aniso_vals):.2f}"
            else:
                aniso_range = "NaN"

            gene_stats.append({
                'Gene': gene,
                'Runs': len(gene_df),
                'First_Run': gene_df['run_date'].min(),
                'Last_Run': gene_df['run_date'].max(),
                'Status': status,
                'Anisotropy_Range': aniso_range
            })

    gene_stats_df = pd.DataFrame(gene_stats)

    if not gene_stats_df.empty:
        static_genes = gene_stats_df[gene_stats_df['Status'] == 'Static']
        dynamic_genes = gene_stats_df[gene_stats_df['Status'] == 'Dynamic']

        report_lines.append(f"- Total Genes Tracked: {len(gene_stats_df)}")
        report_lines.append(f"- Static Genes (Unchanged across runs): {len(static_genes)}")
        report_lines.append(f"- Dynamic Genes (Changed at least once): {len(dynamic_genes)}")
        report_lines.append("")

        report_lines.append("### Top 10 Static Genes (Most Runs)")
        report_lines.append(static_genes.sort_values('Runs', ascending=False).head(10).to_markdown(index=False))
        report_lines.append("")

        report_lines.append("### Top 10 Dynamic Genes (Most Variability)")
        # Calculate variance or just list them
        report_lines.append(dynamic_genes.sort_values('Runs', ascending=False).head(10).to_markdown(index=False))

        # Specific check for key candidates
        key_candidates = ['LBX1', 'PIEZO2', 'LMNA', 'POC5', 'GHR']
        report_lines.append("")
        report_lines.append("### Key Candidate Status")
        key_stats = gene_stats_df[gene_stats_df['Gene'].isin(key_candidates)]
        if not key_stats.empty:
            report_lines.append(key_stats.to_markdown(index=False))
        else:
            report_lines.append("None of the key candidates found in multiple runs.")

    # Write report
    report_path = "reports/evidence_freshness_audit.md"
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))

    print(f"Audit complete. Report written to {report_path}")

if __name__ == "__main__":
    audit_freshness()
