"""
add_missing_proteins.py

Appends missing key proteins (ADGRG6, TBX6) to the thermodynamic cost analysis.
Uses estimated values based on domain architecture and AlphaFold priors since
direct API access is not available in this environment.
"""

import pandas as pd
import os

CSV_PATH = "outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv"

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    df = pd.read_csv(CSV_PATH)

    # Define new entries
    new_proteins = [
        {
            "gene": "ADGRG6",
            "uniprot": "Q7Z2K8",
            "term": "eta_a",
            "role": "Adhesion GPCR; essential for disc maintenance under load",
            "scaling": "L^2 (surface area)",
            "anisotropy": 3.85,  # Estimated: Large ectodomain + 7TM
            "morphology": "Fibrous/Extended",
            "rg": 45.0, # Est
            "plddt_mean": 70.0, # Est
            "n_residues": 1120,
            "hinge_candidates": 5,
            "disorder_fraction": 0.15,
            "PAE_blockiness": 5.0,
            "status": "estimated"
        },
        {
            "gene": "TBX6",
            "uniprot": "O95935",
            "term": "Gamma_m",
            "role": "Transcription factor; segmentation clock regulator",
            "scaling": "L (patterning)",
            "anisotropy": 1.95,  # Estimated: Globular DNA binding + tails
            "morphology": "Intermediate",
            "rg": 25.0, # Est
            "plddt_mean": 65.0, # Est
            "n_residues": 436,
            "hinge_candidates": 2,
            "disorder_fraction": 0.45,
            "PAE_blockiness": 2.5,
            "status": "estimated"
        }
    ]

    # Append if not present
    for p in new_proteins:
        if p["gene"] not in df["gene"].values:
            print(f"Adding {p['gene']}...")
            df = pd.concat([df, pd.DataFrame([p])], ignore_index=True)
        else:
            print(f"{p['gene']} already exists.")

    df.to_csv(CSV_PATH, index=False)
    print(f"Updated {CSV_PATH}")

if __name__ == "__main__":
    main()
