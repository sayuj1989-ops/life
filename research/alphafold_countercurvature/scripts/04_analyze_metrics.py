#!/usr/bin/env python3
"""
04_analyze_metrics.py

Computes geometric and confidence metrics for all downloaded structures.
"""

import sys
import pandas as pd
from pathlib import Path
import warnings

# Suppress Bio.PDB warnings
warnings.filterwarnings("ignore")

repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(repo_root))

from research.alphafold_countercurvature.src.afcc.structure import StructureParser
from research.alphafold_countercurvature.src.afcc.metrics import MetricsAnalyzer

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MANIFEST_FILE = DATA_DIR / "manifest.csv"
OUTPUT_FILE = DATA_DIR / "processed" / "protein_metrics.csv"
CANDIDATES_FILE = DATA_DIR / "processed" / "candidates.csv"

def main():
    print("📏 Analyzing Structural Metrics...")

    if not MANIFEST_FILE.exists():
        print("❌ Manifest not found.")
        sys.exit(1)

    manifest = pd.read_csv(MANIFEST_FILE)
    downloaded = manifest[manifest['status'].isin(['downloaded', 'cached'])]

    # Load candidate info to get Source tags
    candidates = pd.read_csv(CANDIDATES_FILE) if CANDIDATES_FILE.exists() else None

    results = []
    parser = StructureParser()
    analyzer = MetricsAnalyzer()

    print(f"   Processing {len(downloaded)} structures...")

    for idx, row in downloaded.iterrows():
        pdb_path = Path(row['pdb_path'])
        gene = row['gene_symbol']
        uid = row['uniprot']

        structure = parser.parse_pdb(pdb_path, gene)
        if not structure:
            continue

        coords, plddt, resnames = parser.extract_coords_and_plddt(structure)
        metrics = analyzer.analyze_structure(structure, plddt, coords=coords, resnames=resnames)

        # Merge basic info
        metrics['gene_symbol'] = gene
        metrics['uniprot'] = uid

        # Merge source info
        if candidates is not None:
             cand_row = candidates[candidates['gene_symbol'] == gene]
             if not cand_row.empty:
                 metrics['source_category'] = cand_row.iloc[0]['source']
                 metrics['dise_score'] = cand_row.iloc[0]['total_score']

        results.append(metrics)

        if (idx + 1) % 5 == 0:
            print(f"   ... {idx + 1} done")

    df = pd.DataFrame(results)

    # Reorder columns
    cols = ['gene_symbol', 'uniprot', 'source_category', 'morphology',
            'anisotropy', 'radius_of_gyration', 'mean_plddt', 'n_residues', 'dise_score']
    # Add remaining cols
    remaining = [c for c in df.columns if c not in cols]
    df = df[cols + remaining]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ Metrics calculated for {len(df)} proteins.")
    print(f"📄 Saved to: {OUTPUT_FILE}")

    # Preview
    print("\nTop 5 High Anisotropy:")
    print(df.sort_values('anisotropy', ascending=False)[['gene_symbol', 'morphology', 'anisotropy', 'mean_plddt']].head().to_string(index=False))

if __name__ == "__main__":
    main()
