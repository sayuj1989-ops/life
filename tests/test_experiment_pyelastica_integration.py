"""
Integration test for the protein simulation experiment script.

This test ensures that `scripts/experiments/experiment_protein_simulation_pyelastica.py`
can be executed successfully and produces the expected artifacts.
"""

import csv
import os
import subprocess
import sys
from pathlib import Path

import pytest

# Path to the experiment script
SCRIPT_PATH = Path("scripts/experiments/experiment_protein_simulation_pyelastica.py")
OUTPUT_DIR = Path("outputs/tests/pyelastica_integration")
OUTPUT_CSV = OUTPUT_DIR / "results.csv"

def test_experiment_script_execution():
    """
    Test that the experiment script runs without error in quick-test mode
    and generates valid output files.
    """
    if not SCRIPT_PATH.exists():
        pytest.fail(f"Experiment script not found at {SCRIPT_PATH}")

    # Ensure output directory is clean-ish
    if OUTPUT_CSV.exists():
        os.remove(OUTPUT_CSV)

    # Construct command
    cmd = [
        sys.executable,
        str(SCRIPT_PATH),
        "--quick-test",
        "--out-file", str(OUTPUT_CSV)
    ]

    # Run the script
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": os.getcwd()}
    )

    # Check for successful execution
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    # Verify artifacts
    assert OUTPUT_CSV.exists(), "Output CSV was not created."

    # Verify CSV content
    with open(OUTPUT_CSV, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) > 0, "CSV is empty."

        # Check for key columns
        expected_columns = [
            "bio_label", "input_anisotropy", "cobb_angle", "u_cc", "runtime_sec"
        ]
        for col in expected_columns:
            assert col in rows[0], f"Column {col} missing in CSV."

    # Verify Markdown report
    md_file = OUTPUT_CSV.with_suffix(".md")
    assert md_file.exists(), "Markdown report was not created."

    # Check stdout for success message
    assert "Experiment Summary" in result.stdout or "Parameters" in result.stdout
