
import numpy as np
import pytest
import sys
import time
from pathlib import Path

# Add scripts directory to path to import the script as module
# Assuming this test is in tests/
sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts" / "data_management"))

try:
    from bolt_biofold_analysis import compute_surface_metrics
except ImportError:
    # If run from root without PYTHONPATH, try adding scripts/data_management manually
    sys.path.append("scripts/data_management")
    from bolt_biofold_analysis import compute_surface_metrics

def test_compute_surface_metrics_correctness():
    # Test case 1: Isolated point (exposed)
    coords = np.array([[0.0, 0.0, 0.0]])
    resnames = np.array(['ALA'])
    plddts = np.array([90.0]) # High confidence

    # Neighbor count for isolated point is 0. Exposed if count < 20 and pLDDT >= 70.
    metrics = compute_surface_metrics(coords, resnames, plddts)
    assert metrics['exposed_surface_proxy'] == 1
    assert metrics['charged_patch_score'] == 0.0

    # Test case 2: Buried point (many neighbors)
    # Create a dense cluster around origin
    # 30 points within 2.0 distance
    np.random.seed(42)
    cluster = np.random.rand(30, 3) * 2.0
    # Add one point at origin (index 0)
    cluster[0] = [0, 0, 0]

    resnames = np.array(['ALA'] * 30)
    plddts = np.array([90.0] * 30)

    metrics = compute_surface_metrics(cluster, resnames, plddts)

    # 30 points in small volume -> dense -> not exposed
    assert metrics['exposed_surface_proxy'] < 30

def test_compute_surface_metrics_charged():
    # 2 exposed points, 1 charged (ARG), 1 uncharged (ALA)
    coords = np.array([
        [0.0, 0.0, 0.0],
        [20.0, 0.0, 0.0] # Far away
    ])
    resnames = np.array(['ARG', 'ALA'])
    plddts = np.array([90.0, 90.0])

    metrics = compute_surface_metrics(coords, resnames, plddts)
    assert metrics['exposed_surface_proxy'] == 2
    assert metrics['charged_patch_score'] == 0.5

def test_compute_surface_metrics_performance():
    # Benchmark with N=3000
    N = 3000
    np.random.seed(42)
    coords = np.random.rand(N, 3) * 100
    resnames = np.array(['ALA'] * N)
    plddts = np.array([90.0] * N)

    # Warmup
    compute_surface_metrics(coords, resnames, plddts)

    t0 = time.time()
    count = 20
    for _ in range(count):
        compute_surface_metrics(coords, resnames, plddts)
    t1 = time.time()

    avg_time = (t1 - t0) / count
    print(f"\nAvg time per call (N={N}): {avg_time*1000:.3f} ms")

    # We expect optimization to keep this low.
    # Without optimization: ~21ms
    # With optimization: ~8ms
    # Set threshold comfortably high for CI variability but low enough to catch huge regressions
    assert avg_time < 0.100

if __name__ == "__main__":
    pytest.main([__file__])
