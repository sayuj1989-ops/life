import sys
import numpy as np
import pandas as pd
from scipy.cluster.vq import kmeans2

def main():
    # Load data
    try:
        metrics_df = pd.read_csv('outputs/afcc/current_metrics.csv')
        candidates_df = pd.read_csv('data/candidates_master.csv')
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        sys.exit(1)

    # Preprocess metrics_df
    # Extract gene_symbol from Identity "SYMBOL (UNIPROT)" or just "SYMBOL"
    metrics_df['gene_symbol'] = metrics_df['Identity'].apply(lambda x: x.split()[0] if isinstance(x, str) else x)

    # Rename columns to match what we need
    rename_map = {
        'Length': 'length',
        'pLDDT_mean': 'pLDDT_mean',
        'Anisotropy': 'anisotropy_index',
        'Disorder_Proxy': 'disorder_fraction_proxy',
        'Domains': 'predicted_domain_segments',
        'Rg': 'radius_of_gyration',
        'End_to_End': 'end_to_end_distance'
    }
    metrics_df.rename(columns=rename_map, inplace=True)

    # Merge
    merged_df = pd.merge(metrics_df, candidates_df[['gene_symbol', 'pathway_tags']], on='gene_symbol', how='left')
    merged_df['pathway_tags'] = merged_df['pathway_tags'].fillna('')

    # Calculate derived metrics
    # Elongation = End-to-End Distance / Radius of Gyration
    merged_df['elongation'] = merged_df.apply(
        lambda row: row['end_to_end_distance'] / row['radius_of_gyration'] if row['radius_of_gyration'] > 0 else 0, axis=1
    )

    # Select features
    features = ['length', 'pLDDT_mean', 'anisotropy_index', 'disorder_fraction_proxy', 'predicted_domain_segments', 'elongation']

    # Fill missing
    for col in features:
        if col not in merged_df.columns:
            print(f"Warning: Column {col} not found. Creating dummy.")
            merged_df[col] = 0
        merged_df[col] = merged_df[col].fillna(merged_df[col].mean())

    data = merged_df[features].values.astype(float)

    # Standardize
    data_mean = np.mean(data, axis=0)
    data_std = np.std(data, axis=0)
    data_std[data_std == 0] = 1.0
    data_scaled = (data - data_mean) / data_std

    # Run K-Means
    k = 3 # Reduced k due to small dataset size
    np.random.seed(42)
    centroids, labels = kmeans2(data_scaled, k, minit='points')
    merged_df['cluster'] = labels

    # Report
    print(f"--- Cluster Analysis (k={k}) ---\n")
    for i in range(k):
        cluster_data = merged_df[merged_df['cluster'] == i]
        n_members = len(cluster_data)
        print(f"Cluster {i}: {n_members} members")

        print("  Mean Features:")
        print(cluster_data[features].mean().to_string())

        pathways = []
        for tags in cluster_data['pathway_tags']:
            if tags:
                pathways.extend([t.strip() for t in tags.split(',')])
        print("  Top Pathways:")
        pathway_counts = pd.Series(pathways).value_counts().head(5)
        if not pathway_counts.empty:
            print(pathway_counts.to_string())
        else:
            print("    (No pathway tags found)")

        print("  Members:")
        for _, row in cluster_data.iterrows():
            print(f"    {row['gene_symbol']} (Aniso: {row['anisotropy_index']:.2f}, Domains: {row['predicted_domain_segments']})")
        print("\n" + "-"*30 + "\n")

if __name__ == "__main__":
    main()
