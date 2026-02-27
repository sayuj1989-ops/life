
import numpy as np
import pytest
import time
from afcc.metrics import MetricsAnalyzer

def test_compute_surface_metrics_correctness():
    analyzer = MetricsAnalyzer()

    # Test case 1: Isolated point (exposed)
    coords = np.array([[0.0, 0.0, 0.0]])
    resnames = np.array(['ALA'])
    plddts = np.array([90.0]) # High confidence

    # analyze_structure computes everything
    metrics = analyzer.analyze_structure(coords=coords, resnames=resnames, plddt_scores=plddts)

    # Neighbor count for isolated point is 0 -> exposed
    # Fraction exposed = 1/1 = 1.0
    assert metrics['exposed_surface_proxy'] == 1.0
    assert metrics['charged_patch_score'] == 0.0

    # Test case 2: Buried point (many neighbors)
    np.random.seed(42)
    cluster = np.random.rand(30, 3) * 2.0
    cluster[0] = [0, 0, 0]
    resnames = np.array(['ALA'] * 30)
    plddts = np.array([90.0] * 30)

    metrics = analyzer.analyze_structure(coords=cluster, resnames=resnames, plddt_scores=plddts)

    # 30 points in small volume -> dense -> mostly buried -> exposed fraction low
    assert metrics['exposed_surface_proxy'] < 1.0

def test_compute_surface_metrics_charged():
    analyzer = MetricsAnalyzer()
    # 2 exposed points, 1 charged (ARG), 1 uncharged (ALA)
    coords = np.array([
        [0.0, 0.0, 0.0],
        [20.0, 0.0, 0.0] # Far away
    ])
    resnames = np.array(['ARG', 'ALA'])
    plddts = np.array([90.0, 90.0])

    metrics = analyzer.analyze_structure(coords=coords, resnames=resnames, plddt_scores=plddts)

    # Both exposed
    assert metrics['exposed_surface_proxy'] == 1.0
    # Charged score = 1 charged / 2 exposed = 0.5
    assert metrics['charged_patch_score'] == 0.5

def test_compute_surface_metrics_performance():
    analyzer = MetricsAnalyzer()
    N = 3000
    np.random.seed(42)
    coords = np.random.rand(N, 3) * 100
    resnames = np.array(['ALA'] * N)
    plddts = np.array([90.0] * N)

    # Warmup
    analyzer.analyze_structure(coords=coords, resnames=resnames, plddt_scores=plddts)

    t0 = time.time()
    count = 5 # Reduced count for heavier integration test
    for _ in range(count):
        analyzer.analyze_structure(coords=coords, resnames=resnames, plddt_scores=plddts)
    t1 = time.time()

    avg_time = (t1 - t0) / count
    print(f"\nAvg time per call (N={N}): {avg_time*1000:.3f} ms")

    # Loose threshold for full analysis
    assert avg_time < 0.500

if __name__ == "__main__":
    pytest.main([__file__])
