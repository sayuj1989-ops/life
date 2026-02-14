import sys
import subprocess
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import pandas as pd
import datetime

# Add scripts directory to path to import afcc_daily_refresh
scripts_path = Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(scripts_path))

import afcc_daily_refresh

def test_run_pipeline_calls_scripts():
    """Test that run_pipeline calls the correct scripts via subprocess."""
    with patch("subprocess.check_call") as mock_check_call:
        afcc_daily_refresh.run_pipeline()

        # Verify two calls
        assert mock_check_call.call_count == 2

        # Verify arguments
        calls = mock_check_call.call_args_list
        fetch_call = calls[0][0][0]
        analyze_call = calls[1][0][0]

        assert sys.executable in fetch_call
        assert "02_fetch_afdb.py" in fetch_call[1]

        assert sys.executable in analyze_call
        assert "04_analyze_metrics.py" in analyze_call[1]

def test_generate_outputs_failure(tmp_path):
    """Test that generate_outputs creates failure.md if metrics file is missing."""
    # Mock paths
    original_outputs_dir = afcc_daily_refresh.OUTPUTS_DIR
    original_data_processed = afcc_daily_refresh.DATA_PROCESSED

    afcc_daily_refresh.OUTPUTS_DIR = tmp_path / "outputs"
    afcc_daily_refresh.DATA_PROCESSED = tmp_path / "processed"
    afcc_daily_refresh.OUTPUTS_DIR.mkdir()
    afcc_daily_refresh.DATA_PROCESSED.mkdir()

    try:
        # Run generate_outputs (without creating metrics file)
        res = afcc_daily_refresh.generate_outputs()

        # Should return None
        assert res is None

        # Check for failure.md
        today = datetime.date.today().isoformat()
        failure_path = afcc_daily_refresh.OUTPUTS_DIR / today / "failure.md"
        assert failure_path.exists()

        content = failure_path.read_text()
        assert "Failure Report" in content
        assert "Metrics file was not generated" in content

    finally:
        afcc_daily_refresh.OUTPUTS_DIR = original_outputs_dir
        afcc_daily_refresh.DATA_PROCESSED = original_data_processed

def test_generate_outputs_success(tmp_path):
    """Test that generate_outputs creates metrics.csv and summary.md if metrics file exists."""
    # Mock paths
    original_outputs_dir = afcc_daily_refresh.OUTPUTS_DIR
    original_data_processed = afcc_daily_refresh.DATA_PROCESSED

    afcc_daily_refresh.OUTPUTS_DIR = tmp_path / "outputs"
    afcc_daily_refresh.DATA_PROCESSED = tmp_path / "processed"
    afcc_daily_refresh.OUTPUTS_DIR.mkdir()
    afcc_daily_refresh.DATA_PROCESSED.mkdir()

    try:
        # Create dummy metrics file
        metrics_data = {
            'gene_symbol': ['TEST1'],
            'anisotropy_index': [5.0],
            'plddt_mean': [90.0],
            'morphology': ['Fibrous']
        }
        pd.DataFrame(metrics_data).to_csv(afcc_daily_refresh.DATA_PROCESSED / "protein_metrics.csv", index=False)

        # Run generate_outputs
        res = afcc_daily_refresh.generate_outputs()

        # Should return path and lines
        assert res is not None
        summary_path, lines = res

        assert summary_path.exists()
        today = datetime.date.today().isoformat()
        assert (afcc_daily_refresh.OUTPUTS_DIR / today / "metrics.csv").exists()

    finally:
        afcc_daily_refresh.OUTPUTS_DIR = original_outputs_dir
        afcc_daily_refresh.DATA_PROCESSED = original_data_processed
