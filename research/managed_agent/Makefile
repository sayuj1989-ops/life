.PHONY: help wp5 wp6 wp7 all list

PYTHON := python3

help:
	@printf '%s\n' \
		'Managed Agent Work Packages' \
		'==========================' \
		'  make wp5   - WP5: Literature landscape 2024-2026' \
		'  make wp6   - WP6: Fundable experiment proposal' \
		'  make wp7   - WP7: Editorial and reference audit' \
		'  make wp8   - WP8: Active Inference Simulation (Paper 5)' \
		'  make all   - Run WP5, WP6, WP7 sequentially' \
		'  make list  - List available work packages'

wp5:
	@echo "=== Launching WP5: Literature Landscape ==="
	cd $(dir $(MAKEFILE_LIST)) && export $$(cat .env | xargs) && $(PYTHON) run_research.py --wp 5

wp6:
	@echo "=== Launching WP6: Fundable Experiment ==="
	cd $(dir $(MAKEFILE_LIST)) && export $$(cat .env | xargs) && $(PYTHON) run_research.py --wp 6

wp7:
	@echo "=== Launching WP7: Editorial Audit ==="
	cd $(dir $(MAKEFILE_LIST)) && export $$(cat .env | xargs) && $(PYTHON) run_research.py --wp 7

wp8:
	@echo "=== Launching WP8: Active Inference Simulation ==="
	cd $(dir $(MAKEFILE_LIST)) && export $$(cat .env | xargs) && $(PYTHON) run_research.py --wp 8

all: wp5 wp6 wp7

list:
	@$(PYTHON) run_research.py --list
