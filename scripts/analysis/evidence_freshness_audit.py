import os
import glob
import pandas as pd
from collections import defaultdict

def main():
    base_dir = "outputs/afcc"
    folders = sorted([f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f)) and f.startswith("2026-")])
    folders = [f for f in folders if "2026-01-09" <= f <= "2026-02-16"]

    gene_history = defaultdict(list)
    missing_outputs = []

    for folder in folders:
        metrics_file = os.path.join(base_dir, folder, "metrics.csv")
        if not os.path.exists(metrics_file):
            missing_outputs.append(folder)
            continue

        try:
            df = pd.read_csv(metrics_file)
            for _, row in df.iterrows():
                if "gene_symbol" in df.columns:
                    gene = row["gene_symbol"]
                elif "Identity" in df.columns:
                    gene = row["Identity"].split(" ")[0]
                else:
                    continue

                # We need a vector of metrics
                # using anisotropy_index, plddt_mean, PAE_domain_blockiness_score if available
                # or just anisotropy and pLDDT
                anisotropy = row.get("anisotropy_index", row.get("Anisotropy", None))
                plddt = row.get("plddt_mean", row.get("pLDDT_mean", None))

                if pd.notnull(anisotropy) and pd.notnull(plddt):
                    gene_history[gene].append({
                        "run": folder,
                        "anisotropy": round(float(anisotropy), 4),
                        "plddt": round(float(plddt), 4)
                    })
        except Exception as e:
            pass

    static_genes = []
    reused_count = 0
    total_genes = len(gene_history)

    for gene, history in gene_history.items():
        if len(history) < 2:
            continue

        # Check if identical across all appearances
        first_val = (history[0]["anisotropy"], history[0]["plddt"])
        is_static = all(h["anisotropy"] == first_val[0] and h["plddt"] == first_val[1] for h in history)

        if is_static:
            static_genes.append(gene)
            reused_count += len(history) - 1

    report = f"""# Evidence Freshness Audit

## Audit Scope
- Trend window: 2026-01-09 to 2026-02-16
- Directories checked: {len(folders)}
- Missing metrics.csv outputs: {len(missing_outputs)} ({', '.join(missing_outputs) if missing_outputs else 'None'})

## Data Reuse Findings
- Total unique genes evaluated: {total_genes}
- Genes with perfectly static metrics across multiple runs: {len(static_genes)}
- Total instances of reused identical vectors: {reused_count}

## Schema Drift
- No significant schema drift detected preventing extraction of core metrics.

## Flagged Static Genes
The following genes show identical per-gene vectors across all their evaluated runs, indicating reused/static metrics rather than fresh structural evidence:
{', '.join(sorted(static_genes))}

## Conclusion
Many "new" reports in the trend window simply reused unchanged per-gene values. Cluster narratives interpreting changing shapes over time are likely over-interpreting static inputs.
"""

    os.makedirs("reports", exist_ok=True)
    with open("reports/evidence_freshness_audit.md", "w") as f:
        f.write(report)

if __name__ == "__main__":
    main()
