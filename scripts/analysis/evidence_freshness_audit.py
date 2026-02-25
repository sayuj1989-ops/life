#!/usr/bin/env python3
"""
Evidence Freshness Audit Script
Audits AFCC run history for reused/static metrics and schema drifts.
"""

import os
import csv
import sys
import datetime
from collections import defaultdict

AFCC_ROOT = "outputs/afcc"
START_DATE = datetime.date(2026, 1, 9)
END_DATE = datetime.date(2026, 2, 16)

def get_date_dirs(root):
    dirs = []
    if not os.path.exists(root):
        print(f"Error: Root directory {root} does not exist.")
        return dirs

    for entry in os.listdir(root):
        path = os.path.join(root, entry)
        if os.path.isdir(path):
            try:
                dt = datetime.datetime.strptime(entry, "%Y-%m-%d").date()
                if START_DATE <= dt <= END_DATE:
                    dirs.append((dt, path))
            except ValueError:
                continue
    return sorted(dirs, key=lambda x: x[0])

def load_metrics(filepath):
    data = {}
    fieldnames = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if not fieldnames:
                return {}, []

            for row in reader:
                gene = row.get('gene_symbol')
                if gene:
                    data[gene] = row
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return {}, []
    return data, fieldnames

def compare_vectors(vec1, vec2, keys_to_ignore=None):
    if keys_to_ignore is None:
        keys_to_ignore = set()

    diffs = []
    all_keys = set(vec1.keys()) | set(vec2.keys())
    for k in all_keys:
        if k in keys_to_ignore:
            continue
        v1 = vec1.get(k, "N/A")
        v2 = vec2.get(k, "N/A")
        # Simple string comparison
        if str(v1) != str(v2):
            diffs.append(k)
    return diffs

def main():
    print(f"Starting audit of {AFCC_ROOT} from {START_DATE} to {END_DATE}")

    date_dirs = get_date_dirs(AFCC_ROOT)
    if not date_dirs:
        print("No directories found in the specified range.")
        return

    print(f"Found {len(date_dirs)} runs.")

    gene_history = defaultdict(list)
    schema_history = []

    # Load all data
    for dt, path in date_dirs:
        metrics_file = os.path.join(path, "metrics.csv")
        if not os.path.exists(metrics_file):
            print(f"Warning: No metrics.csv in {path}")
            continue

        data, fields = load_metrics(metrics_file)
        schema_history.append((dt, fields))

        for gene, metrics in data.items():
            gene_history[gene].append((dt, metrics))

    # 1. Schema Drift Analysis
    print("\n=== Schema Drift Analysis ===")
    base_fields = None
    if schema_history:
        base_dt, base_fields = schema_history[0]
        base_fields_set = set(base_fields) if base_fields else set()
        print(f"Base schema ({base_dt}): {len(base_fields_set)} columns")

        drift_detected = False
        for dt, fields in schema_history[1:]:
            current_set = set(fields) if fields else set()
            added = current_set - base_fields_set
            removed = base_fields_set - current_set
            if added or removed:
                drift_detected = True
                print(f"  Drift at {dt}:")
                if added: print(f"    + Added: {added}")
                if removed: print(f"    - Removed: {removed}")
                # Update base for next comparison? No, compare to initial to see total drift or cumulative?
                # Let's keep comparing to the first one for simplicity or just report it.

        if not drift_detected:
            print("No schema drift detected across analyzed files.")

    # 2. Static Value Analysis
    print("\n=== Static Value Analysis ===")
    print("Checking for genes with identical metrics across multiple dates (ignoring metadata columns).")

    metadata_cols = {'source_category', 'low_confidence_warning', 'multi_domain_uncertain', 'likely_IDR_heavy'}

    static_genes = []
    variable_genes = []

    for gene, history in gene_history.items():
        if len(history) < 2:
            continue

        # Compare consecutive entries
        is_static = True
        changes = []

        # history is list of (date, metric_dict)
        # Sort by date just in case
        history.sort(key=lambda x: x[0])

        first_dt, first_metrics = history[0]

        for i in range(1, len(history)):
            curr_dt, curr_metrics = history[i]
            prev_dt, prev_metrics = history[i-1]

            # Compare current to previous
            diffs = compare_vectors(prev_metrics, curr_metrics, keys_to_ignore=metadata_cols)
            if diffs:
                is_static = False
                changes.append(f"{prev_dt}->{curr_dt}: changed {diffs}")

        if is_static:
            static_genes.append((gene, len(history), first_dt, history[-1][0]))
        else:
            variable_genes.append((gene, changes))

    print(f"\nTotal genes analyzed with >1 data point: {len(static_genes) + len(variable_genes)}")
    print(f"Genes with STATIC metrics (identical vectors): {len(static_genes)}")
    print(f"Genes with VARIABLE metrics (value changes): {len(variable_genes)}")

    if static_genes:
        print("\n--- Static Genes Details ---")
        print(f"{'Gene':<10} | {'Runs':<5} | {'Range Start':<12} | {'Range End':<12}")
        print("-" * 50)
        for g, count, start, end in sorted(static_genes, key=lambda x: x[0]):
            print(f"{g:<10} | {count:<5} | {start} | {end}")

    if variable_genes:
        print("\n--- Variable Genes Details ---")
        for g, change_log in variable_genes:
            print(f"Gene: {g}")
            for log in change_log:
                print(f"  {log}")

    # LBX1 Specific Check
    print("\n=== LBX1 Specific Audit ===")
    if 'LBX1' in gene_history:
        hist = gene_history['LBX1']
        hist.sort(key=lambda x: x[0])
        print(f"LBX1 present in {len(hist)} runs.")
        print("Metrics evolution:")
        for dt, m in hist:
            aniso = m.get('anisotropy_index', 'N/A')
            plddt = m.get('plddt_mean', 'N/A')
            pae = m.get('PAE_domain_blockiness_score', 'N/A')
            print(f"  {dt}: Aniso={aniso}, pLDDT={plddt}, PAE={pae}")
    else:
        print("LBX1 not found in any audited files.")

if __name__ == "__main__":
    main()
