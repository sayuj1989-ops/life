import pandas as pd
import numpy as np
import sys
from collections import Counter

def parse_identity(identity):
    if pd.isna(identity):
        return None
    return identity.split(' ')[0]

def main():
    try:
        metrics = pd.read_csv("outputs/afcc/current_metrics.csv")
        candidates = pd.read_csv("data/candidates_master.csv")
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    # Clean and Merge
    metrics['gene_symbol'] = metrics['Identity'].apply(parse_identity)
    merged = pd.merge(metrics, candidates, on='gene_symbol', how='inner')

    # Define Clusters based on Anisotropy, Disorder, and Surface Charge
    merged['Cluster'] = 'Unclassified'

    # 1. Stiff Rods: High Anisotropy (> 3.0), High Confidence (> 70)
    mask_rod = (merged['Anisotropy'] > 3.0) & (merged['pLDDT_mean'] > 70)
    merged.loc[mask_rod, 'Cluster'] = 'Stiff Rods'

    # 2. Flexible Linkers: Moderate Anisotropy (2.0-3.0), High Disorder (> 0.3)
    mask_linker = (merged['Anisotropy'].between(2.0, 3.0)) & (merged['Disorder_Proxy'] > 0.3)
    merged.loc[mask_linker, 'Cluster'] = 'Flexible Linkers'

    # 3. Globular Hubs: Low Anisotropy (< 1.5), High Domains (> 1)
    mask_hub = (merged['Anisotropy'] < 1.5) & (merged['Domains'] > 1)
    merged.loc[mask_hub, 'Cluster'] = 'Globular Hubs'

    # 4. Charged Surface: High Charged Patch Score (> 0.4)
    # This might overlap, so let's mark it separately or as a sub-cluster if needed.
    # For now, let's treat it as a distinct cluster if not already classified as Rod/Linker/Hub
    mask_charged = (merged['Charged_Patch'] > 0.4) & (merged['Cluster'] == 'Unclassified')
    merged.loc[mask_charged, 'Cluster'] = 'Charged Surface'

    # Analyze Clusters
    print("## Cluster Analysis")
    for cluster in sorted(merged['Cluster'].unique()):
        subset = merged[merged['Cluster'] == cluster]
        print(f"\n### Cluster: {cluster} (n={len(subset)})")
        members = subset['gene_symbol'].tolist()
        print(f"Members: {', '.join(members)}")

        # Pathway Enrichment
        pathways = []
        for tags in subset['pathway_tags'].dropna():
            pathways.extend([t.strip() for t in tags.split(',')])

        common_paths = Counter(pathways).most_common(5)
        print(f"Top Pathways: {common_paths}")

        # Anisotropy Stats
        print(f"Mean Anisotropy: {subset['Anisotropy'].mean():.2f}")
        print(f"Mean pLDDT: {subset['pLDDT_mean'].mean():.2f}")
        print(f"Mean Charged Patch: {subset['Charged_Patch'].mean():.2f}")
        print(f"Mean Disorder: {subset['Disorder_Proxy'].mean():.2f}")

if __name__ == "__main__":
    main()
