all:
	pdflatex main
	bibtex main
	pdflatex main
	pdflatex main

quick:
	pdflatex main

clean:
	rm -f *.aux *.log *.out *.bbl *.blg *.toc *.lof *.lot

cleanall: clean
	rm -f main.pdf
