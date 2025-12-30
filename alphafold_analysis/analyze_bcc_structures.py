"""
Enhanced AlphaFold Structure Analysis for BCC Research
Extracts mechanical properties, geometry, and information metrics
"""

import argparse
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from Bio.PDB import PDBParser, PPBuilder
from Bio.SeqUtils import ProtParam
import matplotlib.pyplot as plt
import json
from scipy.spatial.distance import pdist
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

# Import protein database
from bcc_protein_database import BCC_PROTEINS

def calculate_sequence_entropy(sequence: str) -> float:
    """Calculate Shannon entropy of amino acid composition (sequence heterogeneity)."""
    aa_counts = {}
    for aa in sequence:
        aa_counts[aa] = aa_counts.get(aa, 0) + 1
    
    total = len(sequence)
    if total == 0:
        return 0.0
    
    entropy = 0.0
    for count in aa_counts.values():
        p = count / total
        if p > 0:
            entropy -= p * np.log2(p)
    
    return entropy

def calculate_backbone_curvature(
    coords: np.ndarray,
    window: int = 7,
    mask: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, float, float]:
    """
    Calculate local backbone curvature using sliding window
    Returns: (curvatures array, mean curvature, std curvature)
    """
    if len(coords) < 2 * window + 1:
        return np.array([]), 0.0, 0.0
    
    if mask is None:
        mask = np.ones(len(coords), dtype=bool)
    else:
        mask = np.asarray(mask, dtype=bool)
        if len(mask) != len(coords):
            raise ValueError("Mask length must match coordinates length")

    curvatures = []
    
    for i in range(window, len(coords) - window):
        if not mask[i - window:i + window + 1].all():
            continue
        # Get window of coordinates
        window_coords = coords[i-window:i+window+1]
        
        # Calculate curvature as inverse of radius of fitted circle
        # Simplified: use variance of distances from centroid
        centroid = np.mean(window_coords, axis=0)
        distances = np.linalg.norm(window_coords - centroid, axis=1)
        mean_dist = np.mean(distances)
        
        if mean_dist > 1e-6:
            curvature = 1.0 / mean_dist
        else:
            curvature = 0.0
        
        curvatures.append(curvature)
    
    curvatures = np.array(curvatures)
    if len(curvatures) == 0:
        return curvatures, 0.0, 0.0
    return curvatures, np.mean(curvatures), np.std(curvatures)

def calculate_flexibility(coords: np.ndarray) -> Dict[str, float]:
    """
    Calculate protein flexibility metrics
    Returns: dict with flexibility measures
    """
    if len(coords) < 3:
        return {"mean_bend": 0.0, "max_bend": 0.0, "flexibility_index": 0.0}
    
    # Calculate angles between consecutive segments
    vectors = np.diff(coords, axis=0)
    norms = np.linalg.norm(vectors, axis=1)
    norms[norms == 0] = 1e-6  # Avoid division by zero
    
    normalized_vectors = vectors / norms[:, np.newaxis]
    
    # Calculate bend angles
    bend_angles = []
    for i in range(len(normalized_vectors) - 1):
        dot_product = np.clip(np.dot(normalized_vectors[i], normalized_vectors[i+1]), -1, 1)
        angle = np.arccos(dot_product)
        bend_angles.append(angle)
    
    bend_angles = np.array(bend_angles)
    
    return {
        "mean_bend": np.mean(bend_angles),
        "max_bend": np.max(bend_angles) if len(bend_angles) > 0 else 0.0,
        "flexibility_index": np.std(bend_angles) / (np.mean(bend_angles) + 1e-6),
    }

def calculate_compactness(coords: np.ndarray) -> Dict[str, float]:
    """
    Calculate protein compactness metrics
    """
    if len(coords) < 2:
        return {"radius_of_gyration": 0.0, "end_to_end": 0.0, "compactness": 0.0}
    
    # Radius of gyration
    centroid = np.mean(coords, axis=0)
    distances_from_centroid = np.linalg.norm(coords - centroid, axis=1)
    radius_of_gyration = np.sqrt(np.mean(distances_from_centroid**2))
    
    # End-to-end distance
    end_to_end = np.linalg.norm(coords[-1] - coords[0])
    
    # Compactness (inverse of normalized radius of gyration)
    if end_to_end > 0:
        compactness = 1.0 / (radius_of_gyration / end_to_end + 1e-6)
    else:
        compactness = 0.0
    
    return {
        "radius_of_gyration": radius_of_gyration,
        "end_to_end": end_to_end,
        "compactness": compactness,
    }

def calculate_mechanical_properties(sequence: str, coords: np.ndarray) -> Dict[str, float]:
    """
    Estimate mechanical properties from sequence and structure
    """
    try:
        analyzed_seq = ProtParam.ProteinAnalysis(sequence)
        
        # Amino acid composition
        aa_composition = analyzed_seq.get_amino_acids_percent()
        
        # Estimate stiffness from proline and glycine content
        # Proline: rigid, Glycine: flexible
        proline_content = aa_composition.get('P', 0) / 100.0
        glycine_content = aa_composition.get('G', 0) / 100.0
        
        # Estimated bending stiffness (higher proline = stiffer)
        estimated_stiffness = proline_content / (glycine_content + 0.1)
        
        # Instability index
        instability = analyzed_seq.instability_index()
        
        # Hydrophobicity (GRAVY)
        gravy = analyzed_seq.gravy()
        
        return {
            "estimated_stiffness": estimated_stiffness,
            "instability_index": instability,
            "gravy": gravy,
            "proline_content": proline_content,
            "glycine_content": glycine_content,
        }
    except:
        return {
            "estimated_stiffness": 0.0,
            "instability_index": 0.0,
            "gravy": 0.0,
            "proline_content": 0.0,
            "glycine_content": 0.0,
        }

def calculate_plddt_stats(plddt_values: np.ndarray, threshold: float) -> Dict[str, float]:
    """Compute pLDDT summary statistics."""
    if len(plddt_values) == 0:
        return {
            "plddt_mean": 0.0,
            "plddt_std": 0.0,
            "plddt_fraction_ge_threshold": 0.0,
        }
    plddt_mean = float(np.mean(plddt_values))
    plddt_std = float(np.std(plddt_values))
    plddt_fraction = float(np.mean(plddt_values >= threshold))
    return {
        "plddt_mean": plddt_mean,
        "plddt_std": plddt_std,
        "plddt_fraction_ge_threshold": plddt_fraction,
    }

def residualize(values: np.ndarray, covariates: np.ndarray) -> np.ndarray:
    """Regress values on covariates and return residuals."""
    covariates = np.asarray(covariates)
    if covariates.ndim == 1:
        covariates = covariates.reshape(-1, 1)
    X = np.column_stack([np.ones(len(values)), covariates])
    beta, *_ = np.linalg.lstsq(X, values, rcond=None)
    return values - X @ beta

def safe_pearsonr(x: np.ndarray, y: np.ndarray) -> Tuple[Optional[float], Optional[float]]:
    """Return Pearson r and p-value if possible, else (None, None)."""
    if len(x) < 3 or len(y) < 3:
        return None, None
    if np.std(x) == 0 or np.std(y) == 0:
        return None, None
    return pearsonr(x, y)

def partial_corr(x: np.ndarray, y: np.ndarray, covariates: np.ndarray) -> Tuple[Optional[float], Optional[float]]:
    """Partial correlation between x and y, controlling for covariates."""
    x_res = residualize(x, covariates)
    y_res = residualize(y, covariates)
    return safe_pearsonr(x_res, y_res)

def extract_ca_coords_and_plddt(structure) -> Tuple[np.ndarray, np.ndarray]:
    """Extract CA coordinates and pLDDT values (from B-factor)."""
    ca_coords = []
    plddt_values = []
    for model in structure:
        for chain in model:
            for residue in chain:
                if 'CA' in residue:
                    atom = residue['CA']
                    ca_coords.append(atom.get_coord())
                    plddt_values.append(atom.get_bfactor())
    return np.array(ca_coords), np.array(plddt_values)

def make_json_safe(value):
    """Recursively convert numpy types to built-in Python types for JSON."""
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {k: make_json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [make_json_safe(v) for v in value]
    return value

def analyze_structure(pdb_file: Path, plddt_threshold: float = 70.0) -> Optional[Dict]:
    """Comprehensive analysis of a single protein structure"""
    try:
        # Check if file is valid PDB (not an error response)
        with open(pdb_file, 'r') as f:
            first_line = f.readline()
            if first_line.startswith('<?xml') or first_line.startswith('<Error'):
                print(f"   ⚠️  {pdb_file.name} is an error response, not a valid PDB")
                return None
            # Check file size (too small likely invalid)
            f.seek(0)
            content = f.read(1000)
            if len(content) < 100:  # Very small files are likely errors
                print(f"   ⚠️  {pdb_file.name} is too small, likely invalid")
                return None
            # Scan for ATOM/HETATM records to validate PDB content
            f.seek(0)
            has_atom = False
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                if "ATOM" in chunk or "HETATM" in chunk:
                    has_atom = True
                    break
            if not has_atom:
                print(f"   ⚠️  {pdb_file.name} missing ATOM/HETATM records, likely invalid")
                return None
        
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure('protein', pdb_file)
        
        # Extract sequence
        ppb = PPBuilder()
        sequence = ""
        for pp in ppb.build_peptides(structure):
            sequence += str(pp.get_sequence())
        
        if len(sequence) == 0:
            return None
        
        # Extract CA coordinates (backbone) and pLDDT values
        ca_coords, plddt_values = extract_ca_coords_and_plddt(structure)

        if len(ca_coords) < 10:
            return None

        plddt_stats = calculate_plddt_stats(plddt_values, plddt_threshold)
        
        # Calculate all metrics
        seq_entropy = calculate_sequence_entropy(sequence)
        curvatures, mean_curvature, std_curvature = calculate_backbone_curvature(ca_coords)
        plddt_mask = plddt_values >= plddt_threshold
        curvatures_plddt, mean_curvature_plddt, std_curvature_plddt = calculate_backbone_curvature(
            ca_coords,
            mask=plddt_mask,
        )
        flexibility = calculate_flexibility(ca_coords)
        compactness = calculate_compactness(ca_coords)
        mechanical = calculate_mechanical_properties(sequence, ca_coords)
        
        return {
            "name": pdb_file.stem,
            "sequence": sequence,
            "length": len(sequence),
            "seq_entropy": seq_entropy,
            "mean_curvature": mean_curvature,
            "std_curvature": std_curvature,
            "curvatures": curvatures.tolist() if len(curvatures) > 0 else [],
            "mean_curvature_plddt": mean_curvature_plddt,
            "std_curvature_plddt": std_curvature_plddt,
            "curvatures_plddt": curvatures_plddt.tolist() if len(curvatures_plddt) > 0 else [],
            "curvature_count": len(curvatures),
            "curvature_plddt_count": len(curvatures_plddt),
            **plddt_stats,
            **flexibility,
            **compactness,
            **mechanical,
            "ca_coords": ca_coords.tolist(),  # For visualization
        }
    except Exception as e:
        print(f"   ⚠️  Error analyzing {pdb_file.name}: {e}")
        return None

def generate_comprehensive_report(
    results: List[Dict],
    output_file: Path,
    category_info: Dict = None,
    plddt_threshold: float = 70.0,
):
    """Generate comprehensive analysis report"""
    
    with open(output_file, 'w') as f:
        f.write("# AlphaFold Structure Analysis for BCC Research\n\n")
        f.write("## Comprehensive Protein Structure-Geometry Analysis\n\n")
        
        # Summary statistics
        if len(results) > 0:
            f.write("### Summary Statistics\n\n")
            f.write(f"- **Total proteins analyzed**: {len(results)}\n")
            f.write(f"- **Mean sequence length**: {np.mean([r['length'] for r in results]):.1f} aa\n")
            f.write(f"- **Mean entropy**: {np.mean([r['seq_entropy'] for r in results]):.3f} bits\n")
            f.write(f"- **Mean curvature**: {np.mean([r['mean_curvature'] for r in results]):.4f}\n")
            f.write(f"- **Mean pLDDT (CA)**: {np.mean([r['plddt_mean'] for r in results]):.2f}\n")
            f.write(f"- **Mean curvature (pLDDT >= {plddt_threshold:.0f})**: "
                    f"{np.mean([r['mean_curvature_plddt'] for r in results]):.4f}\n\n")
        
        # Detailed table
        f.write("### Detailed Analysis\n\n")
        f.write(f"| Protein | Length | Entropy | Mean Curv | Mean Curv (pLDDT>={plddt_threshold:.0f}) | "
                f"Mean pLDDT | Frac pLDDT>={plddt_threshold:.0f} | Flex Index | Rg | Stiffness | Instability |\n")
        f.write("|---------|--------|---------|-----------|-----------------------|------------|----------------|------------|----|-----------|------------|\n")
        
        for r in results:
            f.write(f"| {r['name']} | {r['length']} | {r['seq_entropy']:.3f} | "
                   f"{r['mean_curvature']:.4f} | {r['mean_curvature_plddt']:.4f} | "
                   f"{r['plddt_mean']:.2f} | {r['plddt_fraction_ge_threshold']:.2f} | "
                   f"{r['flexibility_index']:.3f} | {r['radius_of_gyration']:.2f} | "
                   f"{r['estimated_stiffness']:.3f} | {r['instability_index']:.2f} |\n")
        
        f.write("\n### Key Findings\n\n")
        
        # Calculate correlations
        if len(results) > 2:
            entropies = np.array([r['seq_entropy'] for r in results])
            curvatures = np.array([r['mean_curvature'] for r in results])
            lengths = np.array([r['length'] for r in results])
            plddt_means = np.array([r['plddt_mean'] for r in results])
            flex_indices = np.array([r['flexibility_index'] for r in results])
            stiffnesses = np.array([r['estimated_stiffness'] for r in results])
            filtered_results = [r for r in results if r['curvature_plddt_count'] > 0]
            
            # Entropy-Curvature correlation (all residues)
            corr_ent_curv, p_val = safe_pearsonr(entropies, curvatures)
            if corr_ent_curv is not None:
                f.write(f"**Entropy-Curvature Correlation (all residues)**: "
                        f"{corr_ent_curv:.3f} (p={p_val:.4f}, N={len(entropies)})\n")
            else:
                f.write("**Entropy-Curvature Correlation (all residues)**: insufficient variance\n")

            # Entropy-Curvature correlation (pLDDT filtered)
            if filtered_results:
                entropies_f = np.array([r['seq_entropy'] for r in filtered_results])
                curvatures_f = np.array([r['mean_curvature_plddt'] for r in filtered_results])
                lengths_f = np.array([r['length'] for r in filtered_results])
                plddt_means_f = np.array([r['plddt_mean'] for r in filtered_results])

                corr_ent_curv_f, p_val_f = safe_pearsonr(entropies_f, curvatures_f)
                if corr_ent_curv_f is not None:
                    f.write(f"**Entropy-Curvature Correlation (pLDDT >= {plddt_threshold:.0f})**: "
                            f"{corr_ent_curv_f:.3f} (p={p_val_f:.4f}, N={len(entropies_f)})\n")
                else:
                    f.write(f"**Entropy-Curvature Correlation (pLDDT >= {plddt_threshold:.0f})**: insufficient variance\n")

                # Partial correlations
                corr_partial_len, p_partial_len = partial_corr(entropies, curvatures, lengths)
                if corr_partial_len is not None:
                    f.write(f"**Partial Correlation (length-adjusted, all residues)**: "
                            f"{corr_partial_len:.3f} (p={p_partial_len:.4f}, N={len(entropies)})\n")
                else:
                    f.write("**Partial Correlation (length-adjusted, all residues)**: insufficient variance\n")

                corr_partial_len_plddt, p_partial_len_plddt = partial_corr(
                    entropies_f,
                    curvatures_f,
                    np.column_stack([lengths_f, plddt_means_f]),
                )
                if corr_partial_len_plddt is not None:
                    f.write(f"**Partial Correlation (length + mean pLDDT, filtered)**: "
                            f"{corr_partial_len_plddt:.3f} (p={p_partial_len_plddt:.4f}, N={len(entropies_f)})\n\n")
                else:
                    f.write("**Partial Correlation (length + mean pLDDT, filtered)**: insufficient variance\n\n")
            else:
                f.write(f"**Entropy-Curvature Correlation (pLDDT >= {plddt_threshold:.0f})**: no valid windows\n")
                f.write("**Partial Correlation (length-adjusted, all residues)**: not computed\n")
                f.write("**Partial Correlation (length + mean pLDDT, filtered)**: not computed\n\n")

            if corr_ent_curv is not None and abs(corr_ent_curv) > 0.5:
                f.write("✅ Strong correlation detected between sequence information content "
                        "and structural curvature, supporting the information-geometry framework.\n\n")
            
            # Stiffness-Flexibility correlation
            corr_stiff_flex, p_val = safe_pearsonr(stiffnesses, flex_indices)
            if corr_stiff_flex is not None:
                f.write(f"**Stiffness-Flexibility Correlation**: {corr_stiff_flex:.3f} (p={p_val:.4f})\n\n")
        
        # Category-specific analysis
        if category_info:
            f.write("\n### Category-Specific Analysis\n\n")
            for category, proteins in category_info.items():
                if isinstance(proteins, dict):
                    protein_names = set(proteins.keys())
                else:
                    protein_names = set([p['name'] for p in proteins])
                category_results = [r for r in results if r['name'] in protein_names]
                if category_results:
                    filtered_category = [r for r in category_results if r['curvature_plddt_count'] > 0]
                    f.write(f"**{category}** ({len(category_results)} proteins):\n")
                    f.write(f"- Mean entropy: {np.mean([r['seq_entropy'] for r in category_results]):.3f}\n")
                    f.write(f"- Mean curvature: {np.mean([r['mean_curvature'] for r in category_results]):.4f}\n")
                    f.write(f"- Mean curvature (pLDDT >= {plddt_threshold:.0f}): "
                            f"{np.mean([r['mean_curvature_plddt'] for r in category_results]):.4f}\n")
                    f.write(f"- Mean pLDDT: {np.mean([r['plddt_mean'] for r in category_results]):.2f}\n")
                    f.write(f"- Mean flexibility: {np.mean([r['flexibility_index'] for r in category_results]):.3f}\n\n")
                    if len(category_results) >= 3:
                        cat_ent = np.array([r['seq_entropy'] for r in category_results])
                        cat_curv = np.array([r['mean_curvature'] for r in category_results])
                        cat_corr, cat_p = safe_pearsonr(cat_ent, cat_curv)
                        if cat_corr is not None:
                            f.write(f"- Entropy-curvature correlation: {cat_corr:.3f} (p={cat_p:.4f})\n")
                    if len(filtered_category) >= 3:
                        cat_ent_f = np.array([r['seq_entropy'] for r in filtered_category])
                        cat_curv_f = np.array([r['mean_curvature_plddt'] for r in filtered_category])
                        cat_corr_f, cat_p_f = safe_pearsonr(cat_ent_f, cat_curv_f)
                        if cat_corr_f is not None:
                            f.write(f"- Entropy-curvature correlation (pLDDT >= {plddt_threshold:.0f}): "
                                    f"{cat_corr_f:.3f} (p={cat_p_f:.4f})\n")
                    f.write(f"\n")
        
        f.write("\n### Interpretation\n\n")
        f.write("This analysis examines how sequence heterogeneity (composition entropy) manifests as ")
        f.write("geometric properties (backbone curvature, flexibility) in protein structures. ")
        f.write("A modest raw entropy-curvature correlation is observed, but the signal weakens ")
        f.write("under pLDDT filtering and length/confidence controls, so the molecular evidence ")
        f.write("should be treated as preliminary. Expanded coverage and higher-confidence segments ")
        f.write("are needed to assess whether mechanosensitive proteins show stronger coupling.\n")

def plot_correlations(results: List[Dict], output_dir: Path, plddt_threshold: float = 70.0):
    """Generate correlation plots"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if len(results) < 3:
        print("   ⚠️  Not enough data for correlation plots")
        return
    
    entropies = [r['seq_entropy'] for r in results]
    curvatures = [r['mean_curvature'] for r in results]
    names = [r['name'] for r in results]
    
    # Entropy vs Curvature
    plt.figure(figsize=(10, 6))
    plt.scatter(entropies, curvatures, s=100, alpha=0.6)
    
    for i, name in enumerate(names):
        plt.annotate(name, (entropies[i], curvatures[i]), 
                    fontsize=8, alpha=0.7)
    
    if len(set(entropies)) > 1 and len(set(curvatures)) > 1:
        z = np.polyfit(entropies, curvatures, 1)
        p = np.poly1d(z)
        plt.plot(entropies, p(entropies), "r--", alpha=0.5, label=f"Fit (r={pearsonr(entropies, curvatures)[0]:.3f})")
        plt.legend()
    
    plt.xlabel('Sequence Entropy (bits)', fontsize=12)
    plt.ylabel('Mean Backbone Curvature', fontsize=12)
    plt.title('Information-Geometry Correlation in BCC Proteins', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    output_file = output_dir / 'entropy_curvature_correlation.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   📊 Saved: {output_file}")

    # Entropy vs Curvature (pLDDT filtered)
    filtered_results = [r for r in results if r['curvature_plddt_count'] > 0]
    if len(filtered_results) < 3:
        print("   ⚠️  Not enough filtered data for pLDDT correlation plot")
        return

    entropies_f = [r['seq_entropy'] for r in filtered_results]
    curvatures_f = [r['mean_curvature_plddt'] for r in filtered_results]
    names_f = [r['name'] for r in filtered_results]

    plt.figure(figsize=(10, 6))
    plt.scatter(entropies_f, curvatures_f, s=100, alpha=0.6)

    for i, name in enumerate(names_f):
        plt.annotate(name, (entropies_f[i], curvatures_f[i]),
                    fontsize=8, alpha=0.7)

    if len(set(entropies_f)) > 1 and len(set(curvatures_f)) > 1:
        z = np.polyfit(entropies_f, curvatures_f, 1)
        p = np.poly1d(z)
        corr_val, _ = pearsonr(entropies_f, curvatures_f)
        plt.plot(entropies_f, p(entropies_f), "r--", alpha=0.5,
                 label=f"Fit (r={corr_val:.3f})")
        plt.legend()

    plt.xlabel('Sequence Entropy (bits)', fontsize=12)
    plt.ylabel(f'Mean Backbone Curvature (pLDDT >= {plddt_threshold:.0f})', fontsize=12)
    plt.title(f'Information-Geometry Correlation (pLDDT >= {plddt_threshold:.0f})', fontsize=14)
    plt.grid(True, alpha=0.3)

    output_file = output_dir / f'entropy_curvature_correlation_plddt{int(plddt_threshold)}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   📊 Saved: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive AlphaFold structure analysis for BCC research"
    )
    parser.add_argument(
        "--pdb-dir",
        default="alphafold_analysis/predictions",
        help="Directory containing PDB files"
    )
    parser.add_argument(
        "--output",
        default="alphafold_analysis/bcc_analysis_report.md",
        help="Output report file"
    )
    parser.add_argument(
        "--json-output",
        default="alphafold_analysis/bcc_analysis_data.json",
        help="Output JSON data file"
    )
    parser.add_argument(
        "--plddt-threshold",
        type=float,
        default=70.0,
        help="Minimum pLDDT threshold for filtered curvature metrics"
    )
    
    args = parser.parse_args()
    
    pdb_dir = Path(args.pdb_dir)
    output_file = Path(args.output)
    json_output = Path(args.json_output)
    
    print("🔬 Comprehensive AlphaFold Structure Analysis for BCC Research")
    print("=" * 70)
    
    if not pdb_dir.exists():
        print(f"❌ PDB directory not found: {pdb_dir}")
        print(f"💡 Run: python alphafold_analysis/fetch_bcc_structures.py")
        return
    
    pdb_files = list(pdb_dir.glob("*.pdb"))
    if not pdb_files:
        print(f"❌ No PDB files found in {pdb_dir}")
        return
    
    print(f"📊 Found {len(pdb_files)} PDB files\n")
    
    results = []
    for pdb_file in pdb_files:
        print(f"Analyzing {pdb_file.name}...", end=" ")
        result = analyze_structure(pdb_file, plddt_threshold=args.plddt_threshold)
        if result:
            results.append(result)
            print(f"✅ (L={result['length']}, H={result['seq_entropy']:.2f}, κ={result['mean_curvature']:.4f})")
        else:
            print("❌")
    
    if results:
        print(f"\n📝 Generating report...")
        generate_comprehensive_report(
            results,
            output_file,
            category_info=BCC_PROTEINS,
            plddt_threshold=args.plddt_threshold,
        )
        print(f"✅ Report saved: {output_file}")
        
        # Save JSON data
        json_output.parent.mkdir(parents=True, exist_ok=True)
        with open(json_output, 'w') as f:
            json.dump(make_json_safe(results), f, indent=2)
        print(f"✅ Data saved: {json_output}")
        
        print(f"\n📊 Generating plots...")
        plot_correlations(results, pdb_dir.parent / 'figures', plddt_threshold=args.plddt_threshold)
        
        print(f"\n✅ Analysis complete! Analyzed {len(results)} structures")
    else:
        print("❌ No structures analyzed successfully")

if __name__ == "__main__":
    main()
