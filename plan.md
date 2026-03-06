1. **Update Title and Abstract**:
   - Modify the title in `manuscript/main.tex` to remove the word "Spacetime" (e.g., "Biological Counter-Curvature: An Information–Cosserat Framework for Vertebral Geometry and Adolescent Scoliosis").
   - Condense `manuscript/sections/abstract.tex` to be under 150 words while retaining the core message, per Nature guidelines.

2. **Refine Content**:
   - Verify that there are no remaining mentions of 'consciousness' in the manuscript text (`manuscript/sections/discussion.tex`, etc.) as verified via `grep`.
   - Remove the heavy General Relativity analogy from `manuscript/sections/theory.tex` to make it more accessible for biomechanics journals.

3. **Fix Citations and References**:
   - Identify undefined citations in the LaTeX build log (e.g., those warned about during `pdflatex` compilation).
   - Fetch real, missing citations dynamically via Crossref/NCBI API and append them to `manuscript/references.bib` to resolve LaTeX warnings.
   - Remove or replace unpublished, future-dated references (e.g., 2026 dates, "in preparation", self-citations).

4. **Generate Missing Figures**:
   - Run the confirmed script `scripts/generate_nature_figures.sh` to generate the required Nature figures and ensure they exist.
   - Ensure the figure references in the manuscript are correctly linked and compile successfully.

5. **Test and Verify**:
   - Run the project's test suite (e.g., `pytest` and `ruff check .`) to ensure the changes are correct and have not introduced regressions.

6. **Complete pre-commit steps**:
   - Complete pre commit steps to make sure proper testing, verifications, reviews and reflections are done.

7. **Submit**:
   - Commit the changes to a new branch and submit the manuscript package.
