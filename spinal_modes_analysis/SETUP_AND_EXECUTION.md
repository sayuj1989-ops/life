# Setup and Execution Guide

## Prerequisites

- **Python:** 3.10 or higher
- **Poetry:** 1.5.0 or higher ([installation guide](https://python-poetry.org/docs/#installation))
- **Git:** For version control

## Initial Setup

### 1. Install Dependencies

```bash
cd /Users/dr.sayujkrishnan/LIFE
poetry install
```

This will:
- Create a virtual environment
- Install all package dependencies
- Install development tools (pytest, ruff, black, mypy)
- Register the `spinalmodes` CLI command

### 2. Verify Installation

```bash
# Check CLI is available
poetry run spinalmodes --help

# Should output:
# Usage: spinalmodes [OPTIONS] COMMAND [ARGS]...
# 
# Spinal modes: Counter-curvature and IEC model
# ...
```

### 3. Run Tests

```bash
# Run full test suite
poetry run pytest tests/ -v

# Expected: All tests pass (some may be skipped)
```

## Execution Pipeline

### Phase 1: Quick Demo

Run a quick demonstration to verify everything works:

```bash
poetry run spinalmodes iec demo \
  --out-prefix outputs/csv/iec_demo \
  --chi-kappa 0.02 \
  --I-mode linear
```

**Expected outputs:**
- `outputs/csv/iec_demo.csv` - Spatial profiles
- `outputs/csv/iec_demo_summary.json` - Summary statistics

**Expected console output:**
```
=== IEC Demo Results ===
Wavelength: XXX.XX mm
Amplitude: XX.XX degrees
Node positions (mm): [...]
Torsion stats: mean=..., std=..., max=...
```

### Phase 2: Parameter Sweeps

Generate parameter sweep data:

```bash
# Sweep chi_kappa
poetry run spinalmodes iec sweep \
  --param chi_kappa \
  --start 0.0 \
  --stop 0.06 \
  --steps 13 \
  --I-mode linear \
  --out-csv outputs/csv/iec_sweep_chi_kappa.csv

# Sweep chi_E
poetry run spinalmodes iec sweep \
  --param chi_E \
  --start -0.3 \
  --stop 0.3 \
  --steps 20 \
  --I-mode linear \
  --out-csv outputs/csv/iec_sweep_chi_E.csv
```

### Phase 3: Phase Diagram

Generate the phase diagram (key figure):

```bash
poetry run spinalmodes iec phase \
  --delta-b 0.0:0.2:41 \
  --gradI 0.0:0.1:21 \
  --out-csv outputs/csv/iec_phase_map.csv \
  --out-fig outputs/figs/fig_iec_phase.png
```

**Expected outputs:**
- `outputs/csv/iec_phase_map.csv` - Phase map data (861 rows)
- `outputs/figs/fig_iec_phase.png` - Phase diagram figure
- `outputs/figs/fig_iec_phase.json` - Metadata

### Phase 4: Discriminator Figures

Generate the main discriminator figure (Figure 1 in manuscript):

```bash
poetry run python -c "
from spinalmodes.fig_iec_discriminators import generate_fig_iec_discriminators
generate_fig_iec_discriminators()
"
```

**Expected outputs:**
- `outputs/figs/fig_iec_discriminators.png` - Three-panel figure
- `outputs/figs/fig_iec_discriminators.json` - Metadata
- `outputs/csv/fig_iec_discriminators.csv` - Source data

### Phase 5: Node Drift Analysis

```bash
poetry run spinalmodes iec node-drift \
  --I-mode step \
  --chi-kappa 0.04 \
  --out-fig outputs/figs/fig_iec_node_drift.png
```

### Phase 6: Helical Threshold Analysis

```bash
poetry run spinalmodes iec helical-threshold \
  --gradI 0.05 \
  --out-fig outputs/figs/fig_iec_threshold.png
```

## Validation

After generating figures, validate they meet requirements:

```bash
poetry run python tools/validate_figures.py
```

**Expected output:**
```
Validating X figure(s)...

Checking fig_iec_discriminators.png...
Checking fig_iec_phase.png...
Checking fig_iec_node_drift.png...
Checking fig_iec_threshold.png...

✅ All figures passed validation!
```

**If validation fails:**
- Check error messages for specific issues (DPI, width, alpha channel)
- Regenerate affected figures
- Ensure JSON sidecars are present

## Quality Checks

Run all quality checks:

```bash
# Full pipeline (format, lint, type check, test)
make green

# Individual checks
make format    # Auto-format code
make lint      # Check code style
make typecheck # Type checking
make test      # Run tests
```

**Expected output:**
```
✅ All checks passed!
```

## Generating Documentation

Build the MkDocs site locally:

```bash
# Serve locally (for preview)
poetry run mkdocs serve

# Build static site
poetry run mkdocs build
```

Open browser to `http://127.0.0.1:8000` to view documentation.

## Troubleshooting

### Issue: `poetry: command not found`

**Solution:** Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Issue: `ImportError: No module named 'spinalmodes'`

**Solution:** Ensure you're using `poetry run`:
```bash
poetry run spinalmodes iec demo
# NOT: spinalmodes iec demo
```

### Issue: Figure validation fails with DPI error

**Solution:** Matplotlib might not be setting DPI correctly. Check:
1. `matplotlib` version is ≥3.7.0
2. `plt.figure(dpi=300)` is used in code
3. `plt.savefig(..., dpi=300)` is used

### Issue: Tests fail with numerical precision errors

**Solution:** Some tests use `pytest.approx()` with tolerances. Check:
1. Numerical solver parameters (grid resolution, convergence criteria)
2. Test tolerance values (may need adjustment for different architectures)

### Issue: CLI commands hang or take too long

**Solution:**
1. Reduce grid resolution: Modify `n_nodes` in `IECParameters` (default: 100)
2. Reduce sweep steps: Use fewer `--steps` in sweep commands
3. Check for infinite loops in solver (should have max iterations)

## Performance Notes

**Typical run times (on modern laptop):**
- `demo`: ~1 second
- `sweep` (13 steps): ~5 seconds
- `phase` (41×21=861 points): ~30 seconds
- `fig_iec_discriminators`: ~60 seconds (3 panels with multiple runs)

**Memory usage:**
- Peak: ~200 MB for most operations
- Phase diagrams: ~500 MB for large grids

## Next Steps

After successful execution:

1. **Review outputs:**
   - Check CSV files in `outputs/csv/`
   - View figures in `outputs/figs/`
   - Verify JSON metadata completeness

2. **Manuscript integration:**
   - Figures are ready for inclusion in manuscript
   - Reference figure files in `docs/manuscript/SpinalCountercurvature_IEC.md`

3. **Parameter tuning:**
   - Adjust IEC parameters based on biological constraints
   - Re-run sweeps with updated ranges

4. **Extension:**
   - Add new coherence field modes in `iec.py`
   - Implement additional CLI commands in `iec_cli.py`
   - Create custom analysis scripts

## Complete Pipeline Script

For convenience, here's a bash script to run the complete pipeline:

```bash
#!/bin/bash
set -e

echo "=== Spinal Modes IEC Pipeline ==="

# 1. Install
echo "Step 1: Installing dependencies..."
poetry install

# 2. Tests
echo "Step 2: Running tests..."
poetry run pytest tests/ -v

# 3. Demo
echo "Step 3: Running demo..."
poetry run spinalmodes iec demo --out-prefix outputs/csv/iec_demo

# 4. Sweeps
echo "Step 4: Parameter sweeps..."
poetry run spinalmodes iec sweep --param chi_kappa --start 0.0 --stop 0.06 --steps 13 --out-csv outputs/csv/sweep_chi_kappa.csv

# 5. Phase diagram
echo "Step 5: Phase diagram..."
poetry run spinalmodes iec phase --delta-b 0.0:0.2:41 --gradI 0.0:0.1:21 --out-csv outputs/csv/phase_map.csv --out-fig outputs/figs/fig_phase.png

# 6. Figures
echo "Step 6: Generating figures..."
poetry run python -c "from spinalmodes.fig_iec_discriminators import generate_fig_iec_discriminators; generate_fig_iec_discriminators()"
poetry run spinalmodes iec node-drift --I-mode step --chi-kappa 0.04 --out-fig outputs/figs/fig_node_drift.png
poetry run spinalmodes iec helical-threshold --gradI 0.05 --out-fig outputs/figs/fig_threshold.png

# 7. Validate
echo "Step 7: Validating figures..."
poetry run python tools/validate_figures.py

# 8. Quality checks
echo "Step 8: Quality checks..."
make green

echo "=== Pipeline Complete! ==="
echo "Outputs:"
echo "  - CSV data: outputs/csv/"
echo "  - Figures: outputs/figs/"
echo "  - Manuscript: docs/manuscript/SpinalCountercurvature_IEC.md"
```

Save as `run_pipeline.sh`, make executable (`chmod +x run_pipeline.sh`), then run: `./run_pipeline.sh`

## Git Workflow

```bash
# Initialize repo (if not already done)
git init
git add .
git commit -m "feat: Initial IEC model implementation"

# Create feature branches for development
git checkout -b feature/new-analysis
# ... make changes ...
git add .
git commit -m "feat(iec): Add new analysis feature"
git checkout main
git merge feature/new-analysis
```

## Contact & Support

For issues or questions:
- **GitHub Issues:** [repository URL]/issues
- **Email:** [your email]
- **Documentation:** See `docs/` directory

