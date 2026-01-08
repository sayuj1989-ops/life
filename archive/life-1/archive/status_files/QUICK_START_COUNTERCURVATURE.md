# Quick Start: Running Countercurvature Experiments

## The Problem

On macOS, Python 3 is typically accessed via `python3` (not `python`). Also, the package needs to be on the Python path.

## Solution 1: Use the Helper Script (Easiest)

```bash
# Run all experiments
./run_experiments.sh all

# Or run individual experiments
./run_experiments.sh spine
./run_experiments.sh microgravity
./run_experiments.sh plant
./run_experiments.sh figure
```

## Solution 2: Use python3 with PYTHONPATH

```bash
# Set PYTHONPATH and use python3
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Run experiments
python3 -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity
python3 -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation
python3 -m spinalmodes.experiments.countercurvature.experiment_plant_upward_growth
python3 -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
```

## Solution 3: Install Package in Development Mode

```bash
# Install the package so you can import it directly
pip3 install -e .

# Then you can use python3 directly
python3 -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity
```

## Solution 4: Create an Alias (Optional)

Add to your `~/.zshrc`:

```bash
alias python='python3'
export PYTHONPATH="${PYTHONPATH}:${HOME}/LIFE/life/src"
```

Then reload:
```bash
source ~/.zshrc
```

## Verify It Works

```bash
# Quick test
PYTHONPATH=src python3 -c "from spinalmodes.countercurvature import compute_countercurvature_metric; print('✅ Success!')"
```

## Output Files

After running experiments, you'll find:

- **CSV data**: `outputs/experiments/*/summary.csv` and `results.csv`
- **Figures**: `outputs/experiments/*/figure.png`
- **Publication figure**: `outputs/figs/fig_countercurvature_metrics.png`

## Check Results

```bash
# View summary metrics
cat outputs/experiments/spine_modes/spine_modes_summary.csv

# Should show columns including D_geo and D_geo_norm
```

