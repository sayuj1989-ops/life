import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "research/alphafold_countercurvature/scripts/02b_backfill_manifest_provenance.py"
PDB = (
    "ATOM      1  N   MET A   1       0.000   0.000   0.000  1.00 90.00           N\n"
    "ATOM      2  CA  MET A   1       0.000   0.000   0.000  1.00 90.00           C\n"
    "END\n"
)


@pytest.fixture
def sandbox(tmp_path):
    base = tmp_path / "life"
    manifest_dir = base / "research/alphafold_countercurvature/data"
    manifest_dir.mkdir(parents=True)
    manifest = manifest_dir / "manifest.csv"
    manifest.write_text(
        "uniprot,gene_symbol,status,pdb_path,pae_path,sha256_pdb,retrieved_at,notes\n"
        "P02452,COL1A1,downloaded,"
        "research/alphafold_countercurvature/data/raw/afdb/P02452/P02452.pdb,"
        ",abc,2026-01-01,\n"
    )
    return base, manifest


def run_backfill(repo_root: Path, manifest_path: Path, report_path: Path):
    env = {**os.environ, "PYTHONPATH": f"{REPO / 'src'}:{REPO}"}
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--manifest",
            str(manifest_path),
            "--repo-root",
            str(repo_root),
            "--report",
            str(report_path),
        ],
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_backfill_records_residues_when_cached_file_exists(sandbox):
    repo_root, manifest_path = sandbox
    pdb = repo_root / "research/alphafold_countercurvature/data/raw/afdb/P02452/P02452.pdb"
    pdb.parent.mkdir(parents=True)
    pdb.write_text(PDB)
    report = repo_root / "reports/afcc_provenance_backfill.json"
    result = run_backfill(repo_root, manifest_path, report)
    assert result.returncode == 0, result.stderr
    frame = pd.read_csv(manifest_path)
    notes = json.loads(frame.iloc[0]["notes"])
    assert notes["residues"] == 1
    assert notes["provenance_source"] == "cached_files"


def test_backfill_marks_unverified_when_raw_missing(sandbox):
    repo_root, manifest_path = sandbox
    report = repo_root / "reports/afcc_provenance_backfill.json"
    result = run_backfill(repo_root, manifest_path, report)
    assert result.returncode == 2, result.stdout + result.stderr
    payload = json.loads(report.read_text())
    missing = payload["unverified"][0]["missing_pdb"]
    assert missing.endswith("research/alphafold_countercurvature/data/raw/afdb/P02452/P02452.pdb")
    assert payload["unverified"][0]["status"] == "UNVERIFIED"
