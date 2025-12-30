"""Configuration for AlphaFold Database integration."""

import os
from pathlib import Path
from typing import Optional


class AFDBConfig:
    """Configuration for AFDB client and caching.

    Attributes:
        api_base_url: Base URL for AFDB REST API
        timeout_seconds: Request timeout
        max_retries: Maximum retry attempts for failed requests
        retry_backoff_factor: Exponential backoff multiplier
        rate_limit_delay: Minimum delay between requests (seconds)
        cache_dir: Directory for cached structures and metadata
        user_agent: User agent string for API requests
    """

    # API endpoints
    API_BASE_URL = "https://alphafold.ebi.ac.uk/api"
    PREDICTION_ENDPOINT = "/prediction/{uniprot_id}"

    # Request settings
    TIMEOUT_SECONDS = 10
    MAX_RETRIES = 3
    RETRY_BACKOFF_FACTOR = 2.0  # 1s, 2s, 4s delays
    RATE_LIMIT_DELAY = 0.07  # ~15 requests/second (EMBL-EBI limit)

    # Cache settings
    DEFAULT_CACHE_DIR = Path.home() / ".spinalmodes_cache" / "afdb"

    # User agent
    USER_AGENT = "spinalmodes-afdb-client/0.1.0 (research use)"

    @classmethod
    def get_cache_dir(cls) -> Path:
        """Get cache directory, respecting environment variable override.

        Returns:
            Path to cache directory (will be created if doesn't exist)
        """
        cache_dir_str = os.environ.get("SPINALMODES_CACHE_DIR")
        if cache_dir_str:
            cache_dir = Path(cache_dir_str) / "afdb"
        else:
            cache_dir = cls.DEFAULT_CACHE_DIR

        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    @classmethod
    def get_api_url(cls, uniprot_id: str) -> str:
        """Construct API URL for a UniProt accession.

        Args:
            uniprot_id: UniProt accession (e.g., 'P02458')

        Returns:
            Full API URL for prediction endpoint
        """
        endpoint = cls.PREDICTION_ENDPOINT.format(uniprot_id=uniprot_id)
        return cls.API_BASE_URL + endpoint
