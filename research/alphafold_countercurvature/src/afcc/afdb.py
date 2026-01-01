import urllib.request
import urllib.error
import json
import time
import hashlib
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any

ALPHAFOLD_API_BASE = "https://alphafold.ebi.ac.uk/api/prediction"
# Note: PAE URL pattern: https://alphafold.ebi.ac.uk/files/AF-{uniprot}-F1-predicted_aligned_error_v4.json

class AlphaFoldFetcher:
    def __init__(self, data_dir: Path, manifest_path: Path, dry_run: str = "none"):
        self.data_dir = data_dir
        self.manifest_path = manifest_path
        self.dry_run_mode = dry_run # "none", "metadata", "full" (skip all)
        self.manifest = self._load_manifest()

        # Subdirectories
        self.afdb_dir = self.data_dir / "afdb"
        self.afdb_dir.mkdir(parents=True, exist_ok=True)

    def _load_manifest(self) -> pd.DataFrame:
        if self.manifest_path.exists():
            try:
                # Ensure all columns exist
                df = pd.read_csv(self.manifest_path)
                cols = ['uniprot', 'gene_symbol', 'status', 'pdb_path', 'pae_path', 'sha256_pdb', 'retrieved_at', 'notes']
                for c in cols:
                    if c not in df.columns:
                        df[c] = None
                return df
            except Exception:
                pass
        return pd.DataFrame(columns=['uniprot', 'gene_symbol', 'status', 'pdb_path', 'pae_path', 'sha256_pdb', 'retrieved_at', 'notes'])

    def _save_manifest(self):
        if self.manifest_path:
            self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
            self.manifest.to_csv(self.manifest_path, index=False)

    def _calculate_sha256(self, filepath: Path) -> str:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _fetch_metadata(self, uniprot_id: str) -> Optional[Dict]:
        """Fetch metadata from AlphaFold DB API (Schema tolerant)."""
        api_url = f"{ALPHAFOLD_API_BASE}/{uniprot_id}"

        try:
            with urllib.request.urlopen(api_url, timeout=30) as response:
                data = json.loads(response.read().decode())

                if not data or len(data) == 0:
                    return None

                # Schema tolerance: API returns a list of entries.
                # Usually the first one is the main one.
                entry = data[0]
                return entry
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            print(f"   ⚠️  AFDB API Error {e.code}: {e.reason}")
            return None
        except Exception as e:
            print(f"   ⚠️  Connection Error: {e}")
            return None

    def _download_file(self, url: str, dest_path: Path) -> bool:
        """Downloads a file with basic retry logic."""
        if self.dry_run_mode != "none":
            print(f"   [Dry Run] Would download {url} to {dest_path}")
            return True

        for attempt in range(3):
            try:
                with urllib.request.urlopen(url, timeout=60) as response, open(dest_path, "wb") as f:
                    f.write(response.read())
                return True
            except Exception as e:
                time.sleep(1 * (attempt + 1))

        print(f"   ❌ Failed to download {url}")
        return False

    def fetch_protein(self, uniprot_id: str, gene_symbol: str) -> Dict[str, Any]:
        """
        Main method to fetch data for a protein.
        Updates manifest and returns status dict.
        """
        # Check manifest first
        existing = self.manifest[self.manifest['uniprot'] == uniprot_id]
        if not existing.empty:
            row = existing.iloc[0]
            if row['status'] == 'downloaded':
                # Verify files exist
                if Path(row['pdb_path']).exists():
                    print(f"   ✅ Already cached: {gene_symbol} ({uniprot_id})")
                    return row.to_dict()

        if self.dry_run_mode == "full": # Skip network completely
             print(f"   ⚠️  [Dry Run] Skipping {gene_symbol}")
             return {'status': 'skipped'}

        print(f"   📡 Fetching metadata for {gene_symbol} ({uniprot_id})...")
        metadata = self._fetch_metadata(uniprot_id)

        if not metadata:
            print(f"   ❌ Not found in AFDB: {gene_symbol}")
            self._update_manifest(uniprot_id, gene_symbol, 'not_found_afdb')
            return {'status': 'not_found'}

        # Extract URLs (Schema tolerant)
        # Look for pdbUrl, cifUrl, etc.
        pdb_url = metadata.get('pdbUrl')
        pae_image_url = metadata.get('paeImageUrl') # Often just the image, need JSON

        # NOTE: The API often doesn't give the PAE JSON URL explicitly in older versions,
        # but the schema usually has it. If not, we can infer it or skip.
        # However, 'ampt' (PAE) might be available via 'paeDocUrl' or similar?
        # Let's look for known keys.

        # Typically: https://alphafold.ebi.ac.uk/files/AF-{uid}-F1-predicted_aligned_error_{v}.json
        # The metadata entry normally has 'cifUrl', 'pdbUrl', 'bcifUrl', 'paeImageUrl', 'paeDocUrl' (maybe).
        # We will try to rely on 'pdbUrl' to infer PAE JSON if not explicit,
        # but let's check keys.

        # Explicit download
        protein_dir = self.afdb_dir / uniprot_id
        protein_dir.mkdir(parents=True, exist_ok=True)

        # 1. PDB
        pdb_path = protein_dir / f"{uniprot_id}.pdb"
        if pdb_url:
            if not self._download_file(pdb_url, pdb_path):
                 self._update_manifest(uniprot_id, gene_symbol, 'download_failed')
                 return {'status': 'failed'}
        else:
             print("   ⚠️  No PDB URL found.")
             self._update_manifest(uniprot_id, gene_symbol, 'no_structure')
             return {'status': 'no_structure'}

        # 2. PAE JSON
        # Infer URL if not present.
        # Example pdbUrl: https://alphafold.ebi.ac.uk/files/AF-P49768-F1-model_v4.pdb
        # PAE URL:        https://alphafold.ebi.ac.uk/files/AF-P49768-F1-predicted_aligned_error_v4.json
        pae_path = protein_dir / f"{uniprot_id}_pae.json"
        pae_url = None

        if pdb_url:
             pae_url = pdb_url.replace("model", "predicted_aligned_error").replace(".pdb", ".json")

        has_pae = False
        if pae_url:
            if self._download_file(pae_url, pae_path):
                has_pae = True
            else:
                # PAE is optional
                print("   ⚠️  PAE JSON not found or download failed (optional).")

        # 3. Checksum
        sha256 = None
        if self.dry_run_mode == "none":
             sha256 = self._calculate_sha256(pdb_path)

        # Update Manifest
        self._update_manifest(
            uniprot_id,
            gene_symbol,
            'downloaded',
            str(pdb_path),
            str(pae_path) if has_pae else None,
            sha256
        )

        return {'status': 'downloaded'}

    def _update_manifest(self, uniprot, gene, status, pdb_path=None, pae_path=None, sha=None):
        if self.dry_run_mode != "none": return

        # Remove old entry
        self.manifest = self.manifest[self.manifest['uniprot'] != uniprot]

        new_row = {
            'uniprot': uniprot,
            'gene_symbol': gene,
            'status': status,
            'pdb_path': pdb_path,
            'pae_path': pae_path,
            'sha256_pdb': sha,
            'retrieved_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'notes': ''
        }

        self.manifest = pd.concat([self.manifest, pd.DataFrame([new_row])], ignore_index=True)
        self._save_manifest()
