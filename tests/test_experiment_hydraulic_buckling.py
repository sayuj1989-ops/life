"""
Test for Hydraulic Buckling Experiment.

Verifies that the experiment script runs successfully and produces expected artifacts.
"""

import sys
import os
import subprocess
from pathlib import Path

def test_hydraulic_buckling_execution():
    """
    Run the experiment script with --quick-test flag.
    Verify:
    1. Exit code is 0 (Success).
    2. Output artifacts exist.
    """
    script_path = Path("scripts/experiments/experiment_hydraulic_buckling.py")

    # Run script
    result = subprocess.run(
        [sys.executable, str(script_path), "--quick-test"],
        capture_output=True,
        text=True
    )

    # Check execution
    if result.returncode != 0:
        print("Script execution failed:")
        print(result.stdout)
        print(result.stderr)
    assert result.returncode == 0, "Experiment script failed to execute."

    # Check artifacts
    figures_dir = Path("outputs/figures")
    reports_dir = Path("reports")

    assert (figures_dir / "hydraulic_buckling_dynamics.png").exists(), "Plot not generated."
    assert (reports_dir / "hydraulic_buckling_report.md").exists(), "Report not generated."

    # Check if report contains content
    report_content = (reports_dir / "hydraulic_buckling_report.md").read_text()
    assert "Hydraulic Buckling Experiment Report" in report_content
    assert "## Results Summary" in report_content
    assert "## Proprioceptive Mismatch" in report_content

if __name__ == "__main__":
    test_hydraulic_buckling_execution()
    print("Test Passed: Hydraulic Buckling Experiment verified.")
