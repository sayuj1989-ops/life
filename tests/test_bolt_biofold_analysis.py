import numpy as np
import pytest
import sys
from pathlib import Path

# Add scripts directory to path to import the script as module
sys.path.append(str(Path(__file__).parent.parent / "scripts/pipeline"))

from bolt_biofold_analysis import compute_geometry_metrics, find_bending_hotspots, find_hinges, find_domains

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
    # Indices: 2 (0.5), 12 (0.6) -> Distance 10 > 5. Should work.
    curvature = np.array([0.0, 0.1, 0.5, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.1, 0.0])
    plddts = np.array([80]*15)
    hotspots = find_bending_hotspots(curvature, plddts, top_n=2)
    assert "k=0.60" in hotspots
    assert "k=0.50" in hotspots

def test_find_hinges():
    # 50 < pLDDT < 80 and Curvature > 0.1
    # Indices 2,3,4 fit.
    plddts = np.array([90, 90, 60, 60, 60, 90, 90])
    curvature = np.array([0.1, 0.1, 0.4, 0.4, 0.4, 0.1, 0.1])
    hinges = find_hinges(plddts, curvature)
    assert "2-4" in hinges

def test_find_domains():
    plddts = np.array([90]*15 + [40]*5 + [90]*15)
    domains = find_domains(plddts, min_len=10)
    assert domains == 2
