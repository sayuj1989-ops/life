#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_FILE = BASE_DIR / "data" / "processed" / "protein_metrics.csv"
BOLT_TARGETS_FILE = BASE_DIR / "data" / "processed" / "bolt_targets.csv"

def main():
    if not METRICS_FILE.exists():
        print(f"ℹ️ {METRICS_FILE} does not exist. No cleaning needed.")
        return

    if not BOLT_TARGETS_FILE.exists():
        print(f"❌ {BOLT_TARGETS_FILE} not found.")
        return

    metrics_df = pd.read_csv(METRICS_FILE)
    targets_df = pd.read_csv(BOLT_TARGETS_FILE)

    target_genes = set(targets_df['gene_symbol'])

    initial_count = len(metrics_df)

    # Filter out target genes
    new_metrics_df = metrics_df[~metrics_df['gene_symbol'].isin(target_genes)]

    final_count = len(new_metrics_df)
    removed_count = initial_count - final_count

    if removed_count > 0:
        new_metrics_df.to_csv(METRICS_FILE, index=False)
        print(f"✅ Removed {removed_count} entries from protein_metrics.csv matching the seed list.")
    else:
        print("ℹ️ No entries found matching the seed list. Nothing removed.")

    print(f"   Final count: {final_count}")

if __name__ == "__main__":
    main()
