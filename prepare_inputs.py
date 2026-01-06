import pandas as pd
import os

# Paths
# The script is run from repo root
REPO_ROOT = os.getcwd()
BASE_DIR = os.path.join(REPO_ROOT, "research/alphafold_countercurvature")
AFCC_DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(AFCC_DATA_DIR, "processed")

# Master candidates is in the root data folder
MASTER_CANDIDATES = os.path.join(REPO_ROOT, "data", "candidates_master.csv")

# Ensure processed directory exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Read master candidates
if not os.path.exists(MASTER_CANDIDATES):
    raise FileNotFoundError(f"Master candidates file not found at: {MASTER_CANDIDATES}")

df = pd.read_csv(MASTER_CANDIDATES)

# Sort by priority_score (descending) and take top 10
top_10 = df.sort_values(by="priority_score", ascending=False).head(10)

# 1. Create uniprot_mapping.csv for 02_fetch_afdb.py
# Columns needed: gene_symbol, uniprot_accession
mapping_df = top_10[["gene_symbol", "uniprot_id"]].rename(columns={"uniprot_id": "uniprot_accession"})
mapping_path = os.path.join(PROCESSED_DIR, "uniprot_mapping.csv")
mapping_df.to_csv(mapping_path, index=False)
print(f"Created {mapping_path}")

# 2. Create candidates.csv for 04_analyze_metrics.py
# Columns needed: gene_symbol, source, total_score
# Map 'pathway_tags' to 'source' (just take the first tag)
# Map 'priority_score' to 'total_score'
candidates_df = top_10[["gene_symbol", "pathway_tags", "priority_score"]].copy()
candidates_df["source"] = candidates_df["pathway_tags"].apply(lambda x: x.split(",")[0] if isinstance(x, str) else "Unknown")
candidates_df = candidates_df.rename(columns={"priority_score": "total_score"})
candidates_path = os.path.join(PROCESSED_DIR, "candidates.csv")
candidates_df.to_csv(candidates_path, index=False)
print(f"Created {candidates_path}")

print("Top 10 Candidates:")
print(top_10[["gene_symbol", "priority_score"]])
