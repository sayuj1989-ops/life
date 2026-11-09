"""Rasterize the generated PDFs and prepare contact sheets for human inspection."""
from pathlib import Path
import json
import subprocess
import sys
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "preview"
OUT.mkdir(exist_ok=True)
report = {}
for stem in ("manuscript", "supplement_S1"):
    prefix = OUT / stem
    if "--contacts-only" not in sys.argv:
        subprocess.run(["pdftoppm", "-r", "110", "-png", str(ROOT / f"{stem}.pdf"), str(prefix)], check=True, capture_output=True)
    pages = (ROOT / f"{stem}.txt").read_text().count("\f")
    # Old preview pages from a longer draft must not enter the current review.
    paths = sorted(p for p in OUT.glob(f"{stem}-*.png") if int(p.stem.rsplit("-",1)[1]) <= pages)
    assert len(paths) == pages
    report[stem] = {"pages":len(paths), "contact_sheets":[]}
    for offset in range(0, len(paths), 8):
        group = paths[offset:offset+8]
        cols, tilew, tileh = 4, 360, 535
        rows = (len(group)+cols-1)//cols
        canvas = Image.new("RGB", (cols*tilew, rows*tileh), "#dddddd")
        draw = ImageDraw.Draw(canvas)
        for index, path in enumerate(group):
            im = Image.open(path).convert("RGB")
            im.thumbnail((tilew-16, tileh-32))
            x = (index % cols)*tilew + (tilew-im.width)//2
            y = (index // cols)*tileh + 25
            canvas.paste(im, (x,y))
            draw.text(((index % cols)*tilew+12, (index // cols)*tileh+6), path.stem, fill="black")
        target = OUT / f"{stem}_contact_{offset//8+1}.png"
        canvas.save(target)
        report[stem]["contact_sheets"].append(str(target))
(ROOT / "RENDER_CHECKS.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
