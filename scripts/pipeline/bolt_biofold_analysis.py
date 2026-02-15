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
import time
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any

import numpy as np
import matplotlib.pyplot as plt

# Add research module to path to import StructureParser
sys.path.append(str(Path(__file__).parent.parent / "research" / "alphafold_countercurvature" / "src"))
from afcc.structure import StructureParser

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super(NumpyEncoder, self).default(obj)

# Constants
TARGET_PROTEINS = [
    "PIEZO1", "PIEZO2", "COL1A1", "COL2A1", "YAP1", "TRPV4",
    "RUNX2", "SOX9", "VINCULIN", "TALIN1", "NOTCH1", "FIBRONECTIN"
]
DEFAULT_PDB_DIR = Path("archive/alphafold_analysis_legacy/predictions")
DEFAULT_OUTPUT_DIR = Path("outputs/bolt_biofold_analysis")

def load_cached_analysis(pdb_path: Path) -> Optional[Dict]:
    """Loads cached analysis results if available."""
    cache_json = pdb_path.with_suffix('.bolt_metrics.json')
    cache_npz = pdb_path.with_suffix('.bolt_arrays.npz')

    if not (cache_json.exists() and cache_npz.exists()):
        return None

    try:
        # Check timestamps
        pdb_time = pdb_path.stat().st_mtime
        if cache_json.stat().st_mtime < pdb_time or cache_npz.stat().st_mtime < pdb_time:
            return None

        with open(cache_json, 'r') as f:
            metrics = json.load(f)

        with np.load(cache_npz) as data:
            # Reconstruct arrays
            metrics['coords'] = data['coords']
            metrics['plddts'] = data['plddts']
            metrics['curvature'] = data['curvature']

        return metrics
    except Exception as e:
        print(f"Warning: Failed to load cache for {pdb_path}: {e}")
        return None

def save_cached_analysis(pdb_path: Path, results: Dict):
    """Saves analysis results to cache."""
    cache_json = pdb_path.with_suffix('.bolt_metrics.json')
    cache_npz = pdb_path.with_suffix('.bolt_arrays.npz')

    try:
        # Separate arrays and scalars
        arrays = {
            'coords': results['coords'],
            'plddts': results['plddts'],
            'curvature': results['curvature']
        }

        # Filter out arrays from json
        scalars = {k: v for k, v in results.items() if k not in arrays}

        with open(cache_json, 'w') as f:
            json.dump(scalars, f, indent=2, cls=NumpyEncoder)

        np.savez_compressed(cache_npz, **arrays)

    except Exception as e:
        print(f"Warning: Failed to save cache for {pdb_path}: {e}")

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

    # ⚡ Bolt Optimization: Single-pass geometry (Rg + Anisotropy)
    # Replace 2 passes (sum-sq + cov) with 1 matrix multiplication
    n = len(coords)
    M = centered.T @ centered

    # Radius of Gyration: Rg = sqrt(trace(M) / N)
    rg = np.sqrt(np.trace(M) / n)

    # End-to-End Distance
    end_to_end = np.linalg.norm(coords[-1] - coords[0])

    # PCA Anisotropy
    # Use N-1 normalization to match np.cov default (unbiased)
    cov = M / (n - 1)
    eigvals, eigvecs = np.linalg.eigh(cov)
    eigvals = np.sort(eigvals)

    lambda_min = eigvals[0]
    lambda_max = eigvals[2]

    if lambda_min > 1e-6:
        anisotropy = lambda_max / lambda_min
    else:
        anisotropy = 1000.0

    # Principal Axis (Eigenvector for lambda_max)
    # eigvals are sorted, so lambda_max is the last one (index 2)
    principal_axis = eigvecs[:, 2]
    principal_axis_str = f"[{principal_axis[0]:.3f}, {principal_axis[1]:.3f}, {principal_axis[2]:.3f}]"

    return {
        "radius_of_gyration": float(rg),
        "end_to_end_distance": float(end_to_end),
        "anisotropy_index": float(anisotropy),
        "max_eigenvalue": float(lambda_max),
        "backbone_principal_axis": principal_axis_str
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

def find_hinges(plddts: np.ndarray, curvature: np.ndarray) -> str:
    """
    Heuristic: Positions where confidence drops (local min) AND curvature is high.
    Returns formatted string of regions.
    """
    # 50 < pLDDT < 70 (Low confidence but structured) AND Curvature > 0.1
    hinge_mask = (plddts > 50) & (plddts < 80) & (curvature > 0.1)

    regions = []
    in_region = False
    start = -1

    for i, val in enumerate(hinge_mask):
        if val:
            if not in_region:
                in_region = True
                start = i
        else:
            if in_region:
                if i - start >= 3:
                     regions.append(f"{start}-{i-1}")
                in_region = False

    if in_region and len(hinge_mask) - start >= 3:
        regions.append(f"{start}-{len(hinge_mask)-1}")

    return "; ".join(regions) if regions else "None"

def find_bending_hotspots(curvature: np.ndarray, plddts: np.ndarray, top_n: int = 3) -> str:
    """
    Identifies top N regions with high curvature in high-confidence segments.
    Returns a string like '120-125 (k=0.55); 200-205 (k=0.48)'
    """
    mask = plddts >= 70
    curv_copy = curvature.copy()
    curv_copy[~mask] = -1.0

    hotspots = []

    for _ in range(top_n):
        if np.max(curv_copy) <= 0:
            break
        idx = np.argmax(curv_copy)
        val = curv_copy[idx]

        # Define range around peak where curvature is high (e.g. > 80% of peak)
        # scan left
        start = idx
        while start > 0 and curv_copy[start-1] > val * 0.8:
            start -= 1
        # scan right
        end = idx
        while end < len(curv_copy) - 1 and curv_copy[end+1] > val * 0.8:
            end += 1

        hotspots.append(f"{start}-{end} (k={val:.2f})")

        # Mask out
        mask_start = max(0, start - 5)
        mask_end = min(len(curv_copy), end + 6)
        curv_copy[mask_start:mask_end] = -1.0

    return "; ".join(hotspots) if hotspots else "None"

def analyze_protein(pdb_path: Path, force: bool = False) -> Dict:
    """
    Analyzes a single PDB file using fast StructureParser with caching.
    """
    # ⚡ Bolt Optimization: Check persistent analysis cache
    if not force:
        cached = load_cached_analysis(pdb_path)
        if cached:
            print(f"  Loaded analysis cache for {pdb_path.name}")
            return cached

    t0 = time.time()
    parser = StructureParser()

    # ⚡ Bolt Optimization: Use fast parser + cache
    coords, plddts, resnames = parser.fast_parse_pdb_arrays(pdb_path)

    if coords is None:
        print(f"Error parsing {pdb_path}")
        return None

    dt = time.time() - t0
    print(f"  Parsed {pdb_path.name} in {dt:.4f}s")

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
    hinge_regions = find_hinges(plddts, full_curvature)
    bending_hotspots = find_bending_hotspots(full_curvature, plddts)

    # Flags
    low_confidence_warning = plddt_mean < 70
    likely_IDR_heavy = disorder_fraction > 0.3
    multi_domain_uncertain = domain_count > 1 and low_confidence_warning

    results = {
        "protein_id": pdb_path.stem,
        "species": "Homo sapiens",
        "length": len(coords),
        "pLDDT_mean": plddt_mean,
        "pLDDT_median": plddt_median,
        "pLDDT_fraction_high": plddt_high_frac,
        "pLDDT_fraction_ok": plddt_ok_frac,
        "pLDDT_fraction_low": plddt_low_frac,
        "PAE_mean": "N/A",
        "PAE_domain_blockiness_score": "N/A",
        "disorder_fraction_proxy": disorder_fraction,
        "predicted_domain_segments": domain_count,
        "hinge_candidates": hinge_regions,
        "mean_curvature_hc": mean_curvature_hc,
        "max_curvature_hc": max_curvature_hc,
        "mean_torsion_hc": mean_torsion_hc,
        "bending_hotspots": bending_hotspots,
        "exposed_surface_proxy": "Not computed",
        "charged_patch_score": "Not computed",
        "low_confidence_warning": low_confidence_warning,
        "multi_domain_uncertain": multi_domain_uncertain,
        "likely_IDR_heavy": likely_IDR_heavy,
        **geo_metrics,
        "coords": coords,
        "plddts": plddts,
        "curvature": full_curvature
    }

    # Save to cache
    save_cached_analysis(pdb_path, results)
    return results

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
    parser.add_argument("--force", action="store_true", help="Force re-computation ignoring cache")
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
        res = analyze_protein(pdb_file, force=args.force)
        if res:
            results.append(res)

    # Write CSV
    csv_path = output_dir / "bolt_biofold_results.csv"
    with open(csv_path, 'w', newline='') as f:
        # Define field order
        fieldnames = [
            "protein_id", "species", "length",
            "pLDDT_mean", "pLDDT_median", "pLDDT_fraction_high", "pLDDT_fraction_ok", "pLDDT_fraction_low",
            "PAE_mean", "PAE_domain_blockiness_score",
            "predicted_domain_segments", "disorder_fraction_proxy", "hinge_candidates",
            "backbone_principal_axis", "radius_of_gyration", "end_to_end_distance",
            "mean_curvature_hc", "mean_torsion_hc", "anisotropy_index", "max_eigenvalue",
            "bending_hotspots", "exposed_surface_proxy", "charged_patch_score",
            "low_confidence_warning", "multi_domain_uncertain", "likely_IDR_heavy"
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

            # What we see
            f.write(f"**What we see:**\n")
            f.write(f"- Geometry: Anisotropy {r['anisotropy_index']:.2f}, Rg {r['radius_of_gyration']:.1f}A.\n")
            if r['mean_curvature_hc'] > 0.1:
                f.write(f"- Curvature: High mean curvature ({r['mean_curvature_hc']:.3f}) with hotspots at {r['bending_hotspots']}.\n")
            else:
                f.write(f"- Curvature: Low mean curvature ({r['mean_curvature_hc']:.3f}), rod-like or globular.\n")
            if r['hinge_candidates'] != "None":
                 f.write(f"- Flexibility: Potential hinges at {r['hinge_candidates']}.\n")

            # Why it matters
            f.write(f"**Why it matters:**\n")
            if r['anisotropy_index'] > 3.0:
                f.write("- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.\n")
            elif r['anisotropy_index'] < 1.5:
                f.write("- Globular shape suggests a catalytic or signaling hub role rather than direct load bearing.\n")
            else:
                 f.write("- Mixed geometry suggests a multifunctional role.\n")

            if "PIEZO" in r['protein_id'] or "TRPV" in r['protein_id']:
                f.write("- Ion channel architecture critical for mechanotransduction.\n")
            elif "COL" in r['protein_id'] or "FIBRONECTIN" in r['protein_id']:
                f.write("- ECM component defining tissue stiffness and elasticity.\n")
            elif "YAP" in r['protein_id'] or "RUNX" in r['protein_id'] or "SOX" in r['protein_id']:
                f.write("- Nuclear factor whose transport/activity is regulated by mechanical signals.\n")

            # Confidence
            f.write(f"**Confidence:** ")
            if r['low_confidence_warning']:
                f.write("LOW. (Caution: IDRs or poor prediction).\n")
            else:
                f.write("HIGH. (Reliable backbone geometry).\n")

            # Next test
            f.write(f"**Next test:** ")
            if r['hinge_candidates'] != "None":
                f.write("Simulate dynamics of hinge regions under tensile load.\n")
            elif r['anisotropy_index'] > 3.0:
                f.write("Test alignment of fibers under cyclic strain.\n")
            else:
                f.write("Investigate binding partners in high-pLDDT surface patches.\n")
            f.write("\n")

        f.write("\n## Best Next Move\n")
        f.write("Prioritize high-anisotropy candidates (Anisotropy > 3.0) for mechanical simulation of 'counter-curvature' generation.\n")

    print(f"Report saved to {md_path}")

if __name__ == "__main__":
    main()
