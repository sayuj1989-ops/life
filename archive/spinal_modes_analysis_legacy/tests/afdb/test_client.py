"""Tests for AFDB client module."""

import json
import pytest
from unittest.mock import Mock, patch

from spinalmodes.afdb.client import AFDBClient


class TestAFDBClient:
    """Test suite for AFDBClient."""

    @pytest.fixture
    def client(self):
        """Create client instance."""
        return AFDBClient()

    @pytest.fixture
    def mock_response_data(self):
        """Sample API response (current schema)."""
        return {
            "uniprotAccession": "P02458",
            "gene": "COL2A1",
            "organismScientificName": "Homo sapiens",
            "latestVersion": "4",
            "pdbUrl": "https://alphafold.ebi.ac.uk/files/AF-P02458-F1-model_v4.pdb",
            "cifUrl": "https://alphafold.ebi.ac.uk/files/AF-P02458-F1-model_v4.cif",
        }

    def test_normalize_current_schema(self, client, mock_response_data):
        """Test normalization of current API schema."""
        normalized = client._normalize_response(mock_response_data, "P02458")

        assert normalized["uniprot_id"] == "P02458"
        assert normalized["gene"] == "COL2A1"
        assert normalized["organism"] == "Homo sapiens"
        assert normalized["model_version"] == "4"
        assert "cif" in normalized["pdb_url"].lower()

    def test_normalize_legacy_schema(self, client):
        """Test handling of legacy field names."""
        legacy_data = {
            "entryId": "P02458",
            "geneName": "COL2A1",
            "modelVersion": "3",
            "modelUrl": "https://example.com/model.pdb",
        }

        normalized = client._normalize_response(legacy_data, "P02458")

        assert normalized["uniprot_id"] == "P02458"
        assert normalized["gene"] == "COL2A1"
        assert normalized["model_version"] == "3"

    def test_normalize_missing_fields(self, client):
        """Test graceful handling of missing fields."""
        minimal_data = {
            "uniprotAccession": "Q92508",
        }

        normalized = client._normalize_response(minimal_data, "Q92508")

        assert normalized["uniprot_id"] == "Q92508"
        assert normalized["gene"] is None
        assert normalized["pdb_url"] is None

    def test_schema_fingerprint(self, client, mock_response_data):
        """Test schema version fingerprinting."""
        fingerprint1 = client._compute_schema_fingerprint(mock_response_data)

        # Same fields → same fingerprint
        fingerprint2 = client._compute_schema_fingerprint(mock_response_data)
        assert fingerprint1 == fingerprint2

        # Different fields → different fingerprint
        altered_data = {**mock_response_data, "newField": "value"}
        fingerprint3 = client._compute_schema_fingerprint(altered_data)
        assert fingerprint1 != fingerprint3

    @patch("spinalmodes.afdb.client.requests.Session.get")
    def test_get_prediction_success(self, mock_get, client, mock_response_data):
        """Test successful API call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [mock_response_data]  # API returns list
        mock_get.return_value = mock_response

        result = client.get_prediction("P02458")

        assert result is not None
        assert result["uniprot_id"] == "P02458"
        assert result["gene"] == "COL2A1"
        assert "_schema_version" in result

    @patch("spinalmodes.afdb.client.requests.Session.get")
    def test_get_prediction_404(self, mock_get, client):
        """Test handling of protein not found."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = client.get_prediction("INVALID")

        assert result is None

    @patch("spinalmodes.afdb.client.requests.Session.get")
    def test_get_prediction_timeout(self, mock_get, client):
        """Test handling of request timeout."""
        import requests

        mock_get.side_effect = requests.exceptions.Timeout()

        result = client.get_prediction("P02458")

        assert result is None

    @patch("spinalmodes.afdb.client.requests.Session.get")
    def test_rate_limiting(self, mock_get, client):
        """Test that rate limiting introduces delays."""
        import time

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"uniprotAccession": "P02458"}]
        mock_get.return_value = mock_response

        # First call
        start = time.time()
        client.get_prediction("P02458")

        # Second call should be delayed
        client.get_prediction("Q92508")
        elapsed = time.time() - start

        # Should have at least one rate limit delay
        assert elapsed >= client.rate_limit_delay
