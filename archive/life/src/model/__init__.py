"""
Legacy shim to preserve existing ``import model`` code paths.

The new implementation lives in ``spinalmodes.model``; this module forwards the
public symbols to avoid breaking older scripts.
"""

from spinalmodes.model import *  # noqa: F401,F403

