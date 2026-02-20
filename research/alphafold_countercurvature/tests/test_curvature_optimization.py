import unittest
import numpy as np
from research.alphafold_countercurvature.src.afcc.metrics import MetricsAnalyzer

class TestCurvatureOptimization(unittest.TestCase):
    def setUp(self):
        self.analyzer = MetricsAnalyzer()

    def test_curvature_match(self):
        """Verifies that the optimized curvature calculation matches the legacy formula."""
        n_residues = 1000
        np.random.seed(42)
        coords = np.zeros((n_residues, 3))
        step = np.random.randn(n_residues, 3)
        coords[0] = [0, 0, 0]
        for i in range(1, n_residues):
            coords[i] = coords[i-1] + step[i]

        # Precompute inputs
        bond_vectors = coords[1:] - coords[:-1]
        bond_lengths = np.linalg.norm(bond_vectors, axis=1)
        normals = np.cross(bond_vectors[:-1], bond_vectors[1:])
        normals_norm = np.linalg.norm(normals, axis=1)

        # 1. Run optimized (normals_norm provided)
        optimized = self.analyzer.calculate_curvature(
            coords,
            bond_vectors=bond_vectors,
            bond_lengths=bond_lengths,
            normals_norm=normals_norm
        )

        # 2. Run legacy path (force normals_norm=None to trigger Heron's formula path)
        # Note: The 'else' block in calculate_curvature implements Heron's formula which is mathematically equivalent
        # to the Area = 0.5 * normals_norm logic used in the optimization.
        legacy = self.analyzer.calculate_curvature(
            coords,
            bond_vectors=bond_vectors,
            bond_lengths=bond_lengths,
            normals_norm=None # Force legacy path
        )

        # Compare
        mask_opt = ~np.isnan(optimized)
        mask_leg = ~np.isnan(legacy)

        self.assertTrue(np.array_equal(mask_opt, mask_leg), "NaN masks do not match")

        diff = np.abs(optimized[mask_opt] - legacy[mask_leg])
        max_diff = np.max(diff)

        self.assertLess(max_diff, 1e-10, f"Max difference {max_diff} exceeds tolerance")

if __name__ == '__main__':
    unittest.main()
