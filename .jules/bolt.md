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

## 2026-01-18 - [SASA Contact Caching]
**Learning:**
The "Exposed Surface Proxy" calculation (SASA) in `analyze_structure` accounts for ~90% of the runtime (0.11s out of 0.12s) due to the neighbor search loop, even with block pruning.
Since AlphaFold structures are static, the neighbor counts (contact numbers) are constant for a given PDB.
Re-computing this O(N^2) metric every time we tweak a downstream metric or generate a report is wasteful.

**Action:**
Refactored `MetricsAnalyzer` to expose `calculate_contact_numbers(coords)` as a public method.
Updated `04_analyze_metrics.py` to cache the contact number array to `<pdb>.sasa.cache.npz`.
The analysis loop now checks for this cache and injects the pre-computed array into `analyze_structure`.

**Results:**
- ~38x speedup in analysis time (0.11s -> 0.003s per structure).
- Total pipeline throughput for 1000 structures would drop from ~3.5 mins to ~10 seconds (excluding parse time).
- Fully backward compatible; falls back to fresh calculation if cache is missing.
