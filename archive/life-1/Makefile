.PHONY: env lint format test figures paper all clean

PY ?= python3

env:
	$(PY) -m pip install -U pip
	$(PY) -m pip install -e ".[dev]"

lint:
	$(PY) -m pip install ruff black
	ruff check src tests
	black --check src tests analysis

format:
	black src tests analysis

test:
	pytest -q

figures:
	$(PY) analysis/01_data_audit.py
	$(PY) analysis/02_validate_solvers.py
	$(PY) analysis/03_iec_phase_amp.py
	$(PY) analysis/04_countercurvature.py
	$(PY) analysis/05_longevity_demo.py

paper:
	@if command -v latexmk >/dev/null; then \
	  cd manuscript && latexmk -pdf -interaction=nonstopmode main_countercurvature.tex ; \
	else \
	  echo "latexmk not found; trying pandoc markdown -> PDF"; \
	  echo "(install docs extra or set up TeXLive for camera-ready)"; \
	fi

all: env test figures paper

clean:
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: build dist arxiv

build:
	$(PY) -m pip install build
	$(PY) -m build

dist: build
	$(PY) -m pip install dist/*.whl --force-reinstall

arxiv:
	bash scripts/arxiv_bundle.sh
