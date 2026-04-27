import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import pandas as pd

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    theta = np.clip(x[0], -10.0, 10.0)
    omega = np.clip(x[1], -10.0, 10.0)
    dtheta = omega
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

print("Test script saved.")
