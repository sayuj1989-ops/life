import pandas as pd
import numpy as np
from scipy.cluster.vq import kmeans2, whiten
import os
import datetime

def main():
    # Paths
    metrics_path = 'outputs/afcc/current_metrics.csv'
    candidates_path = 'data/candidates_master.csv'
    hypothesis_register_path = 'notes/hypothesis_register.md'

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    report_dir = 'reports/structure_clusters/'
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    report_path = f'{report_dir}{today}__cluster_note.md'

    # Load Data
    if not os.path.exists(metrics_path):
        print(f"Error: {metrics_path} not found.")
        return
    if not os.path.exists(candidates_path):
        print(f"Error: {candidates_path} not found.")
        return

    try:
        df_metrics = pd.read_csv(metrics_path)
        df_candidates = pd.read_csv(candidates_path)
    except Exception as e:
        print(f"Error reading CSVs: {e}")
        return

    # Clean Identity to get gene_symbol
    df_metrics['Identity'] = df_metrics['Identity'].astype(str)
    df_metrics['gene_symbol'] = df_metrics['Identity'].apply(lambda x: x.split(' ')[0] if ' ' in x else x)

    # Merge
    df = pd.merge(df_metrics, df_candidates, on='gene_symbol', how='inner')
    print(f"Merged dataset size: {len(df)}")

    if len(df) < 5:
        print("Not enough data points for clustering.")
        return

    # Select features
    features = ['Anisotropy', 'pLDDT_mean', 'Disorder_Proxy']
    df[features] = df[features].apply(pd.to_numeric, errors='coerce')
    X = df[features].fillna(df[features].mean()).values.astype(float)

    # Whiten (normalize)
    X_scaled = whiten(X)

    # Cluster (k=5)
    np.random.seed(42)
    n_clusters = 5
    centroids, labels = kmeans2(X_scaled, k=n_clusters, minit='points')
    df['cluster'] = labels

    # Analyze Clusters
    cluster_stats = []
    target_terms = ["Mechanotransduction", "Spine", "ECM", "Cilia", "Cytoskeleton"]

    print("\nCluster Analysis:")
    for i in range(n_clusters):
        cluster_df = df[df['cluster'] == i]
        mean_aniso = cluster_df['Anisotropy'].mean()
        mean_plddt = cluster_df['pLDDT_mean'].mean()
        mean_disorder = cluster_df['Disorder_Proxy'].mean()

        # Calculate enrichment score
        tags_list = cluster_df['pathway_tags'].dropna().astype(str).tolist()
        all_tags = []
        for tags in tags_list:
            all_tags.extend([t.strip() for t in tags.split(',')])

        enrichment_score = 0
        for term in target_terms:
            count = sum(1 for t in all_tags if term.lower() in t.lower())
            enrichment_score += count

        # Normalize by cluster size to avoid bias towards large clusters
        enrichment_score = enrichment_score / len(cluster_df) if len(cluster_df) > 0 else 0

        members = cluster_df['gene_symbol'].tolist()
        print(f"Cluster {i} (n={len(cluster_df)}): Aniso={mean_aniso:.2f}, pLDDT={mean_plddt:.2f}, Disorder={mean_disorder:.2f}, Enrichment={enrichment_score:.2f}")

        cluster_stats.append({
            'cluster_id': i,
            'mean_aniso': mean_aniso,
            'mean_plddt': mean_plddt,
            'mean_disorder': mean_disorder,
            'enrichment_score': enrichment_score,
            'members': members,
            'tags': tags_list
        })

    # Select best cluster based on enrichment score
    best_cluster = max(cluster_stats, key=lambda x: x['enrichment_score'])
    print(f"\nSelected Cluster {best_cluster['cluster_id']} (Score: {best_cluster['enrichment_score']:.2f})")

    # Generate Hypothesis
    members = best_cluster['members']
    aniso = best_cluster['mean_aniso']
    disorder = best_cluster['mean_disorder']

    hypothesis_id = f"H_{today.replace('-','_')}_Cluster_{best_cluster['cluster_id']}"

    if aniso > 3.0:
        role = "Tensile Tether"
        concept = "High anisotropy suggests these proteins act as molecular calipers or tethers, transmitting force over long distances."
        test = "Apply cyclic strain and measure protein alignment/nuclear translocation."
    elif disorder > 0.4:
        role = "Entropic Spring"
        concept = "High intrinsic disorder suggests these proteins function as entropic springs, tuning stiffness via conformational entropy."
        test = "Measure persistence length via FRET under osmotic compression."
    else:
        role = "Signaling Hub"
        concept = "Globular structure with specific domains suggests a role in signal integration rather than direct mechanics."
        test = "Compare phosphorylation states under static vs dynamic loading."

    # Write Report
    content = f"""# Structure Cluster Report: {today}

## Cluster Analysis
**Focus Cluster:** {best_cluster['cluster_id']} (Enrichment Score: {best_cluster['enrichment_score']:.2f})
**Members:** {', '.join(members)}
**Shared Properties:**
- Mean Anisotropy: {aniso:.2f}
- Mean pLDDT: {best_cluster['mean_plddt']:.2f}
- Mean Disorder: {disorder:.2f}

## Hypothesis: {hypothesis_id}
**Concept:** {concept}
**Proposed Mechanical Role:** {role}

## Concrete Test
**Experiment:** {test}
"""
    with open(report_path, 'w') as f:
        f.write(content)
    print(f"Report written to {report_path}")

    # Update Hypothesis Register
    # Check if hypothesis already exists
    with open(hypothesis_register_path, 'r') as f:
        register_content = f.read()

    if hypothesis_id not in register_content:
        new_entry = f"| **{hypothesis_id}** | {concept} | Cluster analysis identified a group enriched in mechanotransduction with distinct structural properties (Aniso={aniso:.2f}, Disorder={disorder:.2f}). | {test} | Proposed |\n"
        with open(hypothesis_register_path, 'a') as f:
            f.write(new_entry)
        print(f"Hypothesis added to {hypothesis_register_path}")
    else:
        print("Hypothesis already exists in register.")

if __name__ == "__main__":
    main()
