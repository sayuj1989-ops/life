---
description: Create PowerPoint presentation from research content
---

# Create Presentation Workflow

Generate professional presentation slides from research documents using the pptx skill.

## Prerequisites

- Research content (Markdown document or framework)
- Key figures for visualization
- Clear narrative structure

## Steps

### 1. Identify Presentation Scope

Determine:

- Target audience (conference, seminar, defense)
- Time limit (10 min → ~10 slides, 20 min → ~20 slides)
- Key messages (3-5 main points)
- Essential figures to include

### 2. Outline Slide Structure

Standard research presentation structure:

**Title Slide**

- Title
- Author(s)
- Affiliation
- Date/Conference

**Introduction** (2-3 slides)

- Motivation and problem statement
- Research question
- Background context

**Methods/Framework** (3-4 slides)

- Core theoretical approach
- Key equations or models
- Methodology overview

**Results** (3-4 slides)

- Main findings
- Key figures and visualizations
- Data/simulations

**Discussion** (2 slides)

- Implications
- Future directions

**Conclusion** (1 slide)

- Summary of key points
- Take-home message

### 3. Extract Content from Research Document

Identify which sections of your research document map to each slide:

- Copy key equations
- Note figure references
- Extract bullet points
- Highlight important quotes

### 4. Create Presentation

Use the pptx skill to generate slides:

```
Ask: "Create a 15-slide presentation from the scoliosis theoretical framework research"
```

Or be more specific:

```
Ask: "Create a presentation with these sections:
- Title: Biophysical Origins of Scoliosis
- Slide 2: The Gravitational Paradox
- Slide 3: Cosserat Rod Model (include equation for curvature)
- Slide 4: Control Theory with Delay
- Slide 5: Phase diagram figure from research/figures/
..."
```

### 5. Customize Design

Request specific design elements:

- Color scheme matching institution/theme
- Font preferences
- Layout style (minimalist, academic, visual)

Example:

```
Ask: "Use a professional blue color scheme with sans-serif fonts"
```

### 6. Add Figures

Embed key visualizations:

```
Ask: "Add the phase diagram figure from research/figures/scoliosis_phase_diagram.png to slide 8"
```

### 7. Refine Mathematical Content

Ensure equations are readable:

- Use large font sizes (≥18pt for equations)
- Simplify complex derivations
- Highlight key terms

Example:

```
Ask: "Make the equation on slide 4 larger and highlight the delay term τ"
```

### 8. Review and Iterate

Check the presentation:

- Is each slide self-contained?
- Are figures legible?
- Is text minimal (max 5-7 bullet points per slide)?
- Do equations render clearly?

Request revisions:

```
Ask: "Reduce text on slide 3 to just the key points"
Ask: "Split slide 6 into two slides for better pacing"
```

### 9. Export and Test

Save the final presentation and test:

- Open in PowerPoint/Keynote
- Check animations (if any)
- Verify figures display correctly
- Practice timing

## Tips for Effective Science Presentations

### Content

- **One message per slide**: Each slide should convey a single idea
- **Minimal text**: Use bullet points, not paragraphs
- **Visual dominance**: Prefer figures over text
- **Progressive disclosure**: Build complex ideas across multiple slides

### Design

- **High contrast**: Dark text on light background (or vice versa)
- **Large fonts**: Min 24pt for body text, 36pt+ for titles
- **Consistent style**: Same fonts/colors throughout
- **White space**: Don't crowd slides

### Equations

- **Selective**: Only show key equations
- **Annotations**: Label variables and terms
- **Build complexity**: Show simpler form first, then full equation
- **Highlight**: Use color/boxes for important terms

### Figures

- **Readable**: Axes labels visible from back of room
- **Captions**: Include brief caption or title
- **Annotations**: Point out key features
- **Consistency**: Similar style across all figures

## Common Requests

### Title Slide

```
Ask: "Create a title slide with:
Title: [Your Title]
Subtitle: [Conference/Event]
Author: [Your Name]
Institution: [Your Institution]
Date: [Presentation Date]"
```

### Equation Slide

```
Ask: "Create a slide titled 'Core Framework' with the Lagrangian equation from section 2.2 of the research document"
```

### Figure Comparison

```
Ask: "Create a slide comparing two figures side-by-side: phase_diagram.png and energy_landscape.png"
```

### Results Summary

```
Ask: "Create a results summary slide with 4 key findings as bullet points"
```

## Troubleshooting

### Equations Not Rendering

- Equations may be converted to images
- Request larger size or different format
- Consider splitting complex equations

### Figures Too Small

```
Ask: "Make the figure on slide 5 fill more of the slide"
```

### Too Much Text

```
Ask: "Condense slide 4 to just 3-4 key bullet points"
```

### Inconsistent Style

```
Ask: "Apply consistent formatting to all slides using the same template"
```
