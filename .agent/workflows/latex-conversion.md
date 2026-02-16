---
description: Convert research Markdown to LaTeX manuscript
---

# LaTeX Conversion Workflow

Convert research Markdown documents to manuscript-ready LaTeX format.

## Prerequisites

- Research document in Markdown format
- Python 3.7+ installed
- LaTeX distribution (for PDF generation)

## Steps

### 1. Prepare Markdown Document

Ensure your Markdown document follows research conventions:

- Single H1 for title
- H2/H3 for sections
- Mathematical equations in `$...$` or `$$...$$`
- Figures using `![caption](path)` syntax
- Citations using `[@author_year]` format

### 2. Check Figure References

// turbo

```bash
python .agent/skills/research-workflow/scripts/embed_figures.py research/your_document.md --figures-dir research/figures --verbose
```

This validates that all figures exist and are properly referenced.

### 3. Convert to LaTeX

// turbo

```bash
python .agent/skills/research-workflow/scripts/md_to_latex.py research/your_document.md --output manuscript/ manuscript.tex
```

**Options:**

- `--output PATH`: Specify output file path (default: same name with .tex extension)
- `--title "Custom Title"`: Override document title

### 4. Review LaTeX Output

Open `manuscript.tex` and check:

- Title and author information
- Section structure
- Equation formatting
- Figure paths
- Bibliography references

### 5. Add Bibliography (if needed)

If you have citations, create or update `references.bib`:

```bibtex
@article{author2023,
  title={Paper Title},
  author={Author, A.},
  journal={Journal Name},
  year={2023}
}
```

### 6. Generate PDF

// turbo

```bash
python .agent/skills/research-workflow/scripts/generate_pdf.py manuscript.tex --clean
```

**Options:**

- `--runs N`: Number of compilation passes (default: 2)
- `--clean`: Remove auxiliary files after compilation

### 7. Verify Output

Review the generated PDF:

- Check all equations render correctly
- Verify figures are embedded properly
- Ensure citations link to bibliography
- Review overall formatting

## Troubleshooting

### Missing Figures

Run the figure checker to see which figures are missing:

```bash
python .agent/skills/research-workflow/scripts/embed_figures.py research/your_document.md --figures-dir research/figures
```

### LaTeX Compilation Errors

- Check equation syntax (unmatched `$` or `$$`)
- Verify special characters are escaped
- Ensure figure files exist at specified paths
- Check BibTeX file format

### Mathematical Notation Issues

- Use `\\text{}` for text within equations
- Escape special characters: `\\_`, `\\%`, `\\&`
- Use `aligned` environment for multi-line derivations

## Best Practices

1. **Version Control**: Commit Markdown source before conversion
2. **Figure Paths**: Use relative paths from document location
3. **Citations**: Maintain references.bib file separately
4. **Compilation**: Run multiple passes for cross-references
5. **Backup**: Keep both Markdown and LaTeX versions
