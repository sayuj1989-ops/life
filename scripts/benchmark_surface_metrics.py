
import numpy as np
import time
import sys
import importlib.util
from pathlib import Path
from scipy.spatial import cKDTree

# Add research module to path
sys.path.append(str(Path(__file__).parent.parent / "research" / "alphafold_countercurvature" / "src"))
from afcc.structure import StructureParser

# Import the optimized function from the script
spec = importlib.util.spec_from_file_location("bolt_biofold_analysis", "scripts/bolt_biofold_analysis.py")
bolt_module = importlib.util.module_from_spec(spec)
sys.modules["bolt_biofold_analysis"] = bolt_module
spec.loader.exec_module(bolt_module)
compute_surface_metrics_new = bolt_module.compute_surface_metrics

def compute_surface_metrics_original(coords, resnames, plddts):
    """
    Original implementation using broadcasting.
    Including resnames and plddts to match signature, but only using coords for neighbor count logic validation.
    """
    if len(coords) == 0:
        return {
            "exposed_surface_proxy": 0,
            "charged_patch_score": 0.0
        }

    # Compute distance matrix
    # Optimization: Use broadcasting for small N
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    dists = np.sqrt(np.sum(diff**2, axis=-1))

    # Count neighbors (distance < 10.0)
    # Subtract 1 to exclude self
    neighbor_counts = np.sum(dists < 10.0, axis=1) - 1

    # Replicate the rest of the logic for full verification
    exposed_mask = (neighbor_counts < 20) & (plddts >= 70.0)
    exposed_count = np.sum(exposed_mask)

    if exposed_count == 0:
        return {
            "exposed_surface_proxy": 0,
            "charged_patch_score": 0.0
        }

    # Charged residues for surface metrics
    CHARGED_RESIDUES = {'ARG', 'LYS', 'ASP', 'GLU', 'HIS', 'R', 'K', 'D', 'E', 'H'}

    # Check charged
    exposed_resnames = resnames[exposed_mask]
    charged_count = sum(1 for r in exposed_resnames if str(r).upper() in CHARGED_RESIDUES)

    return {
        "exposed_surface_proxy": int(exposed_count),
        "charged_patch_score": float(charged_count) / float(exposed_count)
    }

def main():
    print("Verifying Bolt-BioFold Optimization (Integration Test)...")

    # Load PIEZO1 if available
    pdb_path = Path("archive/alphafold_analysis_legacy/predictions/PIEZO1.pdb")

    parser = StructureParser()
    if pdb_path.exists():
        print(f"Loading {pdb_path}...")
        coords, plddts, resnames = parser.fast_parse_pdb_arrays(pdb_path)
    else:
        print("PIEZO1.pdb not found. Using synthetic data (N=2500).")
        coords = np.random.rand(2500, 3) * 100.0
        plddts = np.random.rand(2500) * 100.0
        resnames = np.array(['ALA'] * 2500)

    if coords is None:
        print("Failed to parse PDB.")
        return

    print(f"Structure Size: N={len(coords)}")

    # Original Benchmark
    t0 = time.time()
    res_orig = compute_surface_metrics_original(coords, resnames, plddts)
    t_orig = time.time() - t0
    print(f"Original Time: {t_orig:.4f}s")
    print(f"Original Result: {res_orig}")

    # Optimized Benchmark (from the module)
    t0 = time.time()
    res_opt = compute_surface_metrics_new(coords, resnames, plddts)
    t_opt = time.time() - t0
    print(f"Optimized Time: {t_opt:.4f}s")
    print(f"Optimized Result: {res_opt}")

    # Verification
    match = (res_orig['exposed_surface_proxy'] == res_opt['exposed_surface_proxy']) and \
            abs(res_orig['charged_patch_score'] - res_opt['charged_patch_score']) < 1e-6

    print(f"Results Match: {match}")

    if t_opt > 0:
        speedup = t_orig / t_opt
        print(f"Speedup: {speedup:.2f}x")
    else:
        print("Speedup: Infinite (too fast to measure)")

if __name__ == "__main__":
    main()
