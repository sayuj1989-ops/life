"""
Tests for the Reissner Resonance Experiment script.
"""

import sys
import os
import shutil
from pathlib import Path
import pytest

# Add scripts/experiments to path so we can import the script as a module
# Repo root is 2 levels up from tests/
repo_root = Path(__file__).resolve().parent.parent
scripts_exp_path = repo_root / "scripts" / "experiments"

if str(scripts_exp_path) not in sys.path:
    sys.path.append(str(scripts_exp_path))

try:
    from experiment_reissner_resonance import run_resonance_experiment
    from spinalmodes.countercurvature.pyelastica_bridge import PYELASTICA_AVAILABLE
except ImportError:
    # If imports fail (e.g. if run from wrong dir), we might need to adjust path or skip
    PYELASTICA_AVAILABLE = False

    # Mock for import failure if needed, but pytest should handle ImportErrors as failures usually
    # unless we skip.

@pytest.mark.skipif(not PYELASTICA_AVAILABLE, reason="PyElastica not available")
def test_reissner_resonance_quick():
    """Test the resonance experiment script runs without error in quick mode."""
    out_dir = "outputs/test_reissner"

    # Cleanup previous run
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    # Run the experiment
    # We use quick_test=True which sets duration=0.1 and elements=20
    results = run_resonance_experiment(
        out_dir=out_dir,
        frequencies=[1.0],
        duration=0.1,
        quick_test=True
    )

    # Assertions
    assert results is not None
    assert len(results) == 1

    row = results[0]
    assert row["frequency_hz"] == 1.0
    assert "max_cobb_angle" in row
    assert "total_energy" in row

    # Check output artifacts
    csv_path = Path(out_dir) / "resonance_results.csv"
    md_path = Path(out_dir) / "resonance_report.md"

    assert csv_path.exists()
    assert md_path.exists()

    # Clean up
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
