#!/usr/bin/env python3
import sys
import os
import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from Bio.PDB import PDBParser
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import subprocess

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

# Configuration: Default Seed List
DEFAULT_SEED_LIST = [
    {"symbol": "FBN1", "uniprot": "P35555", "species": "Homo sapiens"},
    {"symbol": "COL1A1", "uniprot": "P02452", "species": "Homo sapiens"},
    {"symbol": "PIEZO2", "uniprot": "Q9H5I5", "species": "Homo sapiens"},
    {"symbol": "YAP1", "uniprot": "P46937", "species": "Homo sapiens"},
    {"symbol": "PKD2", "uniprot": "Q13563", "species": "Homo sapiens"},
    {"symbol": "IGF1R", "uniprot": "P08069", "species": "Homo sapiens"},
    {"symbol": "LBX1", "uniprot": "P52954", "species": "Homo sapiens"},
    {"symbol": "ADGRG6", "uniprot": "Q7Z2K8", "species": "Homo sapiens"},
    {"symbol": "DMD", "uniprot": "P11532", "species": "Homo sapiens"},
]

OUTPUT_DIR = "outputs"
TEMP_DIR = "temp/afdb"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def get_git_revision_hash() -> str:
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    except Exception:
        return "Unknown (Not a git repo?)"

def fetch_uniprot_metadata(uniprot_id: str) -> Dict[str, str]:
    """Fetches minimal metadata (Gene Name, Species) from UniProt API."""
    try:
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            gene = data.get('genes', [{}])[0].get('geneName', {}).get('value', uniprot_id)
            species = data.get('organism', {}).get('scientificName', 'Unknown')
            return {"symbol": gene, "species": species, "uniprot": uniprot_id}
    except Exception:
        pass
    return {"symbol": uniprot_id, "species": "Unknown", "uniprot": uniprot_id}

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
    parser_args = argparse.ArgumentParser(description="Bolt-BioFold Analysis Cycle")
    parser_args.add_argument("--proteins", type=str, help="Comma-separated list of UniProt IDs")
    args = parser_args.parse_args()

    # ⚡ Bolt Optimization: Use shared StructureParser for caching and fast parsing
    parser = StructureParser()
    analyzer = MetricsAnalyzer()
    results = []

    # Store data for plotting
    plot_data = {}

    proteins_to_process = []
    list_name = "Default Seed List"

    if args.proteins:
        ids = [x.strip() for x in args.proteins.split(',') if x.strip()]
        if ids:
            list_name = "Custom List"
            print(f"Resolving metadata for {len(ids)} custom proteins...")
            for uid in ids:
                meta = fetch_uniprot_metadata(uid)
                proteins_to_process.append(meta)
        else:
            proteins_to_process = DEFAULT_SEED_LIST
    else:
        proteins_to_process = DEFAULT_SEED_LIST

    print(f"Starting Bolt-BioFold Analysis Cycle on {len(proteins_to_process)} proteins ({list_name})...")

    # Metadata
    run_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_hash = get_git_revision_hash()

    for prot in proteins_to_process:
        uid = prot['uniprot']
        symbol = prot['symbol']
        print(f"Processing {symbol} ({uid})...")

        paths = fetch_afdb_data(uid)
        if not paths:
            print(f"Skipping {symbol} - data fetch failed (likely too large or missing from AFDB).")
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
    if not results:
        print("No results generated.")
        return

    df = pd.DataFrame(results)

    # 1. Results Table
    print(f"\n### Results Table ({list_name})")
    print_markdown_table(df)

    print("\n### CSV Output")
    print("```csv")
    print(df.to_csv(index=False))
    print("```")

    # Plotting
    plot_filename = "bolt_biofold_plddt.png"
    plt.figure(figsize=(10, 6))
    for symbol, plddt in plot_data.items():
        plt.plot(plddt, label=symbol, alpha=0.7, linewidth=1)

    plt.title("Per-Residue Confidence (pLDDT)")
    plt.xlabel("Residue Index")
    plt.ylabel("pLDDT")
    plt.axhline(70, color='gray', linestyle='--', alpha=0.5, label='Confidence Threshold (70)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, plot_filename))

    # 2. Key Plots Summary
    print("\n### Key Plots Summary")
    print(f"- **Per-Residue Confidence (pLDDT)**: Generated for {len(plot_data)} proteins. Saved to `{os.path.join(OUTPUT_DIR, plot_filename)}`.")
    print("  - Shows confidence profiles across sequence length.")
    print("  - Threshold line at 70 indicates high-confidence boundary.")

    # 3. Interpretation
    print("\n### Interpretation")
    for row in results:
        symbol = row['protein_id'].split()[0]
        anisotropy = float(row['anisotropy_index'])
        hinges = int(row['hinge_candidates'])
        plddt_high = float(row['pLDDT_fraction_high'])
        curvature = float(row['curvature_summary'])
        disorder = float(row['disorder_fraction_proxy'])

        conf_level = "High" if plddt_high > 0.8 else ("Medium" if plddt_high > 0.5 else "Low")

        # Heuristics
        what_we_see = []
        if anisotropy > 3.0: what_we_see.append("Highly elongated/Fibrous")
        elif anisotropy < 1.5: what_we_see.append("Globular")
        else: what_we_see.append("Intermediate shape")

        if hinges > 0: what_we_see.append(f"{hinges} potential hinge(s)")
        if curvature > 0.1: what_we_see.append("High local curvature")
        if disorder > 0.4: what_we_see.append("Significant disorder (IDR)")

        # Why it matters logic with generic fallback
        matters = "Matters: Structural metrics imply role in mechanical integrity or sensing."

        # Specific known genes (Case insensitive check might be safer but symbols are usually upper)
        s_upper = symbol.upper()
        if "PIEZO" in s_upper:
            matters = "Matters: Mechanosensitive channel; curvature/hinges likely relate to gating mechanics under membrane tension."
        elif "FBN1" in s_upper or "COL" in s_upper:
            matters = "Matters: ECM structural component; anisotropy defines load-bearing axis and tissue stiffness."
        elif "YAP" in s_upper:
            matters = "Matters: Mechanotransducer; structural disorder likely facilitates binding versatility under stress."
        elif "DMD" in s_upper:
            matters = "Matters: Muscle-ECM linker; massive length and flexibility essential for shock absorption."
        elif "LBX1" in s_upper:
             matters = "Matters: Transcription factor; disorder likely mediates phase separation or flexible DNA binding."
        elif "ADGRG6" in s_upper:
             matters = "Matters: Adhesion GPCR; long IDR tail crucial for signaling."
        elif "IGF1R" in s_upper:
             matters = "Matters: Growth factor receptor; structural flexibility critical for ligand binding and activation."
        elif "PKD2" in s_upper:
             matters = "Matters: Polycystin channel; likely involved in flow sensing via cilia."

        # Next Test logic
        if hinges > 0 and anisotropy > 2:
            next_test = "Next: Test mechanical gating/unfolding under force."
        elif disorder > 0.3:
             next_test = "Next: Analyze IDR phase separation potential."
        else:
            next_test = "Next: Compare with orthologs to check conservation of geometry."

        print(f"- **{symbol}**")
        print(f"  - **What we see**: {', '.join(what_we_see)}.")
        print(f"  - **Why it matters**: {matters}")
        print(f"  - **Confidence**: {conf_level} (pLDDT high fraction: {plddt_high})")
        print(f"  - **Next test**: {next_test}")

    # 4. Best Next Move
    print("\n### Best Next Move")
    print("Correlate curvature metrics (especially hinge locations) with known pathogenic variants in these genes to validate mechanical relevance.")

    # Quality Checklist
    print("\n### Quality & Reproducibility Checklist")
    print(f"- **Data Source**: AlphaFold DB (via API)")
    print(f"- **Date/Time**: {run_timestamp}")
    print(f"- **Code Version**: {git_hash}")
    print(f"- **Parameters**: pLDDT threshold=70 (Geometry), Segmentation heuristic (PAE/pLDDT blockiness)")
    print(f"- **Notes**: FBN1 omitted if file fetch failed (likely due to size limits in AFDB monomer v2).")

if __name__ == "__main__":
    main()
