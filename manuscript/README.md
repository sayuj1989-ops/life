# Manuscript Structure Documentation

## Overview
This directory contains the main manuscript "Biological Counter-Curvature: An Information--Cosserat Framework for Vertebral Geometry and Adolescent Scoliosis" by Dr. Sayuj Krishnan S.

## Main Files

### main.tex
The primary LaTeX document that orchestrates the entire manuscript. It includes:
- Document class and package setup
- Custom macros for mathematical notation
- Title, author, and date information
- All section inputs in proper order

### references.bib
Consolidated bibliography containing **44 unique entries** merged from multiple sources:
- `countercurvature/references.bib` (38 entries)
- `manuscript/references.bib` (original 24 entries)
- `life-1/manuscript/refs.bib` (21 entries)
- Note: 2 duplicate entries removed during consolidation

All 10 citations used in the manuscript are verified to be present in this file.

## Sections

The manuscript is organized into the following sections (in order):

1. **abstract.tex** (7 lines) - Manuscript abstract
2. **introduction.tex** (26 lines) - Introduction to biological countercurvature
3. **theory.tex** (88 lines) - Theoretical framework including:
   - Information--Cosserat Manifold
   - Biological metric and effective energy
   - Force and moment balance equations
4. **methods.tex** (40 lines) - Computational methods and implementation
5. **results.tex** (33 lines) - Numerical results and findings
6. **discussion.tex** (45 lines) - Interpretation and context including:
   - Biological countercurvature interpretation
   - Links to developmental genetics
   - Relation to existing biomechanical models
   - Alternative mechanisms
7. **conclusion.tex** (3 lines) - Summary and future directions
8. **availability.tex** (3 lines) - Code and data availability statement
9. **tables.tex** (41 lines) - Computational model parameters table
10. **figures.tex** (67 lines) - Figure captions and placements

Note: `sections/significance.tex` is commented out in main.tex and not included.

## Building the Manuscript

### Using Make
```bash
# Full build with bibliography
make all

# Quick build without bibliography
make quick

# Clean auxiliary files
make clean

# Clean everything including PDF
make cleanall
```

### Manual Build
```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

## Citations

The manuscript uses 10 unique citations:
- gazzola2018forward
- green2018spinal
- grimes2016zebrafish
- moulton2013morphoelastic
- pourquie2011vertebrate
- pyelastica_zenodo
- rodriguez1994stress
- weinstein2008adolescent
- wellik2007hox
- white_panjabi_spine

All citations are properly referenced in the consolidated `references.bib` file.

## Figures and Graphics

Figure files are expected in the `figures/` directory, with LaTeX also checking `../figures/main/` as specified in the Makefile's TEXINPUTS path.

## Version Notes

### Sections Evaluation
The repository contains alternative section versions in `/edited_sections/` with `_v2` suffix. After evaluation:
- Most v2 sections are empty placeholders or incomplete
- Current sections in `manuscript/sections/` are complete and comprehensive
- The existing sections have been retained as the authoritative versions

### Bibliography Consolidation
The bibliography has been consolidated from multiple sources to ensure:
- No duplicate entries (2 duplicates removed)
- All cited references are included
- Comprehensive coverage of related literature (44 entries total)

## Quality Checks

✅ All section files exist and have content  
✅ All citations are present in bibliography  
✅ Bibliography is properly formatted BibTeX  
✅ Main document structure is complete  
✅ Build scripts (Makefile) are configured  

## Contact

**Author:** Dr. Sayuj Krishnan S, MBBS, DNB (Neurosurgery)  
**Email:** dr.sayujkrishnan@gmail.com  
**Institution:** Yashoda Hospitals, Malakpet, Hyderabad, India
