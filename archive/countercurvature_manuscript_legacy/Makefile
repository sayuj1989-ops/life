.PHONY: help venv deps data figs all clean

VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

help:
	@echo "Targets:"
	@echo "  make venv   - create virtualenv"
	@echo "  make deps   - install dependencies"
	@echo "  make data   - generate all CSVs into results/"
	@echo "  make figs   - generate all figures into figures/"
	@echo "  make all    - data + figs + update manuscript placeholders"
	@echo "  make clean  - remove results/ figures/ and venv"

venv:
	@test -d $(VENV) || python3 -m venv $(VENV)

deps: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

data: deps
	@mkdir -p results figures
	$(PY) -m scripts.sweep_params --config config/default.yaml
	$(PY) -m scripts.alphafold_reanalysis --config config/alphafold.yaml

figs: deps
	@mkdir -p results figures
	$(PY) -m scripts.make_figures --config config/default.yaml

all: data figs
	$(PY) -m scripts.update_manuscript --config config/default.yaml

clean:
	rm -rf $(VENV) results figures

