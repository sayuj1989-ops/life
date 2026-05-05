#!/usr/bin/env python3
"""Quick JAX GPU test."""

import sys
sys.path.append('src')

from spinalmodes.countercurvature.jax_rod_solver import jax_run_simulation
import numpy as np

L = 0.5
n_elem = 50
s = np.linspace(0, L, n_elem+1)
I = np.sin(2*np.pi*s/L)**2
dIds = np.gradient(I, s)

print('Running JAX test simulation...')
result = jax_run_simulation(
    chi_M=10.0, length=L, n_elements=n_elem, radius=0.01,
    E0=1e6, rho=1000.0, gravity=9.81,
    info_field_I=I, info_field_grad=dIds,
    final_time=0.5, dt=1e-5, seed=0
)

print(f'✅ JAX GPU test passed')
print(f'Runtime: {result["runtime"]:.3f}s (first run includes JIT compilation)')
print(f'z_tip: {result["z_tip"]:.6f}m (negative = sagging under gravity)')
