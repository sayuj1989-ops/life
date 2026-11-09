import os
from pathlib import Path

import pytest

from research.alphafold_countercurvature.src.afcc.paths import resolve_manifest_path


def test_resolve_manifest_path_joins_repo_root(tmp_path):
    repo_root = tmp_path / "life"
    rel = "research/alphafold_countercurvature/data/raw/afdb/P02452/P02452.pdb"
    resolved = resolve_manifest_path(rel, repo_root)
    assert resolved == repo_root / rel


def test_resolve_manifest_path_strips_docker_app_prefix(tmp_path):
    repo_root = tmp_path / "life"
    docker = "/app/research/alphafold_countercurvature/data/raw/afdb/Q9UKP6/Q9UKP6.pdb"
    resolved = resolve_manifest_path(docker, repo_root)
    assert resolved == repo_root / "research/alphafold_countercurvature/data/raw/afdb/Q9UKP6/Q9UKP6.pdb"


def test_resolve_manifest_path_works_from_non_repo_cwd(tmp_path, monkeypatch):
    repo_root = tmp_path / "life"
    pdb = repo_root / "research/alphafold_countercurvature/data/raw/afdb/P02452/P02452.pdb"
    pdb.parent.mkdir(parents=True)
    pdb.write_text("END\n")
    rel = "research/alphafold_countercurvature/data/raw/afdb/P02452/P02452.pdb"
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    assert resolve_manifest_path(rel, repo_root).exists()
