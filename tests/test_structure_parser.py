
import unittest
import numpy as np
from pathlib import Path
import tempfile
import sys

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_root))

from research.alphafold_countercurvature.src.afcc.structure import StructureParser

class TestStructureParser(unittest.TestCase):
    def setUp(self):
        self.parser = StructureParser()

    def test_fast_parse_pdb_ca_detection(self):
        """Test that fast_parse_pdb_arrays correctly identifies CA atoms and ignores others."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as tmp:
            tmp_path = Path(tmp.name)
            # 1. Valid CA (Index 12=' ', 13='C', 14='A', 15=' ')
            tmp.write("ATOM      1  CA  ALA A   1      10.000  10.000  10.000  1.00 90.00           C  \n")
            # 2. Calcium (CA element, but usually HETATM, let's say it's ATOM for stress test)
            # "CA  " starts at col 13 (Index 12='C', 13='A', 14=' ', 15=' ')
            tmp.write("ATOM      2 CA   CAL A   2      20.000  20.000  20.000  1.00 90.00           Ca \n")
            # 3. Carbon Beta " CB " (Index 12=' ', 13='C', 14='B')
            tmp.write("ATOM      3  CB  ALA A   1      12.000  12.000  12.000  1.00 90.00           C  \n")
            # 4. Carbon " C  " (Index 12=' ', 13='C', 14=' ')
            tmp.write("ATOM      4  C   ALA A   1      13.000  13.000  13.000  1.00 90.00           C  \n")
            # 5. Nitrogen " N  "
            tmp.write("ATOM      5  N   ALA A   1      14.000  14.000  14.000  1.00 90.00           N  \n")
            # 6. Another valid CA
            tmp.write("ATOM      6  CA  GLY A   3      30.000  30.000  30.000  1.00 80.00           C  \n")

        try:
            # We must bypass cache reading by ensuring cache doesn't exist
            # But the parser tries to read cache.
            # If we just created the file, cache won't exist.

            coords, plddt, resnames = self.parser.fast_parse_pdb_arrays(tmp_path)

            # Expecting 2 atoms (1 and 6)
            self.assertEqual(len(coords), 2, f"Expected 2 CA atoms, got {len(coords)}")
            self.assertEqual(len(plddt), 2)
            self.assertEqual(len(resnames), 2)

            self.assertEqual(resnames[0], 'ALA')
            self.assertEqual(resnames[1], 'GLY')

            # Check coords
            np.testing.assert_array_equal(coords[0], [10.0, 10.0, 10.0])
            np.testing.assert_array_equal(coords[1], [30.0, 30.0, 30.0])

        finally:
            if tmp_path.exists():
                tmp_path.unlink()
            # Cleanup cache if created
            cache_path = tmp_path.with_suffix('.pdb.cache.npz')
            if cache_path.exists():
                cache_path.unlink()

if __name__ == '__main__':
    unittest.main()
