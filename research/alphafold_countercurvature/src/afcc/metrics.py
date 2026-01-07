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

    def calculate_pae_metrics(self, pae_matrix: np.ndarray, plddt_scores: np.ndarray) -> Dict[str, float]:
        """
        Calculates PAE-based metrics: mean PAE and domain blockiness.
        """
        if pae_matrix is None or pae_matrix.size == 0:
            return {'pae_mean': 0.0, 'pae_blockiness': 0.0}

        pae_mean = np.mean(pae_matrix)

        # Domain blockiness
        # heuristic: blocks defined by pLDDT >= 70
        # If we have distinct high-conf blocks
        mask_hc = (plddt_scores >= 70).astype(int)
        # Find segments
        bounded = np.hstack(([0], mask_hc, [0]))
        d = np.diff(bounded)
        starts = np.where(d == 1)[0]
        ends = np.where(d == -1)[0]

        segments = list(zip(starts, ends))
        # Filter short segments (< 10 residues)
        segments = [s for s in segments if (s[1] - s[0]) >= 10]

        if len(segments) < 2:
            return {'pae_mean': float(pae_mean), 'pae_blockiness': 0.0}

        intra_scores = []
        inter_scores = []

        for i, (s1, e1) in enumerate(segments):
            # Intra
            # Check bounds
            if s1 >= pae_matrix.shape[0] or e1 > pae_matrix.shape[0]: continue

            block = pae_matrix[s1:e1, s1:e1]
            if block.size > 0:
                intra_scores.append(np.mean(block))

            # Inter
            for j, (s2, e2) in enumerate(segments):
                if i != j:
                    if s2 >= pae_matrix.shape[0] or e2 > pae_matrix.shape[0]: continue
                    block_inter = pae_matrix[s1:e1, s2:e2]
                    if block_inter.size > 0:
                        inter_scores.append(np.mean(block_inter))

        mean_intra = np.mean(intra_scores) if intra_scores else 1.0
        mean_inter = np.mean(inter_scores) if inter_scores else 1.0

        # Avoid div by zero
        if mean_intra < 1e-3: mean_intra = 1e-3

        # Blockiness: contrast. High if inter > intra (meaning low error within, high error between)
        # But PAE is error (lower is better).
        # So we want LOW intra PAE and HIGH inter PAE.
        # Ratio: mean_inter / mean_intra.
        # If domains are well defined: inter is high (uncertain), intra is low (certain). Ratio >> 1.
        blockiness = mean_inter / mean_intra
        return {'pae_mean': float(pae_mean), 'pae_blockiness': float(blockiness)}

    def analyze_structure(self, structure: Structure = None, plddt_scores: np.ndarray = None, coords: np.ndarray = None, resnames: np.ndarray = None, pae_matrix: np.ndarray = None) -> Dict[str, Any]:
        """
        Runs all metrics on a structure.

        Args:
            structure: Bio.PDB Structure object (deprecated, used if coords/plddt not provided)
            plddt_scores: Pre-extracted pLDDT scores
            coords: Pre-extracted CA coordinates
            resnames: Pre-extracted residue names (optional, enables fast path)
            pae_matrix: Optional PAE matrix (N, N)
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
             pass

        rg = self.calculate_rg(coords)
        shape_props = self.calculate_anisotropy(coords)

        mean_plddt = np.mean(plddt_scores) if len(plddt_scores) > 0 else 0
        fraction_low_conf = np.sum(plddt_scores < 70) / len(plddt_scores) if len(plddt_scores) > 0 else 0
        disorder_fraction = np.sum(plddt_scores < 50) / len(plddt_scores) if len(plddt_scores) > 0 else 0

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
            # Optimize: Use KDTree for O(N log N) neighbor search instead of O(N^2) distance matrix.
            # Significant speedup for N > 500.
            from scipy.spatial import cKDTree
            tree = cKDTree(coords)
            # query_ball_point returns number of neighbors within radius.
            # return_length=True returns counts directly, faster than returning indices.
            # We subtract 1 because query includes the point itself.
            cn = tree.query_ball_point(coords, 10.0, return_length=True) - 1

            # Heuristic threshold for "exposed" on CA-only model?
            # Say < 20 neighbors in 10A sphere (dense packing is ~30?).
            # Let's report mean coordination number as proxy?
            # Or fraction with CN < 15.
            n_exposed = np.sum(cn < 15)
            exposed_fraction = n_exposed / len(coords)
        else:
            exposed_fraction = 0.0

        # Charged Patch Score
        # "density of charged residues in high-confidence exposed regions"
        charged_patch_score = 0.0

        if resnames is not None and len(resnames) == len(plddt_scores):
             # Vectorized path
             charged_residues = ['ASP', 'GLU', 'LYS', 'ARG', 'HIS']
             is_charged = np.isin(resnames, charged_residues)

             # Align with cn which is computed on coords
             # Assuming len(coords) == len(plddt_scores) == len(resnames)
             min_len = min(len(coords), len(plddt_scores), len(resnames))

             if min_len > 0:
                 # Masks
                 mask_hc = (plddt_scores[:min_len] >= 70)
                 mask_exposed = (cn[:min_len] < 15)
                 mask_target = mask_hc & mask_exposed

                 exposed_hc_count = np.sum(mask_target)
                 if exposed_hc_count > 0:
                     charged_count = np.sum(is_charged[:min_len] & mask_target)
                     charged_patch_score = float(charged_count / exposed_hc_count)

        elif structure:
            # Slow legacy path
            # Extract sequence and map to exposure
            # iterate residues
            charged_count = 0
            exposed_hc_count = 0

            # Re-iterate to match coords index
            # Assuming coords logic matches this iteration order
            idx = 0
            for model in structure:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            # Check confidence
                            if idx < len(plddt_scores):
                                conf = plddt_scores[idx]
                                # Check exposure
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

        # PAE Metrics
        pae_metrics = self.calculate_pae_metrics(pae_matrix, plddt_scores)

        # Hinge candidates: positions where pLDDT drops (< 70) AND curvature is high
        # High curvature defined as > mean + 1 std (of valid kappa)
        hinge_candidates = 0
        if len(kappa_valid) > 0:
            k_mean = np.mean(kappa_valid)
            k_std = np.std(kappa_valid)
            thresh = k_mean + k_std

            # Use original kappa array but check mask
            # Indices where pLDDT < 70 AND kappa > thresh
            # strict_mask_kappa is where pLDDT >= 70.
            # We want pLDDT < 70.
            # But kappa needs neighbors. If pLDDT is low, kappa might be garbage?
            # User: "hinge_candidates (positions where confidence drops + geometry bends)"
            # This implies the bend is real but confidence is lower (flexible).
            # Let's check kappa where pLDDT is < 70 but > 50 (to avoid total garbage)?
            # Or just pLDDT < 70.

            # We need kappa calculated at i.
            # Check pLDDT[i] < 70.
            mask_hinge = (plddt_scores < 70) & (plddt_scores >= 50)
            # Align with kappa padding (1:-1)
            # We can only check 1:-1
            if len(kappa) > 2:
                 k_vals = kappa[1:-1]
                 m_vals = mask_hinge[1:-1]
                 hinges = (k_vals > thresh) & m_vals & (~np.isnan(k_vals))
                 hinge_candidates = np.sum(hinges)

        # Flags
        low_confidence_warning = (mean_plddt < 70) or (fraction_low_conf > 0.5)
        multi_domain_uncertain = (pae_metrics['pae_blockiness'] > 1.5) and (pae_metrics['pae_mean'] > 10) # Heuristic
        likely_idr_heavy = (disorder_fraction > 0.3)

        morphology = self.classify_morphology(shape_props['anisotropy_ratio'], rg, n_res)

        return {
            'n_residues': n_res,
            'mean_plddt': mean_plddt,
            'fraction_low_plddt': fraction_low_conf,
            'disorder_fraction': disorder_fraction,
            'radius_of_gyration': rg,
            'anisotropy': shape_props['anisotropy_ratio'],
            'morphology': morphology,
            'curvature_summary': mean_curvature,
            'torsion_summary': mean_torsion,
            'end_to_end_distance': end_to_end,
            'bending_hotspots': bending_hotspots_str,
            'hinge_candidates': int(hinge_candidates),
            'exposed_fraction': exposed_fraction,
            'charged_patch_score': charged_patch_score,
            'low_confidence_warning': low_confidence_warning,
            'multi_domain_uncertain': multi_domain_uncertain,
            'likely_idr_heavy': likely_idr_heavy,
            **pae_metrics,
            **shape_props
        }
