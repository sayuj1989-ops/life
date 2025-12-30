import numpy as np

from spinalmodes.model.core import Params, State, uniform_grid, iec_kappa_target
from spinalmodes.model.solvers.euler_bernoulli import integrate_shape_from_curvature
from spinalmodes.utils.metrics import wavelength_via_fft, amplitude, phase_shift_via_xcorr


def test_iec1_phase_shift_preserves_wavelength():
    p = Params(L=1.0, n=2001, chi_k=0.05)
    s = uniform_grid(p.L, p.n)
    k = 8 * np.pi
    A = 0.02
    y0 = A * np.sin(k * s)
    kappa0 = -A * (k**2) * np.sin(k * s)
    st = State(s=s, kappa0=kappa0, I=np.sin(2 * np.pi * s))
    _, y1 = integrate_shape_from_curvature(s, iec_kappa_target(st, p))
    lam0 = wavelength_via_fft(y0, s)
    lam1 = wavelength_via_fft(y1, s)
    dl = abs(lam1 - lam0)
    assert dl / lam0 < 0.02
    assert abs(phase_shift_via_xcorr(y0, y1, s)) > 1e-2


def test_iec2_amplitude_change_small_lambda_change():
    s = uniform_grid(1.0, 2001)
    k = 8 * np.pi
    A = 0.02
    y0 = A * np.sin(k * s)
    kappa0 = -A * (k**2) * np.sin(k * s)
    _, y2 = integrate_shape_from_curvature(s, 0.7 * kappa0)
    lam0 = wavelength_via_fft(y0, s)
    lam2 = wavelength_via_fft(y2, s)
    assert abs(amplitude(y2) / amplitude(y0) - 0.7) < 0.15
    assert abs((lam2 - lam0) / lam0) < 0.02

