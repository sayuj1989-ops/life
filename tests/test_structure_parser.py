import pytest
import numpy as np
from pathlib import Path

from research.alphafold_countercurvature.src.afcc.structure import StructureParser

def test_fast_parse_pdb_arrays_standard(tmp_path):
    """Test fast parsing of standard ATOM records."""
    pdb_content = """
ATOM      1  N   MET A   1     -48.324 -15.228   4.203  1.00 31.92           N
ATOM      2  CA  MET A   1     -49.692 -14.663   4.267  1.00 31.92           C
ATOM      3  C   MET A   1     -49.650 -13.259   3.682  1.00 31.92           C
ATOM      4  O   MET A   1     -48.567 -12.692   3.614  1.00 31.92           O
ATOM      5  N   ALA A   2     -50.768 -12.807   3.126  1.00 35.28           N
ATOM      6  CA  ALA A   2     -50.888 -11.781   2.071  1.00 35.28           C
"""
    pdb_file = tmp_path / "test.pdb"
    pdb_file.write_text(pdb_content.strip())

    parser = StructureParser()
    coords, plddt, resnames = parser.fast_parse_pdb_arrays(pdb_file)

    assert coords is not None
    assert len(coords) == 2
    assert len(plddt) == 2
    assert len(resnames) == 2

    # Check MET
    assert np.allclose(coords[0], [-49.692, -14.663, 4.267])
    assert plddt[0] == 31.92
    assert resnames[0] == "MET"

    # Check ALA
    assert np.allclose(coords[1], [-50.888, -11.781, 2.071])
    assert plddt[1] == 35.28
    assert resnames[1] == "ALA"

def test_fast_parse_pdb_arrays_altloc(tmp_path):
    """Test handling of alternate locations (should keep ' ' or 'A')."""
    pdb_content = """
ATOM      1  CA  MET A   1      10.000  10.000  10.000  1.00 50.00           C
ATOM      2  CA AMET A   2      20.000  20.000  20.000  0.50 60.00           C
ATOM      3  CA BMET A   2      21.000  21.000  21.000  0.50 60.00           C
"""
    # Note: AltLoc is col 17 (index 16). ' ' for atom 1. 'A' for atom 2. 'B' for atom 3.
    # We expect to keep 1 and 2, drop 3.

    pdb_file = tmp_path / "test_alt.pdb"
    pdb_file.write_text(pdb_content.strip())

    parser = StructureParser()
    coords, plddt, resnames = parser.fast_parse_pdb_arrays(pdb_file)

    assert len(coords) == 2
    assert coords[0][0] == 10.0
    assert coords[1][0] == 20.0

def test_fast_parse_pdb_arrays_missing_file(tmp_path):
    parser = StructureParser()
    coords, _, _ = parser.fast_parse_pdb_arrays(tmp_path / "nonexistent.pdb")
    assert coords is None
