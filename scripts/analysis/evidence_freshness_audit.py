import os
import glob
import pandas as pd
from datetime import datetime, timezone

def run_audit():
    base_dir = "outputs/afcc"
    start_date = "2026-01-09"
    end_date = "2026-02-16"

    dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    valid_dirs = []
    for d in dirs:
        try:
            if start_date <= d <= end_date:
                valid_dirs.append(d)
        except ValueError:
            pass

    valid_dirs.sort()

    report_lines = []
    report_lines.append("# Evidence Freshness Audit")
    report_lines.append(f"Audit Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    report_lines.append(f"Trend window: {start_date} to {end_date}")
    report_lines.append("")

    # Baseline schema is the final date in the window
    baseline_metrics_file = os.path.join(base_dir, end_date, "metrics.csv")
    if os.path.exists(baseline_metrics_file):
        df_baseline = pd.read_csv(baseline_metrics_file)
        schema_reference = list(df_baseline.columns)
    else:
        schema_reference = None

    schema_drift_issues = []
    missing_outputs = []

    gene_history = {}

    for d in valid_dirs:
        dir_path = os.path.join(base_dir, d)
        metrics_file = os.path.join(dir_path, "metrics.csv")
        summary_file = os.path.join(dir_path, "summary.md")

        has_metrics = os.path.exists(metrics_file)
        has_summary = os.path.exists(summary_file)

        if not has_metrics or not has_summary:
            missing = []
            if not has_metrics: missing.append("metrics.csv")
            if not has_summary: missing.append("summary.md")
            missing_outputs.append(f"- **{d}**: Missing {', '.join(missing)}")

        if has_metrics:
            try:
                df = pd.read_csv(metrics_file)
                cols = list(df.columns)
                if schema_reference and cols != schema_reference:
                    schema_drift_issues.append(f"- **{d}**: Columns mismatch baseline schema (`{end_date}`).")

                feature_cols = [c for c in cols if c not in ["gene_symbol", "uniprot", "source_category", "low_confidence_warning", "multi_domain_uncertain", "likely_IDR_heavy"]]
                for _, row in df.iterrows():
                    gene = row.get("gene_symbol")
                    if pd.isna(gene): continue

                    vec = {c: row[c] for c in feature_cols if pd.notna(row.get(c))}
                    if gene not in gene_history:
                        gene_history[gene] = []
                    gene_history[gene].append((d, vec))

            except Exception as e:
                missing_outputs.append(f"- **{d}**: Failed to parse metrics.csv: {e}")

    report_lines.append("## Missing Linked Outputs")
    if missing_outputs:
        report_lines.extend(missing_outputs)
    else:
        report_lines.append("No missing standard outputs (metrics.csv, summary.md) found.")
    report_lines.append("")

    report_lines.append("## Schema Drifts")
    if schema_drift_issues:
        report_lines.extend(schema_drift_issues)
    else:
        report_lines.append("No schema drift detected across audited metrics.csv files.")
    report_lines.append("")

    report_lines.append("## Freshness Check: Identical Per-Gene Vectors Across Runs")
    report_lines.append("The following identifies when 'new' runs reused exactly unchanged per-gene values from previous dates (stretches of >1 run).")

    stale_stretches = []
    for gene, history in gene_history.items():
        if len(history) < 2:
            continue

        current_streak_start = history[0][0]
        current_vec = history[0][1]
        streak_count = 1

        for d, vec in history[1:]:
            if vec == current_vec:
                streak_count += 1
            else:
                if streak_count > 1:
                    stale_stretches.append(f"- **{gene}**: Values exactly identical across {streak_count} consecutive runs ({current_streak_start} to {history[history.index((d, vec))-1][0]}).")
                current_streak_start = d
                current_vec = vec
                streak_count = 1

        # Handle trailing streak
        if streak_count > 1:
            stale_stretches.append(f"- **{gene}**: Values exactly identical across {streak_count} consecutive runs ({current_streak_start} to {history[-1][0]}).")

    if stale_stretches:
        report_lines.extend(stale_stretches)
    else:
        report_lines.append("All tracked genes show variance; no identical stagnation detected.")

    report_lines.append("")
    report_lines.append("## Conclusion & Caveat")
    report_lines.append("- Repeatedly reused vectors falsely inflate evidence weight if interpreted as independent confirmations.")
    report_lines.append("- Reports based on these dates should be explicitly caveated that underlying AFCC metrics for these genes were reused/static.")

    os.makedirs("reports", exist_ok=True)
    with open("reports/evidence_freshness_audit.md", "w") as f:
        f.write("\n".join(report_lines))

    print("Audit complete. Wrote reports/evidence_freshness_audit.md")

if __name__ == "__main__":
    run_audit()
