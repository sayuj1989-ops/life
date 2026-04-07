import os
import pandas as pd
import glob

def audit_freshness(base_dir='outputs/afcc'):
    dates = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('2026')])

    schema_drift = []
    missing_metrics = []
    identical_vectors = []

    # Audit logic
    previous_data = {} # {gene_symbol: {metrics}}

    for date in dates:
        csv_path = os.path.join(base_dir, date, 'metrics.csv')
        if not os.path.exists(csv_path):
            missing_metrics.append(date)
            continue

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            continue

        cols = df.columns.tolist()

        # Schema drift check
        gene_col = None
        if 'gene_symbol' in cols:
            gene_col = 'gene_symbol'
        elif 'Gene' in cols:
            gene_col = 'Gene'
            schema_drift.append((date, 'Used "Gene" instead of "gene_symbol"'))
        else:
            schema_drift.append((date, f'Missing gene identifier. Columns: {cols[:5]}'))
            continue

        # Reused identical per-gene vectors check
        current_data = {}
        for _, row in df.iterrows():
            gene = row[gene_col]
            metrics = {
                'anisotropy_index': row.get('anisotropy_index', row.get('anisotropy')),
                'plddt_mean': row.get('pLDDT_mean', row.get('plddt_mean'))
            }
            current_data[gene] = metrics

            if gene in previous_data:
                prev = previous_data[gene]
                if pd.notna(metrics['anisotropy_index']) and pd.notna(prev['anisotropy_index']) and metrics['anisotropy_index'] == prev['anisotropy_index']:
                    if pd.notna(metrics['plddt_mean']) and pd.notna(prev['plddt_mean']) and metrics['plddt_mean'] == prev['plddt_mean']:
                        identical_vectors.append({'date': date, 'gene': gene, 'anisotropy': metrics['anisotropy_index'], 'plddt': metrics['plddt_mean']})

        previous_data = current_data

    # Generate report
    report_path = 'reports/evidence_freshness_audit.md'
    os.makedirs('reports', exist_ok=True)
    with open(report_path, 'w') as f:
        f.write("# Evidence Freshness Audit\n\n")
        f.write("## Overview\n")
        f.write("Audit of AFCC run history to detect reused/static metrics, schema drifts, and missing outputs.\n\n")

        f.write("## Missing Outputs\n")
        if missing_metrics:
            for d in missing_metrics:
                f.write(f"- {d}: Missing metrics.csv\n")
        else:
            f.write("- No missing metrics.csv files found.\n")
        f.write("\n")

        f.write("## Schema Drifts\n")
        if schema_drift:
            for d, issue in schema_drift:
                f.write(f"- {d}: {issue}\n")
        else:
            f.write("- No schema drifts found.\n")
        f.write("\n")

        f.write("## Identical Per-Gene Vectors Across Runs\n")
        if identical_vectors:
            df_identical = pd.DataFrame(identical_vectors)
            counts = df_identical.groupby('gene').size().sort_values(ascending=False).head(20)
            f.write("Warning: The following genes exhibit identical structural metrics (anisotropy and pLDDT) across consecutive dates, suggesting cached/static reuse rather than fresh analysis.\n\n")
            f.write("| Gene | Consecutive Reuses | Example Anisotropy | Example pLDDT |\n")
            f.write("|---|---|---|---|\n")
            for gene, count in counts.items():
                example = df_identical[df_identical['gene'] == gene].iloc[0]
                f.write(f"| {gene} | {count} | {example['anisotropy']} | {example['plddt']} |\n")
        else:
            f.write("- No identically reused metrics vectors found.\n")

if __name__ == "__main__":
    audit_freshness()
