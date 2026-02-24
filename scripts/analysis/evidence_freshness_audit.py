import os
import glob
import pandas as pd
import numpy as np
import sys

# Ensure outputs directory exists
OUTPUT_DIR = "outputs/afcc"
if not os.path.exists(OUTPUT_DIR):
    print(f"Error: {OUTPUT_DIR} does not exist.")
    sys.exit(1)

REPORT_PATH = "reports/evidence_freshness_audit.md"

def audit_freshness():
    # Find all metrics.csv recursively
    # glob pattern: outputs/afcc/*/metrics.csv
    search_path = os.path.join(OUTPUT_DIR, "*", "metrics.csv")
    files = glob.glob(search_path)
    files.sort()

    if not files:
        print("No metrics.csv files found.")
        return

    print(f"Found {len(files)} metrics files.")

    data_frames = []
    schema_history = []

    # Track which runs have linked images
    run_status = []

    for f in files:
        # Extract date from directory name (parent of file)
        date_str = os.path.basename(os.path.dirname(f))

        try:
            df = pd.read_csv(f)
            # Normalize column names if needed (strip whitespace)
            df.columns = df.columns.str.strip()

            # Store schema for drift check
            cols = sorted(list(df.columns))
            schema_history.append({'date': date_str, 'columns': cols})

            # Add metadata
            df['date'] = date_str
            df['source_file'] = f

            # Check for linked outputs (PNGs in same dir)
            dir_path = os.path.dirname(f)
            png_files = glob.glob(os.path.join(dir_path, "*.png"))
            has_images = len(png_files) > 0

            run_status.append({
                'date': date_str,
                'has_images': has_images,
                'image_count': len(png_files),
                'row_count': len(df)
            })

            data_frames.append(df)

        except Exception as e:
            print(f"Error processing {f}: {e}")

    if not data_frames:
        print("No valid data loaded.")
        return

    full_df = pd.concat(data_frames, ignore_index=True)

    # --- Report Generation ---
    with open(REPORT_PATH, "w") as report:
        report.write("# Evidence Freshness Audit Report\n\n")

        # 1. Run History & Output Integrity
        report.write("## 1. Run History & Output Integrity\n\n")
        report.write("| Date | Rows | Linked Images | Status |\n")
        report.write("|---|---|---|---|\n")
        for status in run_status:
            img_status = "✅ Present" if status['has_images'] else "⚠️ Missing"
            report.write(f"| {status['date']} | {status['row_count']} | {status['image_count']} | {img_status} |\n")
        report.write("\n")

        # 2. Schema Drift
        report.write("## 2. Schema Drift Analysis\n\n")
        base_cols = set(schema_history[0]['columns'])
        drift_found = False
        report.write(f"- Baseline ({schema_history[0]['date']}): {len(base_cols)} columns\n")

        for i in range(1, len(schema_history)):
            curr = schema_history[i]
            prev = schema_history[i-1]
            curr_cols = set(curr['columns'])
            prev_cols = set(prev['columns'])

            added = curr_cols - prev_cols
            removed = prev_cols - curr_cols

            if added or removed:
                drift_found = True
                report.write(f"- {curr['date']}: Drift detected.\n")
                if added:
                    report.write(f"  - Added: {', '.join(added)}\n")
                if removed:
                    report.write(f"  - Removed: {', '.join(removed)}\n")

        if not drift_found:
            report.write("- No schema drift detected across all runs.\n")
        report.write("\n")

        # 3. Static vs Dynamic Metrics (Data Reuse)
        report.write("## 3. Data Freshness (Reuse Detection)\n\n")
        report.write("Analysis of identical per-gene values across multiple dates.\n\n")

        # Identify genes present in >1 run
        gene_counts = full_df['gene_symbol'].value_counts()
        multi_run_genes = gene_counts[gene_counts > 1].index.tolist()

        static_genes = []
        dynamic_genes = []

        # Metrics to check for variation
        metrics_to_check = ['anisotropy_index', 'plddt_mean', 'PAE_domain_blockiness_score']
        # Filter to available columns
        available_metrics = [m for m in metrics_to_check if m in full_df.columns]

        if not available_metrics:
            report.write("Warning: Key metrics (anisotropy, pLDDT) missing from schema.\n")

        for gene in multi_run_genes:
            gene_df = full_df[full_df['gene_symbol'] == gene].sort_values('date')

            is_static = True
            changes = []

            for m in available_metrics:
                # Check variance (ignoring NaNs)
                vals = gene_df[m].dropna()
                # Round to avoid float precision issues causing false positives
                # Assuming 6 decimal places is enough
                vals_rounded = vals.round(6)
                if len(vals_rounded) > 1 and vals_rounded.nunique() > 1:
                    is_static = False
                    changes.append(m)

            run_count = len(gene_df)
            date_range = f"{gene_df['date'].min()} to {gene_df['date'].max()}"

            if is_static:
                static_genes.append({
                    'gene': gene,
                    'runs': run_count,
                    'range': date_range
                })
            else:
                dynamic_genes.append({
                    'gene': gene,
                    'runs': run_count,
                    'range': date_range,
                    'changes': ", ".join(changes)
                })

        report.write(f"**Total Multi-Run Genes:** {len(multi_run_genes)}\n")
        report.write(f"**Static Genes (100% Identical Metrics):** {len(static_genes)}\n")
        report.write(f"**Dynamic Genes (Changed Values):** {len(dynamic_genes)}\n\n")

        if static_genes:
            report.write("### Static Genes (Potential Cache Reuse)\n")
            report.write("| Gene | Run Count | Date Range |\n")
            report.write("|---|---|---|\n")
            # Limit to top 20 for brevity if list is long
            for g in static_genes[:20]:
                report.write(f"| {g['gene']} | {g['runs']} | {g['range']} |\n")
            if len(static_genes) > 20:
                report.write(f"| ... ({len(static_genes)-20} more) | ... | ... |\n")
            report.write("\n")

        if dynamic_genes:
            report.write("### Dynamic Genes (Value Updates)\n")
            report.write("| Gene | Run Count | Changes Detected |\n")
            report.write("|---|---|---|\n")
            for g in dynamic_genes:
                report.write(f"| {g['gene']} | {g['runs']} | {g['changes']} |\n")
            report.write("\n")

        # 4. Conclusion
        report.write("## 4. Audit Conclusion\n")
        if len(dynamic_genes) == 0 and len(static_genes) > 0:
            report.write("🔴 **CRITICAL**: All multi-run data appears to be static. Runs are likely reusing cached structural predictions without re-running AlphaFold or re-calculating metrics.\n")
        elif len(static_genes) > len(dynamic_genes):
            report.write("🟠 **WARNING**: Majority of data is static. Verify cache invalidation policies.\n")
        else:
            report.write("🟢 **HEALTHY**: Data shows expected variations across runs.\n")

    print(f"Report generated: {REPORT_PATH}")

if __name__ == "__main__":
    audit_freshness()
