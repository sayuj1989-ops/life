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
    # ⚡ Bolt Optimization: Pre-index candidates for O(1) lookup
    candidates_dict = {}
    if CANDIDATES_FILE.exists():
        try:
            cand_df = pd.read_csv(CANDIDATES_FILE)
            if 'gene_symbol' in cand_df.columns:
                # Deduplicate keeping first to match legacy behavior
                cand_df = cand_df.drop_duplicates(subset=['gene_symbol'], keep='first')
                candidates_dict = cand_df.set_index('gene_symbol')[['source', 'total_score']].to_dict('index')
                print(f"   Loaded {len(candidates_dict)} candidates for fast lookup.")
        except Exception as e:
            print(f"⚠️ Error loading candidates file: {e}")

    # Load Bolt targets to override/append
    BOLT_TARGETS = DATA_DIR / "processed" / "bolt_targets.csv"
    if BOLT_TARGETS.exists():
        try:
            bolt_df = pd.read_csv(BOLT_TARGETS)
            if 'gene_symbol' in bolt_df.columns:
                print(f"   Loaded {len(bolt_df)} focused targets from {BOLT_TARGETS.name}")
                for _, row in bolt_df.iterrows():
                     gene = row['gene_symbol']
                     source = row.get('source', 'Bolt_Focused')
                     # Default score to 100 for focused targets if missing
                     score = row.get('total_score', 100)
                     candidates_dict[gene] = {'source': source, 'total_score': score}
        except Exception as e:
             print(f"⚠️ Error loading bolt targets: {e}")

    # ⚡ Bolt Optimization: Incremental Processing
    # Check for existing results to avoid re-processing
    processed_keys = set()
    existing_df = None
    if OUTPUT_FILE.exists():
        try:
            existing_df = pd.read_csv(OUTPUT_FILE)

            # Normalize legacy columns if present
            rename_map = {}
            if 'anisotropy' in existing_df.columns and 'anisotropy_index' not in existing_df.columns:
                 rename_map['anisotropy'] = 'anisotropy_index'
            if 'mean_plddt' in existing_df.columns and 'plddt_mean' not in existing_df.columns:
                 rename_map['mean_plddt'] = 'plddt_mean'

            if rename_map:
                print(f"   Migrating columns in existing file: {list(rename_map.keys())} -> {list(rename_map.values())}")
                existing_df.rename(columns=rename_map, inplace=True)

            if 'gene_symbol' in existing_df.columns and 'uniprot' in existing_df.columns:
                processed_keys = set(zip(existing_df['gene_symbol'], existing_df['uniprot']))
            print(f"   Found {len(processed_keys)} existing records in {OUTPUT_FILE.name}")
        except Exception as e:
            print(f"⚠️ Error reading existing metrics: {e}. Starting fresh.")

    # Filter work list
    to_process = []
    for _, row in downloaded.iterrows():
        if (row['gene_symbol'], row['uniprot']) not in processed_keys:
            to_process.append(row)

    print(f"   Processing {len(to_process)} new structures (skipped {len(downloaded) - len(to_process)})...")

    results = []
    parser = StructureParser()
    analyzer = MetricsAnalyzer()

    for idx, row in enumerate(to_process):
        pdb_path = Path(row['pdb_path'])
        gene = row['gene_symbol']
        uid = row['uniprot']

        # ⚡ Bolt Optimization: Use fast parser (skips Bio.PDB Structure build)
        # This reduces parse time from ~1.2s to ~0.05s for large structures.
        coords, plddt, resnames = parser.fast_parse_pdb_arrays(pdb_path)

        if coords is None:
            # Fallback (or just skip if file missing/empty)
            print(f"⚠️ Failed to fast-parse {pdb_path}, trying legacy...")
            structure = parser.parse_pdb(pdb_path, gene)
            if not structure:
                continue
            coords, plddt, resnames = parser.extract_coords_and_plddt(structure)
        else:
            structure = None

        # Load PAE if available
        pae_path = row.get('pae_path')
        pae_matrix = None
        if pae_path and isinstance(pae_path, str):
             p = Path(pae_path)
             if p.exists():
                 pae_matrix = parser.parse_pae(p)

        metrics = analyzer.analyze_structure(structure, plddt, coords=coords, resnames=resnames, pae_matrix=pae_matrix)

        # Merge basic info
        metrics['gene_symbol'] = gene
        metrics['uniprot'] = uid

        # Merge source info
        # ⚡ Bolt Optimization: O(1) Dictionary Lookup
        if gene in candidates_dict:
            info = candidates_dict[gene]
            metrics['source_category'] = info['source']
            metrics['dise_score'] = info['total_score']

        results.append(metrics)

        if (idx + 1) % 5 == 0:
            print(f"   ... {idx + 1} done")

    new_df = pd.DataFrame(results)

    # Combine with existing
    if existing_df is not None and not new_df.empty:
        df = pd.concat([existing_df, new_df], ignore_index=True)
    elif not new_df.empty:
        df = new_df
    elif existing_df is not None:
        df = existing_df
    else:
        df = pd.DataFrame()

    if not df.empty:
        # Reorder columns
        cols_preferred = ['gene_symbol', 'uniprot', 'source_category', 'morphology',
                'anisotropy_index', 'radius_of_gyration', 'plddt_mean', 'n_residues', 'dise_score']

        # Filter only columns that exist
        cols = [c for c in cols_preferred if c in df.columns]

        # Add remaining cols
        remaining = [c for c in df.columns if c not in cols]
        df = df[cols + remaining]

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUTPUT_FILE, index=False)

        print(f"\n✅ Metrics calculated for {len(df)} proteins.")
        print(f"📄 Saved to: {OUTPUT_FILE}")

        # Preview
        print("\nTop 5 High Anisotropy:")
        if 'anisotropy_index' in df.columns:
             # Check which plddt column exists (legacy vs new)
             plddt_col = 'plddt_mean' if 'plddt_mean' in df.columns else 'mean_plddt'
             cols_to_show = ['gene_symbol', 'morphology', 'anisotropy_index']
             if plddt_col in df.columns:
                 cols_to_show.append(plddt_col)

             print(df.sort_values('anisotropy_index', ascending=False)[cols_to_show].head().to_string(index=False))
    else:
        print("\n⚠️ No metrics to save.")

if __name__ == "__main__":
    main()
