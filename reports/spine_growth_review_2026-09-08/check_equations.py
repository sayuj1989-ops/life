"""Read-only audit of two existing spine models; writes only its own evidence JSON.

Run: python3 reports/spine_growth_review_2026-09-08/check_equations.py
No patient data, production-model changes, or large simulation runs.
"""
from pathlib import Path
import cmath
import hashlib
import importlib.util
import json
import math

import numpy as np


ROOT = Path(__file__).resolve().parents[2]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def first_hopf(inertia, damping, gravity_moment, kp, kd):
    # Characteristic: I*s^2+b*s-a+(Kp+Kd*s)*exp(-s*tau)=0.
    # Requires zero-delay stability, satisfied by the audited positive gains.
    assert kp > gravity_moment and damping + kd > 0
    roots = np.roots([
        inertia**2,
        2 * gravity_moment * inertia + damping**2 - kd**2,
        gravity_moment**2 - kp**2,
    ])
    z = next(float(x.real) for x in roots if abs(x.imag) < 1e-9 and x.real > 0)
    omega = math.sqrt(z)
    delay = (math.atan2(damping * omega, gravity_moment + inertia * z)
             + math.atan2(kd * omega, kp)) / omega
    s = 1j * omega
    residual = abs(inertia * s**2 + damping * s - gravity_moment
                   + (kp + kd * s) * cmath.exp(-s * delay))
    assert residual < 1e-9
    return delay, omega, residual


def main():
    growth_path = ROOT / 'src/spine_growth_analysis.py'
    ratchet_path = ROOT / 'src/spinalmodes/recovery_ratchet.py'
    growth = load_module('audited_growth', growth_path)
    ratchet = load_module('audited_ratchet', ratchet_path)
    rows = []
    for kd in [2.0, 8.0, 12.0, 20.0]:
        delay, omega, residual = first_hopf(
            growth.I, growth.B, growth.MGL, growth.KP, kd)
        rows.append(dict(kd=kd, independent_first_hopf_s=delay,
                         omega_rad_s=omega, characteristic_residual=residual,
                         existing_untracked_script_delay_s=growth.tau_star(kd)))
    ratchet_rows = []
    for kr in [0.3, 1.0, 6.0]:
        result = ratchet.simulate(kr, 1.0)
        assert np.all(np.diff(result['kappa_p']) >= -1e-12)
        assert np.all(np.diff(result['flexibility']) <= 1e-12)
        assert np.allclose(result['flexibility'], ratchet.KAPPA_E0 / result['kappa'])
        ratchet_rows.append(dict(kr_per_year=kr,
            final_permanent_curvature_au=result['kappa_p_final'],
            final_flexibility=result['flexibility_final']))
    payload = {
        'scope': 'Equation and implementation checks, not biological validation',
        'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (growth_path, ratchet_path)},
        'delay_boundary': rows,
        'ratchet': ratchet_rows,
        'ratchet_inference': 'Monotone accumulation and falling flexibility are imposed by the positive forcing and fixed elastic component.',
        'growth_velocity_at_20': ratchet.growth_velocity(20.0),
    }
    out = Path(__file__).with_name('equation_checks.json')
    out.write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps(payload, indent=2))


if __name__ == '__main__':
    main()
