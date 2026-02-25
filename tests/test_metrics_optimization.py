import sys
import os
import pytest
import numpy as np
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../research/alphafold_countercurvature/src')))
from afcc.metrics import MetricsAnalyzer

class TestMetricsOptimization:
    def setup_method(self):
        self.analyzer = MetricsAnalyzer()

    def test_calculate_rg_simple(self):
        """Test Radius of Gyration on a simple shape (cube vertices)."""
        coords = np.array([
            [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
            [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]
        ], dtype=float)

        rg = self.analyzer.calculate_rg(coords)
        assert rg == pytest.approx(np.sqrt(3), rel=1e-5)

    def test_calculate_curvature_circle(self):
        """Test curvature on a circle of radius R=10."""
        R = 10.0
        theta = np.linspace(0, 2*np.pi, 100)
        x = R * np.cos(theta)
        y = R * np.sin(theta)
        z = np.zeros_like(theta)
        coords = np.column_stack([x, y, z])

        # Expected curvature = 1/R = 0.1
        kappa = self.analyzer.calculate_curvature(coords)

        valid_kappa = kappa[10:-10]
        assert np.allclose(valid_kappa, 0.1, atol=1e-3)

    def test_calculate_torsion_helix(self):
        """Test torsion on a helix."""
        # Helix: x = a cos(t), y = a sin(t), z = b t
        a = 10.0
        b = 2.0
        n_points = 200
        t_max = 4*np.pi
        t = np.linspace(0, t_max, n_points)
        x = a * np.cos(t)
        y = a * np.sin(t)
        z = b * t
        coords = np.column_stack([x, y, z])

        # Continuous torsion
        tau_continuous = b / (a**2 + b**2)

        # Calculate step size ds
        dt = t[1] - t[0]
        ds = np.sqrt(a**2 + b**2) * dt

        # Expected discrete torsion angle = tau * ds
        expected_angle = tau_continuous * ds

        tau_angles = self.analyzer.calculate_torsion(coords)

        valid_tau = tau_angles[10:-10]

        # Check mean absolute torsion angle matches expectation
        # The implementation returns angle in radians between binormals
        assert np.allclose(np.abs(valid_tau), expected_angle, rtol=0.1)

    def test_analyze_structure_consistency(self):
        """Test analyze_structure runs without error and returns consistent types."""
        coords = np.random.rand(50, 3) * 10
        plddt = np.random.rand(50) * 100
        resnames = np.array(['ALA'] * 50)

        metrics = self.analyzer.analyze_structure(coords=coords, plddt_scores=plddt, resnames=resnames)

        assert isinstance(metrics['radius_of_gyration'], float)
        assert isinstance(metrics['curvature_summary'], float)
        assert isinstance(metrics['torsion_summary'], float)
        assert metrics['radius_of_gyration'] > 0

if __name__ == "__main__":
    pytest.main([__file__])
