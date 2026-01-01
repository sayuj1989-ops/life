import unittest
import numpy as np
from Bio.PDB.Structure import Structure
from Bio.PDB.Model import Model
from Bio.PDB.Chain import Chain
from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom
import sys
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(repo_root))

from research.alphafold_countercurvature.src.afcc.metrics import MetricsAnalyzer
from research.alphafold_countercurvature.src.afcc.afdb import AlphaFoldFetcher

class TestAFCCPipeline(unittest.TestCase):

    def setUp(self):
        self.analyzer = MetricsAnalyzer()

    def create_dummy_structure(self, coords):
        # Helper to create a simple structure
        s = Structure("test")
        m = Model(0)
        c = Chain("A")
        s.add(m)
        m.add(c)

        for i, coord in enumerate(coords):
            res = Residue((" ", i, " "), "GLY", " ")
            atom = Atom("CA", coord, 10.0, 1.0, " ", "CA", i, "C")
            res.add(atom)
            c.add(res)
        return s

    def test_rg_calculation(self):
        # 3 points forming a triangle
        coords = np.array([[0,0,0], [1,0,0], [0,1,0]], dtype=float)

        # Test directly with coords array as per new API
        rg = self.analyzer.calculate_rg(coords)

        # Center of mass = (1/3, 1/3, 0)
        # Distances sq from COM:
        # (0-1/3)^2 + (0-1/3)^2 = 2/9
        # (1-1/3)^2 + (0-1/3)^2 = 4/9 + 1/9 = 5/9
        # (0-1/3)^2 + (1-1/3)^2 = 1/9 + 4/9 = 5/9
        # Mean sq dist = (2/9 + 5/9 + 5/9) / 3 = 12/27 = 4/9
        # Sqrt(4/9) = 2/3 = 0.666...

        self.assertAlmostEqual(rg, 0.6666666, places=5)

    def test_anisotropy_linear(self):
        # Linear structure
        coords = np.array([[0,0,0], [1,0,0], [2,0,0]], dtype=float)

        # Test directly with coords array as per new API
        metrics = self.analyzer.calculate_anisotropy(coords)

        # Should be highly anisotropic (l3 >> l1, l2)
        # l1, l2 should be near 0 (planar/linear)

        self.assertGreater(metrics['anisotropy_ratio'], 10.0)

    def test_afdb_fetcher_init(self):
        # Just check it initializes without error
        fetcher = AlphaFoldFetcher(Path("."), Path("manifest.csv"), dry_run="full")
        self.assertEqual(fetcher.dry_run_mode, "full")

if __name__ == '__main__':
    unittest.main()
