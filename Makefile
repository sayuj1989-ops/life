.PHONY: all data figs alphafold alphafold-data alphafold-analyze alphafold-figs alphafold-numbers alphafold-all clean manuscript

PYTHON = .venv/bin/python3

all: data figs manuscript

data: results/sweep_results.csv results/alphafold_summary.csv

results/single_sim.csv: scripts/sim_single.py
	$(PYTHON) scripts/sim_single.py

results/sweep_results.csv: scripts/sweep_params.py scripts/sim_single.py
	$(PYTHON) scripts/sweep_params.py

results/alphafold_summary.csv: scripts/alphafold_reanalysis.py
	$(PYTHON) scripts/alphafold_reanalysis.py

figs: scripts/make_figures.py data
	$(PYTHON) scripts/make_figures.py

manuscript: data
	$(PYTHON) scripts/update_manuscript.py

alphafold: results/alphafold_summary.csv

# AlphaFold analysis pipeline targets
alphafold-data:
	mkdir -p results
	$(PYTHON) -m alphafold_analysis.build_dataset --output results/alphafold_dataset_index.csv

alphafold-analyze:
	mkdir -p results
	$(PYTHON) alphafold_analysis/analyze_bcc_structures.py --index results/alphafold_dataset_index.csv --output-dir results

alphafold-figs:
	mkdir -p figures/main
	$(PYTHON) figures/src/plot_alphafold_main.py --data results/bcc_analysis_data.csv --summary results/bcc_stats_summary.json 2>/dev/null || true
	cp fig_alphafold_*.pdf figures/main/ 2>/dev/null || true
	cp fig_alphafold_*.png figures/main/ 2>/dev/null || true

alphafold-numbers:
	mkdir -p manuscript/numbers
	$(PYTHON) scripts/update_manuscript_numbers.py --stats results/bcc_stats_summary.json --out manuscript/numbers/alphafold_numbers.json 2>/dev/null || true

alphafold-all: alphafold-data alphafold-analyze alphafold-figs alphafold-numbers
	@echo "✅ AlphaFold analysis pipeline complete"

clean:
	rm -rf results/*.csv figures/*.png
	rm -rf results/ .cache/afdb/
