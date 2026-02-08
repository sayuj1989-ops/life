import sys
import os
import pandas as pd
import pytest
from pathlib import Path
import datetime

# Add scripts to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(REPO_ROOT / "scripts"))

import afcc_daily_refresh

def test_prepare_inputs(tmp_path):
    # Mock paths in the module
    original_data_processed = afcc_daily_refresh.DATA_PROCESSED
    afcc_daily_refresh.DATA_PROCESSED = tmp_path / "processed"
    afcc_daily_refresh.DATA_PROCESSED.mkdir()

    try:
        # Create dummy candidates df
        data = {
            'gene_symbol': ['GENE1', 'GENE2'],
            'uniprot_id': ['P12345', 'Q67890'],
            'pathway_tags': ['Path1', 'Path2'],
            'priority_score': [90, 80],
            'justification': ['Just1', 'Just2']
        }
        df = pd.DataFrame(data)

        # Run prepare_inputs
        afcc_daily_refresh.prepare_inputs(df)

        # Check uniprot_mapping.csv
        mapping_path = afcc_daily_refresh.DATA_PROCESSED / "uniprot_mapping.csv"
        assert mapping_path.exists()
        mapping_df = pd.read_csv(mapping_path)
        assert 'gene_symbol' in mapping_df.columns
        assert 'uniprot_accession' in mapping_df.columns
        assert len(mapping_df) == 2
        assert mapping_df.iloc[0]['uniprot_accession'] == 'P12345'

        # Check candidates.csv
        cand_path = afcc_daily_refresh.DATA_PROCESSED / "candidates.csv"
        assert cand_path.exists()
        cand_df = pd.read_csv(cand_path)
        assert 'gene_symbol' in cand_df.columns
        assert 'source' in cand_df.columns
        assert 'total_score' in cand_df.columns
        assert cand_df.iloc[0]['source'] == 'Path1'
        assert cand_df.iloc[0]['total_score'] == 90

    finally:
        afcc_daily_refresh.DATA_PROCESSED = original_data_processed

def test_generate_outputs(tmp_path):
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
            'gene_symbol': ['GENE1', 'GENE2'],
            'anisotropy_index': [4.5, 2.0],
            'plddt_mean': [80.0, 60.0],
            'morphology': ['Fibrous', 'Globular']
        }
        metrics_df = pd.DataFrame(metrics_data)
        metrics_path = afcc_daily_refresh.DATA_PROCESSED / "protein_metrics.csv"
        metrics_df.to_csv(metrics_path, index=False)

        # Run generate_outputs
        res = afcc_daily_refresh.generate_outputs()
        assert res is not None
        summary_path, lines = res

        # Check summary content
        content = "\n".join(lines)
        assert "GENE1" in content
        assert "4.50" in content
        assert "Tension Rods" in content
        assert "Structural Confidence" in content

        # Check output file exists
        assert summary_path.exists()
        assert (summary_path.parent / "metrics.csv").exists()

    finally:
        afcc_daily_refresh.OUTPUTS_DIR = original_outputs_dir
        afcc_daily_refresh.DATA_PROCESSED = original_data_processed
