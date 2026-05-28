# Experiments

This directory contains simulation experiments and parameter sweeps.

## Standard Interface

New experiments should use the `StandardExperimentParser` from `experiment_utils.py` to ensure a consistent CLI.

### Usage

```python
from experiment_utils import StandardExperimentParser, setup_experiment

def main():
    parser = StandardExperimentParser(description="Experiment Description")
    # Add custom arguments if needed
    parser.add_argument("--my-arg", type=int, default=10)

    args = parser.parse_args()
    out_dir = setup_experiment(args)

    # Run experiment...
    # Use args.quick to reduce sweep size for testing
```

### Standard Arguments

All scripts inheriting from `StandardExperimentParser` support:

- `--out-dir`: Directory to save results (default: `outputs/sim/{YYYY-MM-DD}`).
- `--quick`: Run a reduced set of parameters for testing.
- `--debug`: Enable verbose debug logging.

## Directory Structure

- `experiment_utils.py`: Shared utilities for experiments.
- `experiment_*.py`: General experiments (often reproducible or long-lived).
- `weekly_sim_*.py`: Specific simulations tied to weekly research goals.
- `run_*.py`: Legacy scripts (consider refactoring or using as wrappers).

## NVIDIA Warp Acceleration

`experiment_nvidia_warp_beam_sweep.py` is an optional GPU screening layer for
large Euler-Bernoulli beam sweeps. It does not replace the PyElastica
Cosserat-rod validation path; it is used to triage high-risk parameter regimes
before slower nonlinear simulations.

```bash
python scripts/experiments/experiment_nvidia_warp_beam_sweep.py \
  --n-samples 100000 \
  --device auto \
  --out-dir results/nvidia_warp_beam_sweep \
  --refine-pyelastica \
  --refine-count 3 \
  --refine-max-sag-ratio 2.0
```

Install the optional dependency with `pip install warp-lang` if it is not
already present.
