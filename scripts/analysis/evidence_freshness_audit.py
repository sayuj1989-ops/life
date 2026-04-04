import pandas as pd
import glob
import os
import json
from datetime import datetime

def run_audit():
    files = sorted(glob.glob("outputs/afcc/*/metrics.csv"))
    if not files:
        print("No files found.")
        return

    print(f"Found {len(files)} metrics files.")

    audit_results = {
        "identical_runs": [],
        "missing_links": [],
        "schema_drifts": []
    }

    prev_df = None
    prev_file = None
    prev_columns = None

    for file in files:
        date_str = file.split('/')[-2]

        # Check linked outputs
        expected_summary = f"outputs/afcc/{date_str}/summary.md"
        if not os.path.exists(expected_summary):
            audit_results["missing_links"].append(f"Missing summary.md for run {date_str}")

        try:
            df = pd.read_csv(file)
            current_columns = set(df.columns)

            # Check schema drift
            if prev_columns is not None:
                added = current_columns - prev_columns
                removed = prev_columns - current_columns
                if added or removed:
                    drift_info = {"run": date_str, "added": list(added), "removed": list(removed)}
                    audit_results["schema_drifts"].append(drift_info)

            prev_columns = current_columns

            # Check for identical values
            if prev_df is not None:
                common_genes = set(df['gene_symbol']).intersection(set(prev_df['gene_symbol']))
                if common_genes:
                    df_common = df[df['gene_symbol'].isin(common_genes)].set_index('gene_symbol')
                    prev_df_common = prev_df[prev_df['gene_symbol'].isin(common_genes)].set_index('gene_symbol')

                    identical_count = 0
                    for gene in common_genes:
                        try:
                            if df_common.loc[gene, 'anisotropy_index'] == prev_df_common.loc[gene, 'anisotropy_index'] and \
                               df_common.loc[gene, 'plddt_mean'] == prev_df_common.loc[gene, 'plddt_mean']:
                                identical_count += 1
                        except:
                            pass

                    if identical_count == len(common_genes) and identical_count > 0:
                        audit_results["identical_runs"].append(f"{date_str} completely reuses values from {prev_file.split('/')[-2]} for {identical_count} overlapping genes")
                    elif identical_count > 0:
                        audit_results["identical_runs"].append(f"{date_str} reuses values from {prev_file.split('/')[-2]} for {identical_count} out of {len(common_genes)} overlapping genes")

            prev_df = df
            prev_file = file
        except Exception as e:
            print(f"Error processing {file}: {e}")

    with open("reports/evidence_freshness_audit.md", "w") as f:
        f.write("# Evidence Freshness Audit\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")

        f.write("## 1. Identical Per-Gene Vectors Across Runs\n")
        f.write("Many runs appear to simply reuse data from previous runs without computing new structure predictions, resulting in artificial inflation of report counts without new evidence.\n\n")
        for item in audit_results["identical_runs"]:
            f.write(f"- {item}\n")

        f.write("\n## 2. Missing Linked Outputs\n")
        if not audit_results["missing_links"]:
            f.write("No missing linked outputs found.\n")
        else:
            for item in audit_results["missing_links"]:
                f.write(f"- {item}\n")

        f.write("\n## 3. Schema Drifts\n")
        if not audit_results["schema_drifts"]:
            f.write("No schema drifts found.\n")
        else:
            for item in audit_results["schema_drifts"]:
                f.write(f"- Run {item['run']}:\n")
                if item['added']: f.write(f"  - Added: {', '.join(item['added'])}\n")
                if item['removed']: f.write(f"  - Removed: {', '.join(item['removed'])}\n")

run_audit()
