# Quick Compilation Reference

## ✅ Files Ready for Compilation

All required files are present:
- ✅ `main_countercurvature.tex` (28 KB)
- ✅ `refs.bib` (6.7 KB)
- ✅ `fig_countercurvature_panelA.pdf` (16 KB)
- ✅ `fig_countercurvature_panelB.pdf` (17 KB)
- ✅ `fig_countercurvature_panelC.pdf` (14 KB)
- ✅ `fig_countercurvature_panelD.pdf` (16 KB)
- ✅ `fig_phase_diagram_scoliosis.pdf` (261 KB)

---

## 🚀 Option A: Overleaf (Recommended - 5 minutes)

**See:** `OVERLEAF_UPLOAD_GUIDE.md` for detailed steps

**Quick Steps:**
1. Go to https://www.overleaf.com
2. Create new project → Blank Project
3. Upload all 7 files (drag & drop)
4. Set compiler to `pdfLaTeX`
5. Click "Recompile"
6. Download PDF

**Time:** 5-10 minutes  
**Difficulty:** Easy

---

## 💻 Option B: Local LaTeX (If Installed)

```bash
cd manuscript
pdflatex main_countercurvature.tex
bibtex main_countercurvature
pdflatex main_countercurvature.tex
pdflatex main_countercurvature.tex
```

**Check if installed:**
```bash
which pdflatex  # Should show path if installed
```

**Install on macOS:**
```bash
brew install --cask mactex  # Large download (~4GB)
```

---

## ✅ After Compilation - Verification Checklist

- [ ] PDF compiles without errors
- [ ] All citations show as `[1]`, `[2]`, etc. (no `[?]`)
- [ ] Figure 1 shows 4 panels (A-D)
- [ ] Figure 2 shows phase diagram
- [ ] All equations numbered
- [ ] Bibliography appears at end
- [ ] Page count reasonable (15-25 pages)

---

## 📋 Next Steps

Once PDF is ready:
1. Review using `FINAL_PDF_CHECK.md`
2. Submit using `PRX_LIFE_SUBMISSION_SUMMARY.md`

---

**Recommended:** Use Overleaf (easiest, no installation needed)

