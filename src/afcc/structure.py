import numpy as np
import warnings
import json
import os
from Bio import BiopythonWarning
from Bio.PDB import PDBParser

class StructureParser:
    def __init__(self):
        # Bio.PDB.PDBParser with QUIET=True suppresses construction warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', BiopythonWarning)
            self.parser = PDBParser(QUIET=True)

    def fast_parse_pdb_arrays(self, pdb_path):
        """
        Parses a PDB file to extract CA coordinates, pLDDT (B-factors), and residue names.

        Args:
            pdb_path (str): Path to the PDB file.

        Returns:
            tuple: (coords, plddt, resnames)
                - coords: np.array of shape (N, 3)
                - plddt: np.array of shape (N,)
                - resnames: np.array of shape (N,)
                Returns (None, None, None) on failure.
        """
        if not os.path.exists(pdb_path):
            print(f"PDB file not found: {pdb_path}")
            return None, None, None

        try:
            # Use context manager to suppress Biopython warnings during parsing if necessary
            # PDBParser(QUIET=True) usually handles it, but just in case
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', BiopythonWarning)
                structure = self.parser.get_structure('struct', str(pdb_path))

            # Get first model
            model = next(iter(structure))

            coords = []
            plddt = []
            resnames = []

            for residue in model.get_residues():
                # Filter out HETATM if necessary, though AF2 usually doesn't have them in a way that matters here
                # We want standard residues.

                # Get CA atom
                if 'CA' in residue:
                    atom = residue['CA']
                    coords.append(atom.coord)
                    plddt.append(atom.bfactor)
                    resnames.append(residue.resname)

            if not coords:
                print(f"No CA atoms found in {pdb_path}")
                return None, None, None

            return np.array(coords), np.array(plddt), np.array(resnames)

        except Exception as e:
            print(f"Error parsing PDB {pdb_path}: {e}")
            return None, None, None

    def parse_pae(self, pae_path):
        """
        Parses the Predicted Aligned Error (PAE) JSON file.

        Args:
            pae_path (str): Path to the PAE JSON file.

        Returns:
            np.array: PAE matrix, or None on failure.
        """
        if not pae_path or not os.path.exists(pae_path):
            return None

        try:
            with open(pae_path, 'r') as f:
                data = json.load(f)

            # AF2 PAE format: list of dicts, take first one 'predicted_aligned_error'
            if isinstance(data, list) and len(data) > 0:
                if 'predicted_aligned_error' in data[0]:
                     return np.array(data[0]['predicted_aligned_error'])

            # Alternative format
            if isinstance(data, dict) and 'predicted_aligned_error' in data:
                return np.array(data['predicted_aligned_error'])

            return None
        except Exception as e:
            print(f"Error parsing PAE {pae_path}: {e}")
            return None
