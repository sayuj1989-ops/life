---
name: research-workflow
description: Specialized workflow for theoretical biophysics research. Use when working with research documents, theoretical frameworks, mathematical derivations, or scientific papers. Triggers include creating research documents, converting between formats (Markdown/LaTeX/PDF), managing figures, citing references, or organizing theoretical frameworks. Supports scoliosis research, biomechanics, control theory, General Relativity applications, and mathematical modeling (Cosserat theory, AdS/CFT).
---

# Research Workflow Skill

Structured workflows for theoretical biophysics research, optimized for mathematical frameworks and scientific documentation.

## Quick Reference

| Task | Approach |
|------|----------|
| New research document | Use structured template from `assets/` |
| Markdown → LaTeX | `scripts/md_to_latex.py` |
| Generate PDF | `scripts/generate_pdf.py` |
| Embed figures | `scripts/embed_figures.py` |
| Domain concepts | See `references/domain-knowledge.md` |
| LaTeX templates | See `references/latex-templates.md` |

## Research Document Creation

### Standard Structure

Use this structure for theoretical frameworks:

1. **Abstract** - Concise summary (150-250 words)
2. **Introduction** - Context and motivation
3. **Theoretical Framework** - Core mathematical derivations
4. **Results** - Key findings and predictions
5. **Discussion** - Implications and future work
6. **References** - Citations in BibTeX format

### Mathematical Notation

Follow these conventions:

- **Vectors**: Bold ($\mathbf{r}$, $\mathbf{v}$)
- **Tensors**: Sans-serif ($\mathsf{T}$, $\mathsf{g}_{\mu\nu}$)
- **Operators**: Hat notation ($\hat{H}$, $\hat{L}$)
- **Physical quantities**: Italics ($E$, $m$, $c$)
- **Functions**: Roman ($\sin$, $\log$, $\text{erf}$)

### Equation Formatting

```markdown
For inline math: $E = mc^2$

For display equations:
$$
\frac{\partial \mathbf{r}}{\partial t} = \mathbf{v}
$$

For aligned derivations:
$$
\begin{aligned}
F &= ma \\
  &= m\frac{dv}{dt}
\end{aligned}
$$
```

## Figure Management

### Organization

Store figures in `research/figures/` with descriptive names:

- `scoliosis_phase_diagram.png`
- `cosserat_rod_schematic.svg`
- `energy_optimization_plot.pdf`

### Embedding in Markdown

```markdown
![Figure caption describing the content](../figures/filename.png)
```

### Embedding Script

Use `scripts/embed_figures.py` to automatically:

- Find referenced figures
- Check file existence
- Validate image formats
- Generate proper markdown syntax

## Format Conversion

### Markdown to LaTeX

Convert research Markdown to manuscript-ready LaTeX:

```bash
python .agent/skills/research-workflow/scripts/md_to_latex.py input.md --output manuscript.tex
```

Features:

- Preserves mathematical equations
- Converts markdown headings to LaTeX sections
- Handles figure references
- Generates BibTeX citations

See `references/latex-templates.md` for LaTeX document templates.

### PDF Generation

Generate publication-ready PDFs:

```bash
python .agent/skills/research-workflow/scripts/generate_pdf.py manuscript.tex
```

Automatically handles:

- Multiple LaTeX compilation passes
- Bibliography generation (BibTeX)
- Figure resolution optimization

## Domain Knowledge

For quick reference on theoretical concepts, see `references/domain-knowledge.md` which covers:

- Cosserat rod theory basics
- Control theory with delay fundamentals
- AdS/CFT correspondence in biology
- Standard notation conventions

## Research Prompts

### Creating Effective Prompts

Structure research prompts with:

1. **Objective** - Clear research question
2. **Background** - Relevant prior work
3. **Methodology** - Proposed approach
4. **Constraints** - Limitations and assumptions
5. **Deliverables** - Expected outputs

### Template

Use `.agent/templates/research-prompt.md` for consistent prompt structure.

## Collaboration Workflows

### Creating Word Documents

For sharing with collaborators who use Word:

```
Ask: "Convert the scoliosis framework to a Word document"
```

Uses the docx skill to create properly formatted documents with:

- Preserved equations (as images or MathType)
- Embedded figures
- Professional formatting

### Creating Presentations

For conferences and talks:

```
Ask: "Create a presentation from the gravity paradox research"
```

Uses the pptx skill to generate slides with:

- Title slide
- Key equations
- Figure visualizations
- Conclusion slide

### Tracked Changes

For collaborative editing:

```
Ask: "Add tracked changes suggesting revisions to section 3"
```

Uses the doc-coauthoring skill for structured document refinement.

## Best Practices

### Version Control

- Commit research documents to git regularly
- Use meaningful commit messages
- Tag significant versions (e.g., `v1.0-preprint`)

### Citation Management

- Store references in `references.bib`
- Use consistent citation keys (author_year_keyword)
- Include DOIs when available

### Code and Data

- Link to analysis scripts in `scripts/`
- Reference data files in `data/`
- Document computational methods

### Reproducibility

- Include software versions in methods
- Provide environment specifications
- Document random seeds for simulations

## Common Workflows

### New Theoretical Framework

1. Use template: `.agent/templates/theoretical-framework.md`
2. Fill in sections systematically
3. Add mathematical derivations
4. Generate figures with analysis scripts
5. Embed figures using `embed_figures.py`
6. Convert to LaTeX when ready for submission

### Literature Review Integration

1. Collect references in BibTeX format
2. Organize by topic in `references.bib`
3. Cite using `[@author_year]` syntax
4. Auto-generate bibliography on PDF creation

### Manuscript Preparation

1. Start with research Markdown document
2. Refine content using doc-coauthoring skill
3. Convert to LaTeX using `md_to_latex.py`
4. Fine-tune LaTeX formatting
5. Generate PDF using `generate_pdf.py`
6. Review and iterate

## Troubleshooting

### LaTeX Compilation Errors

- Check equation syntax (missing `$` or `$$`)
- Verify figure paths are correct
- Ensure BibTeX file exists
- Check for special characters needing escaping

### Figure Display Issues

- Verify figure file exists in specified path
- Check image format (PNG, PDF, SVG recommended)
- Ensure proper markdown syntax
- Use relative paths from document location

### Mathematical Notation

- Test complex equations in isolation first
- Use `\text{}` for text within math mode
- Split long equations with `aligned` environment
- Reference equations with `\label{}` and `\ref{}`
