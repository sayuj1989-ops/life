#!/usr/bin/env python3
"""Backward-compatible shim — forwards to `dhan_paper_launcher.py`."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

_IMPL = Path(__file__).resolve().parent / "dhan_paper_launcher.py"
sys.argv[0] = str(_IMPL)
runpy.run_path(str(_IMPL), run_name="__main__")
