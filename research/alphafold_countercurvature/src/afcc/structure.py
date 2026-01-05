import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import json
from Bio.PDB import PDBParser
from Bio.PDB.Structure import Structure

class StructureParser:
    def __init__(self):
        self.parser = PDBParser(QUIET=True)

    def parse_pdb(self, pdb_path: Path, structure_id: str = "structure") -> Optional[Structure]:
        """Parses a PDB file using Bio.PDB"""
        if not pdb_path.exists():
            return None
        try:
            structure = self.parser.get_structure(structure_id, str(pdb_path))
            return structure
        except Exception as e:
            print(f"⚠️ Error parsing PDB {pdb_path}: {e}")
            return None

    def extract_plddt(self, structure: Structure) -> np.ndarray:
        """
        Extracts pLDDT scores from the B-factor column of the structure.
        Returns array of scores per residue (averaging atoms if necessary,
        though usually CA is sufficient or all atoms have same pLDDT in AF models).
        """
        _, plddts, _ = self.extract_coords_and_plddt(structure)
        return plddts

    def extract_coords_and_plddt(self, structure: Structure) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Extracts CA coordinates, pLDDT scores, and residue names in a single pass.

        Returns
        -------
        coords : np.ndarray
            Coordinates of CA atoms for residues that have a CA atom.
            Shape: (N, 3), where N is the number of residues with a CA atom.
        plddts : np.ndarray
            pLDDT scores for residues with CA atoms (using the CA B-factor).
            Shape: (N,), aligned with ``coords`` and ``resnames``.
        resnames : np.ndarray
            Residue names for residues with CA atoms, aligned with ``coords``.
            Shape: (N,).
        """
        coords = []
        plddts = []
        resnames = []
        for model in structure:
            for chain in model:
                for residue in chain:
                    if 'CA' in residue:
                        coords.append(residue['CA'].get_coord())
                        plddts.append(residue['CA'].get_bfactor())
                        resnames.append(residue.get_resname().upper())

        return np.array(coords), np.array(plddts), np.array(resnames)

    def parse_pae(self, pae_path: Path) -> Optional[np.ndarray]:
        """
        Parses PAE JSON file.
        Returns PAE matrix (N, N).
        """
        if not pae_path or not Path(pae_path).exists():
            return None

        try:
            with open(pae_path, 'r') as f:
                data = json.load(f)

            # AlphaFold V2/V3 format usually has "predicted_aligned_error" or "pae"
            # It can be a flattened list or list of lists.
            # Usually: [{"predicted_aligned_error": [[...]]}] or similar structure.

            # Common formats:
            # 1. New API: [ { "predicted_aligned_error": [[...]], ... } ]
            # 2. Old/Other: { "predicted_aligned_error": ... }

            pae_data = None
            if isinstance(data, list) and len(data) > 0:
                pae_data = data[0].get("predicted_aligned_error")
            elif isinstance(data, dict):
                pae_data = data.get("predicted_aligned_error")

            if pae_data:
                return np.array(pae_data)

        except Exception as e:
            print(f"⚠️ Error parsing PAE {pae_path}: {e}")

        return None
