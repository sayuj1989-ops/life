import os
import glob
import pandas as pd
import datetime

OUTPUT_DIR = "outputs/afcc"
REPORT_FILE = "reports/evidence_freshness_audit.md"

def get_metrics_files():
    # Find all metrics.csv files under outputs/afcc/YYYY-MM-DD
    files = glob.glob(os.path.join(OUTPUT_DIR, "*", "metrics.csv"))
    # Filter for valid dates
    valid_files = []
    for f in files:
        dirname = os.path.basename(os.path.dirname(f))
        try:
            datetime.datetime.strptime(dirname, "%Y-%m-%d")
            valid_files.append((dirname, f))
        except ValueError:
            pass

    # Sort by date
    valid_files.sort(key=lambda x: x[0])
    return valid_files

def audit_freshness():
    files = get_metrics_files()

    # Store history: gene -> list of (date, metrics_dict)
    history = {}

    # Metrics to track for freshness
    track_cols = ['anisotropy_index', 'plddt_mean', 'PAE_mean', 'plddt_fraction_low']

    # Also handle column name variations if any (e.g. 'Anisotropy' vs 'anisotropy_index')
    # Based on reading metrics.csv earlier:
    # gene_symbol,uniprot,source_category,morphology,anisotropy_index,radius_of_gyration,plddt_mean,...

    for date, filepath in files:
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            continue

        # Standardize columns if needed
        # In 2026-02-16 metrics.csv: anisotropy_index, plddt_mean, PAE_mean, plddt_fraction_low
        # In older files, might be different.
        # Let's try to normalize.

        # Check for 'Identity' column vs 'gene_symbol'
        gene_col = None
        if 'gene_symbol' in df.columns:
            gene_col = 'gene_symbol'
        elif 'Identity' in df.columns: # Sometimes used
             # Need to extract gene from Identity string e.g. "PIEZO2 (Q9H5I5)"
             df['gene_symbol'] = df['Identity'].apply(lambda x: x.split(' ')[0] if isinstance(x, str) else x)
             gene_col = 'gene_symbol'

        if not gene_col:
            continue

        # Check for column aliases
        # Newer files use snake_case, older files or reports might use CamelCase
        col_map = {
            'Anisotropy': 'anisotropy_index',
            'pLDDT_mean': 'plddt_mean',
            'pLDDT_frac_low': 'plddt_fraction_low',
            'PAE_blockiness': 'PAE_domain_blockiness_score' # Not strictly freshness but good to know
        }
        df = df.rename(columns=col_map)

        for _, row in df.iterrows():
            gene = row[gene_col]
            metrics = {}
            for col in track_cols:
                if col in row:
                    metrics[col] = row[col]

            if gene not in history:
                history[gene] = []
            history[gene].append((date, metrics))

    # Analyze for staleness
    report_lines = []
    report_lines.append("# Evidence Freshness Audit")
    report_lines.append(f"Date: {datetime.date.today()}")
    report_lines.append("\n## Summary")

    stale_count = 0
    total_comparisons = 0

    detailed_lines = []
    detailed_lines.append("\n## Detailed Findings")

    stale_genes = set()

    sorted_genes = sorted(history.keys())

    for gene in sorted_genes:
        records = history[gene]
        if len(records) < 2:
            continue

        # Sort by date
        records.sort(key=lambda x: x[0])

        for i in range(1, len(records)):
            prev_date, prev_metrics = records[i-1]
            curr_date, curr_metrics = records[i]

            # Compare float values
            is_identical = True
            compared_keys = 0
            for k in track_cols:
                v1 = prev_metrics.get(k)
                v2 = curr_metrics.get(k)

                if v1 is None or v2 is None:
                    continue # Skip if metric missing

                compared_keys += 1
                try:
                    # Use a small epsilon for float comparison if needed, but exact reuse often means exact equality
                    if float(v1) != float(v2):
                        is_identical = False
                        break
                except:
                    if v1 != v2:
                        is_identical = False
                        break

            if compared_keys > 0:
                total_comparisons += 1
                if is_identical:
                    stale_count += 1
                    stale_genes.add(gene)
                    detailed_lines.append(f"- **{gene}**: {curr_date} is identical to {prev_date} (Reused Data).")

    report_lines.append(f"- **Runs Audited**: {len(files)}")
    report_lines.append(f"- **Total Gene-Date Comparisons**: {total_comparisons}")
    report_lines.append(f"- **Identical/Stale Records**: {stale_count}")
    report_lines.append(f"- **Genes Affected**: {len(stale_genes)}")

    if stale_count > 0:
        report_lines.append("\n### Warning")
        report_lines.append(f"Found {stale_count} instances where metrics were identical across runs. This suggests data reuse rather than re-computation.")
    else:
        report_lines.append("\n### Status: Clean")
        report_lines.append("No identical metric vectors found across consecutive runs.")

    report_lines.extend(detailed_lines)

    with open(REPORT_FILE, "w") as f:
        f.write("\n".join(report_lines))

    print(f"Audit complete. Report written to {REPORT_FILE}")

if __name__ == "__main__":
    audit_freshness()
