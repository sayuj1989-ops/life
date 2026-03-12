import os
import pandas as pd
from glob import glob

def get_afcc_files(start_date, end_date):
    dirs = glob("outputs/afcc/2026-*")
    dirs = [d for d in dirs if os.path.basename(d) >= start_date and os.path.basename(d) <= end_date]
    dirs.sort()
    return dirs

def check_freshness(dirs):
    all_data = []
    missing_outputs = []
    schema_issues = []
    expected_columns = None

    report_lines = ["# Evidence Freshness Audit Report", ""]

    for d in dirs:
        date = os.path.basename(d)
        csv_file = os.path.join(d, "metrics.csv")

        # Check for missing linked outputs
        if not os.path.exists(csv_file):
            missing_outputs.append(date)
            continue

        df = pd.read_csv(csv_file)
        df['date'] = date
        all_data.append(df)

        # Check for schema drifts
        if expected_columns is None:
            expected_columns = list(df.columns)
            expected_columns.remove('date') # Remove date as it was added by us
        else:
            current_columns = list(df.columns)
            current_columns.remove('date')
            if current_columns != expected_columns:
                schema_issues.append(date)

    if missing_outputs:
        report_lines.append("## Missing Linked Outputs")
        report_lines.append(f"Metrics missing locally for runs: {', '.join(missing_outputs)}")
        report_lines.append("")

    if schema_issues:
        report_lines.append("## Schema Drifts")
        report_lines.append(f"Schema drift detected in runs: {', '.join(schema_issues)}")
        report_lines.append("")
    else:
        report_lines.append("## Schema Drifts")
        report_lines.append("None detected in scoped files.")
        report_lines.append("")

    if not all_data:
        return "\n".join(report_lines)

    combined = pd.concat(all_data, ignore_index=True)

    # Check for identical per-gene vectors across runs
    report_lines.append("## Static Metric Reuse")
    report_lines.append("Identical per-gene vectors detected across multiple runs:")

    static_found = False

    # Group by gene
    for gene in combined['gene_symbol'].unique():
        gene_data = combined[combined['gene_symbol'] == gene].sort_values('date')

        # Check if the core metrics are identical
        metrics_cols = ['anisotropy_index', 'plddt_mean', 'PAE_domain_blockiness_score']
        # Filter columns that exist
        metrics_cols = [c for c in metrics_cols if c in gene_data.columns]

        if not metrics_cols:
            continue

        is_static = True
        for col in metrics_cols:
            if len(gene_data[col].unique()) > 1:
                is_static = False
                break

        if is_static and len(gene_data) > 1:
            dates = gene_data['date'].tolist()
            report_lines.append(f"- **{gene}**: Metrics static across {len(dates)} runs ({dates[0]} to {dates[-1]}).")
            static_found = True

    if not static_found:
        report_lines.append("- None detected.")

    return "\n".join(report_lines)

if __name__ == "__main__":
    dirs = get_afcc_files("2026-01-09", "2026-02-16")
    report = check_freshness(dirs)

    os.makedirs("reports", exist_ok=True)
    with open("reports/evidence_freshness_audit.md", "w") as f:
        f.write(report)
    print("Audit written to reports/evidence_freshness_audit.md")
