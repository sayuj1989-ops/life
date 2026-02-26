import os
import pandas as pd
import glob
from datetime import datetime

def audit_evidence_freshness(output_dir="outputs/afcc", report_path="reports/evidence_freshness_audit.md"):
    """
    Audits AFCC output directories for static metric vectors across dates.
    """

    # 1. Find all metrics.csv files
    metric_files = glob.glob(os.path.join(output_dir, "2026-*", "metrics.csv"))
    metric_files.sort()

    if not metric_files:
        print(f"No metrics files found in {output_dir}")
        return

    print(f"Found {len(metric_files)} metrics files to audit.")

    # 2. Load data
    data = []
    for f in metric_files:
        try:
            date_str = os.path.basename(os.path.dirname(f))
            df = pd.read_csv(f)
            # Normalize column names if needed (handle potential case sensitivity)
            df.columns = [c.lower() for c in df.columns]

            # Extract key metrics
            if 'gene_symbol' in df.columns: # standardized
                gene_col = 'gene_symbol'
            elif 'identity' in df.columns: # some older files might use identity
                gene_col = 'identity'
                # clean identity to gene symbol if format is "GENE (UNIPROT)"
                df['gene_symbol'] = df['identity'].apply(lambda x: x.split(' ')[0] if '(' in str(x) else str(x))
                gene_col = 'gene_symbol'
            else:
                print(f"Skipping {f}: No gene/identity column found.")
                continue

            # Ensure necessary columns exist
            req_cols = ['anisotropy_index', 'plddt_mean', 'pae_domain_blockiness_score']

            # Map variations
            column_mapping = {
                'anisotropy': 'anisotropy_index',
                'mean_plddt': 'plddt_mean',
                'pae_blockiness': 'pae_domain_blockiness_score'
            }

            df.rename(columns=column_mapping, inplace=True)

            available_cols = [c for c in req_cols if c in df.columns]

            for _, row in df.iterrows():
                entry = {
                    'date': date_str,
                    'gene': row[gene_col],
                    'file': f
                }
                for c in available_cols:
                    entry[c] = row[c]
                data.append(entry)
        except Exception as e:
            print(f"Error reading {f}: {e}")

    df_all = pd.DataFrame(data)

    # 3. Analyze for static vectors
    report_lines = []
    report_lines.append("# Evidence Freshness Audit Report")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Scope: {len(metric_files)} runs from {df_all['date'].min()} to {df_all['date'].max()}")
    report_lines.append("")

    report_lines.append("## Static Metric Vectors (Zombie Trends)")
    report_lines.append("The following genes have identical metrics across multiple runs, indicating data reuse rather than new biological simulation.")
    report_lines.append("")

    genes = df_all['gene'].unique()
    static_count = 0

    for gene in sorted(genes):
        gene_df = df_all[df_all['gene'] == gene].sort_values('date')
        if len(gene_df) < 2:
            continue

        # Check variance in key metrics
        # We look for identical values in floating point columns
        # If std dev is 0 (or very close), it's static.

        metrics_to_check = ['anisotropy_index', 'plddt_mean']
        is_static = True

        variances = {}
        for m in metrics_to_check:
            if m in gene_df.columns:
                if gene_df[m].nunique() > 1:
                    is_static = False
                    variances[m] = gene_df[m].std()
                else:
                    variances[m] = 0.0

        if is_static:
            static_count += 1
            first_date = gene_df['date'].iloc[0]
            last_date = gene_df['date'].iloc[-1]
            count = len(gene_df)

            # Format sample metric
            sample_aniso = gene_df['anisotropy_index'].iloc[0] if 'anisotropy_index' in gene_df.columns else "N/A"

            report_lines.append(f"### {gene}")
            report_lines.append(f"- **Status**: Static (identical metrics)")
            report_lines.append(f"- **Range**: {first_date} to {last_date} ({count} runs)")
            report_lines.append(f"- **Anisotropy**: {sample_aniso}")
            report_lines.append(f"- **Evidence**: Metrics vectors are bit-for-bit identical.")
            report_lines.append("")

    report_lines.append(f"**Total Static Genes Detected**: {static_count} / {len(genes)}")
    report_lines.append("")

    report_lines.append("## Freshness Summary")
    report_lines.append("| Gene | Runs | Unique Vectors | Freshness Score |")
    report_lines.append("|---|---|---|---|")

    for gene in sorted(genes):
        gene_df = df_all[df_all['gene'] == gene]
        n_runs = len(gene_df)

        # Count unique vectors based on combined key metrics
        # We create a tuple of the metrics to count unique combinations
        cols_for_unique = [c for c in ['anisotropy_index', 'plddt_mean', 'pae_domain_blockiness_score'] if c in gene_df.columns]
        n_unique = gene_df[cols_for_unique].drop_duplicates().shape[0]

        freshness = n_unique / n_runs if n_runs > 0 else 0

        report_lines.append(f"| {gene} | {n_runs} | {n_unique} | {freshness:.2f} |")

    # Write report
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))

    print(f"Report written to {report_path}")

if __name__ == "__main__":
    audit_evidence_freshness()
