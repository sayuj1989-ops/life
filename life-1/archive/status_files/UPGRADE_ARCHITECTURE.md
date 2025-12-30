# Computational Framework Upgrade Architecture

**Project:** Spinal Modes IEC Model
**Date:** 2025-11-04
**Status:** Design Phase → Implementation Ready
**Target:** Publication-Ready Computational Framework

---

## Executive Summary

This document specifies the upgrade from prototype (simplified beam solver, no validation) to publication-ready computational framework with:
- Rigorous BVP solvers (Cosserat rod, analytical benchmarks)
- Comprehensive validation (convergence, sensitivity, uncertainty)
- Reproducible pipeline (Docker, CI, deterministic outputs)
- Publication-ready manuscript with all figures

**Timeline:** 7-14 days full-time equivalent
**Compute Budget:** 120 CPU-minutes target
**Random Seed:** 1337 (deterministic)

---

## Phase B: Proposed File Structure

```
/Users/dr.sayujkrishnan/LIFE/
├── model/                          # NEW: Core computational model
│   ├── __init__.py
│   ├── core.py                     # State, parameters, units, validation
│   ├── coherence_fields.py         # I(s) generators (refactored from iec.py)
│   ├── couplings.py                # IEC-1/2/3 coupling logic
│   ├── solvers/
│   │   ├── __init__.py
│   │   ├── base.py                 # Abstract solver interface
│   │   ├── bvp_scipy.py            # scipy.integrate.solve_bvp (PRIMARY)
│   │   ├── euler_bernoulli.py      # Analytical benchmark
│   │   ├── timoshenko.py           # Shear-deformable beam (optional)
│   │   ├── cosserat_simple.py      # Lightweight Cosserat (if PyElastica too heavy)
│   │   └── legacy_cantilever.py    # Deprecated: current solve_beam_static
│   └── experiments/
│       ├── __init__.py
│       ├── parameter_sweep.py      # χ sweeps with uncertainty
│       ├── ablation_studies.py     # Single-mechanism tests
│       └── sensitivity.py          # Sobol/Morris global sensitivity
│
├── analysis/                       # NEW: Reproducible analysis scripts
│   ├── 01_data_audit.py            # Inventory → tables/data_catalog.csv
│   ├── 02_solver_benchmarks.py     # Convergence, BVP vs analytical
│   ├── 03_iec_discriminators.py    # Main 3-panel figure (node, amp, helical)
│   ├── 04_sensitivity_analysis.py  # Sobol indices, Morris screening
│   ├── 05_phase_diagrams.py        # (ΔB, ||∇I||) planar-helical boundary
│   ├── 06_uncertainty_bands.py     # Bootstrap or Bayesian error bars
│   └── utils.py                    # Shared plotting, provenance
│
├── tests/                          # UPGRADED: Comprehensive test suite
│   ├── test_iec.py                 # Existing unit tests (keep)
│   ├── test_model_core.py          # NEW: Core model validation
│   ├── test_solvers.py             # NEW: Solver accuracy tests
│   │   ├── test_energy_conservation.py
│   │   ├── test_bc_satisfaction.py
│   │   ├── test_convergence_rate.py
│   └── test_experiments.py         # NEW: Parameter sweep integrity
│
├── manuscript/                     # NEW: Single source of truth
│   ├── main.tex                    # LaTeX source (or main.md if Pandoc)
│   ├── sections/
│   │   ├── 00_abstract.tex
│   │   ├── 01_introduction.tex
│   │   ├── 02_theory.tex
│   │   ├── 03_methods.tex
│   │   ├── 04_results.tex
│   │   ├── 05_discussion.tex
│   │   ├── 06_conclusions.tex
│   │   └── 99_reproducibility.tex  # Reproducibility checklist
│   ├── figures/                    # Symlink → ../outputs/figs/
│   ├── tables/                     # Symlink → ../outputs/tables/
│   ├── references.bib
│   ├── ieee.csl                    # Or journal-specific style
│   └── Makefile                    # make pdf, make arxiv-bundle
│
├── outputs/                        # Regenerated artifacts
│   ├── figs/                       # PNG (300+ DPI) + PDF/SVG + JSON provenance
│   ├── tables/                     # CSV + LaTeX tables
│   ├── aor/                        # Analysis of record (full sweep data)
│   └── reports/                    # Summary HTML/PDF reports
│
├── envs/                           # NEW: Environment specs
│   ├── environment.yml             # Conda (pinned versions)
│   ├── requirements.txt            # Pip (pinned with hashes)
│   ├── Dockerfile                  # CPU deterministic build
│   └── docker-compose.yml          # Optional: multi-service
│
├── .github/
│   └── workflows/
│       ├── ci.yml                  # Lint, test, smoke plot
│       ├── pages.yml               # Rebuild docs on push
│       └── docker-publish.yml      # Optional: publish image
│
├── Makefile                        # EXTENDED targets
├── CITATION.cff                    # NEW: Machine-readable citation
├── CHANGELOG.md                    # NEW: Track refactors
└── README.md                       # Updated with one-command reproduce

DEPRECATED (but preserved):
├── src/spinalmodes/                # Keep for backward compat, mark deprecated
│   ├── iec.py                      # → model/core.py + model/couplings.py
│   ├── iec_cli.py                  # → Keep CLI, update to use model/
│   └── fig_iec_discriminators.py   # → analysis/03_iec_discriminators.py
```

---

## Detailed Design Specifications

### 1. Model Framework (`model/`)

#### `model/core.py`
```python
"""Core model state, parameters, units, and validation."""

from dataclasses import dataclass, field
from typing import Literal, Optional
import numpy as np
from numpy.typing import NDArray

@dataclass(frozen=True)  # Immutable for reproducibility
class PhysicalUnits:
    """SI unit definitions for dimensional consistency checks."""
    length: str = "m"
    force: str = "N"
    pressure: str = "Pa"
    moment: str = "N·m"
    curvature: str = "1/m"

@dataclass
class IECParameters:
    """
    Immutable parameter set for IEC model.

    All parameters have units, ranges, and biological justification.
    """
    # Coupling strengths
    chi_kappa: float = field(default=0.0, metadata={"unit": "m", "range": (0.0, 0.1)})
    chi_E: float = field(default=0.0, metadata={"unit": "dimensionless", "range": (-0.5, 0.5)})
    chi_C: float = field(default=0.0, metadata={"unit": "dimensionless", "range": (-0.5, 1.0)})
    chi_f: float = field(default=0.0, metadata={"unit": "N·m", "range": (0.0, 0.2)})

    # Material properties (with units!)
    E0: float = field(default=1e9, metadata={"unit": "Pa"})
    C0: float = field(default=1e6, metadata={"unit": "N·s/m"})
    I_moment: float = field(default=1e-8, metadata={"unit": "m^4"})
    rho: float = field(default=1000.0, metadata={"unit": "kg/m^3"})
    A_cross: float = field(default=1e-4, metadata={"unit": "m^2"})

    # Geometry
    length: float = field(default=0.4, metadata={"unit": "m"})
    n_nodes: int = 100

    # Coherence field
    I_mode: Literal["constant", "linear", "gaussian", "step"] = "constant"
    I_amplitude: float = 1.0
    I_gradient: float = 0.0
    I_center: float = 0.5
    I_width: float = 0.1

    # Loading
    P_load: float = field(default=100.0, metadata={"unit": "N"})
    distributed_load: float = field(default=0.0, metadata={"unit": "N/m"})

    # Numerical
    random_seed: int = 1337

    def __post_init__(self):
        """Validate parameter ranges."""
        self._validate_ranges()
        self._check_dimensional_consistency()

    def _validate_ranges(self):
        """Check parameters within physical bounds."""
        # Implementation validates all metadata["range"] fields
        pass

    def _check_dimensional_consistency(self):
        """Verify dimensional correctness (e.g., EI has units Pa·m^4)."""
        # Implementation checks unit algebra
        pass

    def get_s_array(self) -> NDArray[np.float64]:
        """Generate spatial coordinate array."""
        return np.linspace(0, self.length, self.n_nodes)


@dataclass(frozen=True)
class ModelState:
    """
    Immutable state vector for IEC model at one spatial configuration.
    """
    s: NDArray[np.float64]              # Spatial coordinates (m)
    theta: NDArray[np.float64]          # Deflection angle (rad)
    kappa: NDArray[np.float64]          # Realized curvature (1/m)
    kappa_target: NDArray[np.float64]   # Target curvature from IEC-1 (1/m)
    E_field: NDArray[np.float64]        # Effective modulus from IEC-2 (Pa)
    C_field: NDArray[np.float64]        # Damping from IEC-2 (N·s/m)
    M_active: NDArray[np.float64]       # Active moment from IEC-3 (N·m)
    I_field: NDArray[np.float64]        # Coherence field (dimensionless)

    # Metadata
    solver: str = "unknown"
    timestamp: str = field(default_factory=lambda: np.datetime64('now').isostring())
    git_sha: Optional[str] = None

    def compute_metrics(self) -> dict:
        """Compute derived quantities (wavelength, amplitude, nodes)."""
        # Calls utility functions
        pass

    def to_csv(self, path: str):
        """Export state to CSV with metadata."""
        pass

    def to_json(self, path: str):
        """Export metadata and summary statistics."""
        pass
```

#### `model/solvers/base.py`
```python
"""Abstract base class for all solvers."""

from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np
from numpy.typing import NDArray

from ..core import IECParameters, ModelState


class BaseSolver(ABC):
    """
    Abstract solver interface ensuring all implementations have:
    - Deterministic execution (fixed seed)
    - Convergence monitoring
    - Energy conservation checks
    - Boundary condition satisfaction
    """

    def __init__(self, params: IECParameters):
        self.params = params
        np.random.seed(params.random_seed)

    @abstractmethod
    def solve(self) -> ModelState:
        """
        Solve for equilibrium state.

        Returns:
            ModelState with complete spatial fields
        """
        pass

    @abstractmethod
    def validate_solution(self, state: ModelState) -> dict:
        """
        Validate solution quality.

        Returns:
            Dictionary with:
            - "bc_error": Boundary condition residual
            - "energy_error": Energy conservation error
            - "convergence": True if converged
        """
        pass

    def benchmark_against_analytical(self, analytical_solution: callable) -> float:
        """
        Compare against known analytical solution.

        Returns:
            L2 relative error
        """
        pass
```

#### `model/solvers/bvp_scipy.py` (PRIMARY UPGRADE)
```python
"""
Rigorous boundary value problem solver using scipy.integrate.solve_bvp.

This replaces the simplified forward-integration cantilever model.
Handles general boundary conditions and ensures global equilibrium.
"""

import numpy as np
from scipy.integrate import solve_bvp
from .base import BaseSolver
from ..core import IECParameters, ModelState
from ..couplings import apply_iec_coupling


class BVPSolver(BaseSolver):
    """
    Boundary value problem solver for Cosserat rod equilibrium.

    Governing equations:
        dθ/ds = κ(s)
        dκ/ds = M_ext(s) / (EI(s)) - dκ_target/ds

    Boundary conditions:
        θ(0) = 0, θ(L) = free  (cantilever)
        OR θ(0) = 0, θ(L) = 0  (pinned-pinned)
    """

    def __init__(self, params: IECParameters, bc_type: str = "cantilever"):
        super().__init__(params)
        self.bc_type = bc_type

    def solve(self) -> ModelState:
        """Solve BVP using scipy.integrate.solve_bvp."""
        s = self.params.get_s_array()

        # Get IEC couplings
        kappa_target, E_field, C_field, M_active = apply_iec_coupling(s, self.params)

        # Define ODE system
        def ode_system(s, y):
            """y = [theta, kappa]"""
            theta, kappa = y
            EI = E_field * self.params.I_moment

            # External moment (cantilever with tip load)
            M_ext = self.params.P_load * (self.params.length - s)

            # dy/ds
            dtheta_ds = kappa
            dkappa_ds = (M_ext - M_active) / EI - np.gradient(kappa_target, s)

            return np.vstack((dtheta_ds, dkappa_ds))

        # Boundary conditions
        def bc(ya, yb):
            """ya = state at s=0, yb = state at s=L"""
            if self.bc_type == "cantilever":
                return np.array([ya[0], ya[1]])  # θ(0)=0, κ(0)=0
            elif self.bc_type == "pinned_pinned":
                return np.array([ya[0], yb[0]])  # θ(0)=0, θ(L)=0
            else:
                raise ValueError(f"Unknown BC type: {self.bc_type}")

        # Initial guess (linear interpolation)
        y_init = np.zeros((2, len(s)))

        # Solve BVP
        sol = solve_bvp(ode_system, bc, s, y_init, tol=1e-6, max_nodes=1000)

        if not sol.success:
            raise RuntimeError(f"BVP solver failed: {sol.message}")

        theta = sol.y[0]
        kappa = sol.y[1]

        # Package into ModelState
        state = ModelState(
            s=s,
            theta=theta,
            kappa=kappa,
            kappa_target=kappa_target,
            E_field=E_field,
            C_field=C_field,
            M_active=M_active,
            I_field=generate_coherence_field(s, self.params),
            solver="BVPSolver_scipy",
            git_sha=get_git_sha()
        )

        # Validate
        validation = self.validate_solution(state)
        if not validation["convergence"]:
            raise RuntimeError(f"Solution failed validation: {validation}")

        return state

    def validate_solution(self, state: ModelState) -> dict:
        """Check BC satisfaction and energy balance."""
        # Implementation checks:
        # - |θ(0)| < tol
        # - Energy: ∫ (EI κ^2 / 2) ds ≈ Work by external loads
        # - Residual: max |dθ/ds - κ| < tol
        pass
```

#### `model/solvers/euler_bernoulli.py` (ANALYTICAL BENCHMARK)
```python
"""
Analytical Euler-Bernoulli beam solutions for validation.

Provides exact solutions for:
- Cantilever with tip load
- Simply supported beam with uniform load
- Pinned-pinned with point load

Used to verify BVP solver accuracy.
"""

import numpy as np
from .base import BaseSolver


class EulerBernoulliAnalytical(BaseSolver):
    """
    Analytical solutions for linear Euler-Bernoulli beams.

    Assumptions:
    - Small deflections (linearized kinematics)
    - Uniform EI (no IEC-2)
    - No active moments (no IEC-3)
    - No target curvature bias (no IEC-1)

    Use for solver validation, not IEC studies.
    """

    def solve_cantilever_tip_load(self, P: float, L: float, EI: float) -> dict:
        """
        Exact solution: w(x) = P/(6EI) * (3Lx^2 - x^3)
        """
        s = self.params.get_s_array()

        # Deflection
        w = (P / (6 * EI)) * (3 * L * s**2 - s**3)

        # Slope (dw/dx)
        theta = (P / (2 * EI)) * (2 * L * s - s**2)

        # Curvature (d²w/dx²)
        kappa = (P / EI) * (L - s)

        return {"s": s, "w": w, "theta": theta, "kappa": kappa}

    # Additional methods for other load cases...
```

---

### 2. Analysis Pipeline (`analysis/`)

All scripts follow this template:

```python
"""
analysis/03_iec_discriminators.py

Generate 3-panel discriminator figure showing IEC-1/2/3 signatures.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
from datetime import datetime

from model.core import IECParameters
from model.solvers.bvp_scipy import BVPSolver
from model.couplings import apply_iec_coupling
from analysis.utils import setup_plot_style, save_figure_with_provenance


def main(output_dir: Path = Path("outputs/figs"), seed: int = 1337):
    """
    Generate discriminator figure.

    Panel A: IEC-1 node drift vs chi_kappa
    Panel B: IEC-2 amplitude vs chi_E
    Panel C: IEC-3 helical threshold vs ||gradI||
    """
    np.random.seed(seed)
    setup_plot_style()  # Publication-quality defaults

    fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=300)

    # Panel A: IEC-1
    chi_kappa_range = np.linspace(0, 0.06, 13)
    node_drifts = []
    wavelengths = []

    for chi_k in chi_kappa_range:
        params = IECParameters(
            chi_kappa=chi_k,
            I_mode="step",
            I_center=0.5,
            random_seed=seed
        )
        solver = BVPSolver(params)
        state = solver.solve()

        metrics = state.compute_metrics()
        node_drifts.append(metrics["node_drift_mm"])
        wavelengths.append(metrics["wavelength_mm"])

    axes[0].plot(chi_kappa_range * 1000, node_drifts, 'o-', label="Node drift")
    axes[0].axhline(np.mean(wavelengths), ls='--', color='gray', label=f"Wavelength: {np.mean(wavelengths):.1f} mm")
    axes[0].set_xlabel("$\\chi_\\kappa$ (mm)")
    axes[0].set_ylabel("Node drift (mm)")
    axes[0].legend()
    axes[0].set_title("IEC-1: Target Curvature Bias")

    # Panel B: IEC-2
    chi_E_range = np.linspace(-0.3, 0.3, 13)
    amplitudes = []

    for chi_E in chi_E_range:
        params = IECParameters(chi_E=chi_E, I_mode="constant", random_seed=seed)
        solver = BVPSolver(params)
        state = solver.solve()
        amplitudes.append(state.compute_metrics()["amplitude_deg"])

    axes[1].plot(chi_E_range, amplitudes, 's-', color='C1')
    axes[1].set_xlabel("$\\chi_E$ (dimensionless)")
    axes[1].set_ylabel("Amplitude (degrees)")
    axes[1].set_title("IEC-2: Constitutive Bias")

    # Panel C: IEC-3
    gradI_range = np.linspace(0, 0.1, 21)
    thresholds = []

    for gradI in gradI_range:
        # Compute helical threshold (simplified)
        threshold = compute_helical_threshold(delta_b=0.1, grad_I_norm=gradI, chi_f=0.05)
        thresholds.append(threshold)

    axes[2].plot(gradI_range, thresholds, '^-', color='C2')
    axes[2].set_xlabel("$||\\nabla I||$ (dimensionless)")
    axes[2].set_ylabel("Helical threshold")
    axes[2].set_title("IEC-3: Active Moment")

    plt.tight_layout()

    # Save with provenance
    output_path = output_dir / "fig_iec_discriminators.png"
    provenance = {
        "script": "analysis/03_iec_discriminators.py",
        "timestamp": datetime.now().isoformat(),
        "git_sha": get_git_sha(),
        "random_seed": seed,
        "parameters": {
            "chi_kappa_range": chi_kappa_range.tolist(),
            "chi_E_range": chi_E_range.tolist(),
            "gradI_range": gradI_range.tolist()
        },
        "figure_spec": {
            "dpi": 300,
            "width_px": 1800 * 3,
            "height_px": 1500,
            "format": "PNG"
        }
    }

    save_figure_with_provenance(fig, output_path, provenance)
    print(f"✓ Saved: {output_path}")
    print(f"✓ Provenance: {output_path.with_suffix('.json')}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/figs"))
    parser.add_argument("--seed", type=int, default=1337)
    args = parser.parse_args()
    main(args.output_dir, args.seed)
```

---

### 3. Test Suite Upgrades (`tests/`)

#### `tests/test_solvers.py`
```python
"""Rigorous solver validation tests."""

import pytest
import numpy as np
from model.core import IECParameters
from model.solvers.bvp_scipy import BVPSolver
from model.solvers.euler_bernoulli import EulerBernoulliAnalytical


class TestSolverAccuracy:
    """Validate BVP solver against analytical solutions."""

    def test_cantilever_matches_analytical(self):
        """BVP solver should match Euler-Bernoulli for linear case."""
        # No IEC couplings → linear problem
        params = IECParameters(
            chi_kappa=0.0, chi_E=0.0, chi_C=0.0, chi_f=0.0,
            P_load=100.0, n_nodes=200
        )

        # BVP solver
        bvp_solver = BVPSolver(params)
        state_bvp = bvp_solver.solve()

        # Analytical
        analytical = EulerBernoulliAnalytical(params)
        state_analytical = analytical.solve_cantilever_tip_load(
            P=params.P_load,
            L=params.length,
            EI=params.E0 * params.I_moment
        )

        # Compare
        L2_error = np.linalg.norm(state_bvp.theta - state_analytical["theta"]) / np.linalg.norm(state_analytical["theta"])

        assert L2_error < 0.01, f"L2 error too large: {L2_error:.2%}"

    def test_energy_conservation(self):
        """Total energy should match work by external loads."""
        params = IECParameters(chi_kappa=0.02, P_load=100.0)
        solver = BVPSolver(params)
        state = solver.solve()

        # Elastic energy
        EI = state.E_field * params.I_moment
        elastic_energy = np.trapz(0.5 * EI * (state.kappa - state.kappa_target)**2, state.s)

        # External work
        external_work = params.P_load * state.theta[-1] * params.length  # Simplified

        energy_error = abs(elastic_energy - external_work) / external_work
        assert energy_error < 0.05, f"Energy error: {energy_error:.2%}"

    def test_boundary_condition_satisfaction(self):
        """Boundary conditions should be satisfied to tolerance."""
        params = IECParameters()
        solver = BVPSolver(params, bc_type="cantilever")
        state = solver.solve()

        # Cantilever: θ(0) = 0, κ(0) = 0
        assert abs(state.theta[0]) < 1e-6, f"θ(0) = {state.theta[0]}, expected ~0"
        assert abs(state.kappa[0]) < 1e-4, f"κ(0) = {state.kappa[0]}, expected ~0"


class TestConvergence:
    """Convergence studies (spatial discretization)."""

    @pytest.mark.parametrize("n_nodes", [50, 100, 200, 400])
    def test_spatial_convergence(self, n_nodes):
        """Solution should converge as n_nodes → ∞."""
        params = IECParameters(n_nodes=n_nodes, chi_kappa=0.03)
        solver = BVPSolver(params)
        state = solver.solve()

        # Store result for comparison
        # (Full test would compare against n=800 reference)
        assert state.theta is not None
```

---

### 4. Reproducibility Infrastructure

#### `envs/environment.yml`
```yaml
name: spinalmodes
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10.12   # Pinned patch version
  - numpy=1.24.3
  - scipy=1.11.2
  - matplotlib=3.7.2
  - pandas=2.0.3
  - pytest=7.4.0
  - pytest-cov=4.1.0
  - black=23.7.0
  - ruff=0.0.285
  - mypy=1.5.1
  - typer=0.9.0
  - pydantic=2.3.0
  - pip=23.2.1
  - pip:
      - SALib==1.4.7      # Sensitivity analysis
      - seaborn==0.12.2   # Enhanced plots
```

#### `envs/Dockerfile`
```dockerfile
FROM python:3.10.12-slim

# Deterministic build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY envs/requirements.txt /app/requirements.txt

# Install Python dependencies (pinned with hashes)
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . /app

# Install package
RUN pip install -e .

# Default command
CMD ["make", "all"]
```

#### `Makefile` (Extended)
```makefile
.PHONY: help env test figures paper all clean

help:
	@echo "Spinal Modes IEC Model - Reproducibility Targets"
	@echo ""
	@echo "  make env      - Set up environment (conda or docker)"
	@echo "  make test     - Run full test suite with coverage"
	@echo "  make figures  - Generate all publication figures"
	@echo "  make paper    - Compile manuscript PDF"
	@echo "  make all      - Run complete pipeline (test + figures + paper)"
	@echo "  make clean    - Remove generated files"

env:
	@echo "Setting up environment..."
	conda env create -f envs/environment.yml || pip install -r envs/requirements.txt
	@echo "✓ Environment ready"

test:
	pytest tests/ -v --cov=model --cov=analysis --cov-report=term-missing --cov-report=html
	@echo "✓ All tests passed"

figures:
	@echo "Generating figures..."
	python analysis/01_data_audit.py
	python analysis/02_solver_benchmarks.py
	python analysis/03_iec_discriminators.py
	python analysis/04_sensitivity_analysis.py
	python analysis/05_phase_diagrams.py
	python analysis/06_uncertainty_bands.py
	python tools/validate_figures.py
	@echo "✓ Figures generated and validated"

paper:
	@echo "Compiling manuscript..."
	cd manuscript && make pdf
	@echo "✓ Manuscript PDF: manuscript/main.pdf"

all: test figures paper
	@echo "✓ Complete pipeline executed successfully"
	@echo "  - Tests: htmlcov/index.html"
	@echo "  - Figures: outputs/figs/"
	@echo "  - Manuscript: manuscript/main.pdf"

clean:
	rm -rf outputs/figs/* outputs/tables/* manuscript/main.pdf
	rm -rf .pytest_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
```

---

## Migration Strategy

### Phase 1: Parallel Implementation (1-2 days)
- Create `model/` directory alongside `src/spinalmodes/`
- Implement new solvers, mark `src/spinalmodes/iec.py` as deprecated
- Update imports gradually

### Phase 2: Test Migration (1 day)
- Copy existing tests → `tests/test_iec_legacy.py`
- Add new solver tests
- Ensure 100% backward compat

### Phase 3: Analysis Scripts (1-2 days)
- Create `analysis/` scripts
- Generate first outputs
- Validate against acceptance criteria

### Phase 4: Documentation (1 day)
- Update README with new structure
- Create CHANGELOG.md documenting migration
- Add migration guide for users

### Phase 5: Manuscript Assembly (2-3 days)
- Set up LaTeX pipeline
- Integrate figures
- Compile full PDF

---

## Success Criteria

✅ **Solver Accuracy:**
- L2 error < 1% vs analytical (linear case)
- Energy conservation < 5% error
- BC residual < 10^-6

✅ **Convergence:**
- Second-order spatial convergence (O(Δx²))
- Error vs. cost plots show expected scaling

✅ **Validation:**
- All 15+ existing tests pass
- 20+ new tests (solver, convergence, benchmark)
- Coverage > 80%

✅ **Reproducibility:**
- `make all` runs deterministically
- Docker build succeeds
- CI passes on GitHub

✅ **Manuscript:**
- All figures generated from scripts
- References complete
- Reproducibility checklist included

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| BVP solver unstable | Fall back to shooting method, add relaxation |
| Heavy dependencies (PyElastica) | Implement lightweight Cosserat surrogate |
| Compute budget exceeded | Reduce n_nodes for CI, add `--full` flag |
| Figures don't match acceptance | Adjust parameters with biological justification |

---

## Next Actions (Priority Order)

1. **Create `model/` structure** (30 min)
2. **Implement `model/solvers/bvp_scipy.py`** (3-4 hours)
3. **Add analytical benchmarks** (2 hours)
4. **Run first convergence study** (1 hour)
5. **Generate discriminator figure** (1 hour)
6. **Review and iterate** (2 hours)

**Total Estimated Effort:** 7-14 days FTE
**Critical Path:** BVP solver → validation → figures → manuscript

---

*End of Upgrade Architecture Document*
