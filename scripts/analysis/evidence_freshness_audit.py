import os
import glob
import pandas as pd
from datetime import datetime
import re

def run_audit():
    print("Running Evidence Freshness Audit...")

    afcc_dir = "outputs/afcc/"
    reports_dir = "reports/structure_clusters/"

    metrics_files = sorted(glob.glob(os.path.join(afcc_dir, "2026-*", "metrics.csv")))

    df_list = []
    schemas = []

    schema_drifts = []
    base_schema = None

    for f in metrics_files:
        date_str = f.split("/")[-2]
        try:
            df = pd.read_csv(f)
            df['run_date'] = date_str
            df_list.append(df)

            schema = list(df.columns)
            if base_schema is None:
                base_schema = schema
            elif schema != base_schema:
                schema_drifts.append((date_str, list(set(schema) ^ set(base_schema))))
        except Exception as e:
            print(f"Warning: Could not read {f}: {e}")

    if not df_list:
        print("No data found.")
        return

    all_data = pd.concat(df_list, ignore_index=True)

    genes_to_check = all_data['gene_symbol'].dropna().unique()

    audit_report = [
        "# Evidence Freshness Audit",
        f"**Date Generated:** {datetime.now().strftime('%Y-%m-%d')}",
        "**Author:** Data Integrity Checker",
        ""
    ]

    audit_report.append("## Schema Integrity")
    if not schema_drifts:
        audit_report.append("- No schema drift detected across metrics files.")
    else:
        for date, diff in schema_drifts:
            audit_report.append(f"- 🔴 Schema drift detected in {date}: Diff={diff}")
    audit_report.append("")

    audit_report.append("## Core Gene Freshness")
    audit_report.append("Checks for identical per-gene vectors across runs to prevent treating static AlphaFold snapshots as evolving structural states.")
    audit_report.append("")

    static_count = 0
    total_checked = 0

    static_genes = set()

    for gene in genes_to_check:
        gene_data = all_data[all_data['gene_symbol'] == gene].dropna(subset=['anisotropy_index', 'plddt_mean'])
        if gene_data.empty:
            continue

        anisotropy_vals = gene_data['anisotropy_index'].unique()
        plddt_vals = gene_data['plddt_mean'].unique()

        runs_count = len(gene_data)
        if runs_count <= 1:
            continue

        total_checked += 1
        is_static = len(anisotropy_vals) == 1 and len(plddt_vals) == 1

        if is_static:
            static_genes.add(gene)
            static_count += 1
            status = "🔴 STATIC (reused)"
            audit_report.append(f"### {gene}")
            audit_report.append(f"- Status: {status}")
            audit_report.append(f"- Runs detected: {runs_count}")
            audit_report.append(f"- Static values: Anisotropy={anisotropy_vals[0]:.2f}, pLDDT={plddt_vals[0]:.1f}")
            audit_report.append("")

    audit_report.append(f"Summary: {static_count}/{total_checked} evaluated genes are strictly static across >1 runs.")
    audit_report.append("")

    audit_report.append("## Missing Linked Outputs")
    reports = sorted(glob.glob(os.path.join(reports_dir, "*.md")))
    latest_report = "reports/afcc_latest.md"
    if os.path.exists(latest_report):
        reports.append(latest_report)

    missing_links = []
    for r in reports:
        with open(r, "r") as f:
            content = f.read()
            # find strings matching outputs/afcc/YYYY-MM-DD/something
            links = re.findall(r'outputs/afcc/2026-\d{2}-\d{2}/[^\s\)`]+', content)
            for link in links:
                link = link.strip('`')
                if not os.path.exists(link):
                    missing_links.append((r, link))

    if not missing_links:
        audit_report.append("- No missing linked outputs detected.")
    else:
        for r, link in missing_links:
            audit_report.append(f"- 🔴 Broken link in `{os.path.basename(r)}`: `{link}`")

    audit_report.append("")

    audit_report.append("## Narrative vs Data Drift")
    audit_report.append("Flags instances where structure cluster narratives claim 'new' structural states despite relying on static input vectors.")

    flagged = False
    for r in reports:
        if "cluster_note" not in r:
            continue

        with open(r, "r") as f:
            content = f.read()

            for gene in static_genes:
                if gene in content and ("unfolding" in content.lower() or "strain integration" in content.lower() or "new" in content.lower()):
                    audit_report.append(f"- **Flagged**: `{os.path.basename(r)}` mentions static gene `{gene}` alongside dynamic/novel claims.")
                    flagged = True
                    break

    if not flagged:
        audit_report.append("- No narrative drift flagged programmatically.")

    audit_report.append("")
    audit_report.append("## Recommendations")
    audit_report.append("1. **Stop interpreting static AlphaFold structural metrics as new insights.** If the input string hasn't changed, the structure hasn't changed.")
    audit_report.append("2. **Implement freshness gates.** The pipeline should hash input arrays and exit early if identical to prior runs.")

    report_path = "reports/evidence_freshness_audit.md"
    with open(report_path, "w") as f:
        f.write("\n".join(audit_report))

    print(f"Audit report written to {report_path}")

if __name__ == "__main__":
    run_audit()
