#!/usr/bin/env python3
import argparse
import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np

# Setup paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..'))
SRC_DIR = os.path.join(REPO_ROOT, 'research', 'alphafold_countercurvature', 'src')
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from afcc.metrics import MetricsAnalyzer
from afcc.structure import StructureParser

CACHE_DIR = os.path.join(REPO_ROOT, "data", "afdb_cache")
OUTPUT_BASE = os.path.join(REPO_ROOT, "outputs", "bolt_biofold_cycle")
CANDIDATES_FILE = os.path.join(REPO_ROOT, "data", "candidates_master.csv")

# Seeds
DEFAULT_SEEDS = [
    # Some genes relevant to mechanobiology / spine
    {"gene_symbol": "DCN", "uniprot_id": "P07585", "organism": "Homo sapiens"},
    {"gene_symbol": "LUM", "uniprot_id": "P51884", "organism": "Homo sapiens"},
    {"gene_symbol": "FMOD", "uniprot_id": "Q06828", "organism": "Homo sapiens"}
]

def fetch_afdb_data(uniprot_id: str) -> Optional[Dict[str, str]]:
    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    pdb_path = os.path.join(CACHE_DIR, f"{uniprot_id}.pdb")
    pae_path = os.path.join(CACHE_DIR, f"{uniprot_id}.json")

    if os.path.exists(pdb_path) and os.path.exists(pae_path):
        return {"pdb": pdb_path, "pae": pae_path}
    if os.path.exists(pdb_path):
        return {"pdb": pdb_path, "pae": None}

    print(f"Querying API for {uniprot_id}...")
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 404:
            print(f"API Error 404 for {uniprot_id}. Attempting fallback to local cache.")
            return None
        if response.status_code != 200:
             return None
        data = response.json()
        if not data or not isinstance(data, list):
             return None
        entry = data[0]
        pdb_url = entry.get('pdbUrl')
        pae_url = entry.get('paeDocUrl')
        if not pdb_url: return None

        print(f"Downloading PDB from {pdb_url}...")
        pdb_resp = requests.get(pdb_url, timeout=30)
        if pdb_resp.status_code == 200:
             with open(pdb_path, 'wb') as f: f.write(pdb_resp.content)
        if pae_url:
            pae_resp = requests.get(pae_url, timeout=30)
            if pae_resp.status_code == 200:
                with open(pae_path, 'wb') as f: f.write(pae_resp.content)
        return {"pdb": pdb_path, "pae": pae_path if os.path.exists(pae_path) else None}
    except Exception as e:
        print(f"Exception fetching data for {uniprot_id}: {e}")
        return None

def main():
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_BASE, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_BASE, "figures"), exist_ok=True)

    candidates = DEFAULT_SEEDS

    struct_parser = StructureParser()
    analyzer = MetricsAnalyzer()

    results = []

    for row in candidates:
        symbol = row['gene_symbol']
        uniprot = row['uniprot_id']
        species = row['organism']

        paths = fetch_afdb_data(uniprot)
        if not paths:
            # Fallback to cache?
            pdb_path = os.path.join(CACHE_DIR, f"{uniprot}.pdb")
            pae_path = os.path.join(CACHE_DIR, f"{uniprot}.json")
            if os.path.exists(pdb_path):
                paths = {"pdb": pdb_path, "pae": pae_path if os.path.exists(pae_path) else None}
            else:
                print(f"Skipping {symbol} ({uniprot}): Data fetch failed and not in cache.")
                continue

        pdb_path = Path(paths['pdb'])
        pae_path = Path(paths['pae']) if paths['pae'] and os.path.exists(paths['pae']) else None

        coords, plddt, resnames = struct_parser.fast_parse_pdb_arrays(pdb_path)
        if coords is None:
            continue

        pae_matrix = None
        if pae_path:
            pae_matrix = struct_parser.parse_pae(pae_path)

        metrics = analyzer.analyze_structure(
            coords=coords,
            plddt_scores=plddt,
            resnames=resnames,
            pae_matrix=pae_matrix
        )

        # Build schema according to rules
        result = {
            "protein_id": uniprot,
            "gene_symbol": symbol,
            "species": species,
            "length": metrics.get('n_residues', len(plddt)),
            "pLDDT_mean": metrics.get('plddt_mean'),
            "pLDDT_median": metrics.get('plddt_median'),
            "pLDDT_fraction_high": metrics.get('plddt_fraction_high'),
            "pLDDT_fraction_ok": metrics.get('plddt_fraction_ok'),
            "pLDDT_fraction_low": metrics.get('plddt_fraction_low'),
            "PAE_mean": metrics.get('PAE_mean', "Not implemented" if pae_matrix is None else metrics.get('PAE_mean')),
            "PAE_domain_blockiness_score": metrics.get('PAE_domain_blockiness_score', "Not implemented" if pae_matrix is None else metrics.get('PAE_domain_blockiness_score')),
            "predicted_domain_segments": metrics.get('predicted_domain_segments', "Not implemented"),
            "disorder_fraction_proxy": metrics.get('disorder_fraction_proxy'),
            "hinge_candidates": metrics.get('hinge_candidates'),
            "backbone_principal_axis": str(metrics.get('backbone_principal_axis', "Not implemented")),
            "radius_of_gyration": metrics.get('radius_of_gyration'),
            "end_to_end_distance": metrics.get('end_to_end_distance'),
            "curvature_summary": metrics.get('curvature_summary'),
            "torsion_summary": metrics.get('torsion_summary'),
            "anisotropy_index": metrics.get('anisotropy_index'),
            "bending_hotspots": metrics.get('bending_hotspots', "Not implemented"),
            "exposed_surface_proxy": metrics.get('exposed_surface_proxy', "Not implemented"),
            "charged_patch_score": metrics.get('charged_patch_score', "Not implemented"),
            "low_confidence_warning": metrics.get('low_confidence_warning'),
            "multi_domain_uncertain": metrics.get('multi_domain_uncertain'),
            "likely_IDR_heavy": metrics.get('likely_IDR_heavy')
        }
        results.append(result)

        # Plotting pLDDT
        plt.figure()
        plt.plot(plddt, label=f'{symbol} pLDDT')
        plt.axhline(70, color='r', linestyle='--', label='Conf Threshold')
        plt.xlabel("Residue Index")
        plt.ylabel("pLDDT")
        plt.title(f"{symbol} Confidence")
        plt.legend()
        plt.savefig(os.path.join(OUTPUT_BASE, "figures", f"{symbol}_plddt.png"))
        plt.close()

    if results:
        df = pd.DataFrame(results)
        df.to_csv(os.path.join(OUTPUT_BASE, "metrics.csv"), index=False)

        # Markdown Report
        md = f"""# AlphaFold Counter-Curvature Analysis Report (Bolt-BioFold ⚡)

## Quality & Reproducibility Checklist
- **Data source:** AlphaFold DB API (fallback to local cache)
- **Date/time of run:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Code version:** local (untracked)
- **Parameters:** pLDDT ≥ 70 threshold for geometry, default domain heuristics.

## Interpretation

"""
        for r in results:
            md += f"### {r['gene_symbol']} ({r['protein_id']})\n"
            md += f"- **What we see:** Length {r['length']}, Anisotropy {r.get('anisotropy_index', 'N/A'):.2f}, Rg {r.get('radius_of_gyration', 'N/A'):.2f}. Conf: {r.get('pLDDT_mean', 'N/A'):.1f} mean pLDDT.\n"

            aniso = r.get('anisotropy_index', 0)
            if pd.isna(aniso): aniso = 0
            if aniso > 3.0:
                mech = "High anisotropy suggests an extended, load-bearing fibrous geometry capable of resisting tensile forces."
            else:
                mech = "Compact structure suggests a regulatory/globular role rather than direct tension/compression resistance."
            md += f"- **Why it matters:** {mech} Contributes to mechanical properties of spinal ligaments/cartilage.\n"

            conf_level = "High" if r.get('low_confidence_warning') == False else "Low"
            md += f"- **Confidence level:** {conf_level}\n"
            md += f"- **Next test:** Compare orthologs to see if {r['gene_symbol']} anisotropy is conserved in species with different gravitational loads.\n\n"

        md += "## Best Next Move\n"
        md += "- correlate curvature metrics with known phenotype genes\n"

        with open(os.path.join(OUTPUT_BASE, "report.md"), "w") as f:
            f.write(md)

if __name__ == "__main__":
    main()
