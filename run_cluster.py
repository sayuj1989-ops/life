from pathlib import Path
import numpy as np
import pandas as pd

METRICS_PATH = Path("outputs/afcc/current_metrics.csv")
CANDIDATES_PATH = Path("data/candidates_master.csv")

metrics_df = pd.read_csv(METRICS_PATH)
candidates_df = pd.read_csv(CANDIDATES_PATH)

# Fix Identity parsing
metrics_df['Identity'] = metrics_df['Identity'].apply(lambda x: x.split(' ')[0])
merged_df = pd.merge(metrics_df, candidates_df, left_on='Identity', right_on='gene_symbol', how='inner')
print(f"Loaded {len(merged_df)} merged candidates.")

features = ['Anisotropy', 'Disorder_Proxy']
X = merged_df[features].values
X_mean = np.mean(X, axis=0)
X_std = np.std(X, axis=0)
X_norm = (X - X_mean) / X_std

k = 5
max_iters = 100
np.random.seed(42)
centroids = X_norm[np.random.choice(X_norm.shape[0], k, replace=False)]
labels = np.zeros(X_norm.shape[0])

for _ in range(max_iters):
    distances = np.linalg.norm(X_norm[:, np.newaxis] - centroids, axis=2)
    new_labels = np.argmin(distances, axis=1)
    if np.all(labels == new_labels):
        break
    labels = new_labels
    for i in range(k):
        if np.sum(labels == i) > 0:
            centroids[i] = np.mean(X_norm[labels == i], axis=0)

merged_df['cluster'] = labels

target_tags = ["Mechanotransduction", "Cilia", "ECM", "Thermodynamic_Cost", "Spine"]

best_cluster_score = -1
best_cluster_id = -1

for cluster_id in range(k):
    cluster_data = merged_df[merged_df['cluster'] == cluster_id]
    n_members = len(cluster_data)
    if n_members == 0: continue

    mean_anisotropy = cluster_data['Anisotropy'].mean()
    mean_disorder = cluster_data['Disorder_Proxy'].mean()

    all_tags = []
    for tags in cluster_data['pathway_tags'].dropna():
        all_tags.extend([t.strip() for t in tags.split(',')])

    tag_counts = pd.Series(all_tags).value_counts()
    top_tags = tag_counts.head(5).index.tolist()

    score = 0
    for tag in target_tags:
        count = tag_counts.get(tag, 0)
        score += count / n_members

    print(f"\nCluster {cluster_id}: N={n_members}")
    print(f"  Mean Anisotropy: {mean_anisotropy:.2f}")
    print(f"  Mean Disorder: {mean_disorder:.2f}")
    print(f"  Top Tags: {top_tags}")
    print(f"  Target Score: {score:.2f}")

    if score > best_cluster_score:
        best_cluster_score = score
        best_cluster_id = cluster_id

print(f"\nBest Cluster (ID {best_cluster_id}):")
best_cluster = merged_df[merged_df['cluster'] == best_cluster_id]
for _, row in best_cluster.iterrows():
    print(f"- {row['gene_symbol']}: Anisotropy={row['Anisotropy']:.2f}, Disorder={row['Disorder_Proxy']:.2f}, Tags={row['pathway_tags']}")

high_anisotropy_cluster_id = merged_df.groupby('cluster')['Anisotropy'].mean().idxmax()
if high_anisotropy_cluster_id != best_cluster_id:
    print(f"\nHigh Anisotropy Cluster (ID {high_anisotropy_cluster_id}):")
    high_cluster = merged_df[merged_df['cluster'] == high_anisotropy_cluster_id]
    for _, row in high_cluster.iterrows():
        print(f"- {row['gene_symbol']}: Anisotropy={row['Anisotropy']:.2f}, Disorder={row['Disorder_Proxy']:.2f}, Tags={row['pathway_tags']}")
