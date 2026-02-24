import numpy as np

class MetricsAnalyzer:
    def analyze_structure(self, coords, plddt_scores, resnames, pae_matrix=None):
        """
        Computes structural metrics for a given set of coordinates.

        Args:
            coords (np.array): (N, 3) array of coordinates.
            plddt_scores (np.array): (N,) array of pLDDT scores.
            resnames (np.array): (N,) array of residue names.
            pae_matrix (np.array, optional): (N, N) PAE matrix.

        Returns:
            dict: Dictionary of computed metrics.
        """
        metrics = {}

        # Mean pLDDT
        metrics['plddt_mean'] = np.mean(plddt_scores) if plddt_scores is not None and len(plddt_scores) > 0 else 0.0

        if coords is None or len(coords) < 3:
            metrics['radius_of_gyration'] = 0.0
            metrics['anisotropy_index'] = 0.0
            metrics['morphology'] = 'Undefined'
            return metrics

        # Center coordinates
        centroid = np.mean(coords, axis=0)
        centered_coords = coords - centroid

        # Radius of Gyration
        # Rg = sqrt(mean(dist_to_centroid^2))
        sq_dists = np.sum(centered_coords**2, axis=1)
        rg = np.sqrt(np.mean(sq_dists))
        metrics['radius_of_gyration'] = rg

        # Anisotropy (Gyration Tensor)
        # Gyration Tensor S = 1/N * sum(r_i * r_i^T) (outer product)
        gyration_tensor = np.dot(centered_coords.T, centered_coords) / len(coords)
        eigenvalues = np.linalg.eigvalsh(gyration_tensor)

        # Sort eigenvalues: L1 <= L2 <= L3
        eigenvalues = np.sort(eigenvalues)
        l1, l2, l3 = eigenvalues

        # Anisotropy as Aspect Ratio: Longest axis / Shortest axis
        # Eigenvalues represent variance (length^2).
        # Anisotropy = sqrt(L3 / L1)

        if l1 > 1e-6:
             anisotropy = np.sqrt(l3 / l1)
        else:
             anisotropy = 100.0 # Cap for high linearity to avoid Inf

        metrics['anisotropy_index'] = anisotropy

        # Morphology
        # Threshold: > 3.0 is considered "Fibrous" / "Anisotropic" in this context
        if anisotropy > 3.0:
            metrics['morphology'] = 'Fibrous'
        else:
            metrics['morphology'] = 'Globular'

        return metrics
