"""Inspect locally generated OOXML and compare raw Pandoc rendering."""
from pathlib import Path
import sys
import zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, "/home/sayuj/.codex/plugins/cache/claude-cowork/anthropic-skills/1.0.0/skills/docx/scripts")
from office.soffice import run_soffice

try:
    import lxml.etree
    print("lxml available")
except ImportError:
    print("lxml unavailable")

for path in (ROOT / "preview/manuscript_pandoc.docx", ROOT / "manuscript.docx"):
    print(path.name, path.stat().st_size)
    with zipfile.ZipFile(path) as archive:
        for name in ("[Content_Types].xml", "word/_rels/document.xml.rels", "word/document.xml", "word/styles.xml"):
            data = archive.read(name)
            ET.fromstring(data)
            print(name, data[:550].decode())
    result = run_soffice(["--headless", "--convert-to", "pdf", "--outdir", str(ROOT / "preview"), str(path)], capture_output=True, text=True, timeout=90)
    print(result.returncode, result.stdout, result.stderr)
