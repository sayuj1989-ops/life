# Environments

This directory contains historical and reproducible environment specifications.

**Important:** For active development, please refer to the root `pyproject.toml` (for Poetry) or `requirements.txt`.

## Contents

- `requirements.txt`: Pinned versions for reproducing the IEC model v0.2.0 (BVP solver upgrade).
- `environment.yml`: Conda environment file matching `requirements.txt` for v0.2.0.

These files are preserved to ensure exact reproducibility of past experiments and results. Do not modify them unless you are explicitly creating a new snapshot version.
