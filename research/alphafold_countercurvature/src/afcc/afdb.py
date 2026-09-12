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
from Bio.PDB import MMCIFParser, PDBParser
from Bio.PDB.PDBExceptions import PDBConstructionException
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ALPHAFOLD_API_BASE = "https://alphafold.ebi.ac.uk/api/prediction"
COLUMNS = ["uniprot", "gene_symbol", "status", "pdb_path", "pae_path", "sha256_pdb",
           "retrieved_at", "notes"]


class MetadataError(RuntimeError):
    """Request/schema/selection failure, distinct from an absent AFDB entry."""


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
        self.manifest.to_csv(self.manifest_path, index=False)

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
                   if entry.get("modelEntityId", entry.get("entryId")) == canonical
                   and entry.get("uniprotAccession", uniprot_id) == uniprot_id]
        if len(matches) != 1:
            raise MetadataError(f"Expected one canonical {canonical}; found {len(matches)}")
        return matches[0]

    @staticmethod
    def _valid_file(path, suffix):
        try:
            if suffix == ".json":
                data = json.loads(Path(path).read_text())
                entry = data[0] if isinstance(data, list) and data else data
                matrix = np.asarray(entry["predicted_aligned_error"], dtype=float)
                return (matrix.ndim == 2 and matrix.shape[0] > 0
                        and matrix.shape[0] == matrix.shape[1]
                        and bool(np.isfinite(matrix).all()) and bool((matrix >= 0).all()))
            parser = MMCIFParser(QUIET=True) if suffix == ".cif" else PDBParser(QUIET=True)
            structure = parser.get_structure("validation", str(path))
            return any(atom.name == "CA" and np.isfinite(atom.coord).all()
                       for atom in structure.get_atoms())
        except (ValueError, TypeError, KeyError, IndexError, OSError, PDBConstructionException):
            return False

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
                    or self._calculate_sha256(path) != row.get("sha256_pdb")
                    or not self._valid_file(path, path.suffix)):
                return False
            pae = self._resolve_path(row.get("pae_path"))
            if pae is not None:
                notes = json.loads(row.get("notes", ""))
                return (pae.is_file() and self._valid_file(pae, ".json")
                        and self._calculate_sha256(pae) == notes.get("sha256_pae"))
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
        structure_url = metadata.get("pdbUrl") or metadata.get("cifUrl")
        if not structure_url:
            self._update_manifest(uniprot_id, gene_symbol, "no_structure")
            return {"status": "no_structure"}
        if self.dry_run_mode == "metadata":
            return {"status": "metadata_only", "metadata": metadata}
        suffix = ".pdb" if metadata.get("pdbUrl") else ".cif"
        folder = self.afdb_dir / uniprot_id
        structure = folder / f"{uniprot_id}{suffix}"
        if not self._download_file(structure_url, structure):
            self._update_manifest(uniprot_id, gene_symbol, "download_failed")
            return {"status": "failed"}
        pae_url = metadata.get("paeDocUrl")  # Use published URLs, never guess a release.
        pae = folder / f"{uniprot_id}_pae.json"
        has_pae = bool(pae_url and self._download_file(pae_url, pae))
        notes = {"model_entity_id": metadata.get("modelEntityId", metadata.get("entryId")),
                 "version": metadata.get("latestVersion"),
                 "sequence_start": metadata.get("sequenceStart", metadata.get("uniprotStart")),
                 "sequence_end": metadata.get("sequenceEnd", metadata.get("uniprotEnd")),
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
