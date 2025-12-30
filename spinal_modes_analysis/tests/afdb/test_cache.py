"""Tests for AFDB cache module."""

import json
import pytest
from pathlib import Path

from spinalmodes.afdb.cache import AFDBCache


class TestAFDBCache:
    """Test suite for AFDBCache."""

    @pytest.fixture
    def temp_cache(self, tmp_path):
        """Create cache in temporary directory."""
        cache_dir = tmp_path / "afdb_test_cache"
        return AFDBCache(cache_dir=cache_dir)

    @pytest.fixture
    def sample_metadata(self):
        """Sample metadata dictionary."""
        return {
            "uniprot_id": "P02458",
            "gene": "COL2A1",
            "organism": "Homo sapiens",
            "model_version": "4",
            "pdb_url": "https://example.com/AF-P02458-F1-model_v4.cif",
            "_schema_version": "abc12345",
        }

    def test_cache_initialization(self, temp_cache):
        """Test cache directory creation."""
        assert temp_cache.cache_dir.exists()
        assert temp_cache.metadata_dir.exists()
        assert temp_cache.structures_dir.exists()
        assert temp_cache.index_file.exists()

    def test_store_and_retrieve_metadata(self, temp_cache, sample_metadata):
        """Test metadata storage and retrieval."""
        # Store
        path = temp_cache.store_metadata("P02458", sample_metadata)
        assert path.exists()

        # Retrieve
        retrieved = temp_cache.get_metadata("P02458")
        assert retrieved is not None
        assert retrieved["uniprot_id"] == "P02458"
        assert retrieved["gene"] == "COL2A1"
        assert "_cache_date" in retrieved  # Provenance added

    def test_cache_hit(self, temp_cache, sample_metadata):
        """Test cache hit detection."""
        assert not temp_cache.is_cached("P02458")

        temp_cache.store_metadata("P02458", sample_metadata)

        assert temp_cache.is_cached("P02458")

    def test_index_update(self, temp_cache, sample_metadata):
        """Test cache index is updated correctly."""
        temp_cache.store_metadata("P02458", sample_metadata)

        # Check index
        assert len(temp_cache.index) == 1
        row = temp_cache.index.iloc[0]
        assert row["uniprot_id"] == "P02458"
        assert row["gene"] == "COL2A1"
        assert row["model_version"] == "4"
        assert row["schema_version"] == "abc12345"

    def test_index_persistence(self, temp_cache, sample_metadata):
        """Test index is saved and reloaded correctly."""
        temp_cache.store_metadata("P02458", sample_metadata)

        # Create new cache instance pointing to same directory
        new_cache = AFDBCache(cache_dir=temp_cache.cache_dir)

        # Should reload index from disk
        assert len(new_cache.index) == 1
        assert new_cache.is_cached("P02458")

    def test_cache_info(self, temp_cache, sample_metadata):
        """Test cache statistics."""
        info_empty = temp_cache.get_cache_info()
        assert info_empty["n_proteins"] == 0

        temp_cache.store_metadata("P02458", sample_metadata)

        info = temp_cache.get_cache_info()
        assert info["n_proteins"] == 1
        assert info["cache_dir"] == str(temp_cache.cache_dir)
        assert info["total_size_mb"] > 0  # Metadata file has size

    def test_get_nonexistent_metadata(self, temp_cache):
        """Test retrieval of non-existent protein."""
        result = temp_cache.get_metadata("NONEXISTENT")
        assert result is None

    def test_atomic_writes(self, temp_cache, sample_metadata):
        """Test that writes are atomic (no partial files)."""
        # This is hard to test directly, but we verify no .tmp files remain
        temp_cache.store_metadata("P02458", sample_metadata)

        tmp_files = list(temp_cache.metadata_dir.glob("*.tmp"))
        assert len(tmp_files) == 0
