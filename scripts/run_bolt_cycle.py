#!/usr/bin/env python3
"""
run_bolt_cycle.py

Orchestrates a "Bolt-BioFold" analysis cycle on a default seed list.
"""

import sys
import pandas as pd
from pathlib import Path
import subprocess

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_root))

BASE_DIR = repo_root / "research" / "alphafold_countercurvature"
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Default Seed List
SEEDS = [
    "PIEZO2", "LBX1", "POC5", "FBN1", "PIEZO1",
    "YAP1", "COL1A1", "VIM", "LMNA", "GJA1"
]

def main():
    print("⚡ Bolt-BioFold Cycle Started ⚡")
    print(f"   Selected Seeds: {', '.join(SEEDS)}")

    # 1. Create candidates.csv
    print("\n[1/5] Preparing Candidate List...")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    master_csv = repo_root / "data" / "candidates_master.csv"
    if not master_csv.exists():
        print(f"❌ Master candidates file not found: {master_csv}")
        sys.exit(1)

    master_df = pd.read_csv(master_csv)

    # Filter for seeds
    candidates = master_df[master_df['gene_symbol'].isin(SEEDS)].copy()

    # Map columns to what the pipeline expects
    # Pipeline expects: gene_symbol, source, total_score
    # master_df has: gene_symbol, pathway_tags, priority_score

    candidates['source'] = candidates['pathway_tags'].apply(lambda x: x.split(',')[0] if pd.notna(x) else "Unknown")
    candidates['total_score'] = candidates['priority_score']

    # Select and rename
    candidates = candidates[['gene_symbol', 'source', 'total_score']]

    output_path = PROCESSED_DIR / "candidates.csv"
    candidates.to_csv(output_path, index=False)
    print(f"   Saved {len(candidates)} candidates to {output_path}")

    # 2. Map to UniProt
    print("\n[2/5] Mapping to UniProt...")
    cmd = [sys.executable, str(SCRIPTS_DIR / "01_map_to_uniprot.py")]
    subprocess.check_call(cmd)

    # 3. Fetch AFDB Data
    print("\n[3/5] Fetching AlphaFold Data...")
    cmd = [sys.executable, str(SCRIPTS_DIR / "02_fetch_afdb.py")]
    subprocess.check_call(cmd)

    # 4. Analyze Metrics
    print("\n[4/5] Analyzing Metrics...")
    # Force re-analysis or ensure it picks up the new list
    cmd = [sys.executable, str(SCRIPTS_DIR / "04_analyze_metrics.py")]
    subprocess.check_call(cmd)

    # 5. Generate Report
    print("\n[5/5] Generating Bolt Report...")
    cmd = [sys.executable, str(SCRIPTS_DIR / "06_bolt_report.py")]
    subprocess.check_call(cmd)

    print("\n✅ Bolt-BioFold Cycle Complete!")

    report_path = PROCESSED_DIR / "bolt_biofold_results.md"
    if report_path.exists():
        print(f"\n--- Report Output ({report_path}) ---\n")
        with open(report_path, 'r') as f:
            print(f.read())
    else:
        print("❌ Report file missing!")

if __name__ == "__main__":
    main()
