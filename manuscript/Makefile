# Makefile for Biological Countercurvature Manuscript

LATEX=pdflatex
BIBTEX=bibtex
MAIN=main
TEXINPUTS=.:./figures/main/:

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex references.bib
	export TEXINPUTS=$(TEXINPUTS) && \
	$(LATEX) $(MAIN) && \
	$(BIBTEX) $(MAIN) && \
	$(LATEX) $(MAIN) && \
	$(LATEX) $(MAIN)

quick:
	export TEXINPUTS=$(TEXINPUTS) && \
	$(LATEX) $(MAIN)

clean:
	rm -f *.aux *.log *.out *.bbl *.blg *.toc *.lof *.lot

cleanall: clean
	rm -f $(MAIN).pdf

.PHONY: all quick clean cleanall
