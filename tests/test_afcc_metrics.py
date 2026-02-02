import pytest
import numpy as np
import sys
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_root))

from research.alphafold_countercurvature.src.afcc.metrics import MetricsAnalyzer

@pytest.fixture
def analyzer():
    return MetricsAnalyzer()

def test_rg_calculation(analyzer):
    # Cube corners: (0,0,0) to (1,1,1)
    coords = np.array([
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
        [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]
    ], dtype=float)

    rg = analyzer.calculate_rg(coords)
    assert rg > 0
    # Center is (0.5, 0.5, 0.5). Distance to corner is sqrt(0.5^2 * 3) = sqrt(0.75) ~ 0.866
    assert np.isclose(rg, np.sqrt(0.75))

def test_anisotropy_rod(analyzer):
    # Long rod along Z
    z = np.linspace(0, 10, 20)
    coords = np.column_stack([np.zeros_like(z), np.zeros_like(z), z])

    metrics = analyzer.calculate_anisotropy(coords)
    assert metrics['anisotropy_ratio'] > 3.0
    assert metrics['lambda_max'] > metrics['lambda_min']

def test_anisotropy_sphere(analyzer):
    # Better sphere points (Uniform random on sphere surface)
    np.random.seed(42)
    n = 1000
    pts = np.random.randn(n, 3)
    pts /= np.linalg.norm(pts, axis=1)[:, np.newaxis]
    coords = pts

    metrics = analyzer.calculate_anisotropy(coords)
    # Should be close to 1
    assert 1.0 <= metrics['anisotropy_ratio'] < 1.2

def test_morphology_classification(analyzer):
    # Fibrous
    assert analyzer.classify_morphology(anisotropy=4.0, rg=10.0, n_residues=100) == "Fibrous/Extended"
    # Globular
    assert analyzer.classify_morphology(anisotropy=1.2, rg=10.0, n_residues=100) == "Globular"
    # Intermediate
    assert analyzer.classify_morphology(anisotropy=2.0, rg=10.0, n_residues=100) == "Intermediate"
