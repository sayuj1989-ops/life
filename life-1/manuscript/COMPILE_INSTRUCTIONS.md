# LaTeX Compilation Instructions

## Quick Compilation

```bash
cd manuscript
pdflatex main_countercurvature.tex
bibtex main_countercurvature
pdflatex main_countercurvature.tex
pdflatex main_countercurvature.tex
```

## What to Check After Compilation

### 1. Citations
- Open PDF and search for `[?]` or `??` - should find none
- All citations should show as `[1]`, `[2]`, etc.

### 2. Figures
- **Fig. 1**: Should show 4 panels (A-D) from countercurvature metrics
- **Fig. 2**: Should show phase diagram with scoliosis regimes
- All figures should be clear and high-resolution

### 3. Equations
- All equations should be numbered sequentially
- Check that equation numbers match references in text (if any)

### 4. References Section
- Should appear at the end of the document
- All cited works should be listed
- Format should be consistent

## If LaTeX is Not Installed

### Option 1: Install LaTeX (macOS)
```bash
brew install --cask mactex
```

### Option 2: Use Overleaf (Online)
1. Go to https://www.overleaf.com
2. Create new project
3. Upload:
   - `main_countercurvature.tex`
   - `refs.bib`
   - All PDF figures in `manuscript/` directory
   - `figure1.png` (upload to root or adjust path)
4. Compile in browser

### Option 3: Use Docker
```bash
docker run --rm -v $(pwd):/data texlive/texlive:latest pdflatex main_countercurvature.tex
```

## Common Issues

### Missing Figures
- **Error**: `! LaTeX Error: File 'fig_countercurvature_panelA.pdf' not found.`
- **Fix**: Ensure all PDF figures are in `manuscript/` directory
- **Check**: `ls manuscript/fig_*.pdf` should show 5 files

### Missing Bibliography
- **Error**: Citations show as `[?]`
- **Fix**: Run `bibtex main_countercurvature` between pdflatex runs
- **Check**: `main_countercurvature.bbl` should be generated

### Figure Path Issues
- **Error**: `figure1.png` not found
- **Fix**: Ensure `figure1.png` is in root directory (one level up from `manuscript/`)
- **Check**: `ls ../figure1.png` from manuscript directory

## Expected Output Files

After successful compilation:
- `main_countercurvature.pdf` - Final PDF
- `main_countercurvature.aux` - Auxiliary file
- `main_countercurvature.bbl` - Bibliography file
- `main_countercurvature.blg` - BibTeX log
- `main_countercurvature.log` - Compilation log

## Verification Checklist

- [ ] PDF compiles without errors
- [ ] All citations resolve (no `[?]`)
- [ ] All figures display correctly
- [ ] Equation numbers are sequential
- [ ] Bibliography appears at end
- [ ] Page count is reasonable (typically 15-25 pages)
- [ ] No overfull/underfull hbox warnings (minor, can ignore)

## Next Steps

Once PDF compiles successfully:
1. Review PDF for content and formatting
2. Check all figures are clear
3. Verify all numerical values are correct
4. Proceed to submission using `PRX_LIFE_SUBMISSION_CHECKLIST.md`


