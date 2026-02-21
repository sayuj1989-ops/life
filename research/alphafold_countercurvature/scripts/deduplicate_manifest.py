#!/usr/bin/env python3
"""
deduplicate_manifest.py

Removes duplicate entries from manifest.csv, keeping the most recent one.
Duplicates are identified by (gene_symbol, uniprot).
"""

import pandas as pd
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MANIFEST_FILE = DATA_DIR / "manifest.csv"

def main():
    if not MANIFEST_FILE.exists():
        print("Manifest not found.")
        return

    print(f"Reading {MANIFEST_FILE}...")
    df = pd.read_csv(MANIFEST_FILE)

    initial_count = len(df)

    # Sort by retrieved_at descending to keep latest
    if 'retrieved_at' in df.columns:
        df['retrieved_at'] = pd.to_datetime(df['retrieved_at'], errors='coerce')
        df = df.sort_values('retrieved_at', ascending=False)

    # Deduplicate by uniprot (primary key for AFDB fetch)
    # Also considering gene_symbol to be safe, but uniprot is the unique ID for structure.
    # If same uniprot appears multiple times, it's a duplicate fetch.

    # Remove duplicates based on 'uniprot'
    df_clean = df.drop_duplicates(subset=['uniprot'], keep='first')

    # Also remove duplicates based on 'gene_symbol' if uniprot is different?
    # No, different uniprots for same gene might be valid (isoforms).
    # But let's check if we have exact duplicates of (gene, uniprot).

    # The drop_duplicates on 'uniprot' handles (gene, uniprot) duplicates too since uniprot is part of it.

    final_count = len(df_clean)
    removed = initial_count - final_count

    if removed > 0:
        print(f"Found {removed} duplicate entries.")
        # Sort by gene symbol for tidiness
        df_clean = df_clean.sort_values('gene_symbol')
        df_clean.to_csv(MANIFEST_FILE, index=False)
        print(f"✅ Cleaned manifest saved. {final_count} entries remaining.")
    else:
        print("✅ No duplicates found.")

if __name__ == "__main__":
    main()
