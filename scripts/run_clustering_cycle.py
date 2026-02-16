#!/usr/bin/env python3
"""
Run Clustering Cycle
--------------------
Extracts metrics from bolt_biofold_results.md and runs cluster_structure_metrics.py.
"""

import sys
import re
from pathlib import Path
import subprocess

# Paths
MD_PATH = Path("research/alphafold_countercurvature/data/processed/bolt_biofold_results.md")
TEMP_CSV = Path("temp_metrics.csv")
CLUSTERING_SCRIPT = Path("scripts/cluster_structure_metrics.py")
OUTPUT_REPORT = Path("reports/structure_clusters/latest_clusters.md")

def main():
    if not MD_PATH.exists():
        print(f"Error: {MD_PATH} not found.")
        sys.exit(1)

    print(f"Reading {MD_PATH}...")
    with open(MD_PATH, "r") as f:
        content = f.read()

    # Extract CSV block
    match = re.search(r"```csv\n(.*?)\n```", content, re.DOTALL)
    if not match:
        print("Error: CSV block not found in markdown.")
        sys.exit(1)

    csv_data = match.group(1)

    print(f"Writing CSV to {TEMP_CSV}...")
    with open(TEMP_CSV, "w") as f:
        f.write(csv_data)

    # Run clustering script
    print(f"Running {CLUSTERING_SCRIPT}...")
    subprocess.check_call([sys.executable, str(CLUSTERING_SCRIPT), str(TEMP_CSV)])

    # Print output report
    if OUTPUT_REPORT.exists():
        print(f"\n--- {OUTPUT_REPORT} ---\n")
        with open(OUTPUT_REPORT, "r") as f:
            print(f.read())
    else:
        print(f"Error: {OUTPUT_REPORT} was not generated.")

if __name__ == "__main__":
    main()
