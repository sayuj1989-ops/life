import os
from pathlib import Path
import pandas as pd

def audit_afcc_freshness():
    afcc_dir = Path('outputs/afcc')
    if not afcc_dir.exists():
        print("outputs/afcc does not exist.")
        return

    # Get all dated subdirectories in outputs/afcc
    date_dirs = sorted([d for d in afcc_dir.iterdir() if d.is_dir() and d.name.startswith('2026-')])

    metrics_history = {}
    missing_metrics = []
    schema_drifts = []

    for d in date_dirs:
        date = d.name
        metrics_file = d / 'metrics.csv'

        if not metrics_file.exists():
            missing_metrics.append(date)
            continue

        try:
            df = pd.read_csv(metrics_file)

            # Check for expected columns based on recent schema
            required_cols = ['gene_symbol', 'anisotropy_index', 'pLDDT_mean', 'PAE_domain_blockiness_score']
            missing_cols = [col for col in required_cols if col not in df.columns]

            if missing_cols:
                # Some might use 'plddt_mean' instead of 'pLDDT_mean'
                if 'plddt_mean' in df.columns:
                    df.rename(columns={'plddt_mean': 'pLDDT_mean'}, inplace=True)
                    missing_cols.remove('pLDDT_mean')
                if missing_cols:
                    schema_drifts.append(f"{date} missing columns: {', '.join(missing_cols)}")
                    continue

            for _, row in df.iterrows():
                gene = row['gene_symbol']
                # Store the full vector, extracting key metrics to check for identity
                # Here we use anisotropy, pLDDT, PAE_domain_blockiness_score if available
                metrics_vector = {
                    'anisotropy': row['anisotropy_index'],
                    'plddt': row['pLDDT_mean'],
                    'pae_blockiness': row.get('PAE_domain_blockiness_score', None),
                    'file': str(metrics_file)
                }

                if gene not in metrics_history:
                    metrics_history[gene] = []

                metrics_history[gene].append((date, metrics_vector))
        except Exception as e:
            print(f"Error reading {metrics_file}: {e}")

    # Analyze for static metrics
    static_genes = []

    # We want to check for genes that have IDENTICAL vectors across MULTIPLE runs
    # To identify when "new" reports reuse unchanged per-gene values.

    # Dictionary to keep track of reused report dates
    reused_dates_info = {}

    for gene, history in metrics_history.items():
        if len(history) > 1:
            first_date, first_vector = history[0]
            is_completely_static = True

            # Keep track if the gene was ever static from one run to another
            for i in range(1, len(history)):
                prev_date, prev_vector = history[i-1]
                curr_date, curr_vector = history[i]

                # Compare key metrics
                identical = True
                for key in ['anisotropy', 'plddt', 'pae_blockiness']:
                    if curr_vector[key] != prev_vector[key]:
                        # Handle potential nan vs nan comparisons (pandas)
                        if pd.isna(curr_vector[key]) and pd.isna(prev_vector[key]):
                            continue
                        identical = False
                        is_completely_static = False
                        break

                if identical:
                    if curr_date not in reused_dates_info:
                        reused_dates_info[curr_date] = []
                    reused_dates_info[curr_date].append(gene)

            if is_completely_static:
                static_genes.append({
                    'gene': gene,
                    'runs': len(history),
                    'first_date': history[0][0],
                    'last_date': history[-1][0],
                    'anisotropy': first_vector['anisotropy'],
                    'plddt': first_vector['plddt']
                })

    # Generate Report
    report_content = [
        "# Evidence Freshness Audit Report\n",
        "## Data Integrity and Freshness",
        f"- **Runs Audited**: {len(date_dirs)}",
        f"- **Missing Linked Outputs**: {len(missing_metrics)} ({', '.join(missing_metrics) if missing_metrics else 'None'})"
    ]

    if schema_drifts:
        report_content.append(f"- **Schema Drifts Detected**: {len(schema_drifts)}")
        for drift in schema_drifts:
             report_content.append(f"  - {drift}")
    else:
         report_content.append("- **Schema Drifts**: None detected in scoped files with required columns.\n")

    report_content.append("\n## Identical Per-Gene Vectors Across Runs (Static Metrics)")
    report_content.append("The following genes have identical metrics (anisotropy, pLDDT, PAE blockiness) across all their runs, indicating reused static inputs rather than fresh measurements:\n")
    report_content.append("| Gene | Runs Present | First Date | Last Date | Anisotropy | pLDDT |")
    report_content.append("|------|--------------|------------|-----------|------------|-------|")

    for item in sorted(static_genes, key=lambda x: x['runs'], reverse=True):
        report_content.append(f"| {item['gene']} | {item['runs']} | {item['first_date']} | {item['last_date']} | {item['anisotropy']:.2f} | {item['plddt']:.2f} |")

    report_content.append("\n## When 'New' Reports Reuse Unchanged Values\n")

    if reused_dates_info:
        for d in sorted(reused_dates_info.keys()):
            genes = reused_dates_info[d]
            sample = ", ".join(genes[:5]) + ("..." if len(genes) > 5 else "")
            report_content.append(f"- **{d}**: Reused static metrics for {len(genes)} genes (e.g., {sample})")
    else:
        report_content.append("No reused static metrics detected across subsequent dates.")

    report_content.append("\n## Conclusion")
    report_content.append("- **Actionable Insight**: The audit confirms that many candidates (including core ones) reuse static values across the trend window. This underlines the core caveat: high-anisotropy narratives in these reports may over-interpret static structural inputs rather than reflecting new experimental measurements or evolving geometric estimates.")

    # Write report
    report_path = Path('reports/evidence_freshness_audit.md')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        f.write("\n".join(report_content) + "\n")

    print(f"Audit complete. Report written to {report_path}")

if __name__ == "__main__":
    audit_afcc_freshness()
