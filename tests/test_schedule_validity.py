
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

try:
    from spinalmodes.countercurvature.pyelastica_bridge import compute_U_CC, CounterCurvatureRodSystem
    print("Import successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)
