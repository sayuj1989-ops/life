import pandas as pd
import sys
import subprocess
from pathlib import Path
from datetime import date

# Setup paths
repo_root = Path(__file__).resolve().parent.parent.parent.parent
afcc_root = repo_root / "research" / "alphafold_countercurvature"
data_dir = afcc_root / "data"
scripts_dir = afcc_root / "scripts"
candidates_master = repo_root / "data" / "candidates_master.csv"
candidates_processed = data_dir / "processed" / "candidates.csv"
uniprot_mapping = data_dir / "processed" / "uniprot_mapping.csv"
metrics_file = data_dir / "processed" / "protein_metrics.csv"
today = date.today().strftime("%Y-%m-%d")
output_dir = afcc_root / "outputs" / "afcc" / today
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Identify TOP N (10)
print(f"Reading {candidates_master}...")
df_master = pd.read_csv(candidates_master)
# Sort by priority_score desc
df_top = df_master.sort_values(by="priority_score", ascending=False).head(10).copy()

print("Top 10 Candidates:")
print(df_top[["gene_symbol", "priority_score"]])

# 2. Prepare inputs for pipeline
# 2a. candidates.csv for 04_analyze_metrics.py
# Schema needed: gene_symbol, source, total_score.
# We map priority_score -> total_score.
df_processed = pd.DataFrame({
    "gene_symbol": df_top["gene_symbol"],
    "source": "top_priority",
    "total_score": df_top["priority_score"]
})

# Ensure directory exists
candidates_processed.parent.mkdir(parents=True, exist_ok=True)
df_processed.to_csv(candidates_processed, index=False)
print(f"Saved {candidates_processed}")

# 2b. uniprot_mapping.csv for 02_fetch_afdb.py
# Schema: gene_symbol, uniprot_accession
df_mapping = pd.DataFrame({
    "gene_symbol": df_top["gene_symbol"],
    "uniprot_accession": df_top["uniprot_id"]
})
df_mapping.to_csv(uniprot_mapping, index=False)
print(f"Saved {uniprot_mapping}")

# 3. Fetch Structures
print("Fetching structures...")
# We use --limit 10 just in case, but mapping has only 10.
# We call the script via subprocess to ensure environment/imports work as intended.
cmd_fetch = [sys.executable, str(scripts_dir / "02_fetch_afdb.py"), "--limit", "10"]
subprocess.check_call(cmd_fetch)

# 4. Compute Metrics
print("Computing metrics...")
# To ensure recomputation, we remove these entries from metrics_file if they exist.
if metrics_file.exists():
    print("Removing existing metrics for top candidates to force recompute...")
    df_metrics = pd.read_csv(metrics_file)
    original_len = len(df_metrics)
    df_metrics = df_metrics[~df_metrics["gene_symbol"].isin(df_top["gene_symbol"])]
    if len(df_metrics) < original_len:
        print(f"Removed {original_len - len(df_metrics)} entries.")
        df_metrics.to_csv(metrics_file, index=False)
    else:
        print("No existing entries found to remove.")

cmd_metrics = [sys.executable, str(scripts_dir / "04_analyze_metrics.py")]
subprocess.check_call(cmd_metrics)

# 5. Save Outputs
print(f"Saving outputs to {output_dir}...")
# Copy metrics
if metrics_file.exists():
    df_metrics_new = pd.read_csv(metrics_file)
    # Save the metrics for the top 10.
    df_result = df_metrics_new[df_metrics_new["gene_symbol"].isin(df_top["gene_symbol"])].copy()
    df_result.to_csv(output_dir / "metrics.csv", index=False)

    # Generate summary.md
    summary_path = output_dir / "summary.md"

    with open(summary_path, "w") as f:
        f.write(f"# AFCC Refresh: {today}\n\n")
        f.write("## Top 10 Candidates (Priority Score)\n")
        f.write("| Gene | Priority Score | UniProt |\n")
        f.write("| --- | --- | --- |\n")
        for _, row in df_top.iterrows():
            f.write(f"| {row['gene_symbol']} | {row['priority_score']} | {row['uniprot_id']} |\n")

        f.write("\n\n## Metrics Summary\n")
        if not df_result.empty:
            # Top Anisotropy
            f.write("### Top Anisotropy\n")
            if "anisotropy_index" in df_result.columns:
                cols = ["gene_symbol", "anisotropy_index", "plddt_mean"]
                f.write(f"| {' | '.join(cols)} |\n")
                f.write(f"| {' | '.join(['---']*len(cols))} |\n")
                for _, row in df_result.sort_values("anisotropy_index", ascending=False).head(5)[cols].iterrows():
                    f.write(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.2f} |\n")
            else:
                f.write("Metric 'anisotropy_index' not found in results.\n")
        else:
            f.write("No metrics computed (failed to download?).\n")

    # Update Rolling Dashboard
    dashboard_path = repo_root / "reports" / "afcc_latest.md"
    print(f"Updating {dashboard_path}...")

    with open(dashboard_path, "a") as f:
        f.write(f"\n\n## {today}: Daily Refresh (Top 10)\n\n")
        f.write("**Summary:**\n")
        f.write(f"- **Processed:** {len(df_top)} candidates.\n")
        downloaded_count = len(df_result) # Approx
        f.write(f"- **Analysis:** Metrics computed for {downloaded_count} structures.\n\n")

        f.write("**Key Findings:**\n")
        if not df_result.empty and "anisotropy_index" in df_result.columns:
            top_ani = df_result.sort_values("anisotropy_index", ascending=False).iloc[0]
            f.write(f"- **Top Anisotropy:** **{top_ani['gene_symbol']}** ({top_ani['anisotropy_index']:.2f})\n")

            high_ani = df_result[df_result["anisotropy_index"] > 4.0]
            if not high_ani.empty:
                 genes = ", ".join(high_ani["gene_symbol"].tolist())
                 f.write(f"- **High Anisotropy (>4.0):** {genes}\n")

        f.write("\n**Outputs:**\n")
        rel_path = f"research/alphafold_countercurvature/outputs/afcc/{today}"
        f.write(f"- [Metrics CSV]({rel_path}/metrics.csv)\n")
        f.write(f"- [Summary Report]({rel_path}/summary.md)\n")

    # Failure note if any missing
    failed = len(df_top) - len(df_result)
    if failed > 0:
        fail_path = output_dir / "failure.md"
        with open(fail_path, "w") as f:
            f.write(f"# Failures {today}\n")
            f.write(f"{failed} candidates failed to process (download or metrics).\n")
            missing = set(df_top["gene_symbol"]) - set(df_result["gene_symbol"])
            f.write(f"Missing: {', '.join(missing)}\n")

print("Done.")
