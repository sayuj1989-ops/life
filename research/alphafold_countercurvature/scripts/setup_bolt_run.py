
import pandas as pd
from pathlib import Path
import sys

# Define paths
REPO_ROOT = Path(".").resolve()
MASTER_CANDIDATES_PATH = REPO_ROOT / "data" / "candidates_master.csv"
AFCC_DIR = REPO_ROOT / "research" / "alphafold_countercurvature"
PROCESSED_DIR = AFCC_DIR / "data" / "processed"

SEED_LIST = [
    "PIEZO2", "LBX1", "IFT88", "FBN1", "PIEZO1",
    "YAP1", "POC5", "ITGB1", "KIF3A", "ACAN",
    "COL2A1", "LMNA", "FLNA", "SMAD3", "NF1",
    "COL1A1", "DMD", "DNAH11", "TWIST1", "RHOA"
]

def main():
    print(f"🚀 Preparing Bolt run for {len(SEED_LIST)} seed proteins...")

    # Ensure processed directory exists
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load Master List
    if not MASTER_CANDIDATES_PATH.exists():
        print(f"❌ Master candidates file not found: {MASTER_CANDIDATES_PATH}")
        sys.exit(1)

    df = pd.read_csv(MASTER_CANDIDATES_PATH)

    # Filter for seed list
    filtered_df = df[df['gene_symbol'].isin(SEED_LIST)]

    print(f"✅ Found {len(filtered_df)} candidates matching seed list.")

    missing = set(SEED_LIST) - set(filtered_df['gene_symbol'].unique())
    if missing:
        print(f"⚠️ Missing candidates from master list: {missing}")

    # 2. Create candidates.csv for AFCC pipeline
    candidates_df = pd.DataFrame()
    candidates_df['gene_symbol'] = filtered_df['gene_symbol']
    # Use the first pathway tag as source
    candidates_df['source'] = filtered_df['pathway_tags'].apply(
        lambda x: x.split(',')[0].strip() if isinstance(x, str) and x else "MasterList"
    )
    candidates_df['total_score'] = filtered_df['priority_score']

    candidates_out = PROCESSED_DIR / "candidates.csv"
    candidates_df.to_csv(candidates_out, index=False)
    print(f"📄 Wrote {candidates_out}")

    # 3. Create uniprot_mapping.csv for AFCC pipeline
    mapping_df = pd.DataFrame()
    mapping_df['gene_symbol'] = filtered_df['gene_symbol']
    mapping_df['uniprot_accession'] = filtered_df['uniprot_id']

    mapping_out = PROCESSED_DIR / "uniprot_mapping.csv"
    mapping_df.to_csv(mapping_out, index=False)
    print(f"📄 Wrote {mapping_out}")

    print("✨ Preparation complete.")

if __name__ == "__main__":
    main()
