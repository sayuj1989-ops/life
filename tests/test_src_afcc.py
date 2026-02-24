import pytest
import numpy as np
import os
import json
from afcc.metrics import MetricsAnalyzer
from afcc.structure import StructureParser

# Fixtures or Mocks
@pytest.fixture
def dummy_pdb(tmp_path):
    """Creates a dummy PDB file for testing."""
    pdb_path = tmp_path / "test.pdb"
    content = """
ATOM      1  N   MET A   1      11.104  13.207   9.400  1.00 90.00           N
ATOM      2  CA  MET A   1      11.639  12.443   8.239  1.00 90.00           C
ATOM      3  C   MET A   1      11.666  10.957   8.528  1.00 90.00           C
ATOM      4  O   MET A   1      10.638  10.435   8.948  1.00 90.00           O
ATOM      5  CB  MET A   1      13.064  12.951   7.915  1.00 90.00           C
ATOM      6  CG  MET A   1      13.684  12.454   6.611  1.00 90.00           C
ATOM      7  SD  MET A   1      15.394  12.969   6.435  1.00 90.00           S
ATOM      8  CE  MET A   1      16.141  11.758   5.362  1.00 90.00           C
ATOM      9  N   VAL A   2      12.825  10.283   8.291  1.00 80.00           N
ATOM     10  CA  VAL A   2      13.003   8.868   8.537  1.00 80.00           C
"""
    pdb_path.write_text(content)
    return str(pdb_path)

@pytest.fixture
def dummy_pae(tmp_path):
    """Creates a dummy PAE JSON file."""
    pae_path = tmp_path / "test.json"
    content = '[{"predicted_aligned_error": [[0, 10], [10, 0]]}]'
    pae_path.write_text(content)
    return str(pae_path)

def test_structure_parser(dummy_pdb, dummy_pae):
    parser = StructureParser()

    # Test PDB Parsing
    coords, plddt, resnames = parser.fast_parse_pdb_arrays(dummy_pdb)
    assert coords is not None
    assert plddt is not None
    assert resnames is not None
    assert len(coords) == 2 # Two CA atoms
    assert len(plddt) == 2
    assert plddt[0] == 90.0
    assert plddt[1] == 80.0
    assert resnames[0] == 'MET'

    # Test PAE Parsing
    pae = parser.parse_pae(dummy_pae)
    assert pae is not None
    assert pae.shape == (2, 2)

def test_metrics_analyzer_rod():
    analyzer = MetricsAnalyzer()

    # Create a rod-like structure (along X axis)
    # 10 points along X
    x = np.linspace(0, 10, 10)
    y = np.random.normal(0, 0.1, 10) # Small noise
    z = np.random.normal(0, 0.1, 10)
    coords = np.column_stack((x, y, z))
    plddt = np.full(10, 90.0)
    resnames = np.full(10, 'ALA')

    metrics = analyzer.analyze_structure(coords, plddt, resnames)

    assert metrics['plddt_mean'] == 90.0
    assert metrics['anisotropy_index'] > 3.0 # Should be high
    assert metrics['morphology'] == 'Fibrous'
    assert metrics['radius_of_gyration'] > 0.0

def test_metrics_analyzer_sphere():
    analyzer = MetricsAnalyzer()

    # Create a sphere-like structure (Cube corners)
    coords = np.array([
        [0,0,0], [1,0,0], [0,1,0], [0,0,1],
        [1,1,0], [1,0,1], [0,1,1], [1,1,1]
    ], dtype=float)
    plddt = np.full(8, 50.0)
    resnames = np.full(8, 'GLY')

    metrics = analyzer.analyze_structure(coords, plddt, resnames)

    # Anisotropy should be close to 1.0 (Cube is isotropic)
    # 1.0 is minimal anisotropy
    assert metrics['anisotropy_index'] < 1.5
    assert metrics['morphology'] == 'Globular'
