## 2026-01-23 - [SASA with cKDTree]

**Learning:** Calculating exposed surface proxy (SASA) using manual block-based neighbor search is slow ((N^2)$ worst case) and CPU-intensive for large proteins.

**Action:** Replaced the manual implementation with `scipy.spatial.cKDTree` when available. This reduces the neighbor search complexity to (N \log N)$, yielding a ~20x speedup for 5000-residue proteins (0.5s -> 0.02s per structure) while maintaining exact results.

## 2026-07-17 - [DataFrame Lookup vs Dict Lookup]

**Learning:** Looking up candidate metadata using pandas filtering (`df[df['col'] == val]`) inside a loop over N structures is O(M) per iteration (where M is candidates count). For N=20,000 and growing M, this dominates runtime.

**Action:** Pre-indexed the `candidates` DataFrame into a dictionary (`gene -> {info}`) before the loop. This reduces lookup from O(M) to O(1), yielding a ~6000x speedup for the lookup operation alone and ensuring the pipeline scales linearly with N, not N*M.

## 2026-07-28 - [Vectorized PAE Metrics]

**Learning:** `calculate_pae_metrics` used a nested loop over segments ($O(S^2)$) to compute block means. For proteins with many domains (e.g., 20+), the Python loop overhead became significant. Naive usage of `np.add.reduceat` on the full matrix is slow for sparse segments because it processes the gaps.

**Action:** Implemented a "compact matrix" approach: extract high-confidence rows/cols into a smaller contiguous matrix, then use `np.add.reduceat` to compute all block sums in $O(1)$ Python calls (vectorized). This yields a 16x speedup for 100-domain structures (1.32s -> 0.08s) and 2.5x for sparse structures, while preserving exact results.

## 2026-07-30 - [Torsion Norm Reuse]

**Learning:** `calculate_torsion` computed `np.linalg.norm` on `normals` twice (for overlapping `n1` and `n2` arrays), causing redundant `sqrt` and `sum` operations (~50% overhead for norms).

**Action:** Compute norms of `normals` once for the whole array, then slice to get `n1_norm` and `n2_norm`. This yielded a ~15% speedup for the `calculate_torsion` function (1.28ms -> 1.09ms per structure) and reduces CPU cycles for geometry calculations.

## 2026-08-05 - [Geometry Reuse: Area via Normals]

**Learning:** `calculate_curvature` used Heron's formula (expensive `sqrt` and arithmetic on side lengths) while `calculate_torsion` independently computed cross products. The triangle area needed for curvature is exactly $0.5 \times \|\text{CrossProduct}\|$. Recomputing these separately is wasteful.

**Action:** Refactored `analyze_structure` to precompute `normals` (cross products) and `normals_norm` once. Passed these to both functions. `calculate_curvature` now uses `0.5 * normals_norm` (skipping Heron's entirely), and `calculate_torsion` reuses the precomputed arrays. Benchmarks show 1.29x speedup for curvature and 2.12x for torsion (logic only), with verified identical results.

## 2026-08-06 - [Uncompressed Coordinate Cache]

**Learning:** `np.savez_compressed` adds significant CPU overhead (~3ms per file) when saving small arrays like PDB coordinates (N x 3 floats), with negligible disk space savings compared to uncompressed `np.savez`. For 20k+ structures, this adds up.

**Action:** Switched to `np.savez` (uncompressed) for coordinate caches in `StructureParser`. This yields a ~3x speedup in writing and ~1.7x in reading these specific caches. Loading remains compatible with legacy compressed files.

## 2026-10-27 - [Parallel KDTree Search]

**Learning:** The `exposed_surface_proxy` calculation was consuming >90% of geometry processing time because `cKDTree.query_ball_point` ran sequentially on a single core for every structure. For N=1000-2000 residues, this took ~0.66s.

**Action:** Tuned `cKDTree` parameters: set `leafsize=64` (up from 16) to improve traversal efficiency for dense protein coordinates, and set `workers=-1` to parallelize the query using all available cores. This reduced execution time to ~0.22s (~3x speedup) for the SASA component, and reduced total per-structure analysis time to < 10ms for N=2000 in benchmarks.

## 2026-11-01 - [Optimized PDB Parsing Loop]

**Learning:** The `StructureParser.fast_parse_pdb_arrays` method used a Python `for line in f` loop with repeated string slicing (`line[12:16].strip()`) and checks for every line. For large datasets, the iterator overhead and string operations became a bottleneck.

**Action:** Optimized the parser to use `readlines()` (bulk read) and direct index-based character checks (`line[13:15] == "CA"`) instead of slicing/stripping. This yielded a ~1.5x speedup (7ms -> 5ms) for medium structures like PIEZO2, improving throughput for the initial analysis pass.

## 2026-11-03 - [Faster PDB Atom Filtering]

**Learning:** Even with optimized loops, `line.startswith("ATOM")` incurs a method call overhead for every line in a PDB file. For millions of lines across a dataset, this adds up. String slicing `line[:4] == "ATOM"` is faster in Python. Additionally, redundant string operations (duplicate assignment) were found.

**Action:** Replaced `startswith` with slice check and removed duplicate `res_name` assignment in `StructureParser`. Benchmarks show ~9-14% speedup for parsing PDB structures, further reducing the I/O bottleneck.

## 2026-11-04 - [Optimized PDB Parsing Loop V2]

**Learning:** The previous optimization (using `line[:4] == "ATOM"`) was found to be slightly slower than `line.startswith("ATOM")` in disk-bound scenarios (40ms vs 45ms per 25k lines). More importantly, unconditional `strip()` of residue names (`line[17:20].strip()`) creates allocations for every residue, even when padding is absent.

**Action:** Replaced `slice` check with `startswith()` and `char` indexing (`line[13] == 'C'`). Replaced unconditional `strip()` with a conditional check. This yielded a ~10% speedup on raw parsing and reduces memory churn for large batch processing.

## 2026-11-05 - [Flat List Append for PDB Parsing]

**Learning:** Constructing a list of lists (`coords_list.append([x, y, z])`) inside the parsing loop creates millions of small list objects for large datasets, adding memory allocation overhead. Additionally, looking up `list.append` on every iteration adds method call overhead.

**Action:** Replaced list-of-lists with a flat list append (`coords_flat.append(x); ...`) and aliased `append` to a local variable. This yielded a ~10-15% speedup in the parsing loop (16ms -> 14ms per 2500 residues), further reducing the computational cost of the initial parse before caching.
## 2026-08-20 - [Parser Line Reading Optimization Rejected]
**Learning:** Benchmarked `StructureParser.fast_parse_pdb_arrays` (Python loop vs `readlines` vs `np.fromregex`) for 100k line PDBs.
- `for line in f` (buffered): ~0.2s
- `f.readlines()`: ~0.2s (no significant gain)
- `np.fromregex`: Slower/Fragile due to complex PDB column alignment.
**Action:** Rejected parsing optimization. Parsing is surprisingly efficient. The real bottleneck for repeated analysis is re-computing geometry metrics. Implemented persistent caching (`.npz`/`.json`) instead, yielding ~10x speedup on second run.

## 2026-11-20 - [Geometry Smoothing Optimization]

**Learning:** `np.convolve` creates full-size temporary arrays and performs O(N*W) operations. For simple moving averages (boxcar), `np.cumsum` (Integral Image) is O(N) and ~2x faster even for small windows (W=10). Verified numerically identical results for `mode='valid'`.

**Action:** Replaced `np.convolve` with `np.cumsum` in `scripts/bolt_biofold_analysis.py`.

**Learning:** `scipy.spatial.cKDTree` in version < 1.8.0 lacks `return_length=True` for `query_ball_point`, causing massive memory overhead (list of lists) for neighbor counting. This remains a bottleneck in `metrics.py` but requires dependency upgrade to fix properly.

## 2026-02-16 - [Surface Metrics with cKDTree]

**Learning:** `compute_surface_metrics` used an (N^2)$ broadcasting approach to calculate neighbor counts within 10Å. For large proteins like PIEZO1 (N=2500), this took ~3.3s per structure and scaled poorly.

**Action:** Replaced the distance matrix calculation with `scipy.spatial.cKDTree.query_ball_point(..., return_length=True)`. This reduced complexity to (N \log N)$, yielding a ~350x speedup (3.3s -> 0.009s for PIEZO1) while producing identical results.
