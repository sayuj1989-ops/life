#!/usr/bin/env python3
import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime

OUTPUT_DIR = "outputs/afcc"

def audit_freshness():
    print("Starting Evidence Freshness Audit...")

    # Find all metrics.csv files
    files = glob.glob(os.path.join(OUTPUT_DIR, "*", "metrics.csv"))
    files.sort()

    if not files:
        print("No metrics.csv files found.")
        return

    print(f"Found {len(files)} metrics files.")

    # Data structure: gene -> {date: metrics_row}
    history = {}
    schema_history = {}

    for f in files:
        date_str = os.path.basename(os.path.dirname(f))
        try:
            df = pd.read_csv(f)
        except Exception as e:
            print(f"Error reading {f}: {e}")
            continue

        columns = tuple(sorted(df.columns.tolist()))
        schema_history[date_str] = columns

        # Check for schema drift
        if len(schema_history) > 1:
            prev_date = list(schema_history.keys())[-2]
            if schema_history[date_str] != schema_history[prev_date]:
                print(f"⚠ Schema Drift detected on {date_str} vs {prev_date}")
                diff = set(schema_history[date_str]) ^ set(schema_history[prev_date])
                print(f"   Differences: {diff}")

        # Store metrics
        # Some files might use 'Identity' or 'gene_symbol' as key
        id_col = 'Identity' if 'Identity' in df.columns else 'gene_symbol'
        if id_col not in df.columns:
            print(f"⚠ Skipping {date_str}: No identity column found.")
            continue

        for _, row in df.iterrows():
            gene_id = row[id_col]
            # Normalize gene ID (remove Uniprot if present for matching)
            if "(" in str(gene_id):
                gene_symbol = str(gene_id).split()[0]
            else:
                gene_symbol = str(gene_id)

            if gene_symbol not in history:
                history[gene_symbol] = {}

            # Store key metrics for comparison
            # We'll use Anisotropy, pLDDT_mean, PAE_mean if available
            metrics = {}
            for col in ['Anisotropy', 'anisotropy_index', 'pLDDT_mean', 'plddt_mean', 'PAE_mean']:
                if col in row:
                    val = row[col]
                    # Handle potential string formatting
                    try:
                        metrics[col] = float(val)
                    except:
                        metrics[col] = str(val)

            history[gene_symbol][date_str] = metrics

    print("\n--- Static Value Analysis ---")
    # Check for static values
    for gene, dates in history.items():
        sorted_dates = sorted(dates.keys())
        if len(sorted_dates) < 2:
            continue

        # Check if values changed
        last_metrics = dates[sorted_dates[0]]
        static_count = 0
        total_checks = 0

        print(f"\nGene: {gene} (Found in {len(sorted_dates)} runs)")

        for i in range(1, len(sorted_dates)):
            curr_date = sorted_dates[i]
            curr_metrics = dates[curr_date]

            # Compare overlap keys
            common_keys = set(last_metrics.keys()) & set(curr_metrics.keys())
            if not common_keys:
                print(f"  {sorted_dates[i-1]} -> {curr_date}: No common metrics to compare.")
                continue

            is_identical = True
            for k in common_keys:
                v1 = last_metrics[k]
                v2 = curr_metrics[k]
                # Floating point comparison
                if isinstance(v1, float) and isinstance(v2, float):
                    if not np.isclose(v1, v2, atol=1e-6):
                        is_identical = False
                        break
                elif v1 != v2:
                    is_identical = False
                    break

            if is_identical:
                static_count += 1
                print(f"  ⚠ {sorted_dates[i-1]} -> {curr_date}: Identical metrics (Potential Reuse)")
            else:
                print(f"  ✅ {sorted_dates[i-1]} -> {curr_date}: Metrics changed")

            last_metrics = curr_metrics
            total_checks += 1

        if static_count == total_checks and total_checks > 0:
             print(f"  🔴 CRITICAL: {gene} data is completely static across all observed transitions.")

if __name__ == "__main__":
    audit_freshness()
