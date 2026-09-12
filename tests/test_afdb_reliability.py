import json
from unittest.mock import Mock

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
