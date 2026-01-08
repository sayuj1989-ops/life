# Overleaf Upload Guide - PRX Life Manuscript

**Quick Setup:** 5 minutes to upload and compile

---

## Step 1: Create Overleaf Project

1. Go to https://www.overleaf.com
2. Sign in (or create free account)
3. Click **"New Project"** → **"Blank Project"**
4. Name it: `PRX_Life_Countercurvature`

---

## Step 2: Upload Files

### Required Files (Upload to root of project):

1. **Main LaTeX file:**
   - `main_countercurvature.tex`

2. **Bibliography:**
   - `refs.bib`

3. **All 5 Figure PDFs:**
   - `fig_countercurvature_panelA.pdf`
   - `fig_countercurvature_panelB.pdf`
   - `fig_countercurvature_panelC.pdf`
   - `fig_countercurvature_panelD.pdf`
   - `fig_phase_diagram_scoliosis.pdf`

### How to Upload:

**Option A: Drag & Drop (Easiest)**
- Select all 7 files from your `manuscript/` folder
- Drag them into the Overleaf file browser
- Wait for upload to complete

**Option B: Upload Button**
- Click "Upload" button in Overleaf
- Select all 7 files
- Click "Upload"

---

## Step 3: Set Compiler

1. Click the **"Menu"** button (top left, hamburger icon)
2. Go to **"Settings"**
3. Set **"Compiler"** to: `pdfLaTeX`
4. Set **"Main document"** to: `main_countercurvature.tex`
5. Click **"Recompile"** or close settings (auto-compiles)

---

## Step 4: Compile

1. Click **"Recompile"** button (top toolbar)
2. Wait for compilation (usually 10-30 seconds)
3. Check for errors in the log

---

## Step 5: Fix Common Issues

### Issue 1: Missing Figures
**Error:** `! LaTeX Error: File 'fig_countercurvature_panelA.pdf' not found.`

**Fix:**
- Ensure all 5 PDF figures are uploaded to the **root** of the project (same level as `.tex` file)
- Check file names match exactly (case-sensitive)

### Issue 2: Citations Show as `[?]`
**Error:** Citations appear as `[?]` instead of `[1]`, `[2]`, etc.

**Fix:**
1. Click **"Menu"** → **"Logs and output files"**
2. Click **"Bibliography"** tab
3. Click **"Run BibTeX"** button
4. Click **"Recompile"** (may need 2-3 times)

### Issue 3: Package Not Found
**Error:** `! LaTeX Error: File 'amsmath.sty' not found.`

**Fix:**
- Overleaf should have all standard packages
- If missing, add to preamble: `\usepackage{amsmath}` (should already be there)

---

## Step 6: Verify PDF

### Checklist:
- [ ] PDF compiles without errors (green checkmark)
- [ ] All citations show as `[1]`, `[2]`, etc. (no `[?]`)
- [ ] **Figure 1** shows 4 panels (A-D) clearly
- [ ] **Figure 2** shows phase diagram clearly
- [ ] All equations are numbered
- [ ] Bibliography appears at end
- [ ] Page count looks reasonable (15-25 pages)

---

## Step 7: Download PDF

1. Click **"Download PDF"** button (top toolbar)
2. Save as: `main_countercurvature.pdf`
3. **This is your submission PDF!**

---

## Quick Reference: File Structure in Overleaf

```
PRX_Life_Countercurvature/
├── main_countercurvature.tex    ← Main file
├── refs.bib                      ← Bibliography
├── fig_countercurvature_panelA.pdf
├── fig_countercurvature_panelB.pdf
├── fig_countercurvature_panelC.pdf
├── fig_countercurvature_panelD.pdf
└── fig_phase_diagram_scoliosis.pdf
```

**All files should be at the root level (same folder).**

---

## Alternative: Install LaTeX Locally (macOS)

If you prefer local compilation:

```bash
# Install MacTeX (large download, ~4GB)
brew install --cask mactex

# Then compile:
cd manuscript
pdflatex main_countercurvature.tex
bibtex main_countercurvature
pdflatex main_countercurvature.tex
pdflatex main_countercurvature.tex
```

**Note:** Overleaf is recommended because:
- ✅ No installation needed
- ✅ Automatic BibTeX handling
- ✅ Easy collaboration
- ✅ Cloud backup
- ✅ Works on any device

---

## Troubleshooting

### PDF Won't Compile
1. Check **"Logs and output files"** for error messages
2. Common fixes:
   - Missing files → Upload missing files
   - Syntax error → Check line number in error message
   - Package missing → Add `\usepackage{...}` to preamble

### Citations Still Show `[?]`
1. **Menu** → **"Logs and output files"** → **"Bibliography"** tab
2. Click **"Run BibTeX"**
3. Click **"Recompile"** (repeat 2-3 times if needed)

### Figures Not Appearing
1. Check file names match exactly (case-sensitive)
2. Ensure PDFs are in root directory (not in subfolder)
3. Check `\includegraphics` paths in `.tex` file

---

## Next Steps After Compilation

Once PDF is ready:
1. ✅ Review PDF for content and formatting
2. ✅ Use `FINAL_PDF_CHECK.md` for final verification
3. ✅ Proceed to PRX Life submission using `PRX_LIFE_SUBMISSION_SUMMARY.md`

---

**Estimated Time:** 5-10 minutes  
**Difficulty:** Easy (drag & drop + click compile)

**You're almost there!** 🚀

