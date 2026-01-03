
import sys
import time
import numpy as np
from Bio.PDB.Structure import Structure
from Bio.PDB.Model import Model
from Bio.PDB.Chain import Chain
from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom
from research.alphafold_countercurvature.src.afcc.metrics import MetricsAnalyzer
from research.alphafold_countercurvature.src.afcc.structure import StructureParser

def create_large_dummy_structure(n_residues=2000):
    s = Structure("dummy")
    m = Model(0)
    c = Chain("A")
    s.add(m)
    m.add(c)

    for i in range(n_residues):
        res_name = "ALA" if i % 2 == 0 else "LYS" # Mix of charged/uncharged
        r = Residue((" ", i, " "), res_name, " ")

        # Simple helix-ish coords
        x = np.cos(i/10.0) * 10
        y = np.sin(i/10.0) * 10
        z = i * 1.5

        ca = Atom("CA", [x, y, z], 50.0, 1.0, " ", "CA", 1, "C")
        r.add(ca)
        c.add(r)
    return s

def benchmark():
    parser = StructureParser()
    analyzer = MetricsAnalyzer()

    N_RESIDUES = 3000
    print(f"Generating dummy structure ({N_RESIDUES} residues)...")
    structure = create_large_dummy_structure(N_RESIDUES)

    print("Extracting data...")
    coords, plddt, resnames = parser.extract_coords_and_plddt(structure)

    ITERATIONS = 20

    # Measure Legacy (pass structure, but no resnames)
    # This forces the method to re-iterate the Bio.PDB structure for the charged patch score
    print(f"\n--- Legacy Path (Iterating Bio.PDB Structure) ---")
    start_legacy = time.time()
    for _ in range(ITERATIONS):
        _ = analyzer.analyze_structure(structure=structure, coords=coords, plddt_scores=plddt, resnames=None)
    end_legacy = time.time()
    avg_legacy = (end_legacy - start_legacy) / ITERATIONS
    print(f"Avg time: {avg_legacy:.6f}s")

    # Measure Vectorized (pass resnames)
    print(f"\n--- Vectorized Path (NumPy Arrays) ---")
    start_vec = time.time()
    for _ in range(ITERATIONS):
        _ = analyzer.analyze_structure(structure=structure, coords=coords, plddt_scores=plddt, resnames=resnames)
    end_vec = time.time()
    avg_vec = (end_vec - start_vec) / ITERATIONS
    print(f"Avg time: {avg_vec:.6f}s")

    speedup = avg_legacy / avg_vec
    print(f"\n⚡ Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    sys.path.append(".")
    benchmark()
