import pandas as pd
import glob
import os
from pathlib import Path

def run_audit():
    # Load all metrics.csv across run history
    metrics_files = sorted(glob.glob('outputs/afcc/20*/metrics.csv'))

    audit_log = []

    gene_history = {}
    schema_history = {}

    for mf in metrics_files:
        path = Path(mf)
        run_date = path.parent.name

        # Check missing linked outputs (summary.md)
        summary_path = path.parent / 'summary.md'
        if not summary_path.exists():
            audit_log.append(f"MISSING OUTPUT: {run_date} lacks summary.md")

        df = pd.read_csv(mf)

        # Schema drift check
        current_schema = set(df.columns)
        if not schema_history:
            schema_history['canonical'] = current_schema
            schema_history['last_date'] = run_date
        elif current_schema != schema_history['canonical']:
            missing = schema_history['canonical'] - current_schema
            extra = current_schema - schema_history['canonical']
            audit_log.append(f"SCHEMA DRIFT: {run_date} differs from canonical. Missing: {missing}, Extra: {extra}")

        for idx, row in df.iterrows():
            if 'gene_symbol' not in row and 'Identity' not in row:
                continue

            gene = row.get('gene_symbol', row.get('Identity', 'Unknown'))
            if '(' in gene: # e.g. PIEZO2 (Q9H5I5)
                gene = gene.split(' ')[0]

            aniso = row.get('anisotropy_index', row.get('anisotropy', row.get('Anisotropy', 0)))
            plddt = row.get('plddt_mean', row.get('mean_plddt', row.get('pLDDT_mean', 0)))
            pae_block = row.get('PAE_domain_blockiness_score', row.get('pae_blockiness', row.get('PAE_blockiness', 0)))

            metrics = (round(float(aniso), 2) if pd.notna(aniso) else 0,
                       round(float(plddt), 1) if pd.notna(plddt) else 0,
                       round(float(pae_block), 2) if pd.notna(pae_block) else 0)

            if gene not in gene_history:
                gene_history[gene] = {'last_seen': run_date, 'metrics': metrics, 'static_since': run_date}
            else:
                if gene_history[gene]['metrics'] == metrics:
                    audit_log.append(f"STATIC VECTOR: {run_date}: {gene} reused unchanged metrics from {gene_history[gene]['static_since']}")
                else:
                    gene_history[gene] = {'last_seen': run_date, 'metrics': metrics, 'static_since': run_date}
                    audit_log.append(f"VECTOR UPDATED: {run_date}: {gene} metrics updated")

    # Generate Markdown Report
    os.makedirs('reports', exist_ok=True)
    with open('reports/evidence_freshness_audit.md', 'w') as f:
        f.write("# Evidence Freshness Audit\n\n")
        f.write("## Overview\n")
        f.write("This audit flags when new AFCC summaries are generated from unchanged per-gene metrics across run history, checks for missing outputs, and identifies schema drifts.\n\n")
        f.write("## Log\n")
        for log in audit_log:
            f.write(f"- {log}\n")

    print("Audit complete.")

if __name__ == '__main__':
    run_audit()
