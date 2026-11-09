# Floor transitions and functional aging — publication draft

Prepared for author review, 2 October 2026.

**Title:** The sitting pause as a mechanistic probe of recoil and adaptive control in functional aging

**Primary target:** Frontiers in Aging, Musculoskeletal Aging; Hypothesis and Theory.

**Candidate contribution:** a pause-based experimental framework separating inherited elastic return, fresh muscular preload and chronic functional transfer. Novelty is bounded by a targeted search and is not guaranteed. The paper proposes a potential healthspan mechanism, not an observed lifespan effect.

## Files

- manuscript.docx / manuscript.pdf: editable manuscript and rendered review copy.
- manuscript.md / manuscript_body.md: source text with reference keys.
- supplement_S1.docx / supplement_S1.pdf: analytic verification and scope limitations.
- figures/: two original schematics in PNG, SVG and PDF.
- supplement/: verified standard-library model, checks, all 225 scenarios and illustrative plot.
- references.json / reference_metadata/: bibliography and retained public DOI metadata.
- NOVELTY_AUDIT.md: closest prior art, candidate distinction and search limitations.
- JOURNAL_FIT.md: verified format match and author confirmations.
- COVER_LETTER.md: unsent local draft.
- BUILD_CHECKS.json: document structure, citation and artifact checks.
- BIBLIOGRAPHY_AUDIT.md: reference identities and metadata provenance.
- VISUAL_REVIEW.md: rendering observations and final validation.

publication_package.zip contains the manuscript, supplement, figures, curated references, source files and review notes. Raw public metadata and working previews are retained locally and omitted from the delivery archive.

## Rebuild

`/home/sayuj/life/.venv/bin/python rebuild_documents.py`

The build uses installed Pandoc, Matplotlib, LibreOffice and pdftotext, works offline from the supplied references, and preserves editable Office math. `python3 fetch_references.py` is a separate public-metadata retrieval operation and is not needed to rebuild. Rejected DOI matches are retained in the metadata cache for provenance, not used in the bibliography.

The supplementary model was verified independently in the research dossier; its original script hash and outputs are retained. Document checks do not substitute for human biological validation. No withdrawn or unresolved spine simulation supplies evidence here.

## Status and author action

Complete scientific review draft with journal-fit and novelty notes. Author names/affiliations, correspondence, funding, conflicts, contributions, final scientific/AI review and archive details remain to be confirmed before submission. No journal contact, submission, publication, payment, commit or push has been performed.
