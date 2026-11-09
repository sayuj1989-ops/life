import json
from pathlib import Path

import numpy as np
import pytest

from spinalmodes.iec import solve_beam_static
from spinalmodes.utils import provenance


@pytest.mark.parametrize('field,value', [('E', -1), ('E', 0), ('E', float('nan')),
    ('moment', float('inf')), ('grid', float('nan'))])
def test_invalid_physical_inputs_are_rejected(field, value):
    s = np.linspace(0, 0.4, 10)
    E, moment = np.full(10, 1e9), np.zeros(10)
    if field == 'E': E[3] = value
    if field == 'moment': moment[3] = value
    if field == 'grid': s[3] = value
    with pytest.raises(ValueError):
        solve_beam_static(s, np.zeros(10), E, moment)


def test_broadcasting_cannot_silently_change_the_experiment():
    with pytest.raises(ValueError, match='match the spatial grid'):
        solve_beam_static(np.linspace(0, .4, 10), np.zeros((10, 1)), np.ones(10), np.zeros(10))


def test_cantilever_tip_angle_matches_closed_form_in_si():
    s = np.linspace(0, .4, 50)
    theta, kappa = solve_beam_static(s, np.zeros(50), np.full(50, 1e9), np.zeros(50), I_moment=1e-8, P_load=100)
    assert theta[0] == 0
    assert theta[-1] == pytest.approx(100 * .4**2 / (2 * 1e9 * 1e-8))
    assert kappa[-1] == pytest.approx(0)


def test_provenance_fingerprints_uncommitted_sources_and_keeps_failed_status(tmp_path, monkeypatch):
    (tmp_path / 'src').mkdir()
    source = tmp_path / 'src/solver.py'
    source.write_text('x = 1\n')
    monkeypatch.setattr(provenance, 'REPO', tmp_path)
    monkeypatch.setattr(provenance, 'git_sha', lambda: 'fixture')
    target = tmp_path / 'run.json'
    provenance.write_provenance(target, 42, {'units': 'SI', 'load_N': 100}, status='failed', error_type='ValueError')
    failed = json.loads(target.read_text())
    source.write_text('x = 2\n')
    provenance.write_provenance(target, 42, {'load_N': 100, 'units': 'SI'})
    completed = json.loads(target.read_text())
    assert failed['status'] == 'failed' and failed['error_type'] == 'ValueError'
    assert failed['code_sha256'] != completed['code_sha256']
    assert failed['inputs_sha256'] == completed['inputs_sha256']
    assert completed['generated_at'].endswith('+00:00')


def test_failed_solver_receipt_survives_the_next_success(tmp_path):
    target = tmp_path / 'solver.json'
    with pytest.raises(RuntimeError, match='fixture failure'):
        with provenance.tracked_run(target, 0, {'units': 'SI'}):
            raise RuntimeError('fixture failure')
    with provenance.tracked_run(target, 0, {'units': 'SI'}):
        pass
    receipts = [json.loads(p.read_text()) for p in tmp_path.glob('provenance_runs/*/solver.json')]
    assert sorted(p['status'] for p in receipts) == ['completed', 'failed']
    assert json.loads(target.read_text())['status'] == 'completed'
    assert 'fixture failure' not in json.dumps(receipts)


@pytest.mark.parametrize('parameter,steps', [('misspelled_coupling', 3), ('chi_E', 1)])
def test_sweeps_reject_silent_noops_before_creating_output(tmp_path, parameter, steps):
    from spinalmodes.iec_cli import app
    from typer.testing import CliRunner
    target = tmp_path / 'invalid.csv'
    result = CliRunner().invoke(app, ['sweep', '--param', parameter, '--start', '0', '--stop', '1',
                                    '--steps', str(steps), '--out-csv', str(target)])
    assert result.exit_code != 0
    assert not target.exists()
