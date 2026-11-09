#!/usr/bin/env python3
"""Backfill manifest notes from cached AlphaFold files without downloading."""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(repo_root))

from research.alphafold_countercurvature.src.afcc.afdb import AlphaFoldFetcher
from research.alphafold_countercurvature.src.afcc.paths import resolve_manifest_path

BASE_DIR = Path(__file__).resolve().parent.parent
MANIFEST_FILE = BASE_DIR / "data" / "manifest.csv"
DEFAULT_REPORT = repo_root / "reports" / "afcc_provenance_backfill.json"
VERSION_RE = re.compile(r"model[_ ]v(?:ersion)?\s*(\d+)", re.IGNORECASE)


def _empty_notes(value) -> bool:
    if value is None or (isinstance(value, float) and value != value):
        return True
    return not str(value).strip()


def _version_from_pdb(pdb_path: Path):
    try:
        for line in pdb_path.read_text(errors="replace").splitlines()[:200]:
            match = VERSION_RE.search(line)
            if match:
                return int(match.group(1))
    except OSError:
        return None
    return None


def backfill_manifest(manifest_path: Path, repo_root_path: Path, report_path: Path):
    manifest = pd.read_csv(manifest_path)
    updated = 0
    unverified = []

    for index, row in manifest.iterrows():
        if row.get("status") not in {"downloaded", "cached"} or not _empty_notes(row.get("notes")):
            continue
        pdb_path = resolve_manifest_path(row.get("pdb_path"), repo_root_path)
        if pdb_path is None or not pdb_path.is_file():
            unverified.append(
                {
                    "uniprot": row.get("uniprot"),
                    "gene_symbol": row.get("gene_symbol"),
                    "status": "UNVERIFIED",
                    "missing_pdb": str(pdb_path) if pdb_path is not None else str(row.get("pdb_path")),
                }
            )
            continue
        residues = AlphaFoldFetcher._ca_count(pdb_path)
        if residues == 0:
            unverified.append(
                {
                    "uniprot": row.get("uniprot"),
                    "gene_symbol": row.get("gene_symbol"),
                    "status": "UNVERIFIED",
                    "missing_pdb": str(pdb_path),
                    "reason": "pdb_unparseable",
                }
            )
            continue
        notes = {
            "residues": residues,
            "version": _version_from_pdb(pdb_path),
            "provenance_source": "cached_files",
            "backfilled_at": datetime.now(timezone.utc).isoformat(),
        }
        manifest.at[index, "notes"] = json.dumps(notes)
        updated += 1

    report = {
        "manifest": str(manifest_path),
        "raw_dir_present": (repo_root_path / "research/alphafold_countercurvature/data/raw").is_dir(),
        "updated_rows": updated,
        "unverified_count": len(unverified),
        "unverified": unverified,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2))

    if updated:
        temporary = manifest_path.with_suffix(".csv.tmp")
        manifest.to_csv(temporary, index=False)
        os.replace(temporary, manifest_path)

    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_FILE)
    parser.add_argument("--repo-root", type=Path, default=repo_root)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    if not args.manifest.exists():
        print(f"Manifest not found: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    report = backfill_manifest(args.manifest, args.repo_root.resolve(), args.report)
    print(json.dumps({k: report[k] for k in ("updated_rows", "unverified_count", "raw_dir_present")}, indent=2))
    if report["unverified_count"] and report["updated_rows"] == 0:
        sys.exit(2)
    if report["unverified_count"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
