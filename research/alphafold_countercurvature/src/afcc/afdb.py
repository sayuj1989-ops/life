"""AlphaFold downloads with explicit model selection and validated cache provenance."""
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from Bio.PDB import PDBParser
from Bio.PDB.PDBExceptions import PDBConstructionException
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ALPHAFOLD_API_BASE = "https://alphafold.ebi.ac.uk/api/prediction"
COLUMNS = ["uniprot", "gene_symbol", "status", "pdb_path", "pae_path", "sha256_pdb",
           "retrieved_at", "notes"]
PARSE_ERRORS = (ValueError, TypeError, KeyError, IndexError, OSError, PDBConstructionException)


class MetadataError(RuntimeError):
    """Request/schema/selection failure, distinct from an absent AFDB entry."""


def _first_present(entry, *keys):
    # The field migration serves both spellings; a key present with JSON null must still fall
    # through to the other one, which dict.get(key, default) does not do.
    for key in keys:
        if entry.get(key) is not None:
            return entry[key]
    return None


class AlphaFoldFetcher:
    def __init__(self, data_dir: Path, manifest_path: Path, dry_run="none"):
        if dry_run not in {"none", "metadata", "full"}:
            raise ValueError("dry_run must be none, metadata, or full")
        self.data_dir = Path(data_dir).resolve()
        self.manifest_path = Path(manifest_path)
        self.dry_run_mode = dry_run
        self.afdb_dir = self.data_dir / "afdb"
        self.repo_root = self.data_dir.parent.parent.parent.parent
        self.manifest = self._load_manifest()
        self.session = requests.Session()
        retries = Retry(total=2, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504],
                        allowed_methods=["GET"])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _load_manifest(self):
        if self.manifest_path.exists():
            # Do not silently replace an unreadable research manifest.
            frame = pd.read_csv(self.manifest_path)
            for column in COLUMNS:
                if column not in frame:
                    frame[column] = None
            return frame
        return pd.DataFrame(columns=COLUMNS)

    def _save_manifest(self):
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        # Same write-then-rename as the structure files: a crash mid-write must not leave a
        # truncated publication manifest behind.
        temporary = self.manifest_path.with_name(self.manifest_path.name + ".tmp")
        try:
            self.manifest.to_csv(temporary, index=False)
            os.replace(temporary, self.manifest_path)
        finally:
            temporary.unlink(missing_ok=True)

    @staticmethod
    def _calculate_sha256(path):
        digest = hashlib.sha256()
        with open(path, "rb") as stream:
            for chunk in iter(lambda: stream.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _fetch_metadata(self, uniprot_id):
        try:
            response = self.session.get(f"{ALPHAFOLD_API_BASE}/{uniprot_id}", timeout=30)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise MetadataError(f"Metadata request failed: {exc}") from exc
        if not isinstance(data, list) or any(not isinstance(entry, dict) for entry in data):
            raise MetadataError("Expected a prediction list")
        if not data:
            return None
        canonical = f"AF-{uniprot_id}-F1"
        matches = [entry for entry in data
                   if _first_present(entry, "modelEntityId", "entryId") == canonical
                   and (entry.get("uniprotAccession") or uniprot_id) == uniprot_id]
        if len(matches) != 1:
            raise MetadataError(f"Expected one canonical {canonical}; found {len(matches)}")
        return matches[0]

    @staticmethod
    def _ca_count(path):
        """Residues carrying a finite CA atom; 0 for anything the PDB parser cannot use."""
        try:
            structure = PDBParser(QUIET=True).get_structure("validation", str(path))
            return sum(1 for residue in structure.get_residues()
                       if "CA" in residue and np.isfinite(residue["CA"].coord).all())
        except PARSE_ERRORS:
            return 0

    @staticmethod
    def _pae_dimension(path):
        """Side length of a square, finite, nonnegative PAE matrix; 0 for anything else."""
        try:
            data = json.loads(Path(path).read_text())
            entry = data[0] if isinstance(data, list) and data else data
            matrix = np.asarray(entry["predicted_aligned_error"], dtype=float)
        except PARSE_ERRORS:
            return 0
        if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[0] != matrix.shape[1]:
            return 0
        if not (np.isfinite(matrix).all() and (matrix >= 0).all()):
            return 0
        return matrix.shape[0]

    @classmethod
    def _valid_file(cls, path, suffix):
        return (cls._pae_dimension(path) if suffix == ".json" else cls._ca_count(path)) > 0

    def _download_file(self, url, dest_path):
        if self.dry_run_mode != "none":
            return False
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with self.session.get(url, timeout=60, stream=True) as response:
                response.raise_for_status()
                with tempfile.NamedTemporaryFile(dir=dest_path.parent, delete=False) as output:
                    temporary = Path(output.name)
                    for chunk in response.iter_content(chunk_size=65536):
                        output.write(chunk)
            if not self._valid_file(temporary, dest_path.suffix):
                return False
            os.replace(temporary, dest_path)
            return True
        except (requests.RequestException, OSError):
            return False
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def _resolve_path(self, value):
        if not isinstance(value, str) or not value:
            return None
        path = Path(value)
        return path if path.is_absolute() else self.repo_root / path

    def _cache_valid(self, row):
        path = self._resolve_path(row.get("pdb_path"))
        try:
            if (path is None or not path.is_file()
                    or self._calculate_sha256(path) != row.get("sha256_pdb")):
                return False
            residues = self._ca_count(path)
            if residues == 0:
                return False
            pae = self._resolve_path(row.get("pae_path"))
            if pae is None:
                return True
            if not pae.is_file() or self._pae_dimension(pae) != residues:
                return False
            notes = row.get("notes")
            if isinstance(notes, str) and notes:
                return self._calculate_sha256(pae) == json.loads(notes).get("sha256_pae")
            # Rows written before 2026-09-09 never recorded a PAE checksum. Demanding one would
            # re-download every publication structure on the next run instead of reusing it.
            return True
        except (OSError, ValueError, TypeError):
            return False

    def fetch_protein(self, uniprot_id, gene_symbol):
        if not isinstance(uniprot_id, str) or not uniprot_id.isalnum():
            raise ValueError("Expected a canonical UniProt accession")
        if self.dry_run_mode == "full":
            return {"status": "skipped"}
        existing = self.manifest[self.manifest["uniprot"] == uniprot_id]
        if self.dry_run_mode == "none" and not existing.empty:
            row = existing.iloc[0]
            if row["status"] == "downloaded" and self._cache_valid(row):
                return {**row.to_dict(), "status": "cached"}
        try:
            metadata = self._fetch_metadata(uniprot_id)
        except MetadataError as exc:
            self._update_manifest(uniprot_id, gene_symbol, "metadata_failed", notes=str(exc))
            return {"status": "failed", "reason": str(exc)}
        if metadata is None:
            self._update_manifest(uniprot_id, gene_symbol, "not_found_afdb")
            return {"status": "not_found"}
        structure_url = metadata.get("pdbUrl")
        if not structure_url:
            # Every downstream reader (StructureParser, alpha_gold) is PDB-only: a CIF stored at
            # pdb_path parses to zero residues and enters the metrics table as an empty protein.
            status = "no_pdb_model" if metadata.get("cifUrl") else "no_structure"
            self._update_manifest(uniprot_id, gene_symbol, status)
            return {"status": "no_structure", "reason": status}
        if self.dry_run_mode == "metadata":
            return {"status": "metadata_only", "metadata": metadata}
        folder = self.afdb_dir / uniprot_id
        structure = folder / f"{uniprot_id}.pdb"
        if not self._download_file(structure_url, structure):
            self._update_manifest(uniprot_id, gene_symbol, "download_failed")
            return {"status": "failed"}
        residues = self._ca_count(structure)
        pae_url = metadata.get("paeDocUrl")  # Use published URLs, never guess a release.
        pae = folder / f"{uniprot_id}_pae.json"
        has_pae = bool(pae_url and self._download_file(pae_url, pae))
        if has_pae and self._pae_dimension(pae) != residues:
            # The API pairs one PAE with one model. A size mismatch is an inconsistent pair, and
            # metrics.py averages whatever matrix it is handed without checking.
            reason = f"pae_dimension_mismatch: pae={self._pae_dimension(pae)} residues={residues}"
            self._update_manifest(uniprot_id, gene_symbol, "download_failed", notes=reason)
            return {"status": "failed", "reason": reason}
        notes = {"model_entity_id": _first_present(metadata, "modelEntityId", "entryId"),
                 "version": metadata.get("latestVersion"),
                 "sequence_start": _first_present(metadata, "sequenceStart", "uniprotStart"),
                 "sequence_end": _first_present(metadata, "sequenceEnd", "uniprotEnd"),
                 "residues": residues,
                 "structure_url": structure_url, "pae_url": pae_url,
                 "sha256_pae": self._calculate_sha256(pae) if has_pae else None}
        self._update_manifest(uniprot_id, gene_symbol, "downloaded", structure,
                              pae if has_pae else None, self._calculate_sha256(structure),
                              notes=json.dumps(notes))
        return {"status": "downloaded"}

    def _update_manifest(self, uniprot, gene, status, pdb_path=None, pae_path=None, sha=None,
                         notes=""):
        if self.dry_run_mode != "none":
            return

        def relative(value):
            if value is None:
                return None
            path = Path(value).resolve()
            try:
                return str(path.relative_to(self.repo_root))
            except ValueError:
                return str(path)

        row = dict(uniprot=uniprot, gene_symbol=gene, status=status,
                   pdb_path=relative(pdb_path), pae_path=relative(pae_path), sha256_pdb=sha,
                   retrieved_at=datetime.now(timezone.utc).isoformat(), notes=notes)
        self.manifest = self.manifest[self.manifest["uniprot"] != uniprot]
        self.manifest = pd.concat([self.manifest, pd.DataFrame([row])], ignore_index=True)
        self._save_manifest()
