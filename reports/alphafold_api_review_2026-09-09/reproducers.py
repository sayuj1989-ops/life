"""Offline reproducers for the LIMITATION / OK items in REVIEW.md (2026-09-12).

Run from the repository root:  PYTHONPATH=src:. .venv/bin/python reports/alphafold_api_review_2026-09-09/reproducers.py
Uses synthetic files in a temporary directory only; never reads or writes the publication dataset.
The DEFECT items are reproduced by the tests added to tests/test_afdb_reliability.py instead.
"""
import io
import json
import os
import tempfile
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from Bio.PDB import MMCIFIO, PDBParser

from research.alphafold_countercurvature.src.afcc.afdb import AlphaFoldFetcher, MetadataError
from research.alphafold_countercurvature.src.afcc.metrics import MetricsAnalyzer
from research.alphafold_countercurvature.src.afcc.structure import StructureParser

warnings.simplefilter("ignore")
PDB5 = "\n".join([f"ATOM      {i+1}  CA  ALA A   {i+1}       {1.5*i:.3f}   0.000   {0.2*i*i:.3f}  1.00 {90-10*i:.2f}           C"
                  for i in range(5)] + ["END", ""]).encode()
TMP = Path(tempfile.mkdtemp(prefix="afdb_review_"))
REL = "research/alphafold_countercurvature/data/raw"


def fetcher(name):
    return AlphaFoldFetcher(TMP / name / REL, TMP / name / "research/alphafold_countercurvature/data/manifest.csv")


def section(title):
    print(f"\n== {title}")


section("F. PAE precision through the downstream parser (structure.py / metrics.py)")
pae = TMP / "F" / "x_pae.json"
pae.parent.mkdir(parents=True)
pae.write_text(json.dumps([{"predicted_aligned_error": [[0, 1.5], [2.9, 0.75]]}]))
parsed = StructureParser().parse_pae(pae)
print("  parse_pae([[0,1.5],[2.9,0.75]]) ->", parsed.tolist(), parsed.dtype,
      "| cache written:", sorted(p.name for p in pae.parent.iterdir()))
true_mean = np.mean([[0, 1.5], [2.9, 0.75]])
got = MetricsAnalyzer().calculate_pae_metrics(np.array([[0, 1.5], [2.9, 0.75]]), np.array([90, 90]))["pae_mean"]
print(f"  calculate_pae_metrics on the float matrix: pae_mean={got} (true mean {true_mean})")
print("  fetcher accepts the same fractional file:", AlphaFoldFetcher._valid_file(pae, ".json"))
for bad in ([[0, 300], [1, 0]], [[0, -1.0], [1, 0]]):
    pae.write_text(json.dumps([{"predicted_aligned_error": bad}]))
    for cache in pae.parent.glob("*.npy"):
        cache.unlink()
    print(f"  parse_pae({bad}) ->", StructureParser().parse_pae(pae),
          "| fetcher _valid_file:", AlphaFoldFetcher._valid_file(pae, ".json"))

section("E. A CIF stored at pdb_path, read by the downstream PDB-only parsers")
structure = PDBParser(QUIET=True).get_structure("x", io.StringIO(PDB5.decode()))
cif = TMP / "E" / "P02452.cif"
cif.parent.mkdir(parents=True)
writer = MMCIFIO()
writer.set_structure(structure)
writer.save(str(cif))
parser = StructureParser()
print("  fast_parse_pdb_arrays ->", parser.fast_parse_pdb_arrays(cif))
legacy = parser.parse_pdb(cif, "g")
coords, plddt, resnames = parser.extract_coords_and_plddt(legacy)
metrics = MetricsAnalyzer().analyze_structure(legacy, plddt, coords=coords, resnames=resnames)
print("  PDBParser on CIF -> atoms:", len(list(legacy.get_atoms())), "| analyze_structure row:",
      {k: metrics[k] for k in ("n_residues", "plddt_mean", "morphology")})
print("  (fetcher now refuses CIF-only entries: see test_cif_only_entry_is_not_recorded_as_a_pdb_download)")

section("B. Malformed / unexpected structure URLs")
fx = fetcher("B")
fx.session = requests.Session()
for url in ["ftp://alphafold.ebi.ac.uk/x.pdb", "file:///etc/hostname", "not a url", 123, {"u": 1}]:
    print(f"  _download_file({url!r}) ->", fx._download_file(url, TMP / "B" / "m.pdb"))
print("  no host allowlist: an https URL on any host would be fetched (trust is transitive from the API response)")

section("A2. Lower-case accession is a loud MetadataError, not a silent miss")
from unittest.mock import Mock
fx = fetcher("A2")
resp = Mock(status_code=200)
resp.json.return_value = [{"modelEntityId": "AF-P02452-F1"}]
fx.session.get = Mock(return_value=resp)
try:
    fx._fetch_metadata("p02452")
except MetadataError as exc:
    print("  ", exc)

section("C2. Manifest rows with missing columns / a valid PDB whose stored SHA-256 no longer matches")
fx = fetcher("C2")
fx.manifest_path.parent.mkdir(parents=True)
fx.manifest_path.write_text("uniprot,status\nP02452,downloaded\n")
fx.manifest = fx._load_manifest()
print("  columns after load:", fx.manifest.columns.tolist())
print("  row lacking pdb_path is cache-valid:", fx._cache_valid(fx.manifest.iloc[0]))
folder = fx.afdb_dir / "P02452"
folder.mkdir(parents=True)
(folder / "P02452.pdb").write_bytes(PDB5)
row = {"pdb_path": f"{REL}/afdb/P02452/P02452.pdb", "sha256_pdb": fx._calculate_sha256(folder / "P02452.pdb"), "notes": ""}
print("  matching sha, no PAE:", fx._cache_valid(row))
(folder / "P02452.pdb").write_bytes(PDB5.replace(b"90.00", b"91.00", 1))  # still a valid PDB, different bytes
print("  valid PDB but sha differs:", fx._cache_valid(row))

section("G. Downstream path resolution (03_parse_structures.py / 04_analyze_metrics.py)")
manifest = pd.read_csv("research/alphafold_countercurvature/data/manifest.csv")
rel = manifest["pdb_path"].dropna()
print("  publication manifest pdb_path: relative rows =", int((~rel.str.startswith("/")).sum()),
      "| absolute rows =", rel[rel.str.startswith("/")].tolist())
print("  scripts use Path(row['pdb_path']) without joining repo_root -> resolves only when cwd is the repo root;")
os.chdir(TMP)
print("  from another cwd Path(rel).exists() ->", Path(rel.iloc[1]).exists(), "(04_analyze_metrics.py then `continue`s silently)")
print("  data/raw present on this checkout:", (Path("/home/sayuj/life") / REL).exists())
