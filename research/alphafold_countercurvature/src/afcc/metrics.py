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
        sq_dists = np.sum((coords - center_of_mass)**2, axis=1)
        rg = np.sqrt(np.mean(sq_dists))
        return float(rg)

    def calculate_anisotropy(self, coords: np.ndarray) -> Dict[str, float]:
        """
        Calculates Principal Moments of Inertia and Anisotropy.
        Using CA atoms as point masses.
        """
        if len(coords) < 3:
            return {'lambda_min': 0, 'lambda_mid': 0, 'lambda_max': 0, 'anisotropy_ratio': 1.0}

        center = np.mean(coords, axis=0)
        coords_centered = coords - center

        tensor = np.dot(coords_centered.T, coords_centered) / len(coords)

        eigvals = np.linalg.eigvalsh(tensor)
        eigvals = np.sort(eigvals)
        l1, l2, l3 = eigvals

        # Anisotropy ratio (largest / smallest)
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

    def calculate_curvature(self, coords: np.ndarray) -> np.ndarray:
        """
        Calculates discrete curvature (kappa) for each residue (assigning to the middle of 3 points).
        Returns array of size len(coords), padded with NaNs at ends.
        Curvature = 4 * Area / (abc)
        """
        if len(coords) < 3:
            return np.full(len(coords), np.nan)

        # Vectorized calculation using 3-point sliding window
        A = coords[:-2]
        B = coords[1:-1]
        C = coords[2:]

        a = np.linalg.norm(B - C, axis=1) # Side opposite A
        b = np.linalg.norm(A - C, axis=1) # Side opposite B
        c = np.linalg.norm(A - B, axis=1) # Side opposite C

        # Heron's formula for area
        s = (a + b + c) / 2
        arg = s * (s - a) * (s - b) * (s - c)
        arg = np.maximum(arg, 0)
        area = np.sqrt(arg)

        denom = a * b * c
        with np.errstate(divide='ignore', invalid='ignore'):
            kappa = 4 * area / denom
            kappa[denom == 0] = 0.0

        result = np.full(len(coords), np.nan)
        result[1:-1] = kappa
        return result

    def calculate_torsion(self, coords: np.ndarray) -> np.ndarray:
        """
        Calculates discrete torsion (tau) for each residue.
        Returns array of size len(coords), padded with NaNs.
        """
        if len(coords) < 4:
            return np.full(len(coords), np.nan)

        b1 = coords[1:-2] - coords[:-3]
        b2 = coords[2:-1] - coords[1:-2]
        b3 = coords[3:] - coords[2:-1]

        n1 = np.cross(b1, b2)
        n2 = np.cross(b2, b3)

        n1_norm = np.linalg.norm(n1, axis=1)
        n2_norm = np.linalg.norm(n2, axis=1)

        with np.errstate(divide='ignore', invalid='ignore'):
            cos_phi = np.einsum('ij,ij->i', n1, n2) / (n1_norm * n2_norm)
            cos_phi = np.clip(cos_phi, -1.0, 1.0)
            phi = np.arccos(cos_phi)

            cross_n1_n2 = np.cross(n1, n2)
            sign_check = np.einsum('ij,ij->i', cross_n1_n2, b2)
            sign = np.sign(sign_check)

        torsion = phi * sign # in radians

        result = np.full(len(coords), np.nan)
        result[1:-2] = torsion
        return result

    def analyze_structure(self, structure: Structure = None, plddt_scores: np.ndarray = None, coords: np.ndarray = None, pae_matrix: np.ndarray = None) -> Dict[str, Any]:
        """
        Runs all metrics on a structure.

        Args:
            structure: Bio.PDB Structure object
            plddt_scores: Pre-extracted pLDDT scores
            coords: Pre-extracted CA coordinates
            pae_matrix: Pre-extracted PAE matrix (optional)
        """
        if coords is None and structure is not None:
            coords_list = []
            for model in structure:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            coords_list.append(residue['CA'].get_coord())
            coords = np.array(coords_list)

        rg = self.calculate_rg(coords)
        shape_props = self.calculate_anisotropy(coords)

        mean_plddt = np.mean(plddt_scores) if len(plddt_scores) > 0 else 0
        fraction_low_conf = np.sum(plddt_scores < 70) / len(plddt_scores) if len(plddt_scores) > 0 else 0

        # pLDDT Fractions
        plddt_fraction_high = np.sum(plddt_scores >= 90) / len(plddt_scores) if len(plddt_scores) > 0 else 0
        plddt_fraction_ok = np.sum((plddt_scores >= 70) & (plddt_scores < 90)) / len(plddt_scores) if len(plddt_scores) > 0 else 0
        plddt_fraction_low = fraction_low_conf
        plddt_mean = mean_plddt
        plddt_median = np.median(plddt_scores) if len(plddt_scores) > 0 else 0

        # Geometry
        kappa = self.calculate_curvature(coords)
        tau = self.calculate_torsion(coords)

        # High confidence mask (pLDDT >= 70)
        plddt_mask = (plddt_scores >= 70)

        strict_mask_kappa = np.zeros(len(coords), dtype=bool)
        if len(coords) >= 3:
            m = plddt_mask[:-2] & plddt_mask[1:-1] & plddt_mask[2:]
            strict_mask_kappa[1:-1] = m

        kappa_valid = kappa[strict_mask_kappa & ~np.isnan(kappa)]

        strict_mask_tau = np.zeros(len(coords), dtype=bool)
        if len(coords) >= 4:
            m = plddt_mask[:-3] & plddt_mask[1:-2] & plddt_mask[2:-1] & plddt_mask[3:]
            strict_mask_tau[1:-2] = m

        tau_valid = tau[strict_mask_tau & ~np.isnan(tau)]

        mean_curvature = np.mean(kappa_valid) if len(kappa_valid) > 0 else 0.0
        mean_torsion = np.mean(np.abs(tau_valid)) if len(tau_valid) > 0 else 0.0

        # End-to-end distance (longest high-confidence segment)
        is_hc = plddt_mask.astype(int)
        bounded = np.hstack(([0], is_hc, [0]))
        d = np.diff(bounded)
        starts = np.where(d == 1)[0]
        ends = np.where(d == -1)[0]

        max_len = 0
        best_segment = None

        for s, e in zip(starts, ends):
            length = e - s
            if length > max_len:
                max_len = length
                best_segment = (s, e)

        if best_segment:
            s, e = best_segment
            seg_coords = coords[s:e]
            if len(seg_coords) > 1:
                end_to_end = np.linalg.norm(seg_coords[-1] - seg_coords[0])
            else:
                end_to_end = 0.0
        else:
            end_to_end = 0.0

        # Bending Hotspots
        hotspots = []
        if len(kappa_valid) > 0:
            valid_indices = np.where(strict_mask_kappa & ~np.isnan(kappa))[0]
            valid_kappas = kappa[valid_indices]
            sorted_idx = np.argsort(valid_kappas)[::-1]
            top_k = min(3, len(sorted_idx))
            for k in range(top_k):
                idx = valid_indices[sorted_idx[k]]
                val = valid_kappas[sorted_idx[k]]
                hotspots.append(f"{idx}:{val:.2f}")

        bending_hotspots_str = "; ".join(hotspots)

        # Exposed Surface Proxy (CN < 15)
        charged_patch_score = 0.0
        exposed_fraction = 0.0

        if len(coords) > 0:
            # Vectorized distance calculation
            dists = np.sqrt(np.sum((coords[:, np.newaxis, :] - coords[np.newaxis, :, :]) ** 2, axis=2))
            cn = np.sum(dists < 10.0, axis=1) - 1 # exclude self
            n_exposed = np.sum(cn < 15)
            exposed_fraction = n_exposed / len(coords)

            if structure:
                charged_count = 0
                exposed_hc_count = 0
                idx = 0
                for model in structure:
                    for chain in model:
                        for residue in chain:
                            if 'CA' in residue:
                                if idx < len(cn): # Safety check
                                    conf = plddt_scores[idx]
                                    is_exposed = (cn[idx] < 15)
                                    if conf >= 70 and is_exposed:
                                        exposed_hc_count += 1
                                        resname = residue.get_resname().upper()
                                        if resname in ['ASP', 'GLU', 'LYS', 'ARG', 'HIS']:
                                            charged_count += 1
                                idx += 1
                if exposed_hc_count > 0:
                    charged_patch_score = charged_count / exposed_hc_count

        # PAE Metrics
        pae_mean = 0.0
        pae_blockiness = 0.0
        if pae_matrix is not None and pae_matrix.size > 0:
            pae_mean = np.mean(pae_matrix)
            # Simple blockiness proxy: Ratio of (mean near diagonal) / (mean far from diagonal)
            # Diagonal block +/- 10 residues
            n = pae_matrix.shape[0]
            indices = np.indices((n, n))
            dist_from_diag = np.abs(indices[0] - indices[1])

            near_mask = dist_from_diag < 20
            far_mask = dist_from_diag >= 20

            mean_near = np.mean(pae_matrix[near_mask]) if np.any(near_mask) else 0
            mean_far = np.mean(pae_matrix[far_mask]) if np.any(far_mask) else 0

            # Contrast. High score = distinct domains (low intra, high inter).
            # If single domain, mean_far is roughly mean_near. Score ~ 1.
            # If multi domain, mean_near is low, mean_far is high. Score > 1.
            epsilon = 1e-8
            if mean_near > epsilon:
                pae_blockiness = mean_far / mean_near
            else:
                pae_blockiness = 0.0

        n_res = len(plddt_scores)
        morphology = self.classify_morphology(shape_props['anisotropy_ratio'], rg, n_res)

        # Flags
        low_confidence_warning = (mean_plddt < 70) or (fraction_low_conf > 0.5)
        # multi_domain_uncertain: high inter-domain PAE?
        # Simple proxy: High blockiness but also High overall PAE?
        # Or just checking if PAE blockiness > threshold (e.g. 2.0)
        multi_domain_uncertain = (pae_blockiness > 1.5) and (pae_mean > 10.0)
        likely_IDR_heavy = (fraction_low_conf > 0.3)

        return {
            'n_residues': n_res,
            'pLDDT_mean': plddt_mean,
            'pLDDT_median': plddt_median,
            'pLDDT_fraction_high': plddt_fraction_high,
            'pLDDT_fraction_ok': plddt_fraction_ok,
            'pLDDT_fraction_low': plddt_fraction_low,
            'radius_of_gyration': rg,
            'anisotropy': shape_props['anisotropy_ratio'],
            'morphology': morphology,
            'curvature_summary': mean_curvature,
            'torsion_summary': mean_torsion,
            'end_to_end_distance': end_to_end,
            'bending_hotspots': bending_hotspots_str,
            'exposed_fraction': exposed_fraction,
            'charged_patch_score': charged_patch_score,
            'PAE_mean': pae_mean,
            'PAE_domain_blockiness_score': pae_blockiness,
            'low_confidence_warning': low_confidence_warning,
            'multi_domain_uncertain': multi_domain_uncertain,
            'likely_IDR_heavy': likely_IDR_heavy,
            'backbone_principal_axis': f"{shape_props['lambda_min']:.2f},{shape_props['lambda_mid']:.2f},{shape_props['lambda_max']:.2f}",
            **shape_props
        }
