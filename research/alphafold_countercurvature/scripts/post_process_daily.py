#!/usr/bin/env python3
"""
post_process_daily.py

Moves metrics to versioned output folder and updates the daily report.
"""

import pandas as pd
from pathlib import Path
import datetime
import shutil

# Config
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
METRICS_FILE = REPO_ROOT / "research/alphafold_countercurvature/data/processed/protein_metrics.csv"
OUTPUTS_DIR = REPO_ROOT / "outputs/afcc"
REPORT_FILE = REPO_ROOT / "reports/afcc_latest.md"

def main():
    today = datetime.date.today().strftime("%Y-%m-%d")
    daily_dir = OUTPUTS_DIR / today
    daily_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy metrics
    if not METRICS_FILE.exists():
        print(f"❌ Metrics file not found: {METRICS_FILE}")
        return

    dest_metrics = daily_dir / "metrics.csv"
    shutil.copy(METRICS_FILE, dest_metrics)
    print(f"✅ Copied metrics to {dest_metrics}")

    # 2. Analyze for summary
    df = pd.read_csv(METRICS_FILE)
    count = len(df)

    if count == 0:
        print("⚠️ No metrics to summarize.")
        return

    # Top anisotropy
    top_aniso = df.sort_values(by="anisotropy_index", ascending=False).iloc[0]
    top_gene = top_aniso["gene_symbol"]
    top_val = top_aniso["anisotropy_index"]

    # Avg pLDDT
    avg_plddt = df["plddt_mean"].mean()

    # Identify missing (from original candidates vs what we have)
    # We can't easily know what was missing here without loading the original list,
    # but we can report what we have.

    # 3. Generate Summary MD
    summary_path = daily_dir / "summary.md"
    summary_content = f"""# AFCC Daily Summary: {today}

- **Total Structures Analyzed**: {count}
- **Top Anisotropy**: {top_gene} ({top_val:.2f})
- **Average pLDDT**: {avg_plddt:.1f}

## Top 5 by Anisotropy
| Gene | Anisotropy | Morphology | pLDDT |
|---|---|---|---|
"""

    for _, row in df.sort_values(by="anisotropy_index", ascending=False).head(5).iterrows():
        summary_content += f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row.get('morphology', 'N/A')} | {row['plddt_mean']:.1f} |\n"

    with open(summary_path, "w") as f:
        f.write(summary_content)

    print(f"✅ Generated summary at {summary_path}")

    # 4. Update Rolling Dashboard
    dashboard_entry = f"""
## {today} Refresh
- Analyzed {count} top candidates.
- Highest anisotropy: **{top_gene}** ({top_val:.2f}).
- Average pLDDT: {avg_plddt:.1f}.
- Metrics saved to `outputs/afcc/{today}/metrics.csv`.
"""

    if REPORT_FILE.exists():
        with open(REPORT_FILE, "r") as f:
            content = f.read()

        # Append to end
        with open(REPORT_FILE, "a") as f:
            f.write(dashboard_entry)
        print(f"✅ Updated dashboard at {REPORT_FILE}")
    else:
        print(f"⚠️ Dashboard file not found at {REPORT_FILE}")

if __name__ == "__main__":
    main()
