#!/usr/bin/env python3
import sys
import os
import json
import requests
import numpy as np
import pandas as pd
import datetime
from Bio.PDB import PDBParser
from typing import Dict, Any, List, Optional

# Add the source directory to sys.path to import metrics
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../research/alphafold_countercurvature/src')))
try:
    from afcc.metrics import MetricsAnalyzer
except ImportError:
    # If the import fails, we might be running from repo root
    sys.path.append(os.path.abspath('research/alphafold_countercurvature/src'))
    from afcc.metrics import MetricsAnalyzer

OUTPUT_BASE = "outputs/afcc"
TEMP_DIR = "temp/afdb"
os.makedirs(TEMP_DIR, exist_ok=True)

def get_todays_output_dir():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    out_dir = os.path.join(OUTPUT_BASE, today)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

def get_top_candidates(n=10):
    candidates_path = "data/candidates_master.csv"
    if not os.path.exists(candidates_path):
        print(f"Error: {candidates_path} not found.")
        sys.exit(1)

    df = pd.read_csv(candidates_path)
    # clean priority_score column
    df['priority_score'] = pd.to_numeric(df['priority_score'], errors='coerce')
    df = df.sort_values(by='priority_score', ascending=False)
    return df.head(n)

def fetch_afdb_data(uniprot_id: str) -> Optional[Dict[str, str]]:
    """Fetches PDB and PAE JSON for a given UniProt ID using the API."""
    if not uniprot_id or pd.isna(uniprot_id):
        return None

    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"

    pdb_path = os.path.join(TEMP_DIR, f"{uniprot_id}.pdb")
    pae_path = os.path.join(TEMP_DIR, f"{uniprot_id}.json")

    # Check if files already exist
    if os.path.exists(pdb_path) and os.path.exists(pae_path):
        return {"pdb": pdb_path, "pae": pae_path}

    print(f"Querying API for {uniprot_id}...")
    try:
        response = requests.get(api_url, timeout=30)
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
        pdb_resp = requests.get(pdb_url, timeout=30)
        if pdb_resp.status_code == 200:
             with open(pdb_path, 'wb') as f:
                 f.write(pdb_resp.content)
        else:
             print(f"Failed to download PDB: {pdb_resp.status_code}")
             return None

        # Download PAE
        if pae_url:
            print(f"Downloading PAE from {pae_url}...")
            pae_resp = requests.get(pae_url, timeout=30)
            if pae_resp.status_code == 200:
                with open(pae_path, 'wb') as f:
                    f.write(pae_resp.content)
            else:
                print(f"Failed to download PAE: {pae_resp.status_code}")
                # Optional but good to have

        return {"pdb": pdb_path, "pae": pae_path if os.path.exists(pae_path) else None}

    except Exception as e:
        print(f"Exception fetching data for {uniprot_id}: {e}")
        return None

def parse_pdb(pdb_path: str):
    """Parses PDB file to get coords, pLDDT, and resnames."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("struct", pdb_path)

    coords = []
    plddt_scores = []
    resnames = []

    for model in structure:
        for chain in model:
            for residue in chain:
                if 'CA' in residue:
                    coords.append(residue['CA'].get_coord())
                    plddt_scores.append(residue['CA'].get_bfactor())
                    resnames.append(residue.get_resname())

    return np.array(coords), np.array(plddt_scores), np.array(resnames)

def parse_pae(pae_path: str) -> Optional[np.ndarray]:
    """Parses PAE JSON file."""
    if not pae_path:
        return None
    try:
        with open(pae_path, 'r') as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0 and 'predicted_aligned_error' in data[0]:
            return np.array(data[0]['predicted_aligned_error'])
    except Exception as e:
        print(f"Error parsing PAE JSON: {e}")
    return None

def main():
    todays_dir = get_todays_output_dir()
    metrics_csv_path = os.path.join(todays_dir, "metrics.csv")
    summary_md_path = os.path.join(todays_dir, "summary.md")
    failure_md_path = os.path.join(todays_dir, "failure.md")

    top_candidates = get_top_candidates(10)
    print(f"Processing top {len(top_candidates)} candidates based on priority score.")

    analyzer = MetricsAnalyzer()
    results = []
    failures = []

    for index, row in top_candidates.iterrows():
        symbol = row['gene_symbol']
        uid = row['uniprot_id']
        species = row.get('organism', 'Unknown')

        print(f"Processing {symbol} ({uid})...")

        paths = fetch_afdb_data(uid)
        if not paths:
            print(f"Skipping {symbol} - data fetch failed.")
            failures.append(f"- **{symbol}** ({uid}): Data fetch failed (API error or missing files).")
            continue

        coords, plddt, resnames = parse_pdb(paths['pdb'])
        pae_matrix = parse_pae(paths['pae'])

        # Run Analysis
        try:
            metrics = analyzer.analyze_structure(
                coords=coords,
                plddt_scores=plddt,
                resnames=resnames,
                pae_matrix=pae_matrix
            )

            # Combine identity + metrics
            entry = {
                "gene_symbol": symbol,
                "uniprot_id": uid,
                "species": species,
                "length": metrics['n_residues'],

                # Confidence
                "pLDDT_mean": f"{metrics['plddt_mean']:.2f}",
                "PAE_mean": f"{metrics['PAE_mean']:.2f}",

                # Architecture
                "morphology": metrics['morphology'],

                # Geometry
                "radius_of_gyration": f"{metrics['radius_of_gyration']:.2f}",
                "anisotropy_index": f"{metrics['anisotropy_index']:.2f}",

                # Detailed metrics
                "pLDDT_fraction_high": f"{metrics['plddt_fraction_high']:.2f}",
                "pLDDT_fraction_low": f"{metrics['plddt_fraction_low']:.2f}",
                "PAE_domain_blockiness_score": f"{metrics['PAE_domain_blockiness_score']:.2f}",
                "predicted_domain_segments": metrics['predicted_domain_segments'],
                "disorder_fraction_proxy": f"{metrics['disorder_fraction_proxy']:.2f}",
                "hinge_candidates": metrics['hinge_candidates'],
                "backbone_principal_axis": metrics['backbone_principal_axis'],
                "end_to_end_distance": f"{metrics['end_to_end_distance']:.2f}",
                "curvature_summary": f"{metrics['curvature_summary']:.4f}",
                "torsion_summary": f"{metrics['torsion_summary']:.4f}",
                "bending_hotspots": metrics['bending_hotspots'],
                "exposed_surface_proxy": f"{metrics['exposed_surface_proxy']:.2f}",
                "charged_patch_score": f"{metrics['charged_patch_score']:.2f}",
                "low_confidence_warning": metrics['low_confidence_warning'],
                "multi_domain_uncertain": metrics['multi_domain_uncertain'],
                "likely_IDR_heavy": metrics['likely_IDR_heavy']
            }
            results.append(entry)

        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            failures.append(f"- **{symbol}** ({uid}): Analysis failed with error: {e}")

    # Generate Outputs
    df = pd.DataFrame(results)
    if not df.empty:
        df.to_csv(metrics_csv_path, index=False)
        print(f"Saved metrics to {metrics_csv_path}")

        # Summary MD
        with open(summary_md_path, "w") as f:
            f.write(f"# AFCC Daily Refresh: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(f"## Run Summary\n")
            f.write(f"- **Candidates Processed**: {len(results)}\n")

            # Find top candidate by anisotropy
            # df['anisotropy_index'] is string, need to convert back for sorting
            df['anisotropy_float'] = pd.to_numeric(df['anisotropy_index'], errors='coerce')
            top_ani = df.sort_values(by='anisotropy_float', ascending=False).iloc[0]
            f.write(f"- **Top Candidate**: {top_ani['gene_symbol']} (Anisotropy: {top_ani['anisotropy_index']})\n")
            if failures:
                f.write(f"- **Failed/Missing**: {len(failures)}\n")

            f.write(f"\n## Top 5 High-Anisotropy Structures\n")
            f.write(f"| Gene | Anisotropy | pLDDT (Mean) | Morphology |\n")
            f.write(f"|------|------------|--------------|------------|\n")

            top_5 = df.sort_values(by='anisotropy_float', ascending=False).head(5)
            for _, row in top_5.iterrows():
                f.write(f"| {row['gene_symbol']} | {row['anisotropy_index']} | {row['pLDDT_mean']} | {row['morphology']} |\n")

            f.write(f"\n## Key Observations\n")
            high_ani_count = len(df[df['anisotropy_float'] > 4.0])
            f.write(f"- **Tension Rods**: Found {high_ani_count} candidates with Anisotropy > 4.0, suggesting fibrous/extended load-bearing structures.\n")

            low_conf_count = len(df[pd.to_numeric(df['pLDDT_mean']) < 70])
            f.write(f"- **Structural Confidence**: {low_conf_count} candidates have low confidence (pLDDT < 70), indicating disorder or flexibility.\n")

            f.write(f"- **Top Mover**: {top_ani['gene_symbol']} remains the most anisotropic structure in this batch.\n")

        print(f"Saved summary to {summary_md_path}")

        # Update reports/afcc_latest.md
        latest_report_path = "reports/afcc_latest.md"
        if os.path.exists(latest_report_path):
            with open(latest_report_path, "a") as f:
                f.write(f"\n# AFCC Daily Refresh: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write(f"## Run Summary\n")
                f.write(f"- **Candidates Processed**: {len(results)}\n")
                f.write(f"- **Top Candidate**: {top_ani['gene_symbol']} (Anisotropy: {top_ani['anisotropy_index']})\n")

                f.write(f"\n## Top 5 High-Anisotropy Structures\n")
                f.write(f"| Gene | Anisotropy | pLDDT (Mean) | Morphology |\n")
                f.write(f"|------|------------|--------------|------------|\n")
                for _, row in top_5.iterrows():
                    f.write(f"| {row['gene_symbol']} | {row['anisotropy_index']} | {row['pLDDT_mean']} | {row['morphology']} |\n")

                f.write(f"\n## Key Observations\n")
                f.write(f"- **Tension Rods**: Found {high_ani_count} candidates with Anisotropy > 4.0, suggesting fibrous/extended load-bearing structures.\n")
                f.write(f"- **Structural Confidence**: {low_conf_count} candidates have low confidence (pLDDT < 70), indicating disorder or flexibility.\n")
                f.write(f"- **Top Mover**: {top_ani['gene_symbol']} remains the most anisotropic structure in this batch.\n")
            print(f"Updated {latest_report_path}")

    if failures:
        with open(failure_md_path, "w") as f:
            f.write(f"# AFCC Failure Log: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
            for fail in failures:
                f.write(f"{fail}\n")
        print(f"Saved failure log to {failure_md_path}")

if __name__ == "__main__":
    main()
