"""
Build Dataset for AlphaFold Analysis
Fetches proteins and creates an index CSV
"""

import argparse
import pandas as pd
import json
from pathlib import Path
from alphafold_analysis.fetch_bcc_structures import fetch_protein_structure, get_all_proteins

def main():
    parser = argparse.ArgumentParser(
        description="Build dataset index for AlphaFold analysis"
    )
    parser.add_argument(
        "--output",
        default="results/alphafold_dataset_index.csv",
        help="Output CSV file"
    )

    args = parser.parse_args()
    output_file = Path(args.output)

    print("🧬 Building AlphaFold Dataset Index")
    print("=" * 70)

    # Get all proteins
    proteins = get_all_proteins()

    results = []
    for i, protein in enumerate(proteins, 1):
        print(f"[{i}/{len(proteins)}] {protein['name']} ({protein['gene']})")
        # Fetch or get cached structure
        result = fetch_protein_structure(protein)

        # Add to results if we have a PDB path
        if result['status'] in ['downloaded', 'cached'] and result['pdb_path']:
             results.append({
                 "name": protein['name'],
                 "gene": protein['gene'],
                 "uniprot_id": protein['uniprot'],
                 "category": protein['category'],
                 "pdb_path": result['pdb_path'],
                 "function": protein['function']
             })

    # Create DataFrame
    df = pd.DataFrame(results)

    # Save to CSV
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"\n✅ Dataset index built with {len(df)} proteins")
    print(f"📝 Saved to: {output_file}")

if __name__ == "__main__":
    main()
