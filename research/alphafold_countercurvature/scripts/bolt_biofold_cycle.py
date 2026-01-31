#!/usr/bin/env python3
"""
bolt_biofold_cycle.py

Executes one focused analysis cycle for Bolt-BioFold.
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

def run_step(script_name, description):
    print(f"\n⚡ [Bolt-BioFold] {description} ({script_name})...")
    script_path = SCRIPTS_DIR / script_name
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run {script_name}: {e}")
        sys.exit(1)

def main():
    print("⚡ Bolt-BioFold Analysis Cycle Initiated ⚡")

    # 1. Map candidates to UniProt
    run_step("01_map_to_uniprot.py", "Mapping candidates to UniProt")

    # 2. Fetch AlphaFold data
    run_step("02_fetch_afdb.py", "Fetching AlphaFold structures")

    # 3. Analyze metrics
    run_step("04_analyze_metrics.py", "Computing structural metrics")

    # 4. Generate Report
    run_step("06_bolt_report.py", "Generating Report")

    print("\n✅ Cycle Complete. Check research/alphafold_countercurvature/data/processed/bolt_biofold_results.md")

if __name__ == "__main__":
    main()
