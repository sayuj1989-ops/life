#!/usr/bin/env python3
"""
bolt_focused_cycle.py

Orchestrates a focused analysis cycle on a specific set of proteins.
If no inputs provided (default mode), runs on a "Default Seed List" of 5 representative proteins.

1. Sets up input CSVs (candidates.csv, bolt_targets.csv, uniprot_mapping.csv).
2. Runs 02_fetch_afdb.py to get structures.
3. Runs 04_analyze_metrics.py to compute metrics.
4. Runs 06_bolt_report.py to generate report.
5. Prints the final report to stdout.
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

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Default Seed List (Sourced from data/candidates_master.csv)
SEED_LIST = [
    {"gene_symbol": "PIEZO2", "uniprot_id": "Q9H5I5", "source": "DefaultSeed_Proprioception", "total_score": 95},
    {"gene_symbol": "LMNA",   "uniprot_id": "P02545", "source": "DefaultSeed_NuclearStiffness", "total_score": 92},
    {"gene_symbol": "COL1A1", "uniprot_id": "P02452", "source": "DefaultSeed_ECM_Gravity", "total_score": 90},
    {"gene_symbol": "DNAH11", "uniprot_id": "Q96DT5", "source": "DefaultSeed_Cilia_Flow", "total_score": 88},
    {"gene_symbol": "RUNX3",  "uniprot_id": "Q13761", "source": "DefaultSeed_Proprioception_Dev", "total_score": 95},
]

def run_step(script_name, description):
    print(f"\n🚀 Running {script_name}: {description}...")
    script_path = SCRIPT_DIR / script_name
    try:
        # Pass stdout/stderr to sys to see progress
        subprocess.run([sys.executable, str(script_path)], check=True)
        print(f"✅ {script_name} completed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name} failed with exit code {e.returncode}.")
        sys.exit(e.returncode)

def main():
    print("=== Bolt-BioFold ⚡ Focused Analysis Cycle ===")
    print("Mode: Default Seed List")

    # 1. Prepare Dataframes
    df = pd.DataFrame(SEED_LIST)

    # processed/candidates.csv (Used by 04_analyze_metrics.py)
    # Needs: gene_symbol, uniprot_id, source, total_score
    candidates_path = PROCESSED_DIR / "candidates.csv"
    df.to_csv(candidates_path, index=False)
    print(f"📄 Wrote {len(df)} candidates to {candidates_path}")

    # processed/bolt_targets.csv (Used by 06_bolt_report.py for filtering)
    # Needs: gene_symbol, source
    # (Actually 06 checks source_category in metrics, but uses this file to filter list)
    targets_path = PROCESSED_DIR / "bolt_targets.csv"
    df[['gene_symbol', 'source']].to_csv(targets_path, index=False)
    print(f"📄 Wrote targets to {targets_path}")

    # processed/uniprot_mapping.csv (Used by 02_fetch_afdb.py)
    # Needs: gene_symbol, uniprot_accession
    mapping_path = PROCESSED_DIR / "uniprot_mapping.csv"
    mapping_df = df[['gene_symbol', 'uniprot_id']].rename(columns={'uniprot_id': 'uniprot_accession'})
    mapping_df.to_csv(mapping_path, index=False)
    print(f"📄 Wrote mapping to {mapping_path}")

    # 2. Run Pipeline
    # Skip 01 (we made the mapping)

    # 02 Fetch
    run_step("02_fetch_afdb.py", "Fetch PDB/PAE from AlphaFold DB")

    # 04 Metrics
    run_step("04_analyze_metrics.py", "Compute Structural Metrics")

    # 06 Report
    run_step("06_bolt_report.py", "Generate Summary Report")

    # 3. Output Result
    report_path = PROCESSED_DIR / "bolt_biofold_results.md"
    if report_path.exists():
        print("\n" + "="*40)
        print("       FINAL REPORT OUTPUT")
        print("="*40 + "\n")
        with open(report_path, 'r') as f:
            print(f.read())
        print("\n" + "="*40)
    else:
        print(f"❌ Report not found at {report_path}")

if __name__ == "__main__":
    main()
