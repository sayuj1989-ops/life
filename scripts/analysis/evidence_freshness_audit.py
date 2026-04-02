import os
import pandas as pd
from pathlib import Path

def run_audit():
    afcc_dir = Path('outputs/afcc')

    # Get all dated directories
    date_dirs = sorted([d for d in afcc_dir.iterdir() if d.is_dir() and d.name.startswith('2026-')])

    # Audit for reused metrics
    all_data = []
    schemas = []

    for d in date_dirs:
        metrics_file = d / 'metrics.csv'
        if metrics_file.exists():
            df = pd.read_csv(metrics_file)
            df['run_date'] = d.name

            schemas.append({
                'run_date': d.name,
                'columns': set(df.columns.drop('run_date')) # Exclude run_date we just added
            })

            # Check for linked outputs
            df['has_summary'] = (d / 'summary.md').exists()
            df['has_failure'] = (d / 'failure.md').exists()

            all_data.append(df)

    if not all_data:
        return "No metrics files found"

    combined = pd.concat(all_data, ignore_index=True)

    # Generate Markdown Report
    report = "# Evidence Freshness and Integrity Audit\n\n"
    report += "## 1. Reused Metrics Analysis\n"
    report += "This section flags when 'new' reports reuse unchanged per-gene vectors from previous runs.\n\n"
    report += "| Gene | Total Runs | Unique Anisotropy | Unique pLDDT | Status |\n"
    report += "|------|------------|-------------------|--------------|--------|\n"

    # Check all genes present in the dataset
    all_genes = combined['gene_symbol'].unique()

    static_genes = 0
    updated_genes = 0

    for gene in sorted(all_genes):
        gene_data = combined[combined['gene_symbol'] == gene].sort_values('run_date')
        if not gene_data.empty:
            num_runs = len(gene_data)
            unique_aniso = gene_data['anisotropy_index'].nunique()
            unique_plddt = gene_data['plddt_mean'].nunique()

            if num_runs > 1: # Only report genes present in multiple runs
                if unique_aniso == 1 and unique_plddt == 1:
                    status = "STATIC REUSE"
                    static_genes += 1
                else:
                    status = "UPDATED"
                    updated_genes += 1
                report += f"| {gene} | {num_runs} | {unique_aniso} | {unique_plddt} | {status} |\n"

    report += f"\n**Summary:** Out of genes tracked across multiple runs, {static_genes} are completely static across key metrics, and {updated_genes} have been updated.\n"

    report += "\n## 2. Missing Linked Outputs\n"
    report += "Flagging runs where expected outputs are missing.\n\n"
    report += "| Run Date | Missing summary.md | Missing failure.md |\n"
    report += "|----------|--------------------|--------------------|\n"

    for d in date_dirs:
        missing_summary = not (d / 'summary.md').exists()
        missing_failure = not (d / 'failure.md').exists()
        if missing_summary or missing_failure:
             report += f"| {d.name} | {missing_summary} | {missing_failure} |\n"

    report += "\n## 3. Schema Drift\n"
    report += "Analyzing differences in columns across run dates.\n\n"

    base_schema = schemas[0]['columns']
    drift_detected = False

    for s in schemas[1:]:
        missing_cols = base_schema - s['columns']
        extra_cols = s['columns'] - base_schema
        if missing_cols or extra_cols:
            drift_detected = True
            report += f"- **{s['run_date']} Drift:** "
            if missing_cols:
                report += f"Missing base columns ({', '.join(missing_cols)}). "
            if extra_cols:
                report += f"Extra columns added ({', '.join(extra_cols)})."
            report += "\n"

    if not drift_detected:
        report += "No schema drift detected. All columns consistent across runs.\n"

    with open('reports/evidence_freshness_audit.md', 'w') as f:
        f.write(report)

run_audit()
