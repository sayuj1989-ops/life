# Bolt's Journal

## 2026-01-15 - [SASA Optimization with Bounding Box Pruning]
**Learning:**
Calculating the "Exposed Surface Proxy" (SASA) involves pairwise distances between all residues ($O(N^2)$). For large proteins (e.g., PIEZO1, N=4554), this dominated the metric calculation time (~90%).
While the previous implementation used blocked matrix multiplication to handle memory, it still computed all pairwise distances.

**Action:**
Implemented "Bounding Box Pruning" within the blocked loop.
For each pair of blocks $(I, J)$, we calculate their bounding boxes ($min, max$).
If the boxes are further apart than the threshold (10 Angstroms), we skip the expensive pairwise distance calculation entirely.
This reduces the complexity for elongated or multi-domain proteins significantly.

**Results:**
- PIEZO1 (4554 res): ~2.5x speedup in SASA calc (290ms -> 110ms)
- VANGL2 (2972 res): ~2.5x speedup
- Exact numerical results preserved.

## 2026-01-17 - [Structure Parsing Cache]
**Learning:**
Repeatedly parsing PDB files to extract coordinates, pLDDT, and residue names consumes significant CPU time (~8-9ms per file), even with the optimized `fast_parse_pdb_arrays`.
For large datasets or iterative analysis, this I/O parsing overhead accumulates.
The existing `parse_pae` method successfully uses sidecar `.npz` files to cache results, speeding up loading by ~15x.

**Action:**
Implemented a similar `.npz` caching mechanism for `fast_parse_pdb_arrays` in `research/alphafold_countercurvature/src/afcc/structure.py`.
The parser now checks for a `<pdb>.pdb.cache.npz` file. If valid (newer than PDB), it loads arrays directly (taking ~1ms).
If invalid/missing, it parses and saves the cache.

**Results:**
- 4x speedup in structure loading (~400ms -> ~110ms for 100 iterations).
- Avoids redundant string processing.
- Handles read-only filesystems gracefully (suppresses repeated warnings).

## 2026-06-03 - [Float32 Optimization for Metrics Analysis]
**Learning:**
AlphaFold coordinates and pLDDT scores (originally float32 precision) were being processed as float64, doubling memory usage and slowing down O(N^2) SASA calculations. The float64 overhead was unnecessary given the input precision (3 decimal places).

**Action:**
Enforced `float32` in `StructureParser` (for file parsing and cache) and `MetricsAnalyzer` (for internal calculations). Added explicit `astype(np.float32, copy=False)` checks to ensure downstream calculations (especially blocked matrix operations) benefit from reduced memory bandwidth.

**Results:**
- ~1.8x overall speedup for PIEZO1 analysis (770ms -> 433ms).
- ~3.15x speedup for SASA calculation isolated.
- 2x memory reduction for coordinate arrays.
- Numerical differences are negligible (< 1e-6), preserving scientific validity.
