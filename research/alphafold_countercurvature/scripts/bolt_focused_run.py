#!/usr/bin/env python3
"""
bolt_focused_run.py

Executes a focused "Bolt-BioFold" analysis cycle on a specific seed list of proteins.
bypasses the daily candidate selection logic and directly prepares the pipeline for specific targets.
"""

import sys
import pandas as pd
import subprocess
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
AFCC_DIR = REPO_ROOT / "research" / "alphafold_countercurvature"
DATA_DIR = AFCC_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

PROCESSED_CANDIDATES = PROCESSED_DIR / "candidates.csv"
BOLT_TARGETS = PROCESSED_DIR / "bolt_targets.csv"
MAPPING_FILE = PROCESSED_DIR / "uniprot_mapping.csv"
METRICS_FILE = PROCESSED_DIR / "protein_metrics.csv"

# Seed List
SEED_LIST = [
    {"gene_symbol": "PIEZO2", "uniprot_id": "Q9H5I5", "priority_score": 95},
    {"gene_symbol": "LMNA",   "uniprot_id": "P02545", "priority_score": 92},
    {"gene_symbol": "FBN1",   "uniprot_id": "P35555", "priority_score": 92},
    {"gene_symbol": "EGR3",   "uniprot_id": "Q06889", "priority_score": 92},
    {"gene_symbol": "RUNX3",  "uniprot_id": "Q13761", "priority_score": 95}
]

def run_script(script_name):
    print(f"\n🚀 Running {script_name}...")
    script_path = SCRIPT_DIR / script_name
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
        print(f"✅ {script_name} completed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name} failed with exit code {e.returncode}.")
        sys.exit(e.returncode)

def main():
    print("=== Bolt-BioFold ⚡ Focused Analysis Cycle ===")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Prepare Dataframes
    print("📋 Preparing input data...")
    df = pd.DataFrame(SEED_LIST)
    df['source'] = 'Bolt_Seed_List'
    df['total_score'] = df['priority_score']

    # Prepare candidates.csv with correct schema
    # Expected: gene_symbol, uniprot_accession, source, total_score, priority_score, justification
    cand_df = df.rename(columns={'uniprot_id': 'uniprot_accession'})
    cand_df['justification'] = "Focused Cycle Run"

    # Write candidates.csv (used by 04 metrics)
    cand_df.to_csv(PROCESSED_CANDIDATES, index=False)
    print(f"   Saved candidates to {PROCESSED_CANDIDATES}")

    # Write bolt_targets.csv (used by 06 report)
    df[['gene_symbol', 'source']].to_csv(BOLT_TARGETS, index=False)
    print(f"   Saved targets to {BOLT_TARGETS}")

    # Write uniprot_mapping.csv (used by 02 fetcher)
    mapping_df = df[['gene_symbol', 'uniprot_id']].rename(columns={'uniprot_id': 'uniprot_accession'})
    mapping_df['organism_id'] = "9606"
    mapping_df.to_csv(MAPPING_FILE, index=False)
    print(f"   Saved mapping to {MAPPING_FILE}")

    # 2. Force Refresh of Metrics
    # Remove these proteins from protein_metrics.csv to force re-computation
    if METRICS_FILE.exists():
        print("🧹 Cleaning old metrics for target proteins...")
        metrics_df = pd.read_csv(METRICS_FILE)
        initial_count = len(metrics_df)
        target_genes = df['gene_symbol'].tolist()

        metrics_df = metrics_df[~metrics_df['gene_symbol'].isin(target_genes)]

        removed = initial_count - len(metrics_df)
        metrics_df.to_csv(METRICS_FILE, index=False)
        print(f"   Removed {removed} entries from {METRICS_FILE}")

    # 3. Run Pipeline Steps
    # Step 02: Fetch Data
    run_script("02_fetch_afdb.py")

    # Step 04: Analyze Metrics
    run_script("04_analyze_metrics.py")

    # Step 06: Generate Report
    run_script("06_bolt_report.py")

    print("\n✅ Focused Cycle Complete.")
    print(f"📝 Report: {PROCESSED_DIR / 'bolt_biofold_results.md'}")

if __name__ == "__main__":
    main()
