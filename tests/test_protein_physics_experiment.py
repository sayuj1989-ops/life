
import os
import pytest
import csv
from pathlib import Path

# Import the module unconditionally
import experiment_protein_physics

@pytest.mark.skipif(
    not experiment_protein_physics.PYELASTICA_AVAILABLE,
    reason="PyElastica not installed"
)
def test_run_protein_experiment_integration(tmp_path):
    """
    Test that the protein physics experiment script runs and produces expected output.
    """

    out_file = tmp_path / "test_protein_results.csv"

    # Use specific scenario to limit run time
    selected_scenarios = ["Control"]

    # Run with short time and few elements
    experiment_protein_physics.run_protein_experiment(
        out_file=str(out_file),
        selected_scenarios=selected_scenarios,
        n_elements=10,
        final_time=0.01,
        save_every=100
    )

    assert out_file.exists()

    with open(out_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 1
    row = rows[0]

    # Verify scenario data
    assert row["scenario_name"] == "Control"
    assert "stiffness_anisotropy" in row
    assert float(row["stiffness_anisotropy"]) == 2.0  # Control has 2.0

    # Verify metrics
    assert "max_curvature" in row
    assert float(row["max_curvature"]) >= 0.0
    assert "runtime_sec" in row
    assert "peak_memory_mb" in row

@pytest.mark.skipif(
    not experiment_protein_physics.PYELASTICA_AVAILABLE,
    reason="PyElastica not installed"
)
def test_run_protein_experiment_multiple_scenarios(tmp_path):
    """
    Test running multiple scenarios.
    """
    out_file = tmp_path / "test_multi_results.csv"

    selected_scenarios = ["Control", "Fibrillin_Loss"]

    experiment_protein_physics.run_protein_experiment(
        out_file=str(out_file),
        selected_scenarios=selected_scenarios,
        n_elements=10,
        final_time=0.01
    )

    with open(out_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 2
    names = {r["scenario_name"] for r in rows}
    assert "Control" in names
    assert "Fibrillin_Loss" in names
