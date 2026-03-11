all: main.pdf

main.pdf: main.tex references.bib sections/*.tex
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex

clean:
	rm -f *.aux *.log *.bbl *.blg *.out *.toc *.lof *.lot *.pdf
