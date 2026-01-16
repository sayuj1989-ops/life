"""
Compatibility module for legacy model imports.

This file exists to satisfy Poetry's package discovery requirements.
All actual functionality is in spinalmodes.model.
"""

# Re-export core for backwards compatibility
from spinalmodes.model.core import *  # noqa: F401,F403
