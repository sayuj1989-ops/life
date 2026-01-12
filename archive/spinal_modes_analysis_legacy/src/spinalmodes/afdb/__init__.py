"""AlphaFold Database integration for spinalmodes.

This package provides programmatic access to the AlphaFold Database (AFDB)
to retrieve protein structure predictions and extract biophysically relevant
features for parameterizing the Information-Elasticity Coupling (IEC) model.

Key modules:
    - client: REST API wrapper for AFDB
    - cache: Disk-based caching layer for reproducibility
    - features: Structural feature extraction from PDB/CIF files
    - datasets: Build tidy datasets of protein features
    - transfer_functions: Map protein features to IEC parameters

Data from AlphaFold Database (alphafold.ebi.ac.uk)
Licensed under CC-BY 4.0 (creativecommons.org/licenses/by/4.0/)
"""

from .client import AFDBClient
from .cache import AFDBCache

__all__ = ["AFDBClient", "AFDBCache"]
__version__ = "0.1.0"
