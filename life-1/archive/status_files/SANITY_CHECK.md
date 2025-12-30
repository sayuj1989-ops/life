# Sanity Check: "Is the Machine Green?"

## Quick Verification Script

Run these commands to verify the codebase is operational:

```bash
# 1) All tests (if pytest is installed)
pytest -v

# 2) Quick experiments
python3 -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity --quick
python3 -m spinalmodes.experiments.countercurvature.experiment_phase_diagram --quick
python3 -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation --quick

# 3) Quick figure + demo
python3 -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
python3 examples/quickstart.py
```

## Expected Outputs

### Tests
- `test_pyelastica_bridge.py`: 2 tests (may skip if PyElastica not installed)
- `test_countercurvature_metrics.py`: 8 tests (should all pass)
- `test_iec.py`: Existing tests (should all pass)

### Experiments
- `outputs/experiments/spine_modes/spine_modes_results.csv` - Contains I(s), dIds, curvature profiles
- `outputs/experiments/spine_modes/spine_modes_summary.csv` - Contains D_geo_norm metrics
- `outputs/experiments/phase_diagram/phase_diagram_data.csv` - Contains S_lat, Cobb-like angles
- `outputs/experiments/microgravity/microgravity_summary.csv` - Contains D_geo_norm vs g

### Figures
- `outputs/figs/fig_countercurvature_metrics.png` - 4-panel countercurvature figure
- `outputs/examples/quickstart_curvature.png` - Quickstart demo plot

## Verification Checklist

- [ ] All tests pass (or skip gracefully for optional dependencies)
- [ ] All experiments run without errors
- [ ] CSV files are created with expected columns
- [ ] Figures are generated successfully
- [ ] Quickstart demo runs and produces plot

## If Something Fails

1. **Import errors**: Check `PYTHONPATH` includes `src/` directory
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

2. **Missing dependencies**: Install from `envs/requirements.txt` or `envs/environment.yml`

3. **PyElastica not available**: Tests will skip; experiments will use beam solver only

4. **File not found errors**: Run experiments first to generate data files

## Status

Once all checks pass, the codebase is **operationally complete** and ready for:
- Full parameter sweeps
- Data extraction for paper
- Publication submission

