
import sys
import os
import pytest
import csv
from pathlib import Path

# Add scripts directory to path to allow importing the script as a module
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.append(str(SCRIPTS_DIR))

# Import the module unconditionally.
# It should be importable since we added scripts to sys.path
import experiment_minimal_elastica

@pytest.mark.skipif(
    not experiment_minimal_elastica.PYELASTICA_AVAILABLE,
    reason="PyElastica not installed"
)
def test_run_experiment_integration(tmp_path):
    """
    Test that the minimal experiment script runs and produces expected output.
    Uses a very short simulation time and few elements for speed.
    """

    out_file = tmp_path / "test_results.csv"

    # Minimal configuration
    anisotropies = [1.0]
    chi_kappas = [0.0]
    chi_taus = [1.0] # Test non-zero torsion
    boundary_condition = "fixed"
    n_elements = 10
    final_time = 0.01 # Very short time

    experiment_minimal_elastica.run_experiment(
        out_file=str(out_file),
        anisotropies=anisotropies,
        chi_kappas=chi_kappas,
        chi_taus=chi_taus,
        boundary_condition=boundary_condition,
        n_elements=n_elements,
        final_time=final_time,
        save_every=100
    )

    assert out_file.exists()

    with open(out_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 1
    row = rows[0]

    # Check if new column exists
    assert "chi_tau" in row
    assert float(row["chi_tau"]) == 1.0

    # Check if metrics are present
    assert "max_curvature" in row
    assert "max_torsion" in row

    # Check for NaN (basic stability check)
    assert row["max_curvature"] != "nan"

@pytest.mark.skipif(
    not experiment_minimal_elastica.PYELASTICA_AVAILABLE,
    reason="PyElastica not installed"
)
def test_run_experiment_custom_info(tmp_path):
    """
    Test that custom info field parameters are passed correctly and recorded.
    """
    out_file = tmp_path / "test_custom_info.csv"

    experiment_minimal_elastica.run_experiment(
        out_file=str(out_file),
        anisotropies=[1.0],
        chi_kappas=[0.0],
        chi_taus=[0.0],
        boundary_condition="fixed",
        n_elements=10,
        final_time=0.01,
        info_center=0.5,
        info_width=0.2,
        info_amplitude=0.3,
        save_every=100
    )

    assert out_file.exists()

    with open(out_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 1
    row = rows[0]

    assert float(row["info_center"]) == 0.5
    assert float(row["info_width"]) == 0.2
    assert float(row["info_amplitude"]) == 0.3
