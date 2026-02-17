
import unittest
import numpy as np
import sys
from pathlib import Path

# Add scripts to path to import the function
sys.path.append(str(Path(__file__).parent.parent / "scripts" / "data_management"))
from bolt_biofold_analysis import compute_surface_metrics

class TestSurfaceMetrics(unittest.TestCase):
    def test_isolated_cluster_high_conf(self):
        """
        Cluster 1: 25 points (buried).
        Cluster 2: 1 point far away (exposed).
        All High Confidence (pLDDT=90).
        """
        np.random.seed(42)
        # Cluster 1: 25 points
        c1 = np.random.rand(25, 3)
        n1 = ['ALA'] * 25
        p1 = [90.0] * 25

        # Cluster 2: 1 point
        c2 = np.array([[20.0, 20.0, 20.0]])
        n2 = ['ARG'] # Charged
        p2 = [90.0]

        coords = np.vstack([c1, c2])
        resnames = np.array(n1 + n2)
        plddts = np.array(p1 + p2)

        metrics = compute_surface_metrics(coords, resnames, plddts)

        # 1 exposed point (HC)
        self.assertEqual(metrics['exposed_surface_proxy'], 1)
        # Charged score 1.0
        self.assertAlmostEqual(metrics['charged_patch_score'], 1.0)

    def test_low_confidence_exclusion(self):
        """
        1 point far away (exposed).
        But Low Confidence (pLDDT=50).
        Should be ignored.
        """
        coords = np.array([[20.0, 20.0, 20.0]])
        resnames = np.array(['ARG'])
        plddts = np.array([50.0]) # Low confidence

        metrics = compute_surface_metrics(coords, resnames, plddts)

        # Should be 0 exposed (HC)
        self.assertEqual(metrics['exposed_surface_proxy'], 0)
        self.assertEqual(metrics['charged_patch_score'], 0.0)

    def test_mixed_confidence(self):
        """
        2 far points (exposed).
        Pt 1: ARG, pLDDT=90 (HC, Charged)
        Pt 2: ALA, pLDDT=50 (LC, Ignored)
        """
        coords = np.array([[0.0, 0.0, 0.0], [20.0, 20.0, 20.0]])
        resnames = np.array(['ARG', 'ALA'])
        plddts = np.array([90.0, 50.0])

        metrics = compute_surface_metrics(coords, resnames, plddts)

        # Only 1 HC exposed
        self.assertEqual(metrics['exposed_surface_proxy'], 1)
        # That 1 is ARG -> score 1.0
        self.assertAlmostEqual(metrics['charged_patch_score'], 1.0)

    def test_empty(self):
        coords = np.array([])
        resnames = np.array([])
        plddts = np.array([])
        metrics = compute_surface_metrics(coords, resnames, plddts)
        self.assertEqual(metrics['exposed_surface_proxy'], 0)
        self.assertEqual(metrics['charged_patch_score'], 0.0)

if __name__ == '__main__':
    unittest.main()
