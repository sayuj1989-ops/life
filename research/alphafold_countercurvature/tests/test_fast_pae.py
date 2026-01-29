
import unittest
import numpy as np
import json
import sys
from pathlib import Path
import os

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(repo_root))

from research.alphafold_countercurvature.src.afcc.structure import StructureParser

class TestFastPAE(unittest.TestCase):
    def setUp(self):
        self.parser = StructureParser()
        self.list_file = Path("test_pae_list.json")
        self.dict_file = Path("test_pae_dict.json")
        self.matrix = np.random.randint(0, 30, (50, 50)).tolist()

        # Create List format
        with open(self.list_file, 'w') as f:
            json.dump([{"predicted_aligned_error": self.matrix}], f)

        # Create Dict format
        with open(self.dict_file, 'w') as f:
            json.dump({"predicted_aligned_error": self.matrix}, f)

    def tearDown(self):
        if self.list_file.exists(): self.list_file.unlink()
        if self.dict_file.exists(): self.dict_file.unlink()
        # Clean up potential cache files
        cache_list = self.list_file.with_suffix('.pae.npz')
        cache_dict = self.dict_file.with_suffix('.pae.npz')
        if cache_list.exists(): cache_list.unlink()
        if cache_dict.exists(): cache_dict.unlink()

    def test_list_format(self):
        # Ensure no cache first
        cache = self.list_file.with_suffix('.pae.npz')
        if cache.exists(): cache.unlink()

        arr = self.parser.parse_pae(self.list_file)
        self.assertIsNotNone(arr)
        self.assertEqual(arr.shape, (50, 50))
        np.testing.assert_array_equal(arr, np.array(self.matrix))

    def test_dict_format(self):
        # Ensure no cache first
        cache = self.dict_file.with_suffix('.pae.npz')
        if cache.exists(): cache.unlink()

        arr = self.parser.parse_pae(self.dict_file)
        self.assertIsNotNone(arr)
        self.assertEqual(arr.shape, (50, 50))
        np.testing.assert_array_equal(arr, np.array(self.matrix))

    def test_cache_creation(self):
        # Ensure no cache first
        cache = self.list_file.with_suffix('.pae.npz')
        if cache.exists(): cache.unlink()

        # Run once to create cache
        self.parser.parse_pae(self.list_file)
        self.assertTrue(cache.exists())

        # Verify loading from cache works
        arr = self.parser.parse_pae(self.list_file)
        np.testing.assert_array_equal(arr, np.array(self.matrix))

if __name__ == '__main__':
    unittest.main()
