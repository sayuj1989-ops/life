# Reproducibility Guide

This guide details the steps required to reproduce the computational results presented in the *Bio-Gravitational Number* and *Information-Elasticity Coupling* research. The repository provides a vertically integrated pipeline, spanning from AlphaFold structure retrieval to macroscopic Cosserat rod simulations.

## 1. System Requirements

### Hardware
- **CPU**: Standard x86-64 processor (Intel/AMD). Multi-core recommended for parameter sweeps.
- **Memory**: 16 GB RAM minimum recommended for AlphaFold analysis and large-scale simulations.
- **Storage**: ~5 GB for repository and initial data (excluding full AlphaFold database downloads).
- **GPU**: Optional. PyElastica runs efficiently on CPU; GPU acceleration is not currently implemented in the main pipeline.

### Software
- **OS**: Linux (Ubuntu 20.04+ recommended) or macOS (12+). Windows users should use WSL2.
- **Python**: Version 3.10 or higher.
- **Git**: For version control.

## 2. Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Set up Virtual Environment**:
    We recommend using `venv` or `conda`.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Verify Environment**:
    Ensure the `src` directory is in your `PYTHONPATH` (though scripts are designed to handle this automatically, explicit setting is robust):
    ```bash
    export PYTHONPATH=$PYTHONPATH:$(pwd)/src:$(pwd)
    ```

## 3. Quick Start: Verify Simulation Engine

To verify that the physics engine (PyElastica + SpinalModes) is working correctly without fetching external data, run the self-contained protein simulation experiment.

**Command:**
```bash
python scripts/experiments/reproducible_protein_sim.py
```

**Expected Output:**
- Terminal output showing simulation progress for different profiles (e.g., "WildType_Control", "Marfan_Like").
- A generated report at `outputs/reproducible_protein_sim/report.md`.
- A CSV file at `outputs/reproducible_protein_sim/results.csv`.

## 4. Full Pipeline: Data Acquisition & Analysis

The data pipeline fetches AlphaFold structures for candidate proteins, analyzes their geometry (curvature, anisotropy), and prepares them for simulation.

### Step 4.1: Candidate Selection
The pipeline reads from `data/candidates_master.csv`. Ensure this file exists and contains valid gene symbols.

### Step 4.2: Run Daily Refresh
This script orchestrates fetching, parsing, and analyzing structures.

**Command:**
```bash
# Process the top 5 candidates
python scripts/data_management/afcc_daily_refresh.py --top-n 5
```

**Outputs:**
- `research/alphafold_countercurvature/data/processed/metrics.csv`: Computed metrics (Anisotropy, Radius of Gyration, etc.).
- `reports/afcc_latest.md`: A summary dashboard of the latest run.

## 5. Simulation Experiments

Once protein metrics are established, or using theoretical values, you can run macroscopic simulations of spinal growth.

### Example: Growth vs. Anisotropy Phase Diagram
This experiment maps the stability landscape of the spine by varying Stiffness Anisotropy and Growth Drive.

**Command:**
```bash
python scripts/experiments/weekly_sim_growth_anisotropy_phase.py
```

**Outputs:**
- Located in `outputs/sim/<date>/`.
- `phase_diagram_growth_anisotropy.png`: Heatmap of spinal instability.
- `report.md`: Summary of findings.

## 6. Directory Structure Reference

- **`src/`**: Core libraries.
    - `spinalmodes`: Physics engine and counter-curvature logic.
    - `alphafold`: Utilities for PDB parsing and geometric analysis.
- **`scripts/`**: Executable scripts.
    - `data_management/`: Data fetching and processing pipelines.
    - `experiments/`: Simulation sweeps and hypothesis tests.
- **`data/`**: Input data (candidate lists).
- **`research/`**: Research-specific modules and local data storage.
- **`outputs/`**: Generated artifacts (plots, reports, CSVs).
- **`docs/`**: Documentation.

## 7. Troubleshooting

- **`ModuleNotFoundError`**: Ensure you are running scripts from the repository root and that `PYTHONPATH` includes `src`.
- **PyElastica Errors**: Ensure `pyelastica` is installed correctly. Numba compilation may take time on the first run.
- **AlphaFold Fetch Failures**: Requires internet access. Rate limits from the AlphaFold DB may apply. The script includes basic error handling and will skip failed downloads.
