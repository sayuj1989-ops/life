"""AlphaFold Database REST API client with schema-agnostic design.

This module implements a robust client for fetching protein structure predictions
from the AFDB REST API, with defensive programming to handle API schema changes.
"""

import hashlib
import logging
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import AFDBConfig

logger = logging.getLogger(__name__)


class AFDBClient:
    """Client for AlphaFold Database REST API.

    Features:
        - Schema-agnostic field extraction (handles API changes)
        - Automatic retries with exponential backoff
        - Rate limiting to respect EMBL-EBI limits
        - Schema version fingerprinting for reproducibility

    Example:
        >>> client = AFDBClient()
        >>> data = client.get_prediction("P02458")  # COL2A1
        >>> if data:
        ...     print(data['uniprot_id'], data.get('pdb_url'))
    """

    def __init__(
        self,
        timeout: int = AFDBConfig.TIMEOUT_SECONDS,
        max_retries: int = AFDBConfig.MAX_RETRIES,
        rate_limit_delay: float = AFDBConfig.RATE_LIMIT_DELAY,
    ):
        """Initialize AFDB client.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            rate_limit_delay: Minimum delay between requests (seconds)
        """
        self.timeout = timeout
        self.rate_limit_delay = rate_limit_delay
        self._last_request_time = 0.0

        # Setup session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=AFDBConfig.RETRY_BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update({"User-Agent": AFDBConfig.USER_AGENT})

    def _rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self._last_request_time = time.time()

    def get_prediction(self, uniprot_id: str) -> Optional[Dict[str, Any]]:
        """Fetch prediction metadata for a UniProt accession.

        Args:
            uniprot_id: UniProt accession (e.g., 'P02458', 'Q92508')

        Returns:
            Normalized metadata dictionary, or None if not found/error

        Raises:
            requests.exceptions.RequestException: On network errors
        """
        url = AFDBConfig.get_api_url(uniprot_id)

        self._rate_limit()

        try:
            logger.debug(f"Fetching {uniprot_id} from {url}")
            response = self.session.get(url, timeout=self.timeout)

            if response.status_code == 404:
                logger.warning(f"Protein {uniprot_id} not found in AFDB")
                return None

            response.raise_for_status()
            data = response.json()

            # Handle both single entry and list responses
            if isinstance(data, list):
                if len(data) == 0:
                    logger.warning(f"Empty response for {uniprot_id}")
                    return None
                data = data[0]  # Take first entry

            # Normalize schema
            normalized = self._normalize_response(data, uniprot_id)

            # Add schema fingerprint for reproducibility
            normalized["_schema_version"] = self._compute_schema_fingerprint(data)

            return normalized

        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching {uniprot_id}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {uniprot_id}: {e}")
            return None
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse response for {uniprot_id}: {e}")
            return None

    def _normalize_response(self, data: Dict[str, Any], uniprot_id: str) -> Dict[str, Any]:
        """Extract fields robustly, handling schema changes.

        This method maps various possible field names to a consistent schema,
        ensuring compatibility even if AFDB API changes field names.

        Args:
            data: Raw API response
            uniprot_id: UniProt ID for logging

        Returns:
            Normalized dictionary with consistent field names
        """
        available_fields = set(data.keys())

        # Field mapping: target_name -> [candidates in priority order]
        field_map = {
            "uniprot_id": ["uniprotAccession", "uniprot_id", "entryId"],
            "gene": ["gene", "geneName", "uniprotId"],
            "organism": ["organismScientificName", "organism", "taxId"],
            "model_version": ["latestVersion", "modelVersion", "version"],
            "pdb_url": ["pdbUrl", "cifUrl", "modelUrl"],
            "pae_image_url": ["paeImageUrl", "pae_image_url", "confidenceImageUrl"],
            "pae_json_url": ["paeDocUrl", "pae_json_url"],
        }

        normalized = {}

        for target_field, candidates in field_map.items():
            for candidate in candidates:
                if candidate in available_fields:
                    normalized[target_field] = data[candidate]
                    break
            else:
                # Field not found, log warning but continue
                if target_field in ["uniprot_id", "pdb_url"]:
                    logger.warning(f"Critical field '{target_field}' not found for {uniprot_id}")
                normalized[target_field] = None

        # Fallback: ensure uniprot_id is set
        if not normalized.get("uniprot_id"):
            normalized["uniprot_id"] = uniprot_id

        # Copy any additional fields not in our map (for future-proofing)
        for key, value in data.items():
            if key not in normalized:
                normalized[f"_raw_{key}"] = value

        return normalized

    @staticmethod
    def _compute_schema_fingerprint(data: Dict[str, Any]) -> str:
        """Compute fingerprint of API response structure for reproducibility.

        Args:
            data: Raw API response

        Returns:
            8-character hex string fingerprint
        """
        field_names = sorted(data.keys())
        fingerprint_input = ",".join(field_names).encode("utf-8")
        return hashlib.md5(fingerprint_input).hexdigest()[:8]

    def test_connection(self) -> bool:
        """Test if AFDB API is accessible.

        Returns:
            True if API responds successfully
        """
        try:
            # Test with a well-known protein (COL2A1)
            result = self.get_prediction("P02458")
            return result is not None
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
