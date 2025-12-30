"""Disk-based caching for AlphaFold Database structures and metadata.

Implements a persistent cache to avoid redundant API calls and ensure
reproducibility of analyses.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from .config import AFDBConfig

logger = logging.getLogger(__name__)


class AFDBCache:
    """Disk-based cache for AFDB predictions.

    Cache structure:
        cache_dir/
        ├── metadata/
        │   └── {uniprot_id}_{gene}.json
        ├── structures/
        │   └── {uniprot_id}_v{version}.cif
        └── cache_index.csv

    Features:
        - Atomic writes (temp file + rename)
        - Version tracking (AFDB model version)
        - Cache index for quick lookups
        - Provenance metadata (fetch date, API version)

    Example:
        >>> cache = AFDBCache()
        >>> cache.store_metadata("P02458", metadata_dict)
        >>> cached = cache.get_metadata("P02458")
        >>> if cached:
        ...     print(f"Cached on {cached['_cache_date']}")
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize cache.

        Args:
            cache_dir: Cache directory (default: ~/.spinalmodes_cache/afdb)
        """
        self.cache_dir = cache_dir or AFDBConfig.get_cache_dir()
        self.metadata_dir = self.cache_dir / "metadata"
        self.structures_dir = self.cache_dir / "structures"
        self.index_file = self.cache_dir / "cache_index.csv"

        # Create directories
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.structures_dir.mkdir(parents=True, exist_ok=True)

        # Load or create index
        self._load_index()

    def _load_index(self) -> None:
        """Load cache index from disk."""
        if self.index_file.exists():
            try:
                self.index = pd.read_csv(self.index_file)
            except Exception as e:
                logger.warning(f"Failed to load cache index: {e}. Creating new index.")
                self.index = self._create_empty_index()
        else:
            self.index = self._create_empty_index()

    def _create_empty_index(self) -> pd.DataFrame:
        """Create empty cache index DataFrame."""
        return pd.DataFrame(
            columns=[
                "uniprot_id",
                "gene",
                "model_version",
                "date_fetched",
                "metadata_path",
                "structure_path",
                "plddt_mean",
                "schema_version",
            ]
        )

    def _save_index(self) -> None:
        """Save cache index to disk."""
        try:
            self.index.to_csv(self.index_file, index=False)
        except Exception as e:
            logger.error(f"Failed to save cache index: {e}")

    def get_metadata(self, uniprot_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached metadata for a protein.

        Args:
            uniprot_id: UniProt accession

        Returns:
            Metadata dictionary, or None if not cached
        """
        # Check index first
        matches = self.index[self.index["uniprot_id"] == uniprot_id]
        if matches.empty:
            return None

        metadata_path = Path(matches.iloc[0]["metadata_path"])
        if not metadata_path.exists():
            logger.warning(f"Index entry exists but file missing: {metadata_path}")
            return None

        try:
            with open(metadata_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load metadata from {metadata_path}: {e}")
            return None

    def store_metadata(self, uniprot_id: str, metadata: Dict[str, Any]) -> Path:
        """Store metadata to cache.

        Args:
            uniprot_id: UniProt accession
            metadata: Metadata dictionary from API

        Returns:
            Path to cached metadata file
        """
        # Add cache provenance
        metadata["_cache_date"] = datetime.now().isoformat()
        metadata["_cache_uniprot_id"] = uniprot_id

        # Generate filename
        gene = metadata.get("gene", "UNKNOWN")
        filename = f"{uniprot_id}_{gene}.json"
        metadata_path = self.metadata_dir / filename

        # Atomic write: write to temp file, then rename
        temp_path = metadata_path.with_suffix(".json.tmp")
        try:
            with open(temp_path, "w") as f:
                json.dump(metadata, f, indent=2)
            temp_path.rename(metadata_path)
        except Exception as e:
            logger.error(f"Failed to write metadata to {metadata_path}: {e}")
            if temp_path.exists():
                temp_path.unlink()
            raise

        # Update index
        self._update_index(uniprot_id, metadata, metadata_path)

        logger.info(f"Cached metadata for {uniprot_id} at {metadata_path}")
        return metadata_path

    def _update_index(self, uniprot_id: str, metadata: Dict[str, Any], metadata_path: Path) -> None:
        """Update cache index with new entry."""
        # Remove existing entry if present
        self.index = self.index[self.index["uniprot_id"] != uniprot_id]

        # Add new entry
        new_row = pd.DataFrame(
            [
                {
                    "uniprot_id": uniprot_id,
                    "gene": metadata.get("gene"),
                    "model_version": metadata.get("model_version"),
                    "date_fetched": metadata.get("_cache_date"),
                    "metadata_path": str(metadata_path),
                    "structure_path": None,  # Will be filled when structure downloaded
                    "plddt_mean": None,  # Will be filled after feature extraction
                    "schema_version": metadata.get("_schema_version"),
                }
            ]
        )

        self.index = pd.concat([self.index, new_row], ignore_index=True)
        self._save_index()

    def get_structure_path(self, uniprot_id: str) -> Optional[Path]:
        """Get path to cached structure file.

        Args:
            uniprot_id: UniProt accession

        Returns:
            Path to structure file, or None if not cached
        """
        matches = self.index[self.index["uniprot_id"] == uniprot_id]
        if matches.empty:
            return None

        structure_path_str = matches.iloc[0]["structure_path"]
        if pd.isna(structure_path_str):
            return None

        structure_path = Path(structure_path_str)
        if not structure_path.exists():
            logger.warning(f"Index entry exists but structure missing: {structure_path}")
            return None

        return structure_path

    def store_structure_path(self, uniprot_id: str, structure_path: Path) -> None:
        """Update index with path to downloaded structure.

        Args:
            uniprot_id: UniProt accession
            structure_path: Path to structure file (CIF/PDB)
        """
        mask = self.index["uniprot_id"] == uniprot_id
        if not mask.any():
            logger.warning(f"Cannot update structure path for {uniprot_id}: no metadata entry")
            return

        self.index.loc[mask, "structure_path"] = str(structure_path)
        self._save_index()

    def is_cached(self, uniprot_id: str) -> bool:
        """Check if protein is in cache.

        Args:
            uniprot_id: UniProt accession

        Returns:
            True if metadata exists in cache
        """
        return uniprot_id in self.index["uniprot_id"].values

    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        return {
            "cache_dir": str(self.cache_dir),
            "n_proteins": len(self.index),
            "n_with_structures": self.index["structure_path"].notna().sum(),
            "total_size_mb": self._compute_cache_size(),
            "oldest_entry": (self.index["date_fetched"].min() if not self.index.empty else None),
            "newest_entry": (self.index["date_fetched"].max() if not self.index.empty else None),
        }

    def _compute_cache_size(self) -> float:
        """Compute total cache size in MB."""
        total_bytes = 0
        for path_col in ["metadata_path", "structure_path"]:
            for path_str in self.index[path_col].dropna():
                path = Path(path_str)
                if path.exists():
                    total_bytes += path.stat().st_size
        return total_bytes / (1024 * 1024)  # Convert to MB
