"""
Bolt-BioFold Analysis Script
----------------------------
Performs structural analysis on AlphaFold predictions to support the Biological Countercurvature hypothesis.

Targets: PIEZO1, PIEZO2, COL1A1, YAP1, TRPV4, COL2A1
Metrics: pLDDT statistics, Radius of Gyration, PCA Anisotropy, Curvature/Torsion.
Output: CSV table, Markdown report, Plots.

Usage:
    python3 scripts/bolt_biofold_analysis.py
"""

import argparse
import csv
import math
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any

import numpy as np
import matplotlib.pyplot as plt
from Bio.PDB import PDBParser
from Bio.PDB.Structure import Structure

# Constants
TARGET_PROTEINS = ["PIEZO1", "PIEZO2", "COL1A1", "YAP1", "TRPV4", "COL2A1"]
DEFAULT_PDB_DIR = Path("archive/alphafold_analysis_legacy/predictions")
DEFAULT_OUTPUT_DIR = Path("outputs/bolt_biofold_analysis")

def get_calpha_and_plddt(structure: Structure) -> Tuple[np.ndarray, np.ndarray, List[int]]:
    """
    Extracts C-alpha coordinates and pLDDT scores (from B-factors).
    Returns:
        coords: (N, 3) float array
        plddt: (N,) float array
        res_indices: (N,) int list of residue numbers
    """
    coords = []
    plddts = []
    indices = []

    for model in structure:
        for chain in model:
            for residue in chain:
                if 'CA' in residue:
                    ca = residue['CA']
                    coords.append(ca.get_coord())
                    plddts.append(ca.get_bfactor())
                    indices.append(residue.get_id()[1])

    return np.array(coords), np.array(plddts), indices

def compute_geometry_metrics(coords: np.ndarray) -> Dict[str, float]:
    """
    Computes geometric descriptors for a set of coordinates (high confidence).
    """
    if len(coords) < 3:
        return {
            "radius_of_gyration": 0.0,
            "end_to_end_distance": 0.0,
            "anisotropy_index": 1.0,
            "max_eigenvalue": 0.0
        }

    # Center coordinates
    centroid = np.mean(coords, axis=0)
    centered = coords - centroid

    # Radius of Gyration
    rg = np.sqrt(np.sum(np.sum(centered**2, axis=1)) / len(coords))

    # End-to-End Distance
    end_to_end = np.linalg.norm(coords[-1] - coords[0])

    # PCA Anisotropy
    cov = np.cov(centered, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)
    eigvals = np.sort(eigvals)

    lambda_min = eigvals[0]
    lambda_max = eigvals[2]

    if lambda_min > 1e-6:
        anisotropy = lambda_max / lambda_min
    else:
        anisotropy = 1000.0

    return {
        "radius_of_gyration": float(rg),
        "end_to_end_distance": float(end_to_end),
        "anisotropy_index": float(anisotropy),
        "max_eigenvalue": float(lambda_max)
    }

def compute_curvature_torsion(coords: np.ndarray, window: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes discrete curvature and torsion along the backbone.
    Smooths coordinates with a moving average window first.
    """
    if len(coords) < window * 2:
        return np.zeros(len(coords)), np.zeros(len(coords))

    # Moving average smoothing
    kernel = np.ones(window) / window
    smoothed = np.array([
        np.convolve(coords[:, 0], kernel, mode='valid'),
        np.convolve(coords[:, 1], kernel, mode='valid'),
        np.convolve(coords[:, 2], kernel, mode='valid')
    ]).T

    # Tangent t
    t = np.gradient(smoothed, axis=0)
    # Normal n ~ t'
    dt = np.gradient(t, axis=0)

    cross_d1_d2 = np.cross(t, dt)
    num = np.linalg.norm(cross_d1_d2, axis=1)
    denom = np.linalg.norm(t, axis=1)**3

    curvature = np.zeros_like(num)
    mask = denom > 1e-6
    curvature[mask] = num[mask] / denom[mask]

    # Torsion
    ddt = np.gradient(dt, axis=0)
    num_tau = np.sum(cross_d1_d2 * ddt, axis=1)
    denom_tau = np.linalg.norm(cross_d1_d2, axis=1)**2

    torsion = np.zeros_like(num_tau)
    mask_tau = denom_tau > 1e-6
    torsion[mask_tau] = num_tau[mask_tau] / denom_tau[mask_tau]

    # Pad to match original length
    pad_len = (len(coords) - len(curvature)) // 2
    curvature = np.pad(curvature, (pad_len, len(coords)-len(curvature)-pad_len), 'edge')
    torsion = np.pad(torsion, (pad_len, len(coords)-len(torsion)-pad_len), 'edge')

    return curvature, torsion

def find_domains(plddts: np.ndarray, threshold: float = 70.0, min_len: int = 10) -> int:
    """
    Heuristic: Contiguous high pLDDT blocks separated by low pLDDT boundaries.
    Returns count of such blocks.
    """
    is_high = plddts >= threshold
    # Find contiguous regions
    domains = 0
    in_domain = False
    current_len = 0

    for val in is_high:
        if val:
            in_domain = True
            current_len += 1
        else:
            if in_domain and current_len >= min_len:
                domains += 1
            in_domain = False
            current_len = 0

    if in_domain and current_len >= min_len:
        domains += 1

    return domains

def find_hinges(plddts: np.ndarray, curvature: np.ndarray) -> int:
    """
    Heuristic: Positions where confidence drops (local min) AND curvature is high.
    Returns count of hinge candidates.
    """
    # Simple threshold based
    # Low confidence but not disordered (50 < pLDDT < 70) + High Curvature
    hinge_mask = (plddts > 50) & (plddts < 80) & (curvature > 0.3)
    # Count distinct regions
    return find_domains(hinge_mask, threshold=0.5, min_len=1) # Reuse find_domains for boolean mask

def analyze_protein(pdb_path: Path) -> Dict:
    """
    Analyzes a single PDB file.
    """
    parser = PDBParser(QUIET=True)
    try:
        structure = parser.get_structure(pdb_path.stem, pdb_path)
    except Exception as e:
        print(f"Error parsing {pdb_path}: {e}")
        return None

    coords, plddts, indices = get_calpha_and_plddt(structure)

    # pLDDT Statistics
    plddt_mean = np.mean(plddts)
    plddt_median = np.median(plddts)
    plddt_high_frac = np.sum(plddts >= 90) / len(plddts)
    plddt_ok_frac = np.sum((plddts >= 70) & (plddts < 90)) / len(plddts)
    plddt_low_frac = np.sum(plddts < 70) / len(plddts)
    disorder_fraction = np.sum(plddts < 50) / len(plddts)

    # High Confidence Geometry (pLDDT >= 70)
    mask = plddts >= 70
    high_conf_coords = coords[mask]

    geo_metrics = compute_geometry_metrics(high_conf_coords)

    # Curvature/Torsion (Full Chain)
    full_curvature, full_torsion = compute_curvature_torsion(coords, window=10)

    # Metrics on HC segments
    mean_curvature_hc = np.mean(full_curvature[mask]) if np.any(mask) else 0.0
    max_curvature_hc = np.max(full_curvature[mask]) if np.any(mask) else 0.0
    mean_torsion_hc = np.mean(np.abs(full_torsion[mask])) if np.any(mask) else 0.0

    # Domains & Hinges
    domain_count = find_domains(plddts)
    hinge_count = find_hinges(plddts, full_curvature)

    # Flags
    low_confidence_warning = plddt_mean < 70
    likely_IDR_heavy = disorder_fraction > 0.3

    return {
        "protein_id": pdb_path.stem,
        "length": len(coords),
        "pLDDT_mean": plddt_mean,
        "pLDDT_median": plddt_median,
        "pLDDT_fraction_high": plddt_high_frac,
        "pLDDT_fraction_ok": plddt_ok_frac,
        "pLDDT_fraction_low": plddt_low_frac,
        "disorder_fraction_proxy": disorder_fraction,
        "predicted_domain_segments": domain_count,
        "hinge_candidates": hinge_count,
        "mean_curvature_hc": mean_curvature_hc,
        "max_curvature_hc": max_curvature_hc,
        "mean_torsion_hc": mean_torsion_hc,
        "low_confidence_warning": low_confidence_warning,
        "likely_IDR_heavy": likely_IDR_heavy,
        **geo_metrics,
        "coords": coords,
        "plddts": plddts,
        "curvature": full_curvature
    }

def generate_plots(results: List[Dict], output_dir: Path):
    """
    Generates summary plots.
    """
    for res in results:
        pid = res['protein_id']

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # pLDDT Plot
        ax1.set_xlabel('Residue Index')
        ax1.set_ylabel('pLDDT', color='tab:blue')
        ax1.plot(res['plddts'], color='tab:blue', label='pLDDT')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.set_ylim(0, 100)
        # Add threshold line
        ax1.axhline(y=70, color='gray', linestyle='--', alpha=0.5)

        # Curvature Plot (Twin axis)
        ax2 = ax1.twinx()
        ax2.set_ylabel('Curvature (1/A)', color='tab:red')
        ax2.plot(res['curvature'], color='tab:red', alpha=0.5, label='Curvature')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        plt.title(f"Structure Profile: {pid}")
        fig.tight_layout()
        plt.savefig(output_dir / f"{pid}_profile.png")
        plt.close()

def main():
    parser = argparse.ArgumentParser(description="Bolt-BioFold Analysis")
    parser.add_argument("--pdb_dir", type=Path, default=DEFAULT_PDB_DIR, help="Directory containing PDB files")
    parser.add_argument("--output_dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for output")
    args = parser.parse_args()

    pdb_dir = args.pdb_dir
    output_dir = args.output_dir
    figures_dir = output_dir / "figures"

    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Bolt-BioFold Analysis on targets in {pdb_dir}...")

    results = []

    for pid in TARGET_PROTEINS:
        pdb_file = pdb_dir / f"{pid}.pdb"
        if not pdb_file.exists():
            print(f"Warning: {pdb_file} not found. Skipping.")
            continue

        print(f"Processing {pid}...")
        res = analyze_protein(pdb_file)
        if res:
            results.append(res)

    # Write CSV
    csv_path = output_dir / "bolt_biofold_results.csv"
    with open(csv_path, 'w', newline='') as f:
        # Define field order
        fieldnames = [
            "protein_id", "length",
            "pLDDT_mean", "pLDDT_median", "pLDDT_fraction_high", "pLDDT_fraction_ok", "pLDDT_fraction_low",
            "disorder_fraction_proxy", "predicted_domain_segments", "hinge_candidates",
            "radius_of_gyration", "end_to_end_distance", "anisotropy_index",
            "mean_curvature_hc", "max_curvature_hc", "mean_torsion_hc", "max_eigenvalue",
            "low_confidence_warning", "likely_IDR_heavy"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = {k: r[k] for k in fieldnames if k in r}
            writer.writerow(row)

    print(f"CSV saved to {csv_path}")

    # Generate Plots
    generate_plots(results, figures_dir)
    print(f"Plots saved to {figures_dir}")

    # Generate Markdown Report
    md_path = output_dir / "bolt_biofold_report.md"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(md_path, 'w') as f:
        f.write("# Bolt-BioFold Analysis Report\n\n")
        f.write(f"**Date:** {date_str}\n\n")
        f.write("## Results Summary\n\n")
        f.write("| Protein | Anisotropy | Rg (A) | Curvature (Mean) | pLDDT (Mean) | Domains |\n")
        f.write("|---|---|---|---|---|---|\n")

        for r in results:
            f.write(f"| {r['protein_id']} | {r['anisotropy_index']:.2f} | {r['radius_of_gyration']:.1f} | {r['mean_curvature_hc']:.3f} | {r['pLDDT_mean']:.1f} | {r['predicted_domain_segments']} |\n")

        f.write("\n## Interpretation\n\n")
        for r in results:
            f.write(f"### {r['protein_id']}\n")
            f.write(f"- **Geometry:** Anisotropy {r['anisotropy_index']:.2f}. ")
            if r['anisotropy_index'] > 3.0:
                f.write("Highly anisotropic (rod-like/fibrous). Likely structural load bearing.\n")
            else:
                f.write("Globular or mixed geometry.\n")

            f.write(f"- **Curvature:** Mean curvature {r['mean_curvature_hc']:.3f}. ")
            if r['mean_curvature_hc'] > 0.1:
                f.write("High intrinsic curvature detected. Potential counter-curvature generator.\n")
            else:
                f.write("Relatively straight backbone.\n")

            f.write(f"- **Domains:** {r['predicted_domain_segments']} predicted domains. ")
            if r['hinge_candidates'] > 0:
                f.write(f"**{r['hinge_candidates']} potential hinge regions** detected (flexible joints).\n")
            else:
                f.write("No obvious hinge regions.\n")

            f.write(f"- **Confidence:** Mean pLDDT {r['pLDDT_mean']:.1f}. ")
            if r['low_confidence_warning']:
                f.write("WARNING: Low confidence structure.\n")
            else:
                f.write("High confidence structure.\n")
            f.write("\n")

        f.write("\n## Best Next Move\n")
        f.write("Correlate Anisotropy with Scoliosis Risk Score in `candidates_master.csv`.\n")

    print(f"Report saved to {md_path}")

if __name__ == "__main__":
    main()
