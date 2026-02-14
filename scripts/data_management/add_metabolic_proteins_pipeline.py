#!/usr/bin/env python3
"""
scripts/add_metabolic_proteins_pipeline.py

Adds 6 missing metabolic proteins to the AFCC pipeline:
PPARGC1A, IGF1R, GHR, ARNTL, DMD, MYLK.

This script:
1. Extracts their data from candidates_master.csv.
2. Updates input files for the AFCC fetch/analyze pipeline.
3. Runs the fetch and analysis scripts.
4. Copies the output metrics to a manual update folder to ensure downstream tools pick them up.
"""

import sys
import shutil
import subprocess
import pandas as pd
from pathlib import Path

# Proteins to add
TARGETS = [
    "PPARGC1A", "IGF1R", "GHR", "ARNTL", "DMD", "MYLK"
]

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = REPO_ROOT / "data"
AFCC_DIR = REPO_ROOT / "research" / "alphafold_countercurvature"
PROCESSED_DIR = AFCC_DIR / "data" / "processed"
SCRIPTS_DIR = AFCC_DIR / "scripts"
OUTPUTS_DIR = REPO_ROOT / "outputs" / "afcc" / "manual_metabolic_update"

def main():
    print(f"🧬 Adding {len(TARGETS)} metabolic proteins to pipeline...")

    # 1. Read Master CSV to get details
    master_csv = DATA_DIR / "candidates_master.csv"
    if not master_csv.exists():
        print(f"Error: {master_csv} not found.")
        sys.exit(1)

    df = pd.read_csv(master_csv)

    # Filter for targets
    subset = df[df['gene_symbol'].isin(TARGETS)].copy()

    # Verify all targets found
    found = subset['gene_symbol'].tolist()
    missing = set(TARGETS) - set(found)
    if missing:
        print(f"Warning: Missing targets in master CSV: {missing}")

    print(f"   Found {len(subset)} targets in master CSV.")

    # Ensure processed directory exists
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Update uniprot_mapping.csv (for fetcher)
    mapping_path = PROCESSED_DIR / "uniprot_mapping.csv"
    mapping_df = subset[['gene_symbol', 'uniprot_id']].rename(columns={'uniprot_id': 'uniprot_accession'})
    mapping_df.to_csv(mapping_path, index=False)
    print(f"   -> Wrote temporary mapping to {mapping_path}")

    # 3. Update candidates.csv (for analyzer metadata)
    cand_path = PROCESSED_DIR / "candidates.csv"
    subset['source'] = subset['pathway_tags']
    subset['total_score'] = subset['priority_score']
    cols = ['gene_symbol', 'source', 'total_score', 'justification']
    # Ensure columns exist
    for c in cols:
        if c not in subset.columns:
            subset[c] = ""
    subset[cols].to_csv(cand_path, index=False)
    print(f"   -> Wrote temporary candidates metadata to {cand_path}")

    # 4. Run Fetch
    fetch_script = SCRIPTS_DIR / "02_fetch_afdb.py"
    print(f"\n🚀 Running Fetch Script: {fetch_script.name}...")
    try:
        subprocess.check_call([sys.executable, str(fetch_script)])
    except subprocess.CalledProcessError as e:
        print(f"Error running fetch script: {e}")
        # Continue if possible, maybe some fetched

    # 5. Run Analyze
    analyze_script = SCRIPTS_DIR / "04_analyze_metrics.py"
    print(f"\n🚀 Running Analyze Script: {analyze_script.name}...")
    try:
        subprocess.check_call([sys.executable, str(analyze_script)])
    except subprocess.CalledProcessError as e:
        print(f"Error running analyze script: {e}")
        sys.exit(1)

    # 6. Copy metrics to output dir
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    metrics_src = PROCESSED_DIR / "protein_metrics.csv"
    metrics_dst = OUTPUTS_DIR / "metrics.csv"

    if metrics_src.exists():
        shutil.copy(metrics_src, metrics_dst)
        print(f"\n✅ Pipeline Complete. Copied metrics to:\n   {metrics_dst}")
    else:
        print("\n❌ Error: Metrics file not generated!")
        sys.exit(1)

if __name__ == "__main__":
    main()
