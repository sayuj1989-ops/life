#!/usr/bin/env python3
import sys
import os
import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Bio.PDB import PDBParser
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add the source directory to sys.path to import metrics
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../research/alphafold_countercurvature/src')))
try:
    from afcc.metrics import MetricsAnalyzer
    from afcc.structure import StructureParser
except ImportError:
    # If the import fails, we might be running from repo root
    sys.path.append(os.path.abspath('research/alphafold_countercurvature/src'))
    from afcc.metrics import MetricsAnalyzer
    from afcc.structure import StructureParser

# Configuration
PROTEINS = [
    {"symbol": "FBN1", "uniprot": "P35555", "species": "Homo sapiens"},
    {"symbol": "COL1A1", "uniprot": "P02452", "species": "Homo sapiens"},
    {"symbol": "PIEZO2", "uniprot": "Q9H5I5", "species": "Homo sapiens"},
    {"symbol": "YAP1", "uniprot": "P46937", "species": "Homo sapiens"},
    {"symbol": "PKD2", "uniprot": "Q13563", "species": "Homo sapiens"},
    {"symbol": "IGF1R", "uniprot": "P08069", "species": "Homo sapiens"},
    {"symbol": "LBX1", "uniprot": "P52954", "species": "Homo sapiens"},
    {"symbol": "ADGRG6", "uniprot": "Q7Z2K8", "species": "Homo sapiens"},
    {"symbol": "DMD", "uniprot": "P11532", "species": "Homo sapiens"},
    {"symbol": "PPARGC1A", "uniprot": "Q9UBK2", "species": "Homo sapiens"},
    {"symbol": "GHR", "uniprot": "P10912", "species": "Homo sapiens"},
    {"symbol": "ARNTL", "uniprot": "O00327", "species": "Homo sapiens"},
    {"symbol": "MYLK", "uniprot": "Q15746", "species": "Homo sapiens"},
]

OUTPUT_DIR = "outputs"
TEMP_DIR = "temp/afdb"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def fetch_afdb_data(uniprot_id: str) -> Optional[Dict[str, str]]:
    """Fetches PDB and PAE JSON for a given UniProt ID using the API."""
    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"

    pdb_path = os.path.join(TEMP_DIR, f"{uniprot_id}.pdb")
    pae_path = os.path.join(TEMP_DIR, f"{uniprot_id}.json")

    # Check if files already exist
    if os.path.exists(pdb_path) and os.path.exists(pae_path):
        return {"pdb": pdb_path, "pae": pae_path}

    print(f"Querying API for {uniprot_id}...")
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
             print(f"API Error for {uniprot_id}: {response.status_code}")
             return None
        data = response.json()
        if not data or not isinstance(data, list):
             print(f"Invalid API response for {uniprot_id}")
             return None

        # Take the first entry (usually the main one)
        entry = data[0]
        pdb_url = entry.get('pdbUrl')
        pae_url = entry.get('paeDocUrl')

        if not pdb_url:
             print(f"No PDB URL found for {uniprot_id}")
             return None

        # Download PDB
        print(f"Downloading PDB from {pdb_url}...")
        pdb_resp = requests.get(pdb_url)
        if pdb_resp.status_code == 200:
             with open(pdb_path, 'wb') as f:
                 f.write(pdb_resp.content)
        else:
             print(f"Failed to download PDB: {pdb_resp.status_code}")
             return None

        # Download PAE
        if pae_url:
            print(f"Downloading PAE from {pae_url}...")
            pae_resp = requests.get(pae_url)
            if pae_resp.status_code == 200:
                with open(pae_path, 'wb') as f:
                    f.write(pae_resp.content)
            else:
                print(f"Failed to download PAE: {pae_resp.status_code}")
                # Optional

        return {"pdb": pdb_path, "pae": pae_path if os.path.exists(pae_path) else None}

    except Exception as e:
        print(f"Exception fetching data for {uniprot_id}: {e}")
        return None

def print_markdown_table(df: pd.DataFrame):
    """Prints a DataFrame as a Markdown table manually."""
    if df.empty:
        print("No data to display.")
        return

    cols = df.columns.tolist()
    # Header
    print("| " + " | ".join(cols) + " |")
    # Separator
    print("| " + " | ".join(["---"] * len(cols)) + " |")
    # Rows
    for _, row in df.iterrows():
        row_str = [str(val) for val in row.values]
        print("| " + " | ".join(row_str) + " |")

def main():
    # ⚡ Bolt Optimization: Use shared StructureParser for caching and fast parsing
    parser = StructureParser()
    analyzer = MetricsAnalyzer()
    results = []

    # Store data for plotting
    plot_data = {}

    print(f"Starting Bolt-BioFold Analysis Cycle on {len(PROTEINS)} proteins...")

    for prot in PROTEINS:
        uid = prot['uniprot']
        symbol = prot['symbol']
        print(f"Processing {symbol} ({uid})...")

        paths = fetch_afdb_data(uid)
        if not paths:
            print(f"Skipping {symbol} - data fetch failed.")
            continue

        # ⚡ Bolt Optimization: Use fast parser with caching
        coords, plddt, resnames = parser.fast_parse_pdb_arrays(Path(paths['pdb']))
        if coords is None:
            print(f"Skipping {symbol} - PDB parsing failed.")
            continue

        pae_matrix = parser.parse_pae(Path(paths['pae'])) if paths['pae'] else None

        # Run Analysis
        metrics = analyzer.analyze_structure(
            coords=coords,
            plddt_scores=plddt,
            resnames=resnames,
            pae_matrix=pae_matrix
        )

        # Combine identity + metrics
        entry = {
            "protein_id": f"{symbol} ({uid})",
            "species": prot['species'],
            "length": metrics['n_residues'],

            # Confidence
            "pLDDT_mean": f"{metrics['plddt_mean']:.2f}",
            "pLDDT_median": f"{metrics['plddt_median']:.2f}",
            "pLDDT_fraction_high": f"{metrics['plddt_fraction_high']:.2f}",
            "pLDDT_fraction_ok": f"{metrics['plddt_fraction_ok']:.2f}",
            "pLDDT_fraction_low": f"{metrics['plddt_fraction_low']:.2f}",
            "PAE_mean": f"{metrics['PAE_mean']:.2f}",
            "PAE_domain_blockiness_score": f"{metrics['PAE_domain_blockiness_score']:.2f}",

            # Architecture
            "predicted_domain_segments": metrics['predicted_domain_segments'],
            "disorder_fraction_proxy": f"{metrics['disorder_fraction_proxy']:.2f}",
            "hinge_candidates": metrics['hinge_candidates'],
            "morphology": metrics['morphology'],

            # Geometry
            "backbone_principal_axis": metrics['backbone_principal_axis'],
            "radius_of_gyration": f"{metrics['radius_of_gyration']:.2f}",
            "end_to_end_distance": f"{metrics['end_to_end_distance']:.2f}",
            "curvature_summary": f"{metrics['curvature_summary']:.4f}",
            "torsion_summary": f"{metrics['torsion_summary']:.4f}",
            "anisotropy_index": f"{metrics['anisotropy_index']:.2f}",
            "bending_hotspots": metrics['bending_hotspots'],

            # Surface
            "exposed_surface_proxy": f"{metrics['exposed_surface_proxy']:.2f}",
            "charged_patch_score": f"{metrics['charged_patch_score']:.2f}",

            # Flags
            "low_confidence_warning": metrics['low_confidence_warning'],
            "multi_domain_uncertain": metrics['multi_domain_uncertain'],
            "likely_IDR_heavy": metrics['likely_IDR_heavy']
        }

        results.append(entry)
        plot_data[symbol] = plddt

    # Generate Outputs
    df = pd.DataFrame(results)

    # Markdown Table
    print("\n### Results Table")
    print_markdown_table(df)

    # CSV Block
    print("\n### CSV Output")
    print("```csv")
    print(df.to_csv(index=False))
    print("```")

    # Plotting
    plt.figure(figsize=(10, 6))
    for symbol, plddt in plot_data.items():
        plt.plot(plddt, label=symbol, alpha=0.7, linewidth=1)

    plt.title("Per-Residue Confidence (pLDDT)")
    plt.xlabel("Residue Index")
    plt.ylabel("pLDDT")
    plt.axhline(70, color='gray', linestyle='--', alpha=0.5, label='Confidence Threshold (70)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "bolt_biofold_plddt.png"))
    print(f"\nSaved plot to {os.path.join(OUTPUT_DIR, 'bolt_biofold_plddt.png')}")

    # Interpretation
    print("\n### Interpretation")
    for row in results:
        symbol = row['protein_id'].split()[0]
        anisotropy = float(row['anisotropy_index'])
        hinges = int(row['hinge_candidates'])
        plddt_high = float(row['pLDDT_fraction_high'])
        curvature = float(row['curvature_summary'])

        interp = f"- **{symbol}**: "
        conf_level = "High" if plddt_high > 0.8 else ("Medium" if plddt_high > 0.5 else "Low")

        # Heuristics
        what_we_see = []
        if anisotropy > 3.0: what_we_see.append("Highly elongated/Fibrous")
        elif anisotropy < 1.5: what_we_see.append("Globular")
        else: what_we_see.append("Intermediate shape")

        if hinges > 0: what_we_see.append(f"{hinges} potential hinge(s)")
        if curvature > 0.1: what_we_see.append("High local curvature")

        interp += f"({conf_level} Confidence). We see: {', '.join(what_we_see)}. "

        # Why it matters
        if "PIEZO" in symbol:
            interp += "Matters: Mechanosensitive channel; curvature/hinges likely relate to gating mechanics under membrane tension."
        elif "FBN1" in symbol or "COL" in symbol:
            interp += "Matters: ECM structural component; anisotropy defines load-bearing axis and tissue stiffness."
        elif "YAP" in symbol:
            interp += "Matters: Mechanotransducer; structural disorder likely facilitates binding versatility under stress."
        elif "DMD" in symbol:
            interp += "Matters: Muscle-ECM linker; massive length and flexibility essential for shock absorption."
        else:
            interp += "Matters: Structural metrics imply role in mechanical integrity or sensing."

        # Next Test
        if hinges > 0 and anisotropy > 2:
            next_test = "Next: Test mechanical gating/unfolding under force."
        elif row['likely_IDR_heavy']:
             next_test = "Next: Analyze IDR phase separation potential."
        else:
            next_test = "Next: Compare with orthologs to check conservation of geometry."

        print(f"{interp} {next_test}")

    # Best Next Move
    print("\n### Best Next Move")
    print("Correlate curvature metrics (especially hinge locations) with known pathogenic variants in these genes.")

if __name__ == "__main__":
    main()
