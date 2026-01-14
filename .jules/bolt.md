## 2024-03-24 - [Optimize Metric Calculation Loop]

**Learning:** BioPython `Structure` traversal is slow when repeated multiple times. Iterating over residues to extract coordinates for Rg, then again for Anisotropy, then again for pLDDT is inefficient.
**Action:** Implemented `extract_coords_and_plddt` in `StructureParser` to do a single pass extraction into NumPy arrays. Refactored `MetricsAnalyzer` to operate on these arrays, achieving ~1.8x speedup on metric calculation.

**Learning:** When refactoring methods that take complex objects (like `Structure`) to take simple arrays, backward compatibility can be tricky if the `analyze` method is the public entry point.
**Action:** Updated `analyze_structure` to handle both the extraction (if needed) and the calculation, but optimized the main pipeline script `04_analyze_metrics.py` to perform extraction once and pass arrays.

## 2025-01-05 - [Fast PDB Parsing]

**Learning:** `Bio.PDB.PDBParser` is a significant bottleneck when processing thousands of structures just to extract coordinates and pLDDT. It builds a complex object hierarchy (Model->Chain->Residue->Atom) which is unnecessary for simple array extraction. Parsing a 10,000 residue protein took ~1.2s.
**Action:** Implemented `fast_parse_pdb_arrays` in `StructureParser` which reads the PDB file line-by-line and extracts data directly into NumPy arrays. This reduced parse time to ~0.05s (~20x speedup). Updated `04_analyze_metrics.py` to use this fast parser, with a fallback to the legacy parser if needed.

## 2025-01-09 - [Shared Geometry Vectors]

**Learning:** Curvature and Torsion calculations both compute bond vectors ($r_{i+1} - r_i$) and bond lengths. For a 10,000 residue protein, repeatedly allocating these arrays and computing norms adds overhead (~200ms).
**Action:** Refactored `MetricsAnalyzer` to pre-calculate `bond_vectors` and `bond_lengths` once in `analyze_structure` and pass them to `calculate_curvature` and `calculate_torsion`. This reduced geometry calculation time by ~15% and reduced memory churn.

## 2025-05-22 - [Incremental Processing]

**Learning:** The pipeline re-processes all structures every run, even if they haven't changed. As the dataset grows (>500 proteins), this wastes minutes parsing PDBs and computing identical metrics.
**Action:** Implemented incremental processing in `04_analyze_metrics.py`. It now loads the existing `protein_metrics.csv`, filters out `(gene, uniprot)` pairs that are already present, and processes only new additions. This reduces runtime for updates from O(N) to O(N_new). Also fixed a crash in report generation due to column name mismatches (`anisotropy` vs `anisotropy_index`).

## 2025-06-15 - [Blocked Matrix Algebra for Surface Proxy]

**Learning:** The "Exposed Surface Proxy" calculation (counting neighbors < 10A) used a hybrid approach: full O(N^2) broadcasting for N<2000 and a slow Python loop for N>=2000. The broadcasting spike caused high memory usage (50MB+ for N=1500) and the loop was CPU-bound.
**Action:** Replaced the hybrid logic with a unified "Blocked Matrix Algebra" approach. It computes pairwise distances using `np.dot` (BLAS-optimized) in blocks of 1000 residues.
**Impact:**
- N=1500: ~6x speedup (0.13s -> 0.02s)
- N=5000: ~3x speedup (0.95s -> 0.32s)
- Removes massive memory spikes for medium-sized proteins.

## 2026-01-14 - Torsion Calculation Optimization

**Learning:** Computing geometric metrics like torsion involves repetitive vector operations. Specifically, for a chain of atoms, the torsion angle calculation requires cross products of adjacent bond vectors ($b_i \times b_{i+1}$) and ($b_{i+1} \times b_{i+2}$). These are normally calculated as independent arrays `n1` and `n2`, effectively computing each cross product twice across the chain.

**Action:** Implemented an optimization in `src/afcc/metrics.py` to compute the cross products of all adjacent bond pairs once (`normals`), then sliced this array to get `n1` and `n2`. This reduced the number of cross product operations by ~50%.

**Result:** Benchmarking showed a ~14% speedup in the `calculate_torsion` method for a 5000-residue chain (0.82 ms -> 0.70 ms per call). While small per-call, this adds up across thousands of structures and bootstrap iterations. Correctness was verified with a unit test for a known geometry.
