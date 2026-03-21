import sys
try:
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy
    print("Dependencies available.")
except ImportError as e:
    print(f"Missing: {e}")
