import sys
import os
import time
import requests
import numpy as np
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../research/alphafold_countercurvature/src')))
from afcc.structure import StructureParser
from afcc.metrics import MetricsAnalyzer

def fetch_pdb_via_api(uniprot_id, output_dir="temp/afdb"):
    os.makedirs(output_dir, exist_ok=True)
    pdb_path = Path(output_dir) / f"{uniprot_id}.pdb"

    if pdb_path.exists():
        return pdb_path

    print(f"Querying API for {uniprot_id}...")
    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    try:
        resp = requests.get(api_url)
        if resp.status_code != 200:
            print(f"API Error: {resp.status_code}")
            return None
        data = resp.json()
        if not data or not isinstance(data, list):
             return None

        # Get first entry
        entry = data[0]
        pdb_url = entry.get('pdbUrl')

        if not pdb_url:
             return None

        print(f"Downloading PDB from {pdb_url}...")
        pdb_resp = requests.get(pdb_url)
        if pdb_resp.status_code == 200:
             with open(pdb_path, 'wb') as f:
                 f.write(pdb_resp.content)
        else:
             print(f"Failed to download PDB: {pdb_resp.status_code}")
             return None

        return pdb_path
    except Exception as e:
        print(f"Error: {e}")
        return None

def benchmark():
    # 1. Micro-benchmark of _norm_fast vs np.linalg.norm
    print("--- Micro-Benchmark: Norm Calculation ---")
    analyzer = MetricsAnalyzer()

    sizes = [300, 3000, 30000]
    for N in sizes:
        print(f"\nN={N} vectors:")
        a = np.random.rand(N, 3)

        # Baseline: np.linalg.norm
        start = time.time()
        for _ in range(100):
            _ = np.linalg.norm(a, axis=1)
        dt_base = (time.time() - start) / 100

        # Optimized: _norm_fast
        start = time.time()
        for _ in range(100):
            _ = analyzer._norm_fast(a)
        dt_opt = (time.time() - start) / 100

        print(f"  np.linalg.norm: {dt_base*1000:.4f} ms")
        print(f"  _norm_fast:     {dt_opt*1000:.4f} ms")
        print(f"  Speedup:        {dt_base/dt_opt:.2f}x")

    # 2. Macro-benchmark: analyze_structure on real protein
    print("\n--- Macro-Benchmark: analyze_structure ---")

    # Use COL1A1 (P02452) or a large protein if available
    uniprot_id = "P02452" # COL1A1 (~1464 residues)
    pdb_path = fetch_pdb_via_api(uniprot_id)

    if not pdb_path:
        print("Could not download PDB for macro-benchmark.")
        return

    parser = StructureParser()
    coords, plddt, resnames = parser.fast_parse_pdb_arrays(pdb_path)
    print(f"Benchmarking on {uniprot_id} ({len(coords)} residues)...")

    # Measure analyze_structure time
    n_runs = 50
    start = time.time()
    for _ in range(n_runs):
        metrics = analyzer.analyze_structure(
            coords=coords,
            plddt_scores=plddt,
            resnames=resnames
        )
    dt_avg = (time.time() - start) / n_runs
    print(f"  analyze_structure avg time: {dt_avg*1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
