
import unittest
import numpy as np
import os
import sys

# Add source directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../research/alphafold_countercurvature/src')))
from afcc.metrics import MetricsAnalyzer

class TestBoltBioFoldCycle(unittest.TestCase):

    def setUp(self):
        self.analyzer = MetricsAnalyzer()

    def test_curvature_calculation(self):
        # Create a simple bent line: (0,0,0) -> (1,0,0) -> (1,1,0)
        # This is a 90 degree bend.
        coords = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0]
        ])

        # We need more points for the sliding window logic of calculate_curvature
        # The logic usually needs at least 3 points.
        # Let's verify what calculate_curvature returns.

        kappa = self.analyzer.calculate_curvature(coords)

        # For a discrete bend, we expect a non-zero value at the middle index
        # kappa array size is N, with 0 and N-1 as NaN usually or 0.
        # Let's inspect the middle value.

        # The function pads with NaN at ends.
        self.assertTrue(np.isnan(kappa[0]))
        self.assertTrue(np.isnan(kappa[-1]))

        # Middle value should be valid
        middle_val = kappa[1]
        self.assertFalse(np.isnan(middle_val))
        self.assertGreater(middle_val, 0.0)

    def test_anisotropy_calculation(self):
        # Create a long rod
        coords = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [3.0, 0.0, 0.0],
            [4.0, 0.0, 0.0]
        ])

        metrics = self.analyzer.calculate_anisotropy(coords)

        # Should be highly anisotropic
        self.assertGreater(metrics['anisotropy_ratio'], 3.0)

        # Principal axis should be effectively [1, 0, 0]
        # The implementation returns a string representation, let's just check ratio for now.

    def test_radius_of_gyration(self):
        # Simple square
        coords = np.array([
            [1.0, 1.0, 0.0],
            [-1.0, 1.0, 0.0],
            [-1.0, -1.0, 0.0],
            [1.0, -1.0, 0.0]
        ])
        # COM is at 0,0,0
        # Dist sq to center is 1^2 + 1^2 = 2 for all points.
        # Mean sq dist = 2
        # Rg = sqrt(2) = 1.414...

        rg = self.analyzer.calculate_rg(coords)
        self.assertAlmostEqual(rg, np.sqrt(2), places=3)

if __name__ == '__main__':
    unittest.main()
