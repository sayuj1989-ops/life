# PRX Life Data & Code Availability Statement

**For use in the PRX Life submission form "Data Availability" field**

---

## Version 1: Full Statement (Recommended)

All code, data, and analysis scripts required to reproduce the results in this manuscript are openly available:

**Code Repository:**
https://github.com/sayujks0071/life (archived at Zenodo: 10.5281/zenodo.17634760)

**Version:** v0.1.0

**Software:** The `spinalmodes` Python package (MIT License) implements:
- Information-Elasticity Coupling (IEC) beam and Cosserat rod solvers
- Biological countercurvature metric and geodesic curvature deviation ($\widehat{D}_{\mathrm{geo}}$)
- Scoliosis metrics ($S_{\mathrm{lat}}$, Cobb-like angles)
- Full integration with PyElastica for 3D Cosserat rod dynamics

**Data:** All numerical results are regenerable by running experiment scripts in `src/spinalmodes/experiments/countercurvature/` with default parameters. Pre-computed experiment outputs (curvature profiles, metrics, phase diagram data) are included in `outputs/` and documented in `docs/manuscript_code_data_availability.md`.

**Reproducibility:** Minimal working examples are provided in `examples/quickstart.py` and `examples/quickstart.ipynb`. Full reproduction requires Python 3.10+, NumPy, SciPy, Matplotlib, and PyElastica (all listed in `pyproject.toml`). Typical runtime: 5-30 minutes per experiment on a standard workstation.

**Contact:** For questions about code or data, contact Dr. Sayuj Krishnan (dr.sayujkrishnan@gmail.com) or open an issue on the GitHub repository.

---

## Version 2: Concise Statement (If Word Limit Applies)

All code and data are openly available at https://github.com/sayujks0071/life (Zenodo: 10.5281/zenodo.17634760). The `spinalmodes` Python package (v0.1.0, MIT License) implements the IEC-Cosserat framework and reproduces all figures. Experiment scripts are in `src/spinalmodes/experiments/countercurvature/` with full documentation. Typical runtime: 5-30 minutes per experiment. Contact: dr.sayujkrishnan@gmail.com

---

## Version 3: Minimal Statement (If Severe Character Limit)

Code and data: https://github.com/sayujks0071/life (Zenodo: 10.5281/zenodo.17634760). Python package `spinalmodes` v0.1.0 reproduces all results. See repository README for instructions. Contact: dr.sayujkrishnan@gmail.com

---

## Instructions

1. ✅ **Zenodo DOI updated:** 10.5281/zenodo.17634760

2. **Choose version based on submission form character limits:**
   - Version 1: Use if >500 characters allowed (recommended for full transparency)
   - Version 2: Use if 200-500 characters allowed
   - Version 3: Use if <200 characters allowed

3. **Copy-paste directly into PRX Life submission portal** Data Availability field

4. **Note:** The full statement is already included in the manuscript (Code and Data Availability section), so this is just for the submission form metadata

---

## Additional Information (For Your Reference)

### What PRX Life Looks For in Data Availability:

✅ **Public repository with permanent identifier** (GitHub + Zenodo DOI)
✅ **Clear instructions for reproduction** (examples, documentation)
✅ **License information** (MIT License)
✅ **Software dependencies clearly listed** (pyproject.toml)
✅ **Contact information** (email)
✅ **Reasonable computational requirements** (standard workstation, <1 hour runtime)

### What You've Provided:

✅ GitHub repository (will be public)
✅ Zenodo archival (will be created)
✅ MIT License (open source)
✅ Comprehensive README with quickstart
✅ Full environment specification (pyproject.toml, requirements.txt, environment.yml)
✅ Example scripts (quickstart.py, quickstart.ipynb)
✅ Experiment scripts with CLI
✅ Unit tests for verification
✅ Documentation in docs/

**Your data/code availability is EXEMPLARY.** Reviewers will appreciate this level of transparency.

---

## Common Reviewer Questions & Your Prepared Answers

**Q1: "Can the results be reproduced without specialized hardware?"**
**A:** Yes. All experiments run on a standard workstation with Python 3.10+. No GPU required. Typical runtime: 5-30 minutes per experiment.

**Q2: "Are the dependencies publicly available?"**
**A:** Yes. All dependencies (NumPy, SciPy, Matplotlib, PyElastica) are available via `pip install` from PyPI. Full environment specifications are provided in `pyproject.toml` and `requirements.txt`.

**Q3: "Can I run just one figure to verify?"**
**A:** Yes. Run `python examples/quickstart.py` for a minimal demonstration, or see `docs/manuscript_code_data_availability.md` for per-figure instructions.

**Q4: "What if a dependency version changes in the future?"**
**A:** The Zenodo archive captures the exact code version and full environment specifications. The repository also includes Docker and conda environment files for long-term reproducibility.

**Q5: "Is the data FAIR-compliant?"**
**A:** Yes. The data is:
- **Findable:** GitHub + Zenodo with DOI
- **Accessible:** Public repository, MIT License
- **Interoperable:** Standard formats (CSV, PDF, Python)
- **Reusable:** Clear documentation, examples, open license

---

**Created:** 2025-11-18
**For:** PRX Life submission
**Status:** ✅ Ready to use (Zenodo DOI: 10.5281/zenodo.17634760)
