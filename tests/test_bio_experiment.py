"""Test for the bio-countercurvature experiment script."""

import os
import pytest
from src.spinalmodes.countercurvature.pyelastica_bridge import PYELASTICA_AVAILABLE
from src.spinalmodes.experiments.bio_countercurvature_experiment import run_experiment

@pytest.mark.skipif(not PYELASTICA_AVAILABLE, reason="PyElastica not available")
def test_bio_experiment_runs(tmp_path):
    """
    Verify that the experiment runs without error and produces output.
    Uses a temporary file for output.
    """
    output_file = tmp_path / "experiment_report.txt"
    run_experiment(output_file=str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert "=== Results ===" in content
    assert "Max Curvature:" in content
