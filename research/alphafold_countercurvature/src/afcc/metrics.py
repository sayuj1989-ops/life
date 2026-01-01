import numpy as np
import pandas as pd
from Bio.PDB.Structure import Structure
from typing import Dict, Any

class MetricsAnalyzer:
    def __init__(self):
        pass

    def calculate_rg(self, coords: np.ndarray) -> float:
        """Calculates Radius of Gyration based on CA atoms."""
        if len(coords) == 0:
            return 0.0

        center_of_mass = np.mean(coords, axis=0)
        # Rg = sqrt(mean((r_i - r_cm)^2))
        sq_dists = np.sum((coords - center_of_mass)**2, axis=1)
        rg = np.sqrt(np.mean(sq_dists))
        return float(rg)

    def calculate_anisotropy(self, coords: np.ndarray) -> Dict[str, float]:
        """
        Calculates Principal Moments of Inertia and Anisotropy.
        Using CA atoms as point masses.
        """
        if len(coords) < 3:
            return {'lambda1': 0, 'lambda2': 0, 'lambda3': 0, 'anisotropy': 1.0}

        center = np.mean(coords, axis=0)
        coords_centered = coords - center

        # Gyration Tensor / Inertia Tensor equivalent for equal masses
        # T_ij = (1/N) * sum(r_i_a * r_i_b)
        tensor = np.dot(coords_centered.T, coords_centered) / len(coords)

        eigvals = np.linalg.eigvalsh(tensor)
        # Sort ascending
        eigvals = np.sort(eigvals)

        # lambda1 >= lambda2 >= lambda3 usually in physics, but here sorted ascending
        # so l1 is smallest, l3 is largest
        l1, l2, l3 = eigvals

        # Anisotropy ratio (largest / smallest)
        # Add epsilon to avoid div by zero
        ratio = np.sqrt(l3) / (np.sqrt(l1) + 1e-6)

        return {
            'lambda_min': float(l1),
            'lambda_mid': float(l2),
            'lambda_max': float(l3),
            'anisotropy_ratio': float(ratio)
        }

    def classify_morphology(self, anisotropy: float, rg: float, n_residues: int) -> str:
        """
        Heuristic classification:
        - Globular: Low anisotropy (~1-1.5)
        - Fibrous/Extended: High anisotropy (> 3.0)
        - Intermediate: In between
        """
        if anisotropy > 3.0:
            return "Fibrous/Extended"
        elif anisotropy > 1.5:
            return "Intermediate"
        else:
            return "Globular"

    def analyze_structure(self, structure: Structure = None, plddt_scores: np.ndarray = None, coords: np.ndarray = None) -> Dict[str, Any]:
        """
        Runs all metrics on a structure.

        Args:
            structure: Bio.PDB Structure object (deprecated, used if coords/plddt not provided)
            plddt_scores: Pre-extracted pLDDT scores
            coords: Pre-extracted CA coordinates
        """
        # Support legacy call signature for a moment or handle both
        if coords is None and structure is not None:
             # Extract manually if not provided (though this is what we want to avoid)
             # But for strict compatibility with older calls that might pass structure + plddt but not coords
             # we should probably extract coords here if missing.
             # However, let's assume the caller will be updated to pass coords.
             # Or we can re-implement the extraction here if needed.
             coords = []
             for model in structure:
                 for chain in model:
                     for residue in chain:
                         if 'CA' in residue:
                             coords.append(residue['CA'].get_coord())
             coords = np.array(coords)

        if plddt_scores is None and structure is not None:
             # This shouldn't happen based on previous signature, but for safety
             pass

        rg = self.calculate_rg(coords)
        shape_props = self.calculate_anisotropy(coords)

        mean_plddt = np.mean(plddt_scores) if len(plddt_scores) > 0 else 0
        fraction_low_conf = np.sum(plddt_scores < 70) / len(plddt_scores) if len(plddt_scores) > 0 else 0

        # Count residues
        n_res = len(plddt_scores)

        morphology = self.classify_morphology(shape_props['anisotropy_ratio'], rg, n_res)

        return {
            'n_residues': n_res,
            'mean_plddt': mean_plddt,
            'fraction_low_plddt': fraction_low_conf,
            'radius_of_gyration': rg,
            'anisotropy': shape_props['anisotropy_ratio'],
            'morphology': morphology,
            **shape_props
        }
