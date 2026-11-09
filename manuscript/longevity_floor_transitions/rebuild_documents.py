"""Offline build of manuscript, supplement, scientific schematics and DOCX/PDF.

Run with /home/sayuj/life/.venv/bin/python rebuild_documents.py.
Public Crossref retrieval is a separate script; this build does not use a network.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import shutil
import subprocess
import sys
import zipfile
from xml.etree import ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent
DOSSIER = ROOT.parents[1] / "reports" / "longevity_gravity_hypothesis_2026-10-02"
TITLE = "The sitting pause as a mechanistic probe of recoil and adaptive control in functional aging"
RUNNING = "Floor transitions and functional aging"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "m": "http://schemas.openxmlformats.org/officeDocument/2006/math"}
ET.register_namespace("w", NS["w"])
ET.register_namespace("m", NS["m"])
for prefix, uri in {
    "r":"http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp":"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a":"http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic":"http://schemas.openxmlformats.org/drawingml/2006/picture"
}.items():
    ET.register_namespace(prefix, uri)
W = lambda tag: "{" + NS["w"] + "}" + tag

FOOTER_XML = f'''<?xml version="1.0" encoding="UTF-8"?><w:ftr xmlns:w="{NS['w']}"><w:p><w:pPr><w:jc w:val="center"/><w:suppressLineNumbers/></w:pPr><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">Page </w:t></w:r><w:fldSimple w:instr="PAGE"><w:r><w:t>1</w:t></w:r></w:fldSimple></w:p></w:ftr>'''.encode()


def call(args):
    p = subprocess.run([str(x) for x in args], cwd=ROOT, capture_output=True, text=True, check=True)
    if p.stderr.strip():
        print(p.stderr.strip())
    return p.stdout


def figures():
    out = ROOT / "figures"
    out.mkdir(exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.fonttype": "none"})
    fig, ax = plt.subplots(figsize=(7.2, 5.8))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    rows = [
        (0.83, "A  Inherited energy", ["Descent loads\nelastic tissues", "Sitting pause\nchanges storage", "Return during rise\nmay decline"], "Measure loading history, support forces and tissue work.", "#176b83"),
        (0.52, "B  New preload", ["Muscle action\nbefore ascent", "New elastic\nloading", "Return can occur\nafter a long pause"], "Recoil alone does not identify the source of stored energy.", "#8a5a19"),
        (0.21, "C  Chronic adaptation", ["Repeated varied\nfloor transitions", "Adaptation over\nweeks", "Transfer to\nuntrained function"], "Test against comparable activity; quantify strength, mobility and control.", "#347348")
    ]
    for y, label, boxes, note, color in rows:
        ax.text(0.015, y+0.115, label, color=color, fontweight="bold", fontsize=11)
        for x, text in zip((0.015, 0.365, 0.715), boxes):
            ax.add_patch(FancyBboxPatch((x, y-0.035), .265, .115, boxstyle="round,pad=0.013", facecolor=color+"12", edgecolor=color, lw=1.25))
            ax.text(x+.1325, y+.0225, text, ha="center", va="center", fontsize=10)
        for start, end in ((.293, .346), (.643, .696)):
            ax.annotate("", xy=(end, y+.0225), xytext=(start, y+.0225), arrowprops={"arrowstyle": "->", "color": "#404040", "lw":1.4})
        ax.text(.015, y-.075, note, fontsize=8.4, color="#444444", va="top")
    ax.text(.015, .018, "Conceptual relationships; no participant data or effect estimates.", fontsize=8.5, color="#555555")
    fig.tight_layout(pad=.7)
    for ext in ("png", "svg", "pdf"):
        fig.savefig(out / f"figure_1_mechanisms.{ext}", dpi=400, facecolor="white")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 5.8))
    ax.set(xlim=(-1.75, 1.75), ylim=(-1.58, 1.65))
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#888888")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("Metabolic cost increases →", labelpad=12)
    ax.set_ylabel("Recovery error increases →", labelpad=12)
    ax.axhline(0, color="#dddddd", lw=1, zorder=0)
    ax.axvline(0, color="#dddddd", lw=1, zorder=0)
    ax.scatter([0], [0], s=40, color="#333333", zorder=4)
    ax.text(.07, .055, "Common baseline", fontsize=9)
    arrows = [
        ((-1.04, .81), (-1.04, 1.1), "Lower cost, worse recovery\nInadequate stabilization?", "#a33b32"),
        ((-1.08, -.72), (-1.02, -1.13), "Lower cost, better recovery\nCandidate coordination benefit", "#347348"),
        ((1.02, -.72), (1.01, -1.13), "Higher cost, better recovery\nFunctional compensation?", "#176b83"),
        ((-1.25, 0), (-1.14, -.24), "Lower cost, preserved recovery\nMechanical assistance?", "#8a5a19")
    ]
    for xy, labelxy, label, color in arrows:
        ax.annotate("", xy=xy, xytext=(0, 0), arrowprops={"arrowstyle": "->", "lw":1.8, "color":color})
        ax.text(*labelxy, label, ha="center", va="center", fontsize=8.6, color=color,
                bbox={"facecolor":"white", "edgecolor":"none", "pad":2})
    ax.text(.95, .85, "Interpret at matched\ntask demands and\nsupport conditions.", ha="center", color="#444444", fontsize=9)
    ax.text(0, 1.48, "Schematic directions, not a dataset", ha="center", color="#555555", fontsize=9)
    fig.tight_layout(pad=1.2)
    for ext in ("png", "svg", "pdf"):
        fig.savefig(out / f"figure_2_interpretation.{ext}", dpi=400, facecolor="white")
    plt.close(fig)


def title_page(title, supplement=False):
    article = "Supplementary Material S1" if supplement else "Hypothesis and Theory"
    return f"""# {title}

**{article}**

**Sayuj Krishnan** — provisional author list

Affiliation: [author to confirm]

Corresponding author and email: [author to confirm]

Running title: {RUNNING}

Target journal: Frontiers in Aging — Musculoskeletal Aging

Version: 1.0 | 2 October 2026 | Author-review draft

```{{=openxml}}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

"""


def prop(parent, tag, attrs):
    item = parent.find(W(tag))
    if item is None:
        item = ET.SubElement(parent, W(tag))
    for key, value in attrs.items():
        item.set(W(key), str(value))
    return item


def restyle(path):
    with zipfile.ZipFile(path) as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    styles = ET.fromstring(parts["word/styles.xml"])
    # ElementTree drops declarations referenced only inside mc:Ignorable.
    # This draft uses baseline OOXML features, so remove that compatibility hint.
    mc_ignorable = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Ignorable"
    styles.attrib.pop(mc_ignorable, None)
    defaults = styles.find(W("docDefaults"))
    rp = defaults.find("w:rPrDefault/w:rPr", NS)
    prop(rp, "rFonts", {"ascii":"Times New Roman", "hAnsi":"Times New Roman", "cs":"Times New Roman"})
    for key in ("asciiTheme", "hAnsiTheme", "cstheme", "eastAsiaTheme"):
        rp.find(W("rFonts")).attrib.pop(W(key), None)
    prop(rp, "sz", {"val":24}); prop(rp, "szCs", {"val":24})
    pp = defaults.find("w:pPrDefault/w:pPr", NS)
    prop(pp, "spacing", {"line":240, "lineRule":"auto", "after":120})
    for style in styles.findall(W("style")):
        sid = style.get(W("styleId"), "")
        if sid.startswith("Heading"):
            p = style.find(W("pPr"))
            if p is None: p = ET.SubElement(style, W("pPr"))
            prop(p, "keepNext", {}); prop(p, "spacing", {"before":200, "after":120})
            r = style.find(W("rPr"))
            if r is None: r = ET.SubElement(style, W("rPr"))
            prop(r, "rFonts", {"ascii":"Times New Roman", "hAnsi":"Times New Roman"})
            prop(r, "sz", {"val":28 if sid in ("Heading1", "Heading2") else 24})
            prop(r, "color", {"val":"000000"})
    parts["word/styles.xml"] = ET.tostring(styles, encoding="utf-8", xml_declaration=True)
    document = ET.fromstring(parts["word/document.xml"])
    document.attrib.pop(mc_ignorable, None)
    body = document.find(W("body"))
    for p in body.findall(W("p")):
        text = "".join(p.itertext())
        if text in ("Tables", "Figures", "References") or text.startswith("Table 2."):
            pp = p.find(W("pPr"))
            if pp is None: pp = ET.SubElement(p, W("pPr"))
            prop(pp, "pageBreakBefore", {})
        ps = p.find("w:pPr/w:pStyle", NS)
        if ps is not None and ps.get(W("val")) == "Bibliography":
            pp = p.find(W("pPr"))
            prop(pp, "spacing", {"line":240, "lineRule":"auto", "before":0, "after":40})
            prop(pp, "keepLines", {})
        if p.find(".//w:drawing", NS) is not None:
            pp = p.find(W("pPr"))
            if pp is None: pp = ET.SubElement(p, W("pPr"))
            prop(pp, "keepNext", {})
    for table in body.findall(W("tbl")):
        for index, row in enumerate(table.findall(W("tr"))):
            trp = row.find(W("trPr"))
            if trp is None: trp = ET.SubElement(row, W("trPr"))
            prop(trp, "cantSplit", {})
            if index == 0: prop(trp, "tblHeader", {})
            for run in row.findall(".//w:r", NS):
                rpr = run.find(W("rPr"))
                if rpr is None: rpr = ET.SubElement(run, W("rPr"))
                prop(rpr, "sz", {"val":20})
    sec = body.find(W("sectPr"))
    prop(sec, "pgSz", {"w":11906, "h":16838})
    prop(sec, "pgMar", {"top":1440, "bottom":1440, "left":1440, "right":1440, "header":720, "footer":720})
    prop(sec, "lnNumType", {"countBy":1, "start":1, "restart":"continuous", "distance":240})
    parts["word/document.xml"] = ET.tostring(document, encoding="utf-8", xml_declaration=True)
    # Pandoc's existing footer relationship makes page numbering portable.
    footer_names = [name for name in parts if re.fullmatch(r"word/footer\d+\.xml", name)]
    if footer_names:
        for name in footer_names:
            parts[name] = FOOTER_XML
    else:
        relpath = "word/_rels/document.xml.rels"
        rel = ET.fromstring(parts[relpath])
        relns = "http://schemas.openxmlformats.org/package/2006/relationships"
        existing = {r.attrib["Id"] for r in rel}
        num = 99
        while f"rId{num}" in existing: num += 1
        rid = f"rId{num}"
        ET.SubElement(rel, "{" + relns + "}Relationship", {"Id":rid, "Type":"http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer", "Target":"footer99.xml"})
        # Package manifests use the default namespace for importer compatibility.
        ET.register_namespace("", relns)
        parts[relpath] = ET.tostring(rel, encoding="utf-8", xml_declaration=True)
        rns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        footer_ref = ET.Element(W("footerReference"), {W("type"):"default", "{"+rns+"}id":rid})
        sec.insert(0, footer_ref)
        parts["word/document.xml"] = ET.tostring(document, encoding="utf-8", xml_declaration=True)
        parts["word/footer99.xml"] = FOOTER_XML
        ct = ET.fromstring(parts["[Content_Types].xml"])
        ET.SubElement(ct, "{http://schemas.openxmlformats.org/package/2006/content-types}Override", {"PartName":"/word/footer99.xml", "ContentType":"application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"})
        ET.register_namespace("", "http://schemas.openxmlformats.org/package/2006/content-types")
        parts["[Content_Types].xml"] = ET.tostring(ct, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in parts.items(): archive.writestr(name, data)


def build(markdown, output, cite=False):
    args = ["pandoc", markdown, "--from=markdown-implicit_figures+tex_math_dollars", "--standalone", "--output", output,
            "--metadata=lang:en-US", "--resource-path=."]
    if cite: args += ["--citeproc", "--bibliography=references.json", "--csl=harvard.csl"]
    call(args)
    previews = ROOT / "preview"
    previews.mkdir(exist_ok=True)
    shutil.copy2(ROOT / output, previews / output.replace(".docx", "_pandoc.docx"))
    restyle(ROOT / output)
    office = "/home/sayuj/.codex/plugins/cache/claude-cowork/anthropic-skills/1.0.0/skills/docx/scripts"
    sys.path.insert(0, office)
    from office.soffice import run_soffice
    result = run_soffice(["--headless", "--convert-to", "pdf", "--outdir", str(ROOT), str(ROOT / output)], capture_output=True, text=True, timeout=90)
    if result.returncode: raise RuntimeError(result.stdout + result.stderr)
    pdf = ROOT / output.replace(".docx", ".pdf")
    if not pdf.exists(): raise RuntimeError(result.stdout + result.stderr)
    if pdf.stat().st_mtime < (ROOT / output).stat().st_mtime:
        raise RuntimeError("PDF is older than the generated Word document.")
    call(["pdftotext", "-layout", pdf, pdf.with_suffix(".txt")])


def main():
    refs = json.loads((ROOT / "references.json").read_text())
    body = (ROOT / "manuscript_body.md").read_text().replace("{width=95%}", "{width=6.15in}")
    # Pandoc's OMML writer omits TeX tag labels; keep labels editable and visible.
    body = re.sub(r"\\tag\{(\d+)\}", r"\\qquad(\1)", body)
    keys = set(re.findall(r"@([a-z]+\d+)", body))
    refkeys = {r["id"] for r in refs}
    assert keys == refkeys, {"missing":sorted(keys-refkeys), "unused":sorted(refkeys-keys)}
    figures()
    (ROOT / "manuscript.md").write_text(title_page(TITLE) + body)
    supplement = ROOT / "supplement"
    supplement.mkdir(exist_ok=True)
    for name in ("recoil_model.py", "recoil_model_checks.json", "recoil_sensitivity.csv", "recoil_sensitivity.png", "recoil_sensitivity.svg", "render_recoil.py"):
        shutil.copy2(DOSSIER / name, supplement / name)
    check = json.loads((supplement / "recoil_model_checks.json").read_text())
    assert sha256((supplement / "recoil_model.py").read_bytes()).hexdigest() == check["script_sha256"]
    supp_body = (ROOT / "supplement_body.md").read_text()
    (ROOT / "supplement_S1.md").write_text(title_page("Supplementary Material S1: verification of the illustrative viscoelastic balance", True) + supp_body)
    build("manuscript.md", "manuscript.docx", True)
    build("supplement_S1.md", "supplement_S1.docx")
    with zipfile.ZipFile(ROOT / "manuscript.docx") as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        equations = len(document.findall(".//m:oMath", NS))
        table_count = len(document.findall(".//w:tbl", NS))
        images = len([x for x in archive.namelist() if x.startswith("word/media/")])
        assert equations >= 6 and table_count == 2 and images == 2
        assert document.find(".//w:lnNumType", NS) is not None
        assert any("footer" in x for x in archive.namelist())
    text = (ROOT / "manuscript.txt").read_text()
    assert "CITATION NOT FOUND" not in text and "[@" not in text
    text_without_line_numbers = re.sub(r"(?m)^\s*\d+\s+", "", text)
    for r in refs:
        # DOI presence independently checks that every bibliography entry rendered.
        if "DOI" in r:
            assert r["DOI"].lower() in re.sub(r"\s+", "", text_without_line_numbers).lower(), r["id"]
    abstract = body.split("## Abstract\n\n",1)[1].split("\n\n**Keywords",1)[0]
    main_text = body.split("## 1. Introduction",1)[1].split("## Declarations",1)[0]
    stats = {"built_utc": datetime.now(timezone.utc).isoformat(), "references":len(refs),
             "abstract_words_approx":len(abstract.split()), "main_text_words_approx":len(main_text.split()),
             "editable_math_objects":equations, "tables":table_count, "figures":images,
             "manuscript_pages":text.count("\f"), "supplement_pages":(ROOT / "supplement_S1.txt").read_text().count("\f"),
             "citation_keys_complete":True, "bibliography_dois_rendered":True,
             "model_script_hash_matches_verified_artifact":True,
             "remaining_author_checks":["author list", "affiliations", "correspondence", "funding", "conflicts", "contributions", "scientific and AI review", "optional archive location/license if used"]}
    (ROOT / "BUILD_CHECKS.json").write_text(json.dumps(stats, indent=2) + "\n")
    print(json.dumps(stats, indent=2))
    if "--review" in sys.argv:
        print(call([sys.executable, ROOT / "render_review.py"]))


if __name__ == "__main__":
    main()
