import numpy as np
import pytest
import sys
from pathlib import Path

# Add scripts directory to path to import the script as module
sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts" / "data_management"))

from bolt_biofold_analysis import (
    compute_geometry_metrics,
    find_bending_hotspots,
    find_hinges,
    find_domain_segments,
    compute_curvature_torsion,
    compute_pae_metrics
)

def test_compute_curvature_torsion():
    # Test linear chain (curvature 0)
    # Using simple list of lists for coords
    coords = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [3, 0, 0],
        [4, 0, 0],
        [5, 0, 0],
        [6, 0, 0],
        [7, 0, 0],
        [8, 0, 0],
        [9, 0, 0]
    ])
    curv, tors = compute_curvature_torsion(coords, window=3)
    # Curvature should be near 0
    # Note: padding might affect ends, check middle
    assert np.all(np.abs(curv[3:-3]) < 1e-6)

    # Test bent chain
    # 90 degree turn
    coords_bent = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [3, 0, 0],
        [3, 1, 0],
        [3, 2, 0],
        [3, 3, 0],
        [3, 4, 0]
    ])
    curv, tors = compute_curvature_torsion(coords_bent, window=3)
    # Peak curvature around index 3 or 4
    # We check max curvature is significant
    assert np.max(curv) > 0.1

def test_compute_geometry_metrics():
    # Create a simple linear chain
    coords = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [3.0, 0.0, 0.0]
    ])
    metrics = compute_geometry_metrics(coords)
    assert metrics['anisotropy_index'] > 10.0 # Highly anisotropic
    assert metrics['end_to_end_distance'] == pytest.approx(3.0)
    assert 'backbone_principal_axis' in metrics

def test_find_bending_hotspots():
    # Peaks must be separated by mask radius (5 residues)
    # 15 residues.
    curvature = np.array([0.0, 0.1, 0.5, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.1, 0.0])
    plddts = np.array([80]*15)
    hotspots = find_bending_hotspots(curvature, plddts, top_n=2)
    # Should find peak at 12 (0.6) and 2 (0.5)
    assert "k=0.60" in hotspots
    assert "k=0.50" in hotspots

def test_find_hinges():
    # 50 < pLDDT < 80 and Curvature > 0.1
    # Indices 2,3,4 fit.
    plddts = np.array([90, 90, 60, 60, 60, 90, 90])
    curvature = np.array([0.1, 0.1, 0.4, 0.4, 0.4, 0.1, 0.1])
    hinges = find_hinges(plddts, curvature)
    assert "2-4" in hinges

def test_find_domain_segments():
    # 15 high, 5 low, 15 high
    # min_len=10
    plddts = np.array([90]*15 + [40]*5 + [90]*15)
    domains = find_domain_segments(plddts, min_len=10)
    assert len(domains) == 2
    assert domains[0] == (0, 14)
    assert domains[1] == (20, 34)

def test_compute_pae_metrics():
    # Mock PAE and domains
    # 2 domains: 0-9 and 10-19.
    # Intra: low (e.g. 5). Inter: high (e.g. 20).
    domains = [(0, 9), (10, 19)]
    pae = np.zeros((20, 20))

    # Fill intra
    pae[0:10, 0:10] = 5.0
    pae[10:20, 10:20] = 5.0

    # Fill inter
    pae[0:10, 10:20] = 20.0
    pae[10:20, 0:10] = 20.0

    mean_pae, blockiness = compute_pae_metrics(pae, domains)

    # Mean intra = 5.0
    # Mean inter = 20.0
    # Blockiness = 15.0

    assert blockiness == pytest.approx(15.0)
