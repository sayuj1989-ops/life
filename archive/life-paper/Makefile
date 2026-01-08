.PHONY: help env reproduce longevity clean

VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

help:
	@echo "Publication-ready reproducibility targets:"
	@echo "  make env        - Create virtualenv and install dependencies"
	@echo "  make longevity  - Run longevity analysis (generates results/longevity/)"
	@echo "  make reproduce  - Full pipeline: longevity + copy figures to paper/"
	@echo "  make clean      - Remove .venv, results/, and generated files"

env:
	@test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

longevity: env
	@mkdir -p results/longevity
	$(PY) analysis/longevity/longevity_deep_dive.py \
		--input data/processed/bcc_analysis_data.json \
		--outdir results/longevity

reproduce: longevity
	@mkdir -p paper/figures paper/tables
	@cp results/longevity/*.pdf paper/figures/ 2>/dev/null || true
	@cp results/longevity/*.md paper/tables/ 2>/dev/null || true
	@echo "✅ Reproducibility complete! Check paper/figures/ and paper/tables/"

clean:
	rm -rf $(VENV) results/ paper/figures/*.pdf paper/tables/*.md


