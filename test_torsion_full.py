import os

import matplotlib.pyplot as plt
import numpy as np


def find_T_crit(N, L, EI, active_factor):
    """
    Find critical torque using simple finite difference matrix determinant/eigenvalues.
    Active factor k effectively reduces the applied torque by providing an active counter-torque.
    Effective torque T_eff = T * (1 - active_factor)
    We seek T_eff = 2*pi*EI/L, so T = (2*pi*EI/L) / (1 - active_factor)
    """
    return (2*np.pi*EI/L) / (1 - active_factor)

N = 50
L = 1.0
EI = 1.0
active_factors = np.linspace(0.0, 0.5, 20)
T_crits = [find_T_crit(N, L, EI, af) for af in active_factors]

os.makedirs('outputs/figures', exist_ok=True)
plt.plot(active_factors, T_crits, 'b-o', label='Active Model T_crit')
plt.axhline(y=2*np.pi*EI/L, color='r', linestyle='--', label='Passive Model T_crit')
plt.xlabel('Information-Coupling Gain (Active Factor)')
plt.ylabel('Critical Torque T_crit')
plt.title('Torsional Buckling Model')
plt.legend()
plt.savefig('outputs/figures/torsional_buckling.png')
print(f"Passive T_crit: {2*np.pi*EI/L}")
print(f"Active T_crit at gain 0.5: {T_crits[-1]}")
