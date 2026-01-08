"""
Optional thin bridge to PyElastica for full Cosserat rod simulations.

Import-safe even when PyElastica is absent, enabling CI smoke tests to skip gracefully.
"""

from __future__ import annotations

from typing import Any


def available() -> bool:
    """Return True if PyElastica is importable."""
    try:
        import elastica  # type: ignore

        return True
    except Exception:
        return False


def simulate_cosserat(params: dict[str, Any]) -> dict[str, Any]:
    """
    Placeholder for a minimal rod + gravity + target curvature actuation simulation.

    Returns a dict with ok/reason/result keys so callers can handle missing dependencies cleanly.
    """
    if not available():
        return {"ok": False, "reason": "PyElastica not installed", "result": None}
    # TODO: implement minimal rod + gravity + target curvature actuation
    return {"ok": True, "reason": None, "result": {}}

