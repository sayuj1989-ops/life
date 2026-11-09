"""Verify current deliverables and create a local archive without publishing."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys
import zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
subprocess.run([sys.executable, str(ROOT / "render_review.py"), "--contacts-only"], check=True, capture_output=True, text=True)
checks = json.loads((ROOT / "BUILD_CHECKS.json").read_text())
render = json.loads((ROOT / "RENDER_CHECKS.json").read_text())
assert render["manuscript"]["pages"] == checks["manuscript_pages"] == 15
assert render["supplement_S1"]["pages"] == checks["supplement_pages"] == 4
text = (ROOT / "manuscript.txt").read_text()
assert "Codex" in text and "ChatGPT" not in text
assert text.count("Figure 1.") == 1 and text.count("Figure 2.") == 1
for stem in ("manuscript", "supplement_S1"):
    doc = ROOT / f"{stem}.docx"
    pdf = ROOT / f"{stem}.pdf"
    assert pdf.read_bytes().startswith(b"%PDF")
    assert pdf.stat().st_mtime >= doc.stat().st_mtime
    with zipfile.ZipFile(doc) as archive:
        assert archive.testzip() is None
        ET.fromstring(archive.read("word/document.xml"))
with zipfile.ZipFile(ROOT / "manuscript.docx") as archive:
    xml = ET.fromstring(archive.read("word/document.xml"))
    display_count = len(xml.findall(".//{http://schemas.openxmlformats.org/officeDocument/2006/math}oMathPara"))
    assert display_count == 6
checks["editable_display_equations"] = display_count
checks["final_validation_utc"] = datetime.now(timezone.utc).isoformat()
checks["pdf_freshness_verified"] = True
checks["remaining_author_checks"][-1] = "optional archive location/license if used"
(ROOT / "BUILD_CHECKS.json").write_text(json.dumps(checks, indent=2)+"\n")
core = [
    "README.md", "manuscript.docx", "manuscript.pdf", "manuscript.md", "manuscript_body.md",
    "supplement_S1.docx", "supplement_S1.pdf", "supplement_S1.md", "supplement_body.md",
    "NOVELTY_AUDIT.md", "JOURNAL_FIT.md", "COVER_LETTER.md", "VISUAL_REVIEW.md",
    "BIBLIOGRAPHY_AUDIT.md", "BUILD_CHECKS.json", "RENDER_CHECKS.json",
    "references.json", "reference_seeds.json", "harvard.csl", "fetch_references.py",
    "rebuild_documents.py", "render_review.py", "finalize_packet.py", "reference_fetch_errors.json"
]
paths = [ROOT / name for name in core]
for directory in ("figures", "supplement"):
    paths += sorted(p for p in (ROOT / directory).rglob("*") if p.is_file())
assert all(p.exists() for p in paths)
manifest = {"prepared_utc":datetime.now(timezone.utc).isoformat(), "status":"AUTHOR_REVIEW_DRAFT_NOT_SUBMITTED",
            "raw_public_metadata_retained_locally":True,
            "files":[{"path":str(p.relative_to(ROOT)), "bytes":p.stat().st_size,
                      "sha256":sha256(p.read_bytes()).hexdigest()} for p in paths]}
manifest_path = ROOT / "PACKET_MANIFEST.json"
manifest_path.write_text(json.dumps(manifest, indent=2)+"\n")
archive_path = ROOT / "publication_package.zip"
with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in paths + [manifest_path]:
        archive.write(path, Path("longevity_floor_transitions") / path.relative_to(ROOT))
with zipfile.ZipFile(archive_path) as archive:
    assert archive.testzip() is None
    for record in manifest["files"]:
        data = archive.read("longevity_floor_transitions/" + record["path"])
        assert sha256(data).hexdigest() == record["sha256"]
print(json.dumps({"archive":str(archive_path), "bytes":archive_path.stat().st_size,
                  "files":len(paths)+1, "status":manifest["status"],
                  "manuscript_pages":15, "supplement_pages":4}, indent=2))
