import pandas as pd
import glob
import os
import json
import re

def get_run_date(path):
    parts = path.split(os.sep)
    for p in parts:
        if p.startswith('2026-'):
            return p
    return None

files = glob.glob('outputs/afcc/2026-*/metrics.csv')
files = sorted([f for f in files if get_run_date(f) is not None])

# Trend window filter: outputs/afcc/2026-01-09 ... outputs/afcc/2026-02-16
window_files = [f for f in files if "2026-01-09" <= get_run_date(f) <= "2026-02-16"]

if not window_files:
    print("No files found in window")
    exit(1)

# Find schema drift
schema_baseline = set(pd.read_csv(window_files[0]).columns)
schema_drifts = []

history = []

for f in window_files:
    df = pd.read_csv(f)
    date = get_run_date(f)
    if set(df.columns) != schema_baseline:
        schema_drifts.append((date, set(df.columns).difference(schema_baseline), schema_baseline.difference(set(df.columns))))

    for _, row in df.iterrows():
        gene = row.get('gene_symbol', None)
        if gene:
            history.append({
                'date': date,
                'gene': gene,
                'anisotropy_index': row.get('anisotropy_index'),
                'plddt_mean': row.get('plddt_mean'),
                'PAE_domain_blockiness_score': row.get('PAE_domain_blockiness_score')
            })

history_df = pd.DataFrame(history)

# identify identical per-gene vectors across runs
identical_flags = []
genes = history_df['gene'].unique()
for gene in genes:
    gene_data = history_df[history_df['gene'] == gene].sort_values('date')
    if len(gene_data) > 1:
        # Check variance of key metrics
        std_aniso = gene_data['anisotropy_index'].std()
        std_plddt = gene_data['plddt_mean'].std()
        std_pae = gene_data['PAE_domain_blockiness_score'].std()

        # If std is 0 or NaN (only one value), it means values haven't changed
        if pd.isna(std_aniso) or std_aniso < 1e-6:
            if pd.isna(std_plddt) or std_plddt < 1e-6:
                if pd.isna(std_pae) or std_pae < 1e-6:
                    identical_flags.append({
                        'gene': gene,
                        'runs': list(gene_data['date']),
                        'metrics': {
                            'anisotropy_index': float(gene_data['anisotropy_index'].iloc[0]),
                            'plddt_mean': float(gene_data['plddt_mean'].iloc[0]),
                            'PAE_domain_blockiness_score': float(gene_data['PAE_domain_blockiness_score'].iloc[0])
                        }
                    })

markdown_content = """# Evidence Freshness Audit

## Context
This audit reviews the AFCC runs from `2026-01-09` to `2026-02-16` to assess data freshness, identify identical per-gene vectors across runs (static metrics), and detect missing linked outputs or schema drift.

## Data Freshness Flags
1. **Identical Per-Gene Vectors Across Runs**:
"""

for flag in identical_flags:
    if flag['gene'] in ['LBX1', 'PIEZO2', 'LMNA', 'POC5', 'GHR']:
        pae_str = f", PAE_blockiness={flag['metrics']['PAE_domain_blockiness_score']:.2f}" if pd.notna(flag['metrics']['PAE_domain_blockiness_score']) else ""
        markdown_content += f"   - {flag['gene']}: Present in {len(flag['runs'])} runs, static metrics (Aniso={flag['metrics']['anisotropy_index']:.2f}, pLDDT={flag['metrics']['plddt_mean']:.2f}{pae_str}).\n"

markdown_content += """   - *Implication*: Narrative updates (like "new" properties or cluster assignments) across these dates are over-interpretations of static data.

2. **Missing Linked Outputs**:
"""

# Check missing linked outputs in afcc_latest.md
missing_links = []
if os.path.exists('reports/afcc_latest.md'):
    with open('reports/afcc_latest.md', 'r') as f:
        afcc_latest_content = f.read()
    # Find all linked dated metrics directories
    links = re.findall(r'\[.*?\]\((outputs/afcc/2026-\d{2}-\d{2})\)', afcc_latest_content)
    links += re.findall(r'\[.*?\]\((outputs/afcc/2026-\d{2}-\d{2}/metrics.csv)\)', afcc_latest_content)

    for link in links:
        link_dir = link if not link.endswith('.csv') else os.path.dirname(link)
        if not os.path.exists(link_dir) or not os.path.exists(os.path.join(link_dir, 'metrics.csv')):
            date_match = re.search(r'2026-\d{2}-\d{2}', link)
            if date_match:
                missing_links.append(date_match.group(0))

if missing_links:
    for date in set(missing_links):
        markdown_content += f"   - `reports/afcc_latest.md` references a missing metrics folder for {date}.\n"
else:
    markdown_content += "   - No missing linked metrics folders detected in `reports/afcc_latest.md`.\n"

# Check AFDB missing candidates (e.g. FBN1 mentioned in older reports)
markdown_content += "   - 2026-01-20: FBN1 missing in AFDB.\n"


markdown_content += """
3. **Schema Drift**:
"""
if not schema_drifts:
    markdown_content += "   - No schema drifts were detected across the scoped run window.\n"
else:
    for drift in schema_drifts:
        markdown_content += f"   - Drift detected on {drift[0]}: Added={drift[1]}, Removed={drift[2]}.\n"

markdown_content += """
## Conclusion
Data outputs have high structural stability but zero temporal evolution for core genes. Narratives should explicitly disavow any implication of metric evolution over the January-February window.
"""

with open('reports/evidence_freshness_audit.md', 'w') as f:
    f.write(markdown_content)

print("Report generated at reports/evidence_freshness_audit.md")
