"""Resolve manifest paths against the repository root."""
from pathlib import Path


def resolve_manifest_path(path_value, repo_root: Path) -> Path | None:
    """Join repo-relative manifest paths; normalize docker-era /app/ absolutes."""
    if path_value is None or (isinstance(path_value, float) and path_value != path_value):
        return None
    text = str(path_value).strip()
    if not text:
        return None
    path = Path(text)
    if path.is_absolute():
        parts = path.parts
        if len(parts) >= 2 and parts[0] == "/" and parts[1] == "app":
            path = Path(*parts[2:])
            return repo_root / path
        return path
    return repo_root / path
