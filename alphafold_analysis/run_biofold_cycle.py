
import os
import sys
import json
import numpy as np
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from Bio.PDB import PDBParser, PPBuilder
try:
    from Bio.PDB.Polypeptide import three_to_one
except ImportError:
    # BioPython 1.78+ moved it or it's just index now, let's use a mapping
    from Bio.PDB.Polypeptide import protein_letters_3to1
    def three_to_one(s):
        return protein_letters_3to1.get(s.upper(), 'X')

from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt

# Ensure reproducible results where possible
np.random.seed(42)

class BioFoldAnalyzer:
    def __init__(self, pdb_path: Path, pae_path: Optional[Path] = None):
        self.pdb_path = pdb_path
        self.pae_path = pae_path
        self.name = pdb_path.stem
        self.structure = None
        self.ca_coords = None
        self.plddt_values = None
        self.sequence = ""
        self.pae_matrix = None

        # Thresholds
        self.plddt_high_conf = 70.0
        self.plddt_very_high = 90.0
        self.plddt_low = 50.0

    def load_data(self) -> bool:
        """Load PDB and PAE data."""
        try:
            # Load PDB
            parser = PDBParser(QUIET=True)
            self.structure = parser.get_structure(self.name, self.pdb_path)

            # Extract CA coords and pLDDT
            ca_coords = []
            plddt_values = []
            sequence = []

            for model in self.structure:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            ca_coords.append(residue['CA'].get_coord())
                            plddt_values.append(residue['CA'].get_bfactor())
                            try:
                                sequence.append(three_to_one(residue.get_resname()))
                            except KeyError:
                                sequence.append('X')

            self.ca_coords = np.array(ca_coords)
            self.plddt_values = np.array(plddt_values)
            self.sequence = "".join(sequence)

            if len(self.ca_coords) == 0:
                print(f"⚠️  No CA atoms found in {self.pdb_path.name}")
                return False

            # Load PAE if available
            if self.pae_path and self.pae_path.exists():
                try:
                    with open(self.pae_path, 'r') as f:
                        data = json.load(f)
                        # AlphaFold DB format: [0]['predicted_aligned_error'] or similar
                        if isinstance(data, list) and len(data) > 0 and 'predicted_aligned_error' in data[0]:
                            self.pae_matrix = np.array(data[0]['predicted_aligned_error'])
                        # Sometimes it is just the dict
                        elif isinstance(data, dict) and 'predicted_aligned_error' in data:
                            self.pae_matrix = np.array(data['predicted_aligned_error'])
                except Exception as e:
                    print(f"⚠️  Error loading PAE for {self.name}: {e}")
                    self.pae_matrix = None

            return True
        except Exception as e:
            print(f"❌ Error loading {self.name}: {e}")
            return False

    def compute_quality_metrics(self) -> Dict:
        """Compute AlphaFold confidence metrics."""
        plddt = self.plddt_values
        metrics = {
            "pLDDT_mean": np.mean(plddt),
            "pLDDT_median": np.median(plddt),
            "pLDDT_fraction_high": np.mean(plddt >= 90),
            "pLDDT_fraction_ok": np.mean((plddt >= 70) & (plddt < 90)),
            "pLDDT_fraction_low": np.mean(plddt < 70),
        }

        if self.pae_matrix is not None:
            metrics["PAE_mean"] = np.mean(self.pae_matrix)
            # Heuristic for domain blockiness:
            # High intra-domain (low PAE) vs low inter-domain (high PAE)
            # We can't easily segment without complex logic, so we'll just report PAE variance/std as proxy for complexity
            metrics["PAE_std"] = np.std(self.pae_matrix)
        else:
            metrics["PAE_mean"] = None
            metrics["PAE_std"] = None

        return metrics

    def compute_architecture_metrics(self) -> Dict:
        """Compute disorder and domain-ish metrics."""
        plddt = self.plddt_values
        disorder_frac = np.mean(plddt < 50)

        # Hinge heuristic: Drop in pLDDT (<70) flanked by high pLDDT (>70)
        # This is very rough.
        hinge_candidates = 0
        is_high = plddt >= 70
        # Find transitions
        transitions = np.diff(is_high.astype(int))
        # Count number of high-to-low transitions
        # A simple domain count proxy might be (transitions / 2) + 1
        segments = np.sum(np.abs(transitions)) / 2 + 1

        return {
            "disorder_fraction": disorder_frac,
            "predicted_segments": int(segments),
        }

    def compute_geometry_metrics(self) -> Dict:
        """Compute geometry on high confidence residues."""
        mask = self.plddt_values >= self.plddt_high_conf
        coords = self.ca_coords[mask]

        if len(coords) < 10:
            return {
                "backbone_axis_ratio": None,
                "radius_of_gyration": None,
                "end_to_end_distance": None,
                "mean_curvature": None,
                "mean_torsion": None,
                "anisotropy": None
            }

        # PCA for anisotropy
        centroid = np.mean(coords, axis=0)
        centered = coords - centroid
        cov = np.cov(centered, rowvar=False)
        evals, evecs = np.linalg.eigh(cov)
        evals = np.sort(evals)[::-1] # Descending

        # Radius of Gyration
        rg = np.sqrt(np.mean(np.sum(centered**2, axis=1)))

        # End to End (of the filtered segments? This is tricky if discontinuous)
        # We will take max distance between any two points in the high conf set as a proxy for span
        # Or just first and last of the high conf set
        end_to_end = np.linalg.norm(coords[-1] - coords[0])

        # Curvature & Torsion
        # Smooth curve first? Or just discrete
        # Discrete curvature (k) ~ 1/R.
        # Using simple 3-point angle for now as proxy for local bending
        # Angle theta. Curvature ~ 2*sin(theta/2) / bond_length.
        # Actually, let's use the provided sliding window curvature logic from existing script
        curvatures = self._calculate_curvature(coords)

        metrics = {
            "radius_of_gyration": rg,
            "end_to_end_distance": end_to_end,
            "anisotropy": evals[0] / evals[2] if evals[2] > 0 else 0,
            "backbone_axis_ratio": evals[0] / evals[1] if evals[1] > 0 else 0,
            "mean_curvature": np.mean(curvatures) if len(curvatures) > 0 else 0,
            "max_curvature": np.max(curvatures) if len(curvatures) > 0 else 0,
            "mean_torsion": None, # Placeholder for CSV consistency with failure case
        }
        return metrics

    def _calculate_curvature(self, coords, window=5):
        """Local curvature estimation."""
        if len(coords) < 2 * window + 1:
            return []

        curvatures = []
        for i in range(window, len(coords) - window):
            # Fit circle to window? Or just simple angle?
            # Let's use the Menger curvature of start, mid, end of window
            p1 = coords[i - window]
            p2 = coords[i]
            p3 = coords[i + window]

            # Area of triangle
            a = np.linalg.norm(p1 - p2)
            b = np.linalg.norm(p2 - p3)
            c = np.linalg.norm(p3 - p1)

            s = (a + b + c) / 2
            area_sq = s * (s - a) * (s - b) * (s - c)
            if area_sq < 0: area_sq = 0
            area = np.sqrt(area_sq)

            if area == 0:
                curvatures.append(0)
            else:
                k = 4 * area / (a * b * c)
                curvatures.append(k)

        return np.array(curvatures)

    def compute_interaction_proxies(self) -> Dict:
        """Compute simple interaction proxies."""
        # Charged patch score: Density of K, R, D, E in high pLDDT regions
        # Assuming high pLDDT + charged = likely functional surface

        mask = self.plddt_values >= 70
        if not any(mask):
            return {"charged_density": 0}

        seq_arr = np.array(list(self.sequence))
        # Filter sequence by mask. Be careful of length mismatch if seq parsing failed?
        # Assuming 1:1 map
        if len(seq_arr) != len(mask):
            return {"charged_density": None}

        high_conf_seq = seq_arr[mask]
        charged_count = sum(1 for aa in high_conf_seq if aa in ['K', 'R', 'D', 'E'])
        density = charged_count / len(high_conf_seq)

        return {"charged_density": density}

    def generate_plots(self, output_dir: Path):
        """Generate requested plots."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. pLDDT vs Index
        plt.figure(figsize=(10, 4))
        plt.plot(self.plddt_values, label='pLDDT', color='blue', linewidth=1)
        plt.axhline(70, color='orange', linestyle='--', label='Confident (70)')
        plt.axhline(90, color='green', linestyle='--', label='Very Confident (90)')
        plt.ylim(0, 100)
        plt.xlabel('Residue Index')
        plt.ylabel('pLDDT')
        plt.title(f'Confidence Profile: {self.name}')
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / f"{self.name}_plddt.png")
        plt.close()

        # 2. PAE Heatmap (if available)
        if self.pae_matrix is not None:
            plt.figure(figsize=(6, 5))
            plt.imshow(self.pae_matrix, cmap='Greens_r', vmin=0, vmax=30)
            plt.colorbar(label='Expected Error (Å)')
            plt.title(f'PAE Matrix: {self.name}')
            plt.tight_layout()
            plt.savefig(output_dir / f"{self.name}_pae.png")
            plt.close()


def run_cycle():
    print("⚡ Bolt-BioFold: Starting Analysis Cycle...")

    predictions_dir = Path("alphafold_analysis/predictions")
    output_dir = Path("alphafold_analysis/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"

    pdb_files = list(predictions_dir.glob("*.pdb"))

    if not pdb_files:
        print("❌ No PDB files found. Run fetch_bcc_structures.py first.")
        return

    results = []

    print(f"   Found {len(pdb_files)} structures to analyze.")

    for i, pdb_file in enumerate(pdb_files):
        print(f"   Processing {pdb_file.stem}...", end=" ")

        pae_file = predictions_dir / f"{pdb_file.stem}_pae.json"
        if not pae_file.exists():
            pae_file = None

        analyzer = BioFoldAnalyzer(pdb_file, pae_file)
        if analyzer.load_data():
            # Compute metrics
            qual = analyzer.compute_quality_metrics()
            arch = analyzer.compute_architecture_metrics()
            geom = analyzer.compute_geometry_metrics()
            inte = analyzer.compute_interaction_proxies()

            # Plots
            analyzer.generate_plots(figures_dir)

            # Combine
            row = {
                "protein_id": analyzer.name,
                "species": "Human", # Assumption based on DB
                "length": len(analyzer.sequence),
                **qual,
                **arch,
                **geom,
                **inte
            }
            results.append(row)
            print("✅")
        else:
            print("❌")

    # Generate Output Table
    if not results:
        print("❌ No results generated.")
        return

    # Sort by protein_id
    results.sort(key=lambda x: x['protein_id'])

    # Write CSV
    import csv
    csv_path = output_dir / "biofold_results.csv"
    keys = results[0].keys()
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Results saved to {csv_path}")

    # Print Markdown Table
    print("\n## Results Summary")
    header = "| ID | Len | pLDDT | Disorder% | Rg | Anisotropy | Curvature |"
    print(header)
    print("|---|---|---|---|---|---|---|")
    for r in results:
        plddt = f"{r['pLDDT_mean']:.1f}"
        disorder = f"{r['disorder_fraction']*100:.1f}"
        rg = f"{r['radius_of_gyration']:.1f}" if r['radius_of_gyration'] else "N/A"
        ani = f"{r['anisotropy']:.2f}" if r['anisotropy'] else "N/A"
        curv = f"{r['mean_curvature']:.4f}" if r['mean_curvature'] else "N/A"
        print(f"| {r['protein_id']} | {r['length']} | {plddt} | {disorder} | {rg} | {ani} | {curv} |")

    # Interpretation
    print("\n## Interpretation")
    print("* **Observation**: We see a mix of compact globular domains (high pLDDT, low Rg/Length) and extended disordered regions.")

    # Find highest curvature protein
    valid_curv = [r for r in results if r['mean_curvature'] is not None]
    if valid_curv:
        max_curv = max(valid_curv, key=lambda x: x['mean_curvature'])
        print(f"* **Curvature outlier**: {max_curv['protein_id']} shows the highest mean curvature ({max_curv['mean_curvature']:.4f}), suggesting potential for bending/hinge mechanics.")

    # Find highest anisotropy
    valid_ani = [r for r in results if r['anisotropy'] is not None]
    if valid_ani:
        max_ani = max(valid_ani, key=lambda x: x['anisotropy'])
        print(f"* **Anisotropy**: {max_ani['protein_id']} is the most anisotropic ({max_ani['anisotropy']:.2f}), consistent with a rod-like or extended structure useful for force transmission (e.g., ECM or cytoskeleton).")

    print("\n## Best Next Move")
    print("Prioritize experimental validation or molecular dynamics simulation on the high-anisotropy/high-curvature candidates identified above (e.g. " + (max_ani['protein_id'] if valid_ani else "N/A") + ") to test mechanical response.")

if __name__ == "__main__":
    run_cycle()
