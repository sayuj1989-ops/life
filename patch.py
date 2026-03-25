import re

with open('notes/synthesis/2026-13__microgravity_spine.md', 'r') as f:
    text = f.read()

replacement = """1.  **Reorganization of Integrin-Based Adhesions** (Observed)
    *   Under microgravity, focal adhesion numbers decrease, and integrin contacts are redistributed above the nucleus within 30 minutes. This disrupts cytoskeletal stability and extracellular matrix tension, impacting structural adaptation.
    *   *Citation:* Andreeva et al., *Life (Basel)* (2022).

2.  **Collagen Network Switch** (Observed)
    *   Prolonged spaceflight in rat femurs leads to reduced mineralization and downregulation of collagen type I, replaced by the appearance of collagen type III, typical of early embryonic tissues and inflammation.
    *   *Citation:* Andreeva et al., *Life (Basel)* (2022) / Arnaud et al., *J. Gravit. Physiol.* (2000).

3.  **Matrisome Transcriptional Divergence** (Observed)
    *   The transcriptional activity of matrisome-related genes (e.g., COL1A1, THBS, PLOD1/2) undergoes complex time-dependent shifts in microgravity, indicating that structural uncoupling begins at the genomic level before macroscopic tissue failure occurs.
    *   *Citation:* Andreeva et al., *Life (Basel)* (2022)."""

text = re.sub(r'1\.\s+\*\*Accelerated.*?\(2025\)\.', replacement, text, flags=re.DOTALL)

with open('notes/synthesis/2026-13__microgravity_spine.md', 'w') as f:
    f.write(text)
