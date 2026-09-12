"""Restore the ten archived documents, refusing to overwrite any current file."""
from pathlib import Path
import hashlib
import json
import shutil
archive = Path(__file__).resolve().parent
root = archive.parents[1]
manifest = json.loads((archive / 'manifest.json').read_text())
for row in manifest['files']:
    source, target = root / row['archived'], root / row['original']
    if target.exists():
        raise SystemExit(f'Refusing to overwrite {target}')
    if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != row['sha256']:
        raise SystemExit(f'Missing or altered archive: {source}')
for row in manifest['files']:
    shutil.move(str(root / row['archived']), str(root / row['original']))
print('Restored 10 documents. README.before-cleanup.md is retained as a separate historical snapshot.')
