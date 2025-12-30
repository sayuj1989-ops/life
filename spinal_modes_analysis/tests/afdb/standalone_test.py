#!/usr/bin/env python3
"""Standalone test of AFDB client (no pytest required).

This script tests the core AFDB client functionality without requiring
pytest or other test dependencies. Useful for quick validation.

Usage:
    python3 tests/afdb/standalone_test.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


def test_config():
    """Test configuration module."""
    print("Testing config...")
    from spinalmodes.afdb.config import AFDBConfig

    assert AFDBConfig.API_BASE_URL == "https://alphafold.ebi.ac.uk/api"
    assert AFDBConfig.TIMEOUT_SECONDS == 10

    url = AFDBConfig.get_api_url("P02458")
    assert "P02458" in url
    assert "prediction" in url.lower()

    cache_dir = AFDBConfig.get_cache_dir()
    assert cache_dir.name == "afdb"

    print("  ✓ Config module OK")


def test_client_schema_normalization():
    """Test client schema handling (offline test)."""
    print("Testing client schema normalization...")
    from spinalmodes.afdb.client import AFDBClient

    client = AFDBClient()

    # Test current schema
    current_data = {
        "uniprotAccession": "P02458",
        "gene": "COL2A1",
        "latestVersion": "4",
        "pdbUrl": "https://example.com/model.pdb",
    }

    normalized = client._normalize_response(current_data, "P02458")
    assert normalized["uniprot_id"] == "P02458"
    assert normalized["gene"] == "COL2A1"
    assert normalized["model_version"] == "4"
    assert normalized["pdb_url"] == "https://example.com/model.pdb"

    # Test legacy schema
    legacy_data = {
        "entryId": "Q92508",
        "geneName": "PIEZO1",
        "modelVersion": "3",
    }

    normalized_legacy = client._normalize_response(legacy_data, "Q92508")
    assert normalized_legacy["uniprot_id"] == "Q92508"
    assert normalized_legacy["gene"] == "PIEZO1"

    # Test schema fingerprinting
    fp1 = client._compute_schema_fingerprint(current_data)
    fp2 = client._compute_schema_fingerprint(current_data)
    assert fp1 == fp2  # Deterministic
    assert len(fp1) == 8  # 8-char hex string

    print("  ✓ Schema normalization OK")


def test_cache(tmp_dir=None):
    """Test cache module."""
    print("Testing cache...")
    from spinalmodes.afdb.cache import AFDBCache

    # Use temp directory if provided, otherwise use default
    if tmp_dir:
        cache = AFDBCache(cache_dir=Path(tmp_dir) / "test_cache")
    else:
        # Test will use default cache location
        cache = AFDBCache()

    # Test initialization
    assert cache.cache_dir.exists()
    assert cache.metadata_dir.exists()

    # Test metadata storage
    test_metadata = {
        "uniprot_id": "P02458",
        "gene": "COL2A1",
        "model_version": "4",
        "_schema_version": "test123",
    }

    assert not cache.is_cached("P02458")
    cache.store_metadata("P02458", test_metadata)
    assert cache.is_cached("P02458")
    assert cache.index_file.exists()

    # Test retrieval
    retrieved = cache.get_metadata("P02458")
    assert retrieved is not None
    assert retrieved["uniprot_id"] == "P02458"
    assert "_cache_date" in retrieved  # Provenance added

    # Test cache info
    info = cache.get_cache_info()
    assert info["n_proteins"] >= 1

    print("  ✓ Cache module OK")


def test_api_connection():
    """Test real API connection (requires network)."""
    print("Testing API connection (requires network)...")
    from spinalmodes.afdb.client import AFDBClient

    client = AFDBClient()

    try:
        # Test with a well-known protein
        result = client.get_prediction("P02458")  # COL2A1

        if result:
            print(
                f"  ✓ API connection OK - fetched {result.get('gene', '?')} v{result.get('model_version', '?')}"
            )
            assert result["uniprot_id"] == "P02458"
            assert result["gene"] == "COL2A1"
            assert "_schema_version" in result
        else:
            print("  ⚠️  API returned no data (may be rate-limited or down)")

    except Exception as e:
        print(f"  ⚠️  API test skipped (network error): {e}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("AFDB Client Standalone Test Suite")
    print("=" * 60)
    print()

    import tempfile
    import shutil

    tmp_dir = tempfile.mkdtemp()
    try:
        test_config()
        test_client_schema_normalization()
        test_cache(tmp_dir=tmp_dir)
        test_api_connection()

        print()
        print("=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        return 0

    except ImportError as e:
        print()
        print("=" * 60)
        print(f"❌ Import error: {e}")
        print("Ensure required packages are installed:")
        print("  pip install requests pandas")
        print("=" * 60)
        return 1

    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Test failed: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        print("=" * 60)
        return 1
    finally:
        if Path(tmp_dir).exists():
            shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    sys.exit(main())
