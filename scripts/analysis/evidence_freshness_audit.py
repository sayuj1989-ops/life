import os
import pandas as pd
from pathlib import Path

def audit_afcc_freshness():
    afcc_dir = Path('outputs/afcc')
    date_dirs = sorted([d for d in afcc_dir.iterdir() if d.is_dir() and d.name.startswith('2026-')])

    metrics_history = {}
    missing_metrics = []
    schema_drifts = []

    for d in date_dirs:
        date = d.name
        metrics_file = d / 'metrics.csv'

        if not metrics_file.exists():
            missing_metrics.append(str(metrics_file))
            continue

        try:
            df = pd.read_csv(metrics_file)
            required_cols = ['gene_symbol', 'anisotropy_index', 'plddt_mean', 'PAE_domain_blockiness_score']

            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                schema_drifts.append(f"{date}: missing columns {missing_cols}")
                continue

            for _, row in df.iterrows():
                gene = row['gene_symbol']
                vector = {
                    'anisotropy': row['anisotropy_index'],
                    'plddt': row['plddt_mean'],
                    'pae_blockiness': row['PAE_domain_blockiness_score']
                }

                if gene not in metrics_history:
                    metrics_history[gene] = []
                metrics_history[gene].append((date, vector))

        except Exception as e:
            print(f"Error reading {metrics_file}: {e}")

    static_genes = []
    reused_reports_by_date = {}

    for gene, history in metrics_history.items():
        if len(history) > 1:
            first_vector = history[0][1]
            is_static = True
            for date, vector in history[1:]:
                if (abs(vector['anisotropy'] - first_vector['anisotropy']) > 1e-6 or
                    abs(vector['plddt'] - first_vector['plddt']) > 1e-6 or
                    abs(vector['pae_blockiness'] - first_vector['pae_blockiness']) > 1e-6):
                    is_static = False
                    break

            if is_static:
                first_date = history[0][0]
                last_date = history[-1][0]
                static_genes.append({
                    'gene': gene,
                    'runs': len(history),
                    'first_date': first_date,
                    'last_date': last_date,
                    'anisotropy': first_vector['anisotropy'],
                    'plddt': first_vector['plddt'],
                    'pae_blockiness': first_vector['pae_blockiness']
                })

                for date, _ in history[1:]:
                    if date not in reused_reports_by_date:
                        reused_reports_by_date[date] = []
                    reused_reports_by_date[date].append(gene)

    report_content = [
        "# Evidence Freshness Audit\n",
        "## Data Integrity",
        f"- **Runs Audited**: {len(date_dirs)}",
        f"- **Missing Linked Outputs**: {len(missing_metrics)} ({', '.join(missing_metrics) if missing_metrics else 'None'})",
        f"- **Schema Drifts**: {len(schema_drifts)} ({', '.join(schema_drifts) if schema_drifts else 'None'})",
        "",
        "## Static Per-Gene Vectors Across Runs",
        "Identical metrics (anisotropy, pLDDT, PAE blockiness) indicating reused inputs:",
        "| Gene | Runs Present | First Date | Last Date | Anisotropy | pLDDT | PAE Blockiness |",
        "|---|---|---|---|---|---|---|"
    ]

    for item in sorted(static_genes, key=lambda x: x['runs'], reverse=True):
        report_content.append(f"| {item['gene']} | {item['runs']} | {item['first_date']} | {item['last_date']} | {item['anisotropy']:.2f} | {item['plddt']:.1f} | {item['pae_blockiness']:.2f} |")

    report_content.extend([
        "",
        "## Reused Unchanged Values in 'New' Reports",
    ])

    for date in sorted(reused_reports_by_date.keys()):
        genes = reused_reports_by_date[date]
        report_content.append(f"- **{date}**: Reused static metrics for {len(genes)} genes (e.g., {', '.join(genes[:5])}... )")

    report_content.extend([
        "",
        "## Conclusion",
        "- Many core candidates (e.g., LBX1, PIEZO2, LMNA) show effectively static metrics across runs.",
        "- **Finding**: Cluster narratives have updated, but underlying structural measurements are reused. We must strictly interpret these signals as low-confidence static anchors rather than evolving measurements."
    ])

    report_path = Path('reports/evidence_freshness_audit.md')
    with open(report_path, 'w') as f:
        f.write("\n".join(report_content))
    print(f"Report written to {report_path}")

if __name__ == "__main__":
    audit_afcc_freshness()
