import os
import pandas as pd
import glob

def run_audit():
    afcc_dirs = sorted(glob.glob('outputs/afcc/2026-*'))
    audit_data = []

    for d in afcc_dirs:
        csv_file = os.path.join(d, 'metrics.csv')
        date_str = os.path.basename(d)
        if os.path.exists(csv_file):
            try:
                df = pd.read_csv(csv_file)
                audit_data.append({'date': date_str, 'df': df})
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")

    if not audit_data:
        print("No metrics.csv files found.")
        return

    # Check for identical vectors across runs
    gene_history = {}
    schema_drifts = []
    missing_outputs = []
    reused_reports = []

    # Detect schema drifts by tracking columns
    first_columns = set(audit_data[0]['df'].columns)

    for entry in audit_data:
        date = entry['date']
        df = entry['df']

        # Schema drift
        curr_columns = set(df.columns)
        if curr_columns != first_columns:
            schema_drifts.append(f"Date {date} has different columns.")

        for _, row in df.iterrows():
            if 'gene_symbol' not in row:
                if 'Identity' in row:
                    gene = row['Identity'].split(' ')[0]
                else:
                    continue
            else:
                gene = row['gene_symbol']

            anisotropy_col = 'anisotropy_index' if 'anisotropy_index' in row else 'Anisotropy' if 'Anisotropy' in row else None
            plddt_col = 'plddt_mean' if 'plddt_mean' in row else 'pLDDT_mean' if 'pLDDT_mean' in row else None
            pae_col = 'PAE_domain_blockiness_score' if 'PAE_domain_blockiness_score' in row else 'PAE_blockiness' if 'PAE_blockiness' in row else None

            metrics = {
                'anisotropy_index': row[anisotropy_col] if anisotropy_col else None,
                'plddt_mean': row[plddt_col] if plddt_col else None,
                'PAE_domain_blockiness_score': row[pae_col] if pae_col else None
            }
            if gene not in gene_history:
                gene_history[gene] = []
            gene_history[gene].append({'date': date, 'metrics': metrics})

    # Flag reused metrics
    reused_flags = []
    for gene, history in gene_history.items():
        if len(history) < 2:
            continue
        first = history[0]
        last = history[-1]

        all_same = True
        for i in range(1, len(history)):
            if history[i]['metrics'] != history[i-1]['metrics']:
                all_same = False
                break

        if all_same:
            reused_flags.append({
                'gene': gene,
                'runs': len(history),
                'first_date': first['date'],
                'last_date': last['date'],
                'anisotropy': first['metrics']['anisotropy_index'],
                'plddt': first['metrics']['plddt_mean']
            })

        # Reused reports per-gene values (unchanged vectors)
        for i in range(1, len(history)):
            prev = history[i-1]['metrics']
            curr = history[i]['metrics']
            if prev == curr:
                reused_reports.append({
                    'gene': gene,
                    'date': history[i]['date'],
                    'prev_date': history[i-1]['date']
                })

    # Missing Outputs Detection (Check reports/afcc_latest.md for dangling links)
    if os.path.exists('reports/afcc_latest.md'):
        with open('reports/afcc_latest.md', 'r') as f:
            content = f.read()
            for d in afcc_dirs:
                date_str = os.path.basename(d)
                if date_str in content and not os.path.exists(os.path.join(d, 'metrics.csv')):
                    missing_outputs.append(f"Missing metrics.csv for linked date: {date_str}")

    # Generate Report
    os.makedirs('reports', exist_ok=True)
    with open('reports/evidence_freshness_audit.md', 'w') as f:
        f.write('# Evidence Freshness Audit Report\n\n')
        f.write('## Data Integrity and Freshness\n\n')
        f.write(f'- **Runs Audited**: {len(audit_data)}\n')

        f.write(f'- **Missing Linked Outputs**: {len(missing_outputs)}\n')
        for output in missing_outputs:
            f.write(f"  - {output}\n")

        f.write(f'- **Schema Drifts**: {len(schema_drifts)}\n')
        for drift in schema_drifts:
            f.write(f"  - {drift}\n")
        f.write('\n')

        f.write('## Identical Per-Gene Vectors Across Runs (Static Metrics)\n\n')
        f.write('The following genes have identical metrics (anisotropy, pLDDT, PAE blockiness) across multiple runs, indicating reused static inputs rather than fresh measurements:\n\n')
        f.write('| Gene | Runs Present | First Date | Last Date | Anisotropy | pLDDT |\n')
        f.write('|------|--------------|------------|-----------|------------|-------|\n')

        reused_flags.sort(key=lambda x: x['runs'], reverse=True)
        for flag in reused_flags:
            f.write(f"| {flag['gene']} | {flag['runs']} | {flag['first_date']} | {flag['last_date']} | {flag['anisotropy']} | {flag['plddt']} |\n")

        f.write('\n## Reused Reports (Unchanged per-gene values)\n\n')
        reused_reports_summary = {}
        for r in reused_reports:
            key = r['date']
            if key not in reused_reports_summary:
                reused_reports_summary[key] = []
            reused_reports_summary[key].append(r['gene'])

        for date, genes in reused_reports_summary.items():
            f.write(f"- **{date}**: Reused identical vectors for {len(genes)} genes (e.g., {', '.join(genes[:3])}{'...' if len(genes) > 3 else ''})\n")

if __name__ == '__main__':
    run_audit()
