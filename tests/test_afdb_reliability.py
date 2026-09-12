import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pandas as pd
import pytest
import requests

from research.alphafold_countercurvature.src.afcc.afdb import AlphaFoldFetcher, MetadataError

PDB = b'ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00 90.00           C\nEND\n'


@pytest.fixture
def fetcher(tmp_path):
    return AlphaFoldFetcher(tmp_path / 'research/alphafold_countercurvature/data/raw',
                            tmp_path / 'research/alphafold_countercurvature/data/manifest.csv')


def response(data=None, status=200, body=b''):
    obj = Mock(status_code=status)
    obj.json.return_value = data
    obj.iter_content.return_value = [body]
    obj.__enter__ = Mock(return_value=obj)
    obj.__exit__ = Mock(return_value=False)
    if status >= 400:
        obj.raise_for_status.side_effect = requests.HTTPError(str(status))
    return obj


@pytest.mark.parametrize('field', ['modelEntityId', 'entryId'])
def test_selects_canonical_model_independent_of_order(fetcher, field):
    entry = {field: 'AF-P02452-F1', 'uniprotAccession': 'P02452'}
    fetcher.session.get = Mock(return_value=response([{field: 'AF-P02452-F2'}, entry]))
    assert fetcher._fetch_metadata('P02452') == entry


@pytest.mark.parametrize('data', [{}, [{'modelEntityId': 'AF-OTHER-F1'}],
                                 [{'modelEntityId': 'AF-P02452-F1'}]*2])
def test_bad_or_ambiguous_metadata_is_not_absence(fetcher, data):
    fetcher.session.get = Mock(return_value=response(data))
    with pytest.raises(MetadataError):
        fetcher._fetch_metadata('P02452')


def test_outage_and_not_found_have_different_manifest_statuses(fetcher):
    fetcher.session.get = Mock(return_value=response(status=503))
    assert fetcher.fetch_protein('P02452', 'COL1A1')['status'] == 'failed'
    assert fetcher.manifest.iloc[0]['status'] == 'metadata_failed'
    fetcher.session.get.return_value = response(status=404)
    assert fetcher.fetch_protein('P02452', 'COL1A1')['status'] == 'not_found'


@pytest.mark.parametrize('status,body', [(404, b'<html>missing</html>'),
                                       (200, b'<html>error</html>'), (200, b'')])
def test_bad_download_preserves_existing_file(fetcher, tmp_path, status, body):
    path = tmp_path / 'model.pdb'
    path.write_bytes(PDB)
    fetcher.session.get = Mock(return_value=response(status=status, body=body))
    assert not fetcher._download_file('https://example.test/model', path)
    assert path.read_bytes() == PDB
    assert list(tmp_path.glob('tmp*')) == []


def test_download_provenance_cache_and_corruption(fetcher, monkeypatch, tmp_path):
    metadata = {'modelEntityId': 'AF-P02452-F1', 'latestVersion': 6,
                'sequenceStart': 1, 'sequenceEnd': 1, 'pdbUrl': 'https://example.test/model'}
    fetcher.session.get = Mock(side_effect=[response([metadata]), response(body=PDB)])
    assert fetcher.fetch_protein('P02452', 'COL1A1')['status'] == 'downloaded'
    notes = json.loads(fetcher.manifest.iloc[0]['notes'])
    assert notes['version'] == 6 and notes['model_entity_id'] == 'AF-P02452-F1'
    assert notes['residues'] == 1
    monkeypatch.chdir(tmp_path.parent)
    fetcher.session.get = Mock(side_effect=AssertionError('cache must avoid network'))
    assert fetcher.fetch_protein('P02452', 'COL1A1')['status'] == 'cached'
    path = fetcher._resolve_path(fetcher.manifest.iloc[0]['pdb_path'])
    path.write_bytes(b'<html>corrupt</html>')
    assert not fetcher._cache_valid(fetcher.manifest.iloc[0])


def test_metadata_dry_run_never_claims_a_download(fetcher):
    fetcher.dry_run_mode = 'metadata'
    fetcher.session.get = Mock(return_value=response([{'modelEntityId': 'AF-P02452-F1',
                                                       'pdbUrl': 'https://example.test/model'}]))
    assert fetcher.fetch_protein('P02452', 'COL1A1')['status'] == 'metadata_only'
    assert not fetcher.manifest_path.exists()
    assert not fetcher.afdb_dir.exists()


@pytest.mark.parametrize('matrix', [[[0, 1], [2, 0]], [[0, 1.5], [2.1, 0]]])
def test_valid_pae(fetcher, tmp_path, matrix):
    path = tmp_path / 'pae.json'
    path.write_text(json.dumps([{'predicted_aligned_error': matrix}]))
    assert fetcher._valid_file(path, '.json')


@pytest.mark.parametrize('matrix', [[], [[0, 1]], [[0, -1], [2, 0]], [[float('nan')]]])
def test_invalid_pae(fetcher, tmp_path, matrix):
    path = tmp_path / 'pae.json'
    path.write_text(json.dumps([{'predicted_aligned_error': matrix}]))
    assert not fetcher._valid_file(path, '.json')


def test_malformed_atom_coordinates_are_rejected(fetcher, tmp_path):
    path = tmp_path / 'bad.pdb'
    path.write_bytes(PDB.replace(b'   0.000', b' invalid', 1))
    assert not fetcher._valid_file(path, '.pdb')


def test_full_dry_run_has_no_network_or_disk_writes(fetcher):
    fetcher.dry_run_mode = 'full'
    fetcher.session.get = Mock(side_effect=AssertionError('network not allowed'))
    assert fetcher.fetch_protein('P02452', 'COL1A1')['status'] == 'skipped'
    assert not fetcher.manifest_path.exists()
    assert not fetcher.afdb_dir.exists()


# --- 2026-09-12 review additions (reports/alphafold_api_review_2026-09-09/REVIEW.md) ---

FETCH_CLI = Path(__file__).resolve().parent.parent / 'research/alphafold_countercurvature/scripts/02_fetch_afdb.py'
REL = 'research/alphafold_countercurvature/data/raw/afdb/P02452/'


def test_null_identifier_fields_fall_back_to_legacy_fields(fetcher):
    entry = {'modelEntityId': None, 'entryId': 'AF-P02452-F1', 'uniprotAccession': None,
             'sequenceStart': None, 'uniprotStart': 1, 'sequenceEnd': None, 'uniprotEnd': 1,
             'pdbUrl': 'https://example.test/model'}
    fetcher.session.get = Mock(return_value=response([entry]))
    assert fetcher._fetch_metadata('P02452') == entry
    fetcher.session.get = Mock(side_effect=[response([entry]), response(body=PDB)])
    assert fetcher.fetch_protein('P02452', 'COL1A1')['status'] == 'downloaded'
    notes = json.loads(fetcher.manifest.iloc[0]['notes'])
    assert notes['model_entity_id'] == 'AF-P02452-F1'
    assert (notes['sequence_start'], notes['sequence_end']) == (1, 1)


def test_pae_not_matching_structure_size_is_a_failed_download(fetcher):
    metadata = {'modelEntityId': 'AF-P02452-F1', 'pdbUrl': 'https://example.test/model',
                'paeDocUrl': 'https://example.test/pae'}
    pae = json.dumps([{'predicted_aligned_error': [[0, 1], [1, 0]]}]).encode()
    fetcher.session.get = Mock(side_effect=[response([metadata]), response(body=PDB), response(body=pae)])
    assert fetcher.fetch_protein('P02452', 'COL1A1')['status'] == 'failed'
    row = fetcher.manifest.iloc[0]
    assert row['status'] == 'download_failed' and 'pae_dimension_mismatch' in row['notes']
    folder = fetcher.afdb_dir / 'P02452'
    stale = {'pdb_path': REL + 'P02452.pdb', 'pae_path': REL + 'P02452_pae.json',
             'sha256_pdb': fetcher._calculate_sha256(folder / 'P02452.pdb'), 'notes': ''}
    assert not fetcher._cache_valid(stale)


def test_cif_only_entry_is_not_recorded_as_a_pdb_download(fetcher):
    fetcher.session.get = Mock(return_value=response([{'modelEntityId': 'AF-P02452-F1',
                                                       'cifUrl': 'https://example.test/model.cif'}]))
    assert fetcher.fetch_protein('P02452', 'COL1A1')['status'] == 'no_structure'
    assert fetcher.manifest.iloc[0]['status'] == 'no_pdb_model'
    assert fetcher.session.get.call_count == 1
    assert not fetcher.afdb_dir.exists()


def test_legacy_row_without_pae_checksum_is_reused_not_refetched(fetcher):
    folder = fetcher.afdb_dir / 'P02452'
    folder.mkdir(parents=True)
    (folder / 'P02452.pdb').write_bytes(PDB)
    (folder / 'P02452_pae.json').write_text(json.dumps([{'predicted_aligned_error': [[0]]}]))
    fetcher.manifest_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([dict(uniprot='P02452', gene_symbol='COL1A1', status='downloaded',
                       pdb_path=REL + 'P02452.pdb', pae_path=REL + 'P02452_pae.json',
                       sha256_pdb=fetcher._calculate_sha256(folder / 'P02452.pdb'),
                       retrieved_at='2026-02-08 19:24:16', notes=None)]
                 ).to_csv(fetcher.manifest_path, index=False)
    fetcher.manifest = fetcher._load_manifest()
    fetcher.session.get = Mock(side_effect=AssertionError('legacy rows must not be re-downloaded'))
    assert fetcher.fetch_protein('P02452', 'COL1A1')['status'] == 'cached'
    (folder / 'P02452_pae.json').write_text(json.dumps([{'predicted_aligned_error': [[0, 1], [1, 0]]}]))
    assert not fetcher._cache_valid(fetcher.manifest.iloc[0])


def test_manifest_write_failure_preserves_previous_manifest(fetcher, monkeypatch):
    fetcher._update_manifest('P02452', 'COL1A1', 'not_found_afdb')
    before = fetcher.manifest_path.read_bytes()

    def truncating_write(self, path, *args, **kwargs):
        Path(path).write_text('uniprot,gene_symbol\nP4')
        raise OSError('disk full')

    monkeypatch.setattr(pd.DataFrame, 'to_csv', truncating_write)
    with pytest.raises(OSError):
        fetcher._update_manifest('P48436', 'SOX9', 'not_found_afdb')
    assert fetcher.manifest_path.read_bytes() == before
    assert list(fetcher.manifest_path.parent.glob('*.tmp')) == []


def test_cli_skips_non_canonical_accessions_instead_of_aborting(tmp_path):
    base = tmp_path / 'afcc'
    (base / 'data/processed').mkdir(parents=True)
    pd.DataFrame({'gene_symbol': ['COL1A1', 'SOX9'], 'uniprot_accession': ['P02452-2', 'P48436']}
                 ).to_csv(base / 'data/processed/uniprot_mapping.csv', index=False)
    result = subprocess.run([sys.executable, str(FETCH_CLI), '--dry-run', 'full'],
                            env={**os.environ, 'AFCC_BASE_DIR': str(base)},
                            capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr
    assert 'Non-canonical accessions' in result.stdout and 'P02452-2' in result.stdout
    assert not (base / 'data/manifest.csv').exists()
