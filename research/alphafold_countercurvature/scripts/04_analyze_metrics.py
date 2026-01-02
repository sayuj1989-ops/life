#!/usr/bin/env python3
"""
04_analyze_metrics.py

Computes geometric and confidence metrics for all downloaded structures.
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import json

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

def load_pae(pae_path):
    if not pae_path or pd.isna(pae_path):
        return None
    try:
        with open(pae_path, 'r') as f:
            data = json.load(f)
            # AlphaFold DB PAE format usually has 'predicted_aligned_error' key
            if isinstance(data, list) and len(data) > 0 and 'predicted_aligned_error' in data[0]:
                return np.array(data[0]['predicted_aligned_error'])
            # Some other formats might differ, but AFDB typically returns list of objects
            # Or if it's the raw JSON from fetch_afdb
            if isinstance(data, list):
                # Try finding one with the key
                for item in data:
                    if 'predicted_aligned_error' in item:
                        return np.array(item['predicted_aligned_error'])
    except Exception as e:
        # print(f"Warning: Failed to load PAE from {pae_path}: {e}")
        pass
    return None

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
        pae_path = row['pae_path'] if 'pae_path' in row else None
        gene = row['gene_symbol']
        uid = row['uniprot']

        structure = parser.parse_pdb(pdb_path, gene)
        if not structure:
            continue

        coords, plddt = parser.extract_coords_and_plddt(structure)

        # Load PAE
        pae_matrix = load_pae(pae_path)

        metrics = analyzer.analyze_structure(structure, plddt, coords=coords, pae_matrix=pae_matrix)

        # Merge basic info
        metrics['gene_symbol'] = gene
        metrics['uniprot'] = uid
        metrics['length'] = metrics['n_residues']
        metrics['species'] = "Homo sapiens" # Default for this run

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

    # Reorder columns as requested
    # Identity
    cols = ['gene_symbol', 'uniprot', 'species', 'length', 'source_category']
    # Quality
    cols += ['pLDDT_mean', 'pLDDT_median', 'pLDDT_fraction_high', 'pLDDT_fraction_ok', 'pLDDT_fraction_low', 'PAE_mean', 'PAE_domain_blockiness_score']
    # Architecture
    cols += ['morphology', 'anisotropy', 'radius_of_gyration', 'low_confidence_warning', 'multi_domain_uncertain', 'likely_IDR_heavy']
    # Geometry
    cols += ['end_to_end_distance', 'curvature_summary', 'torsion_summary', 'bending_hotspots', 'backbone_principal_axis']
    # Interaction
    cols += ['exposed_fraction', 'charged_patch_score']

    # Add any extra cols at the end
    remaining = [c for c in df.columns if c not in cols]
    df = df[cols + remaining]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ Metrics calculated for {len(df)} proteins.")
    print(f"📄 Saved to: {OUTPUT_FILE}")

    # Preview
    print("\nTop 5 High Anisotropy:")
    if 'anisotropy' in df.columns:
        print(df.sort_values('anisotropy', ascending=False)[['gene_symbol', 'morphology', 'anisotropy', 'pLDDT_mean']].head().to_string(index=False))

if __name__ == "__main__":
    main()
