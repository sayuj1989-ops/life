# LaTeX Manuscript: Biological Countercurvature of Spacetime

## Files

- **`main_countercurvature.tex`**: Main LaTeX document with full structure
- **`refs.bib`**: Bibliography with placeholder entries for key references

## Quick Start

### Option 1: Overleaf

1. Create a new Overleaf project
2. Upload `main_countercurvature.tex` and `refs.bib`
3. Set main document to `main_countercurvature.tex`
4. Compile and start pasting content from your markdown drafts

### Option 2: Local LaTeX

```bash
cd manuscript
pdflatex main_countercurvature
bibtex main_countercurvature
pdflatex main_countercurvature
pdflatex main_countercurvature
```

Or use the Makefile (after updating it):

```bash
make -f Makefile_countercurvature all
```

## Content Sources

The LaTeX file has TODO comments indicating where to paste content from your markdown drafts:

- **Abstract**: `docs/paper_draft_abstract.md`
- **Significance**: `docs/paper_draft_significance.md`
- **Introduction**: Draft in `docs/` (or create new)
- **Methods**: 
  - IEC: `docs/paper_draft_methods_iec.md` (if exists)
  - Scoliosis: `docs/paper_draft_methods_scoliosis.md`
- **Results**: `docs/paper_draft_results_subsection.md`
- **Limitations**: `docs/paper_draft_limitations_outlook.md`

## Macros

The document defines convenient macros for recurring notation:

- `\Ifield` → I(s)
- `\gEff` → g_eff
- `\Dgeohat` → D̂_geo
- `\chiK` → χ_κ
- `\Slat` → S_lat
- `\Cobb` → θ_Cobb

## Figures

Figure placeholders are set up for:

1. **4-panel countercurvature figure** (`fig_countercurvature_panelA-D.pdf`)
2. **Phase diagram** (`fig_phase_diagram_scoliosis.pdf`)

Update the `\includegraphics` paths once you generate the actual figures.

## Bibliography

The `refs.bib` file contains a minimal but coherent seed bibliography with actual citations for:

- **PyElastica and Cosserat rods**: PyElastica software, Gazzola et al. (2018), Zhang et al. (2019), Naughton et al. (2021), Antman (2005)
- **Riemannian geometry and GR**: Lee (2018), Einstein (1916), Wald (1984)
- **Spinal biomechanics and scoliosis**: White & Panjabi (1990), Weinstein et al. (2008)
- **Microgravity and spinal health**: Green & Scott (2018), Marfia et al. (2023)

**Extend as needed** with additional references for:
- Information-elasticity coupling
- Analog gravity systems
- Plant growth and gravitropism
- Consciousness and information processing
- Additional spinal biomechanics papers

## Next Steps

1. **Paste content** from markdown drafts into the TODO sections
2. **Generate figures** and update file paths
3. **Replace placeholder citations** in `refs.bib` with actual references
4. **Extract quantitative values** using `docs/DATA_EXTRACTION_TEMPLATE.md`
5. **Tighten language** using `docs/PAPER_TIGHTENING_GUIDE.md`
6. **Finalize** and submit!

## Customization

- **Title/Authors**: Update in the preamble
- **Journal style**: Change `\documentclass` and packages as needed
- **Bibliography style**: Modify `\bibliographystyle{unsrtnat}` if required
- **Figure paths**: Update `\includegraphics` commands with actual file paths

