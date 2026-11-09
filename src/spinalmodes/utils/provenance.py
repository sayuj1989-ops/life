"""Provenance tracking helpers for deterministic runs."""

from __future__ import annotations

import json
import hashlib
import os
import platform
from importlib.metadata import PackageNotFoundError, version
import subprocess
import time
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]


def git_sha() -> str:
    """Return git SHA if available."""
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True, timeout=5).strip()
    except Exception:
        return "unknown"


def code_fingerprint() -> str:
    """Hash current Python sources, including uncommitted and untracked source files."""
    digest = hashlib.sha256()
    for folder in ("src", "scripts"):
        for source in sorted((REPO / folder).rglob("*.py")):
            digest.update(source.relative_to(REPO).as_posix().encode() + b"\0")
            digest.update(hashlib.sha256(source.read_bytes()).digest())
    return digest.hexdigest()


def numerical_versions() -> dict[str, str]:
    result = {}
    for name in ('numpy', 'scipy', 'pyelastica', 'spinalmodes'):
        try:
            result[name] = version(name)
        except PackageNotFoundError:
            result[name] = 'not-installed'
    return result


def _atomic_json(target: Path, payload: dict) -> None:
    fd, temporary = tempfile.mkstemp(prefix=target.name + ".", dir=target.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(payload, stream, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def write_provenance(path: str | Path, seed: int, inputs: dict, *, status: str = "completed",
                     error_type: str | None = None) -> None:
    """Write a small provenance JSON alongside generated artifacts."""
    if status not in {"completed", "failed"}:
        raise ValueError("status must be completed or failed")
    encoded_inputs = json.dumps(inputs, sort_keys=True, allow_nan=False)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_sha": git_sha(),
        "code_sha256": code_fingerprint(),
        "inputs_sha256": hashlib.sha256(encoded_inputs.encode()).hexdigest(),
        "status": status,
        "error_type": error_type,
        "seed": seed,
        "inputs": inputs,
        "system": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numerical_packages": numerical_versions(),
        },
    }
    _atomic_json(target, payload)


@contextmanager
def tracked_run(path: str | Path, seed: int, inputs: dict):
    """Keep a failed numerical run visible without recording exception contents."""
    target = Path(path)
    archive = target.parent / 'provenance_runs' / uuid.uuid4().hex / target.name
    def receipt(status, error_type=None):
        write_provenance(archive, seed, inputs, status=status, error_type=error_type)
        _atomic_json(target, json.loads(archive.read_text()))
    try:
        yield
    except Exception as exc:
        receipt('failed', type(exc).__name__)
        raise
    else:
        receipt('completed')

