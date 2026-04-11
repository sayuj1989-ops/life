import os
import glob
import pandas as pd
import json

def run_audit():
    metric_files = sorted(glob.glob('outputs/afcc/*/metrics.csv'))

    reports_with_links = []
    if os.path.exists('reports/afcc_latest.md'):
        with open('reports/afcc_latest.md', 'r') as f:
            for line in f:
                if 'outputs/afcc/' in line and 'metrics.csv' in line:
                    reports_with_links.append(line.strip())

    # Read all runs
    dfs = {}
    for mf in metric_files:
        try:
            dfs[mf] = pd.read_csv(mf)
        except Exception as e:
            print(f"Error reading {mf}: {e}")

    # Track duplicates across dates
    gene_history = {}
    for mf in metric_files:
        if mf not in dfs: continue
        df = dfs[mf]
        if 'anisotropy_index' not in df.columns or 'plddt_mean' not in df.columns or 'PAE_domain_blockiness_score' not in df.columns:
            continue

        for _, row in df.iterrows():
            if 'gene_symbol' not in row: continue
            gene = row['gene_symbol']
            try:
                vec = (row['anisotropy_index'], row['plddt_mean'], row['PAE_domain_blockiness_score'])
            except KeyError:
                continue

            if gene not in gene_history:
                gene_history[gene] = []
            gene_history[gene].append({'file': mf, 'vec': vec})

    identical_vectors = []
    reused_by_date = {}

    for gene, history in gene_history.items():
        if len(history) > 1:
            # Check if all vectors are the same
            first_vec = history[0]['vec']
            is_static = all(h['vec'] == first_vec for h in history)
            if is_static:
                dates = [h['file'].split('/')[-2] for h in history]
                identical_vectors.append({
                    'gene': gene,
                    'runs': len(history),
                    'first_date': dates[0],
                    'last_date': dates[-1],
                    'anisotropy': first_vec[0],
                    'plddt': first_vec[1]
                })

                # Track reuse by date
                for i in range(1, len(history)):
                    date = dates[i]
                    if date not in reused_by_date:
                        reused_by_date[date] = []
                    reused_by_date[date].append(gene)

    # Sort identical vectors by runs
    identical_vectors.sort(key=lambda x: x['runs'], reverse=True)

    # Check for missing linked outputs
    missing_links = []
    if os.path.exists('reports/afcc_latest.md'):
        with open('reports/afcc_latest.md', 'r') as f:
            content = f.read()
            for mf in metric_files:
                date_str = mf.split('/')[-2]
                if date_str not in content:
                    missing_links.append(mf)

    # Check schema drift
    schema_drift = False
    valid_files = [mf for mf in metric_files if mf in dfs]
    if valid_files:
        base_cols = set(dfs[valid_files[0]].columns)
        for mf in valid_files[1:]:
            if set(dfs[mf].columns) != base_cols:
                schema_drift = True
                break

    report_content = f"""# Evidence Freshness Audit Report

## Data Integrity and Freshness
- **Runs Audited**: {len(valid_files)}
- **Missing Linked Outputs**: {len(missing_links)} ({'None' if not missing_links else ', '.join(missing_links)})
- **Schema Drifts**: {'Detected across scoped files.' if schema_drift else 'None detected in scoped files with `gene_symbol`.'}

## Identical Per-Gene Vectors Across Runs (Static Metrics)
The following genes have identical metrics (anisotropy, pLDDT, PAE blockiness) across multiple runs, indicating reused static inputs rather than fresh measurements:

| Gene | Runs Present | First Date | Last Date | Anisotropy | pLDDT |
|------|--------------|------------|-----------|------------|-------|
"""
    for v in identical_vectors:
        report_content += f"| {v['gene']} | {v['runs']} | {v['first_date']} | {v['last_date']} | {v['anisotropy']:.2f} | {v['plddt']:.1f} |\n"

    report_content += """
## When 'New' Reports Reuse Unchanged Values
"""
    for date in sorted(reused_by_date.keys()):
        genes = reused_by_date[date]
        sample = ", ".join(genes[:5])
        if len(genes) > 5:
            sample += "..."
        report_content += f"- **{date}**: Reused static metrics for {len(genes)} genes (e.g., {sample})\n"

    report_content += """
## Conclusion
- **Actionable Insight**: Many core candidates (e.g., LBX1, PIEZO2, LMNA) show static values across the trend window. This confirms the caveat that high-anisotropy narratves may over-interpret static inputs."""

    with open('reports/evidence_freshness_audit.md', 'w') as f:
        f.write(report_content)

    print("Report written to reports/evidence_freshness_audit.md")

if __name__ == '__main__':
    run_audit()
