#!/usr/bin/env python3
"""
weekly_cluster_analysis.py

Performs clustering on protein metrics to identify structural classes for the weekly hypothesis generation cycle.
Automatically finds the latest metrics output.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.cluster.vq import kmeans2, whiten

# Set up paths
# Assuming this script is in research/alphafold_countercurvature/scripts/
repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(repo_root))

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = repo_root / "data"
OUTPUTS_DIR = repo_root / "outputs" / "afcc"

def get_latest_metrics_file():
    """Finds the latest metrics.csv file in outputs/afcc/."""
    if not OUTPUTS_DIR.exists():
        return None

    # List all date directories
    date_dirs = [d for d in OUTPUTS_DIR.iterdir() if d.is_dir() and d.name.startswith("20")]

    if not date_dirs:
        return None

    # Sort by date
    date_dirs.sort(key=lambda x: x.name, reverse=True)

    for d in date_dirs:
        metrics_file = d / "metrics.csv"
        if metrics_file.exists():
            print(f"✅ Found latest metrics: {metrics_file}")
            return metrics_file

    return None

def main():
    print("🧩 Running Weekly Protein Clustering Analysis...")

    metrics_file = get_latest_metrics_file()
    if not metrics_file:
        print("❌ No metrics.csv found in outputs/afcc/.")
        sys.exit(1)

    # Load metrics
    df_metrics = pd.read_csv(metrics_file)
    print(f"Loaded {len(df_metrics)} proteins from metrics.")

    # Load candidates to get tags
    candidates_file = DATA_DIR / "candidates_master.csv"
    if candidates_file.exists():
        df_candidates = pd.read_csv(candidates_file)
        # Merge tags
        df = df_metrics.merge(df_candidates[['gene_symbol', 'pathway_tags']], on='gene_symbol', how='left')
    else:
        print("⚠️ Candidates file not found, using metrics only.")
        df = df_metrics

    # Features for clustering
    # anisotropy_index: High = Rod-like, Low = Globular
    # PAE_domain_blockiness_score: High = distinct domains (Blocky), Low = continuous/integrated
    features = ['anisotropy_index', 'PAE_domain_blockiness_score']

    # Filter for valid data
    subset = df[features].dropna()
    if subset.empty:
        print("❌ No valid data for clustering.")
        sys.exit(1)

    X = subset.values.astype(float)

    # Whiten the data (normalize variance)
    X_whitened = whiten(X)

    # Cluster (k=3)
    # We expect roughly:
    # 1. Globular (Low Anisotropy, Low Blockiness)
    # 2. Multi-domain/Beads-on-string (Low Anisotropy, High Blockiness)
    # 3. Rods/Fibers (High Anisotropy, Low/Variable Blockiness)
    k = 3
    centroids, labels = kmeans2(X_whitened, k, minit='points', seed=42)

    # Assign labels back to full dataframe (aligning indices)
    df.loc[subset.index, 'cluster'] = labels

    # Analyze clusters
    print("\n" + "="*50)
    print("CLUSTER ANALYSIS")
    print("="*50)

    for cluster in sorted(df['cluster'].dropna().unique()):
        members = df[df['cluster'] == cluster]
        n_members = len(members)

        avg_aniso = members['anisotropy_index'].mean()
        avg_block = members['PAE_domain_blockiness_score'].mean()

        print(f"\nCluster {int(cluster)} (n={n_members})")
        print(f"Properties: Anisotropy={avg_aniso:.2f}, Blockiness={avg_block:.2f}")

        # Collect all tags
        all_tags = []
        if 'pathway_tags' in members.columns:
            for tags in members['pathway_tags'].dropna():
                all_tags.extend([t.strip() for t in tags.split(',')])

        # Show top tags
        if all_tags:
            from collections import Counter
            top_tags = Counter(all_tags).most_common(5)
            tags_str = ", ".join([f"{t}({c})" for t, c in top_tags])
            print(f"Top Tags: {tags_str}")

        # List members (first 20)
        member_list = members['gene_symbol'].tolist()
        print(f"Members: {', '.join(member_list[:20])}")
        if n_members > 20:
            print(f"         ...and {n_members - 20} more.")

if __name__ == "__main__":
    main()
