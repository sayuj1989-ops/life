# CLI Reference

The `spinalmodes` package provides a command-line interface for running IEC model analyses.

## Installation

```bash
poetry install
```

## Usage

```bash
poetry run spinalmodes --help
```

## IEC Commands

All IEC-related commands are under the `iec` subcommand:

```bash
poetry run spinalmodes iec [COMMAND]
```

### `demo`

Run a quick demonstration of the IEC model with default parameters.

**Usage:**
```bash
poetry run spinalmodes iec demo [OPTIONS]
```

**Options:**
- `--out-prefix TEXT`: Output file prefix (default: `outputs/csv/iec_demo`)
- `--chi-kappa FLOAT`: Target curvature coupling χ_κ (default: 0.02)
- `--I-mode TEXT`: Coherence field mode: constant, linear, gaussian, step (default: `linear`)

**Outputs:**
- `{prefix}.csv`: Spatial profiles (s, θ, κ, E, C)
- `{prefix}_summary.json`: Summary statistics (wavelength, amplitude, node positions, torsion)

**Example:**
```bash
poetry run spinalmodes iec demo \
  --out-prefix outputs/csv/my_demo \
  --chi-kappa 0.04 \
  --I-mode step
```

### `sweep`

Sweep a single IEC parameter and record outputs.

**Usage:**
```bash
poetry run spinalmodes iec sweep [OPTIONS]
```

**Required Options:**
- `--param TEXT`: Parameter to sweep (`chi_kappa`, `chi_E`, `chi_C`, `chi_f`)
- `--start FLOAT`: Start value
- `--stop FLOAT`: Stop value
- `--steps INT`: Number of steps

**Optional:**
- `--I-mode TEXT`: Coherence field mode (default: `linear`)
- `--out-csv TEXT`: Output CSV file (default: `outputs/csv/iec_sweep.csv`)

**Outputs:**
- CSV with columns: `{param}`, `wavelength_mm`, `amplitude_deg`, `num_nodes`, `frequency_hz`, `damping_ratio`

**Example:**
```bash
poetry run spinalmodes iec sweep \
  --param chi_kappa \
  --start 0.0 \
  --stop 0.06 \
  --steps 13 \
  --I-mode linear \
  --out-csv outputs/csv/chi_kappa_sweep.csv
```

### `phase`

Generate phase diagram for IEC parameters (asymmetry vs. information gradient).

**Usage:**
```bash
poetry run spinalmodes iec phase [OPTIONS]
```

**Required Options:**
- `--delta-b TEXT`: Delta B range in format `start:stop:steps` (e.g., `0.0:0.2:41`)
- `--gradI TEXT`: Gradient I range in format `start:stop:steps` (e.g., `0.0:0.1:21`)

**Optional:**
- `--out-csv TEXT`: Output CSV file (default: `outputs/csv/iec_phase_map.csv`)
- `--out-fig TEXT`: Output figure (default: `outputs/figs/fig_iec_phase.png`)

**Outputs:**
- CSV with columns: `delta_b`, `gradI`, `threshold`, `stable_mode`, `threshold_reached`, `notes`
- PNG figure with phase diagram
- JSON metadata sidecar

**Example:**
```bash
poetry run spinalmodes iec phase \
  --delta-b 0.0:0.2:41 \
  --gradI 0.0:0.1:21 \
  --out-csv outputs/csv/phase_map.csv \
  --out-fig outputs/figs/phase_diagram.png
```

### `node-drift`

Demonstrate node position drift due to IEC-1 coupling.

**Usage:**
```bash
poetry run spinalmodes iec node-drift [OPTIONS]
```

**Options:**
- `--I-mode TEXT`: Coherence field mode (default: `step`)
- `--chi-kappa FLOAT`: Target curvature coupling (default: 0.04)
- `--out-fig TEXT`: Output figure (default: `outputs/figs/fig_iec_node_drift.png`)

**Outputs:**
- PNG figure showing baseline vs. IEC-1 angle profiles and node positions
- JSON metadata sidecar with drift statistics

**Example:**
```bash
poetry run spinalmodes iec node-drift \
  --I-mode step \
  --chi-kappa 0.04 \
  --out-fig outputs/figs/node_drift_demo.png
```

### `helical-threshold`

Plot helical threshold shift with information gradient.

**Usage:**
```bash
poetry run spinalmodes iec helical-threshold [OPTIONS]
```

**Options:**
- `--gradI FLOAT`: Information gradient magnitude (default: 0.05)
- `--out-fig TEXT`: Output figure (default: `outputs/figs/fig_iec_threshold.png`)

**Outputs:**
- PNG figure showing threshold vs. χ_f
- JSON metadata sidecar

**Example:**
```bash
poetry run spinalmodes iec helical-threshold \
  --gradI 0.08 \
  --out-fig outputs/figs/threshold_analysis.png
```

## Output Directory Structure

The CLI creates outputs in the following structure:

```
outputs/
├── csv/          # Data tables
│   ├── iec_demo.csv
│   ├── iec_sweep.csv
│   └── iec_phase_map.csv
├── figs/         # Figures (PNG + JSON sidecars)
│   ├── fig_iec_phase.png
│   ├── fig_iec_phase.json
│   ├── fig_iec_node_drift.png
│   └── fig_iec_node_drift.json
├── aor/          # Analysis of record
└── reports/      # Generated reports
```

## Validation

After generating figures, run the validation tool:

```bash
poetry run python tools/validate_figures.py
```

This checks:
- PNG DPI ≥ 300
- Width 1800–3600 px
- No alpha channel
- Sidecar JSON present
- CSV headers and row counts

## Tips

1. **Parallel Runs:** Use different `--out-prefix` values to run multiple analyses simultaneously
2. **Large Sweeps:** For extensive parameter sweeps, consider using a job scheduler or parallelization
3. **Debugging:** Add `--help` to any command to see detailed options
4. **Reproducibility:** JSON sidecars record all parameters for exact reproduction

## Environment Variables

- `SPINALMODES_OUTPUT_DIR`: Override default output directory (default: `outputs/`)
- `SPINALMODES_CACHE_DIR`: Cache directory for intermediate results

## See Also

- [Figure Guide](figures.md)
- [Manuscript](manuscript/SpinalCountercurvature_IEC.md)
- [GitHub Repository](https://github.com/[username]/spinalmodes)

