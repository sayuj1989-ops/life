# Code Ocean Capsule Metadata & Instructions

To complete your submission to *Nature Communications*, use the following metadata and follow these final steps within the Code Ocean interface.

## Capsule Metadata

* **Capsule Title:** An Information-Theoretic Framework for Vertebral Morphogenesis: Countercurvature, Energy Deficits, and the Gravity Paradox
* **Description:** This capsule provides the reproducible analysis pipeline for the biological countercurvature hypothesis. It bridges AlphaFold-derived protein structural metrics to macroscopic spinal mechanics using Cosserat rod simulations (PyElastica). It demonstrates how the "Energy Deficit Window" during adolescent growth drives scoliotic instability.
* **Tags:** Biomechanics, Information Theory, AlphaFold, Scoliosis, Thermodynamics, Cosserat Rods, Mechanobiology.
* **Associated Publication:** Nature Communications (Submitted)
* **License:**
  * **Code:** MIT
  * **Data:** CC0

## Environment Configuration

When setting up your environment in the Code Ocean editor:

1. **Select Base Image:** Python 3.10+ (Ubuntu 22.04 recommended).
2. **Apt Packages:** `g++`, `make`, `texlive-full` (if you wish to re-compile the manuscript PDF in the capsule).
3. **Pip Packages:** Use the included `requirements.txt`. Key dependencies are `pyelastica`, `numpy`, `scipy`, `matplotlib`, `biopython`, and `pandas`.

## Final Submission Steps

1. **Data Consolidation:** Due to local environment restrictions, some data files remain in their original folders. Before pushing to Code Ocean, ensure all simulation data is in the `/data` folder at the root.
2. **Reproducible Run:** Click **"Run"** in Code Ocean. The `run.sh` script will automatically execute `main.py`, saving all results (CSV tables and SVG/PNG figures) to the `/results` folder.
3. **Verification:** Check the generated `results.md` and `phase_diagram_energy_deficit.png` in the results pane.
4. **Submit:** Once the reproducible run is successful, use the "Submit Capsule" button to link it to your *Nature Communications* manuscript.

---
**Contact:** Dr. Sayuj Krishnan S (<dr.sayujkrishnan@gmail.com>)
