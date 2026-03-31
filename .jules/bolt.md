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

**Action:** Replaced `startswith` with `startswith()` and `char` indexing (`line[13] == 'C'`). Replaced unconditional `strip()` with a conditional check. This yielded a ~10% speedup on raw parsing and reduces memory churn for large batch processing.

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

## 2026-11-21 - [Surface Metrics O(N) Optimization]

**Learning:** The `compute_surface_metrics` function in `bolt_biofold_analysis.py` used an O(N^2) broadcasting approach to compute neighbor counts. For proteins with >3000 residues, this caused massive memory usage (>200MB) and slow execution (>1.6s).

**Action:** Replaced the broadcasting logic with `scipy.spatial.cKDTree.query_ball_point(return_length=True)`, which is O(N log N). This reduced execution time for N=3000 from 1.69s to 0.015s (~110x speedup) and eliminates the memory bottleneck, enabling efficient analysis of giant proteins like Titin or Piezo1.
## 2026-11-20 - [cKDTree Parallelism] **Learning:** cKDTree in scipy supports parallel execution (workers=-1) and has a tunable leafsize. For N=3000-5000 points (typical protein), leafsize=64 and workers=-1 yielded ~2x speedup (12ms -> 6ms) for neighbor counting. **Action:** Updated compute_surface_metrics in bolt_biofold_analysis.py.

## 2026-11-22 - [Optimized Curvature Geometry]

**Learning:** `calculate_curvature` computed `b_len` (triangle side length) by allocating a temporary `vec_ac` array of size (N, 3) and calling `np.linalg.norm`. This involved significant memory allocation and overhead. By using the geometric identity $|u+v|^2 = |u|^2 + |v|^2 + 2(u \cdot v)$, we can compute `b_len` using `np.einsum` and scalar operations, avoiding the temporary array.

**Action:** Replaced `np.linalg.norm(vec_ac)` with `sqrt(a^2 + c^2 + 2*dot(u,v))` in `MetricsAnalyzer`. Benchmarks show ~2x speedup for this specific calculation (29ms -> 13ms for 10k residues) and identical results (within 1e-15).

## 2026-09-01 - [Fast Cross Product]

**Learning:** `np.cross` is significantly slower (2x-6x) than manual arithmetic for large arrays of 3D vectors due to internal broadcasting checks and overhead. For geometry-heavy pipelines (curvature, torsion), this adds up per-residue.

**Action:** Implemented `_cross_product_fast` using explicit numpy arithmetic. This yielded a ~2.2x speedup for the cross product operation and ~1.23x speedup for the overall geometry kernel (curvature + torsion) in `MetricsAnalyzer`.

## 2026-11-20 - [Redundant Parsing in Aux Scripts]

**Learning:** Standalone scripts like `bolt_biofold_analysis.py` often duplicate core library logic but miss optimizations (e.g., using slow `Bio.PDB` instead of `fast_parse_pdb_arrays`, loading JSON instead of cached `.npz`). This creates inconsistent performance baselines.

**Action:** Refactored `scripts/bolt_biofold_analysis.py` to use the optimized `StructureParser` from `afcc.structure`, gaining ~20% speedup on small sets and massive scalability for large proteins via `.npz` caching.

## 2026-03-05 - [Switch PAE cache to uint8 + uncompressed npy + mmap]

**Learning:**
1. **PAE matrices are compressible but slow to compress:** `np.savez_compressed` takes ~1.5s for 5MB PAE matrix due to zlib overhead. Reading back is also slow (decompression).
2. **Space waste:** Default `np.array(pae_data)` uses `int64` (8 bytes) even though PAE values are 0-31.
3. **Optimized format:** Converting to `uint8` (1 byte) + `np.save` (uncompressed `.npy`) reduces file size by ~8x compared to raw `int64`, making it smaller than compressed `int64` arrays!
4. **Massive Speedup:**
   - Saving: ~20x faster (0.6s vs 14.7s for 2000x2000).
   - Loading: Instant via `mmap_mode='r'` (<0.01s).
   - RAM: `mmap` avoids loading full array into memory, preventing spikes for large proteins (e.g., Titin).

**Action:** Refactored `StructureParser.parse_pae` to use `.npy` cache with `uint8` casting and `mmap` loading. Added backward compatibility to auto-upgrade legacy `.npz` caches.

## 2026-05-25 - [Dynamic KDTree Parallelism]
**Learning:** `scipy.spatial.cKDTree` parallelization (`workers=-1`) has significant thread spin-up overhead. Benchmarks show that for N < 1250, serial execution is faster. For N=500, serial is ~1.8x faster (1.25ms vs 2.23ms).
**Action:** Implemented dynamic worker selection in `metrics.py`: `workers = -1 if len(coords) > 2000 else 1`. This optimizes the "SASA proxy" calculation for the majority of single-chain proteins while retaining speed for large complexes.

## 2026-03-01 - [Fast PAE Matrix Metrics]

**Learning:** `MetricsAnalyzer.calculate_pae_metrics` was a bottleneck due to three issues:
1. `np.mean(pae_matrix)` upcasts `uint8` matrices to `float64` to prevent overflow, which causes slow memory allocation and arithmetic.
2. The domain segment finding loop used python list comprehensions and slow `np.hstack` integer conversions.
3. Extracting the compact block matrix used `np.ix_`, which involves internal function overhead, while direct boolean array indexing or `where` is faster.

**Action:**
- Replaced `np.mean` with explicit `np.sum(pae_matrix, dtype=np.uint64) / pae_matrix.size` (~20% speedup).
- Replaced the list comprehension segment finding with preallocated boolean arrays and `np.diff` on `int8` conversions, directly slicing arrays with valid block lengths.
- Used `valid_idx = np.where(mask_valid)[0]` and advanced indexing `pae_hc = pae_matrix[valid_idx[:, None], valid_idx]` to avoid `np.ix_`.
This reduced the metric calculation overhead significantly while preserving bit-exact matching for metric results.

## 2026-11-25 - [Optimize PAE reduceat axis order]

**Learning:** When using `np.add.reduceat` to calculate block sums in `calculate_pae_metrics`, performing the reduction on the non-contiguous axis (rows) before the contiguous axis (columns) causes significant cache misses. A micro-benchmark showed a ~28% speedup by simply swapping the axis reduction order for the C-contiguous PAE matrix.

**Action:** Swapped `np.add.reduceat` to process `axis=1` (cols) first, then `axis=0` (rows). This improves CPU cache locality during computation, reducing calculation time without altering scientific metrics.

## 2026-11-20 - [Bolt BioFold metrics boolean arrays optimization]
**Learning:** Checking the fraction of residues above/below pLDDT thresholds is a frequent operation inside `MetricsAnalyzer.analyze_structure`. Using `np.sum()` on boolean arrays allocates memory or runs sub-optimally.
**Action:** Replaced `np.sum(plddt >= 90)` with `np.count_nonzero(plddt >= 90)` inside `research/alphafold_countercurvature/src/afcc/metrics.py`. It provides a minor (~3-4x speedup on that specific block) performance boost with identical numerical output.

## 2026-11-26 - [Vectorized End-to-End Distance]
**Learning:** In `MetricsAnalyzer.analyze_structure`, finding the longest contiguous high-confidence segment used `np.hstack` (which forces internal copies and integer upcasting) and a python `for` loop over `zip(starts, ends)` to track the maximum length. This introduced unnecessary overhead for an operation done on every structure.
**Action:** Replaced `np.hstack` with an explicitly pre-allocated boolean array for padding, followed by `np.diff` on `int8`. Replaced the python loop with vectorized `lengths = ends - starts` and `np.argmax(lengths)` to find the longest segment. This yielded a ~6x speedup (from 3.08s to 0.48s for 10,000 runs) and is O(N) instead of O(N) with high python overhead, while returning identical results.

## 2026-03-09 - [Vectorized Variance for Radius of Gyration]

**Learning:** When profiling `run_bolt_analysis_cycle.py`, we observed high cumulative time from parsing coordinates and repeatedly calculating geometric metrics like Radius of Gyration (`calculate_rg`). The previous implementation manually computed the center of mass, squared differences along axes, and mean squared distances, leading to multiple temporary arrays.

**Action:** Optimized `calculate_rg` using NumPy's vectorized variance `np.var`. The identity `Rg = sqrt(sum(Var(coords, axis=0)))` avoids manual broadcasting and computes variance efficiently in C. This provides a ~35% speedup per call (from 0.88s to 0.54s per 10M points) and reduces peak memory allocation for this metric (30MB -> 23MB for 1M points). The output remains mathematically identical.

## $(date +%Y-%m-%d) - [Fast Boolean Diff for Segment Finding]
**Learning:** In AlphaFold structure analysis, `np.diff` is often used to find boundaries of continuous segments (e.g., residues with high pLDDT scores or domains). When operating on boolean arrays, first casting to `int8` before calling `np.diff` adds unnecessary memory overhead. Instead, using a boolean condition `bounded[1:] != bounded[:-1]` and extracting starts/ends with boolean bitwise `&` logic (`diff & bounded[1:]`) achieves the same boundary detection with ~25% to ~30% improved speed.
**Action:** Replaced `np.diff(bounded.astype(np.int8))` with fast boolean diff logic in `research/alphafold_countercurvature/src/afcc/metrics.py` (specifically in PAE segment finding and end-to-end distance calculations).

## 2026-11-20 - [Bolt Optimization: pLDDT boolean mask reuse]   **Learning:** pLDDT fractions calculation repeatedly creates internal boolean masks across array boundaries. This was a pipeline-specific bottleneck pattern resulting in duplicated boolean traversal and slow performance. **Action:** Refactored `analyze_structure` in `metrics.py` to reuse logical boolean masks (`mask_low = plddt_scores < 70` and `mask_high >= 90`) and logical subsetting (`plddt_scores[mask_low] < 50`) to avoid compound logical ops (`&`) and duplicate mask allocations. Improved block speed from ~0.25s to ~0.02s per 10k items.
## 2025-02-28 - [Vectorize modulus condition in Hopf boundary solver]
**Learning:** Python loops over NumPy arrays with conditional blocks are very slow. In `analytical_hopf_boundary` of `alphafold_pipeline_v2.py`, calculating values element-wise over an array of 6000 values took about ~1.1 seconds.
**Action:** Vectorized the initial modulus condition mask `abs(lhs - rhs) / max(lhs, rhs) < 0.002` across the `omega` array before dropping into the `valid_omegas` loop to calculate the phase boundary. This lowered execution time per call to ~0.02s (~40-50x speedup).

## 2026-03-30 - [Matplotlib Figure Reuse]

**Learning:** Repeatedly calling `plt.figure()` and `plt.close()` inside a loop over N structures is slow and creates significant overhead for large datasets due to matplotlib's internal canvas initialization and teardown.

**Action:** Initialized `fig, ax = plt.subplots()` once outside the plotting loops. Reused the axis object inside the loop by calling `ax.clear()` (or `line.set_data()` where appropriate) to reset the data while preserving the figure container. This reduces matplotlib overhead yielding a measurable speedup for the plotting stage while outputting identical figures.

## 2026-03-31 - [Plotting Optimization]
**Learning:** The previous code called `ax.clear()` in the plotting loop for each protein, causing matplotlib to redraw all axes labels, limits, legends, and titles. This took ~2.4 seconds for 8 proteins.
**Action:** Replaced `ax.clear()` with pre-initializing `Line2D` objects outside the loop and updating their data with `set_data()` inside the loop, while manually setting x/y limits. This dropped the plot time to ~1.0-1.5 seconds.
