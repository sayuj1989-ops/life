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

    def calculate_curvature(self, coords: np.ndarray) -> np.ndarray:
        """
        Calculates discrete curvature (kappa) for each residue (assigning to the middle of 3 points).
        Returns array of size len(coords), padded with NaNs at ends.
        Curvature = 4 * Area / (abc)
        """
        if len(coords) < 3:
            return np.full(len(coords), np.nan)

        # Vectorized calculation using 3-point sliding window
        # We need A (i-1), B (i), C (i+1)
        # Shifted arrays
        A = coords[:-2]
        B = coords[1:-1]
        C = coords[2:]

        # Edge lengths
        a = np.linalg.norm(B - C, axis=1) # Side opposite A
        b = np.linalg.norm(A - C, axis=1) # Side opposite B
        c = np.linalg.norm(A - B, axis=1) # Side opposite C

        # Heron's formula for area
        s = (a + b + c) / 2
        # Clip to avoid negative due to float errors
        arg = s * (s - a) * (s - b) * (s - c)
        arg = np.maximum(arg, 0)
        area = np.sqrt(arg)

        # R = abc / 4K
        # Kappa = 4K / abc
        denom = a * b * c
        # Avoid division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            kappa = 4 * area / denom
            kappa[denom == 0] = 0.0

        # Pad results to match original length (lost 1 at start, 1 at end)
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

        # Vectors b1, b2, b3
        b1 = coords[1:-2] - coords[:-3]
        b2 = coords[2:-1] - coords[1:-2]
        b3 = coords[3:] - coords[2:-1]

        # Normals
        n1 = np.cross(b1, b2)
        n2 = np.cross(b2, b3)

        # Normalize to get angle
        # Torsion angle formula
        # cos(phi) = (n1 . n2) / (|n1| |n2|)
        # But we need sign.
        # sign = sign( (n1 x n2) . b2 )

        n1_norm = np.linalg.norm(n1, axis=1)
        n2_norm = np.linalg.norm(n2, axis=1)

        with np.errstate(divide='ignore', invalid='ignore'):
            cos_phi = np.einsum('ij,ij->i', n1, n2) / (n1_norm * n2_norm)
            # Clip for arccos stability
            cos_phi = np.clip(cos_phi, -1.0, 1.0)
            phi = np.arccos(cos_phi)

            # Sign
            cross_n1_n2 = np.cross(n1, n2)
            sign_check = np.einsum('ij,ij->i', cross_n1_n2, b2)
            sign = np.sign(sign_check)

        torsion = phi * sign # in radians

        # Pad results (lost 1 start, 2 end? No, window 4. indices 0,1,2,3 -> torsion at 1 or 2?)
        # Let's align with the bond b2, so between residues i+1 and i+2.
        # Let's just pad to length
        result = np.full(len(coords), np.nan)
        result[1:-2] = torsion # Align somewhat to middle
        return result

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
             coords = []
             for model in structure:
                 for chain in model:
                     for residue in chain:
                         if 'CA' in residue:
                             coords.append(residue['CA'].get_coord())
             coords = np.array(coords)

        if plddt_scores is None and structure is not None:
            # Extract pLDDT scores from B-factors (AlphaFold stores pLDDT in B-factor field)
            plddt_scores = []
            for model in structure:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            plddt_scores.append(residue['CA'].get_bfactor())
            plddt_scores = np.array(plddt_scores)
        
        if plddt_scores is None:
            raise ValueError("plddt_scores are required but not provided and could not be extracted from structure")

        rg = self.calculate_rg(coords)
        shape_props = self.calculate_anisotropy(coords)

        mean_plddt = np.mean(plddt_scores) if len(plddt_scores) > 0 else 0
        fraction_low_conf = np.sum(plddt_scores < 70) / len(plddt_scores) if len(plddt_scores) > 0 else 0

        # Geometry
        kappa = self.calculate_curvature(coords)
        tau = self.calculate_torsion(coords)

        # High confidence mask (pLDDT >= 70)
        # For curvature at i, we need pLDDT at i-1, i, i+1 >= 70
        # Shifted masks
        plddt_mask = (plddt_scores >= 70)
        # We need mask[i-1] & mask[i] & mask[i+1]
        # Valid curvature indices are 1..N-2 (0-based) effectively due to implementation returning padded array
        # But `kappa` has NaNs at ends.

        # Create strict mask for curvature
        # mask_prev = mask[:-2], mask_curr = mask[1:-1], mask_next = mask[2:]
        strict_mask_kappa = np.zeros(len(coords), dtype=bool)
        if len(coords) >= 3:
             # Indices 1 to N-2
             m = plddt_mask[:-2] & plddt_mask[1:-1] & plddt_mask[2:]
             strict_mask_kappa[1:-1] = m

        kappa_valid = kappa[strict_mask_kappa & ~np.isnan(kappa)]

        # Similar for torsion (needs i-1, i, i+1, i+2 effectively, or b1, b2, b3)
        # Torsion at i corresponds to bond i->i+1 usually or the dihedral
        # My implementation pads at 1:-2.
        strict_mask_tau = np.zeros(len(coords), dtype=bool)
        if len(coords) >= 4:
             m = plddt_mask[:-3] & plddt_mask[1:-2] & plddt_mask[2:-1] & plddt_mask[3:]
             strict_mask_tau[1:-2] = m

        tau_valid = tau[strict_mask_tau & ~np.isnan(tau)]

        mean_curvature = np.mean(kappa_valid) if len(kappa_valid) > 0 else 0.0
        mean_torsion = np.mean(np.abs(tau_valid)) if len(tau_valid) > 0 else 0.0

        # End-to-end distance (high confidence)
        # Find first and last high-confidence residue? Or just max distance between any two HC residues?
        # Usually end-to-end of the whole chain, but if disordered tails, it's misleading.
        # User says "Compute these only on **high-confidence backbone segments**".
        # Let's take the longest contiguous high-confidence segment.

        # Identify segments
        is_hc = plddt_mask.astype(int)
        # Find runs of 1s
        # Prepend/append 0 to handle edges
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
            # e is exclusive
            seg_coords = coords[s:e]
            if len(seg_coords) > 1:
                end_to_end = np.linalg.norm(seg_coords[-1] - seg_coords[0])
            else:
                end_to_end = 0.0
        else:
            end_to_end = 0.0

        # Bending Hotspots: top 3 regions by local curvature (in high conf regions)
        # Find peaks in kappa (smoothed or raw?)
        # User says "top 3 regions by local curvature, with residue ranges".
        # Let's pick residues with highest kappa in strict_mask_kappa
        hotspots = []
        if len(kappa_valid) > 0:
            # We want indices.
            valid_indices = np.where(strict_mask_kappa & ~np.isnan(kappa))[0]
            valid_kappas = kappa[valid_indices]

            # Sort descending
            sorted_idx = np.argsort(valid_kappas)[::-1]

            # Pick top 3 non-overlapping?
            # Simple approach: Top 3 points.
            top_k = min(3, len(sorted_idx))
            for k in range(top_k):
                idx = valid_indices[sorted_idx[k]]
                val = valid_kappas[sorted_idx[k]]
                hotspots.append(f"{idx}:{val:.2f}")

        bending_hotspots_str = "; ".join(hotspots)

        # Exposed Surface Proxy (SASA)
        # Heuristic: Count neighbors within X angstroms. Fewer neighbors -> more exposed.
        # Simple generic approach: Neighbor count (CN).
        # Sphere 10A. High CN = buried. Low CN = exposed.
        # Exposed if CN < threshold?
        # User asked for "exposed_surface_proxy (e.g., count of residues likely solvent-exposed)".
        # Let's compute fraction of exposed residues.
        # "Exposed" if coordination number (C-alpha within 10A) < some val (say 14).
        if len(coords) > 0:
            # Distance matrix
            # Use a subset if too large, but 1000 res is fine.
            # dists = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=2)
            # CN = np.sum(dists < 10.0, axis=1) - 1 # exclude self
            # Avoid full matrix for memory? Loop is slow.
            # 20 proteins * 500 res is small.
            dists = np.sqrt(np.sum((coords[:, np.newaxis, :] - coords[np.newaxis, :, :]) ** 2, axis=2))
            cn = np.sum(dists < 10.0, axis=1) - 1
            # Heuristic threshold for "exposed" on CA-only model?
            # Say < 20 neighbors in 10A sphere (dense packing is ~30?).
            # Let's report mean coordination number as proxy?
            # Or fraction with CN < 15, restricted to high-confidence residues (pLDDT >= 70).
            n_exposed = np.sum((cn < 15) & plddt_mask)
            denom = np.sum(plddt_mask)
            exposed_fraction = n_exposed / denom if denom > 0 else 0.0
        else:
            exposed_fraction = 0.0

        # Charged Patch Score
        # "density of charged residues in high-confidence exposed regions"
        # We don't have sequence in coords/plddt call signature easily unless structure is passed.
        # `structure` is passed.
        charged_patch_score = 0.0
        if structure and len(coords) > 0:
            # Ensure cn is defined (should be from exposed_fraction calculation above)
            if 'cn' not in locals():
                # Calculate cn if not already computed
                dists = np.sqrt(np.sum((coords[:, np.newaxis, :] - coords[np.newaxis, :, :]) ** 2, axis=2))
                cn = np.sum(dists < 10.0, axis=1) - 1
            
            # Extract sequence and map to exposure
            # iterate residues
            charged_count = 0
            exposed_hc_count = 0

            # Count total number of residues with CA atoms for validation
            total_ca_residues = 0
            for model in structure:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            total_ca_residues += 1
            
            # Validate that array lengths match
            if total_ca_residues != len(plddt_scores) or total_ca_residues != len(cn):
                raise ValueError(
                    f"Mismatch between number of CA residues ({total_ca_residues}), "
                    f"plddt_scores length ({len(plddt_scores)}), and cn length ({len(cn)})"
                )

            # Re-iterate to match coords index
            # Assuming coords logic matches this iteration order
            idx = 0
            for model in structure:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            # Check confidence (with bounds check)
                            if idx < len(plddt_scores):
                                conf = plddt_scores[idx]
                                # Check exposure (with bounds check)
                                is_exposed = (cn[idx] < 15) if idx < len(cn) else False

                                if conf >= 70 and is_exposed:
                                    exposed_hc_count += 1
                                    resname = residue.get_resname().upper()
                                    # Basic/Acidic? "Charged". Asp, Glu, Lys, Arg, His.
                                    if resname in ['ASP', 'GLU', 'LYS', 'ARG', 'HIS']:
                                        charged_count += 1
                            idx += 1

            if exposed_hc_count > 0:
                charged_patch_score = charged_count / exposed_hc_count

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
            'curvature_summary': mean_curvature,
            'torsion_summary': mean_torsion,
            'end_to_end_distance': end_to_end,
            'bending_hotspots': bending_hotspots_str,
            'exposed_fraction': exposed_fraction,
            'charged_patch_score': charged_patch_score,
            **shape_props
        }
