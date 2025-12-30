# Data Directory

This directory contains datasets used in the manuscript.

## Structure

- **`derived/`** - Small derived datasets that support manuscript claims (tracked in git)
  - Example: Aggregated statistics, processed results tables
  - These files should be small (<100 KB) and reproducible from raw data

- **`external/`** - Large external datasets (NOT tracked in git)
  - Example: AlphaFold structure downloads, raw experimental data
  - Add these files to `.gitignore` to keep repository size manageable
  - Document download sources in `derived/` metadata files

## Usage

All analysis scripts should:
1. Download external data to `data/external/` as needed
2. Process and save derived datasets to `data/derived/`
3. Use derived data for manuscript figures and tables

## Reproducibility

To reproduce the analysis:
```bash
# From repository root
make alphafold-all
```

This will:
- Download necessary external data
- Generate derived datasets
- Create manuscript figures
- Extract manuscript numbers
