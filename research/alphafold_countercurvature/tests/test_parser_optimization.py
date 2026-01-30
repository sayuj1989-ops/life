
import unittest
import numpy as np
import tempfile
import zipfile
from pathlib import Path
import sys

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(repo_root))

from research.alphafold_countercurvature.src.afcc.structure import StructureParser

class TestParserOptimization(unittest.TestCase):
    def setUp(self):
        self.parser = StructureParser()
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.pdb_path = Path(self.tmp_dir.name) / "test.pdb"

        # Create a dummy PDB file
        with open(self.pdb_path, "w") as f:
            f.write("ATOM      1  N   ALA A   1      10.000  20.000  30.000  1.00 90.00           N\n")
            f.write("ATOM      2  CA  ALA A   1      11.000  21.000  31.000  1.00 95.00           C\n")
            f.write("ATOM      3  C   ALA A   1      12.000  22.000  32.000  1.00 90.00           C\n")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_cache_creation_uncompressed(self):
        # First parsing should create cache
        coords, plddt, resnames = self.parser.fast_parse_pdb_arrays(self.pdb_path)

        cache_path = self.pdb_path.with_suffix('.pdb.cache.npz')
        self.assertTrue(cache_path.exists(), "Cache file should be created")

        # Verify content correctness
        self.assertEqual(len(coords), 1)
        self.assertAlmostEqual(coords[0][0], 11.0)
        self.assertAlmostEqual(plddt[0], 95.0)
        self.assertEqual(resnames[0], "ALA")

        # Verify it is loadable
        with np.load(cache_path) as data:
            self.assertTrue('coords' in data)
            self.assertTrue('plddt' in data)
            self.assertTrue('resnames' in data)

        # Verify compression type (Goal: Uncompressed aka Stored = 0)
        # Note: np.savez uses zipfile.ZIP_STORED (0)
        #       np.savez_compressed uses zipfile.ZIP_DEFLATED (8)
        with zipfile.ZipFile(cache_path, 'r') as zf:
            info = zf.getinfo('coords.npy')
            # If my optimization is applied, this should be 0.
            # If not (current state), it should be 8.
            # print(f"Compression type: {info.compress_type}")
            # We assert 0 (ZIP_STORED) because we expect uncompressed now.
            self.assertEqual(info.compress_type, 0, "Cache should be uncompressed (ZIP_STORED) for performance")

    def test_cache_loading(self):
        # Create cache first
        self.parser.fast_parse_pdb_arrays(self.pdb_path)

        # Modify the PDB file to ensure we are reading from cache
        # (Note: parser checks timestamps, so we must keep cache newer or same time)
        # If we touch PDB, cache becomes stale.
        # So we touch cache to make it newer.
        cache_path = self.pdb_path.with_suffix('.pdb.cache.npz')
        cache_path.touch()

        # Now parse again
        coords, plddt, resnames = self.parser.fast_parse_pdb_arrays(self.pdb_path)

        # Should still be ALA/95.0
        self.assertEqual(coords[0][0], 11.0)

if __name__ == '__main__':
    unittest.main()
