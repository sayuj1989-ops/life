import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import numpy as np

# Add scripts to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

import bolt_biofold_cycle

class TestBoltBiofoldCycle(unittest.TestCase):

    def test_calculate_curvature_torsion(self):
        # Create a simple helix or line
        # Line along Z (ensure float)
        coords = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 0, 2],
            [0, 0, 3],
            [0, 0, 4]
        ], dtype=float)
        curv, tors = bolt_biofold_cycle.calculate_curvature_torsion(coords)
        # Curvature should be 0 (straight line)
        self.assertTrue(np.allclose(curv, 0))

        # 90 degree bend
        coords_bend = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 2, 1]
        ], dtype=float)
        curv_bend, _ = bolt_biofold_cycle.calculate_curvature_torsion(coords_bend)
        # t0 = (0,0,1), t1 = (0,1,0). Dot = 0. Angle = pi/2.
        # curv_bend[1] corresponds to angle between t0 and t1.
        self.assertAlmostEqual(curv_bend[1], np.pi/2)

    def test_identify_hotspots(self):
        curv = np.array([0.1, 0.2, 0.5, 0.2, 0.1])
        hotspots = bolt_biofold_cycle.identify_hotspots(curv, threshold=0.3)
        self.assertEqual(len(hotspots), 1)
        self.assertEqual(hotspots[0][0], 2)
        self.assertEqual(hotspots[0][1], 0.5)

    def test_exposed_surface_proxy(self):
        # 3 points in triangle, dist=1
        coords = np.array([[0,0,0], [1,0,0], [0,1,0]], dtype=float)

        # Radius 2.0 covers all
        frac, counts = bolt_biofold_cycle.exposed_surface_proxy_neighbors(coords, radius=2.0)
        # All within 2.0 of each other.
        # Neighbors for each: 2 others.
        # neighbor_counts = [2, 2, 2]
        # Threshold is 15. So all are "exposed" (count < 15).
        self.assertEqual(frac, 1.0)
        self.assertTrue(np.all(counts == 2))

if __name__ == '__main__':
    unittest.main()
