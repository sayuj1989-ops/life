#!/usr/bin/env python3
"""
Confidence-Weighted Structural Ranking Script
Re-ranks candidates based on structural confidence (pLDDT) and anisotropy.
"""

import csv
import os

INPUT_FILE = "outputs/afcc/2026-02-16/metrics.csv"
OUTPUT_FILE = "outputs/afcc/confidence_weighted_ranking.csv"

# Comparator list
COMPARATORS = {'LBX1', 'PIEZO2', 'LMNA', 'POC5', 'ADGRG6', 'RUNX3', 'GHR', 'CNNM2', 'FBLN5'}

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file {INPUT_FILE} not found.")
        return

    candidates = []

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                gene = row['gene_symbol']
                aniso = float(row.get('anisotropy_index', 0))
                plddt = float(row.get('plddt_mean', 0))
                pae_block = float(row.get('PAE_domain_blockiness_score', 0))

                # Calculate Weighted Score
                weighted_score = aniso * (plddt / 100.0)

                # Determine Tier
                if aniso >= 3.0 and plddt >= 70.0:
                    tier = "Tier 1: High Confidence"
                elif aniso >= 3.0 and plddt < 70.0:
                    tier = "Tier 2: Low Confidence"
                else:
                    tier = "Tier 3: Other"

                candidates.append({
                    'gene': gene,
                    'anisotropy': aniso,
                    'plddt': plddt,
                    'pae_blockiness': pae_block,
                    'weighted_score': weighted_score,
                    'tier': tier,
                    'is_comparator': gene in COMPARATORS
                })
            except ValueError:
                continue

    # Sort by Weighted Score descending
    candidates.sort(key=lambda x: x['weighted_score'], reverse=True)

    # Assign Ranks
    for i, c in enumerate(candidates, 1):
        c['rank'] = i

    # Write Output
    headers = ['rank', 'gene', 'tier', 'weighted_score', 'anisotropy', 'plddt', 'pae_blockiness', 'is_comparator']

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for c in candidates:
            writer.writerow(c)

    print(f"Successfully wrote ranked list to {OUTPUT_FILE}")

    # Print Comparators to stdout for quick check
    print("\n--- Comparator Analysis ---")
    comp_list = [c for c in candidates if c['is_comparator']]
    comp_list.sort(key=lambda x: x['weighted_score'], reverse=True) # Sort again just in case

    print(f"{'Rank':<5} | {'Gene':<8} | {'Tier':<22} | {'W.Score':<7} | {'Aniso':<7} | {'pLDDT':<7}")
    print("-" * 75)
    for c in comp_list:
        print(f"{c['rank']:<5} | {c['gene']:<8} | {c['tier']:<22} | {c['weighted_score']:.2f}    | {c['anisotropy']:.2f}    | {c['plddt']:.1f}")

if __name__ == "__main__":
    main()
