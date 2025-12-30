# Makefile for IEC Model Manuscript
# Compiles LaTeX manuscript to PDF

MAIN = main_countercurvature_refined
TEX = $(MAIN).tex
PDF = $(MAIN).pdf
BIB = references.bib

# Default target
all: $(PDF)

# Compile PDF
$(PDF): $(TEX) sections/*.tex $(BIB)
	pdflatex $(MAIN)
	bibtex $(MAIN)
	pdflatex $(MAIN)
	pdflatex $(MAIN)
	@echo "✅ Manuscript compiled: $(PDF)"

# Quick compile (no bibliography)
quick: $(TEX) sections/*.tex
	pdflatex $(MAIN)
	@echo "✅ Quick compile complete (no bibliography)"

# Clean auxiliary files
clean:
	rm -f *.aux *.log *.out *.bbl *.blg *.toc *.lof *.lot
	@echo "✅ Cleaned auxiliary files"

# Clean everything including PDF
cleanall: clean
	rm -f $(PDF)
	@echo "✅ Cleaned all files including PDF"

# View PDF (macOS)
view: $(PDF)
	open $(PDF)

# View PDF (Linux)
view-linux: $(PDF)
	xdg-open $(PDF)

# Help
help:
	@echo "Available targets:"
	@echo "  make all      - Compile full manuscript with bibliography"
	@echo "  make quick    - Quick compile (no bibliography)"
	@echo "  make clean    - Remove auxiliary files"
	@echo "  make cleanall - Remove all files including PDF"
	@echo "  make view     - Open PDF (macOS)"
	@echo "  make view-linux - Open PDF (Linux)"

.PHONY: all quick clean cleanall view view-linux help



