#!/usr/bin/env python3
"""
07_cluster_proteins.py

Performs clustering on protein metrics to identify structural classes.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.cluster.vq import kmeans2, whiten

# Set up paths
repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(repo_root))

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
METRICS_FILE = BASE_DIR / "outputs" / "afcc" / "2026-01-12" / "metrics.csv"

def main():
    print("🧩 Running Protein Clustering Analysis...")

    if not METRICS_FILE.exists():
        print(f"❌ Metrics file not found: {METRICS_FILE}")
        sys.exit(1)

    # Load data
    df = pd.read_csv(METRICS_FILE)

    # Rename columns to match internal feature names
    df = df.rename(columns={
        'anisotropy_index': 'anisotropy',
        'PAE_domain_blockiness_score': 'pae_blockiness'
    })

    # Features for clustering
    features = ['anisotropy', 'pae_blockiness']

    # Check if features exist
    if not all(f in df.columns for f in features):
        print(f"❌ Missing required features: {features}")
        sys.exit(1)

    # Filter for valid data
    subset = df[features].dropna()
    if subset.empty:
        print("❌ No valid data for clustering.")
        sys.exit(1)

    X = subset.values

    # Normalize (whiten)
    X_whitened = whiten(X)

    # Cluster (using scipy's kmeans2)
    # k=3
    centroids, labels = kmeans2(X_whitened, 3, minit='points', seed=42)
    df.loc[subset.index, 'cluster'] = labels

    # Analyze clusters
    print("Cluster Analysis:")
    for cluster in sorted(df['cluster'].dropna().unique()):
        members = df[df['cluster'] == cluster]
        print(f"\nCluster {int(cluster)} (n={len(members)}):")
        print(f"  Avg Anisotropy: {members['anisotropy'].mean():.2f}")
        print(f"  Avg Blockiness: {members['pae_blockiness'].mean():.2f}")

        # Check enrichment
        if 'source_category' in members.columns:
            sources = members['source_category'].fillna('').str.split(',').explode()
            top_sources = sources.value_counts().head(3)
            print(f"  Top Sources: {top_sources.to_dict()}")

        print("  Members:", ", ".join(members['gene_symbol'].tolist()))

if __name__ == "__main__":
    main()
