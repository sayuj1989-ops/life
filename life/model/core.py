"""
Core model state, parameters, units, and validation.

This module provides immutable parameter sets and state vectors with:
- Dimensional consistency checking
- Parameter range validation
- Provenance tracking (git SHA, timestamps)
- Serialization to CSV/JSON
"""

from dataclasses import dataclass, field
from typing import Literal, Optional, Dict, Any
import numpy as np
from numpy.typing import NDArray
import subprocess
from datetime import datetime
import json


def get_git_sha() -> Optional[str]:
    """Get current git commit SHA."""
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        return sha
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


@dataclass(frozen=True)
class PhysicalUnits:
    """
    SI unit definitions for dimensional consistency checks.

    All model quantities must have explicit units to prevent
    dimensional errors in coupling terms.
    """
    length: str = "m"
    force: str = "N"
    pressure: str = "Pa"
    moment: str = "N·m"
    curvature: str = "1/m"
    angular_frequency: str = "rad/s"
    damping: str = "N·s/m"


@dataclass
class IECParameters:
    """
    Immutable parameter set for IEC model.

    All parameters include:
    - Physical units (metadata)
    - Biologically plausible ranges
    - Literature-based defaults

    Attributes:
        # IEC Coupling Strengths
        chi_kappa: Target curvature coupling (m), range [0, 0.1]
        chi_E: Young's modulus coupling (dimensionless), range [-0.5, 0.5]
        chi_C: Damping coupling (dimensionless), range [-0.5, 1.0]
        chi_f: Active moment coupling (N·m), range [0, 0.2]

        # Material Properties
        E0: Baseline Young's modulus (Pa), default 1e9
        C0: Baseline damping coefficient (N·s/m), default 1e6
        I_moment: Second moment of area (m^4), default 1e-8
        rho: Density (kg/m^3), default 1000
        A_cross: Cross-sectional area (m^2), default 1e-4

        # Geometry
        length: Spine segment length (m), default 0.4
        n_nodes: Spatial discretization nodes, default 100

        # Coherence Field I(s)
        I_mode: Field type (constant/linear/gaussian/step)
        I_amplitude: Field amplitude (dimensionless), default 1.0
        I_gradient: Linear gradient strength, default 0.0
        I_center: Center for gaussian/step (normalized), default 0.5
        I_width: Width for gaussian (normalized), default 0.1

        # Loading
        P_load: Applied tip/end load (N), default 100.0
        distributed_load: Uniform distributed load (N/m), default 0.0

        # Gravitation / countercurvature
        g_magnitude: Gravitational field strength (m/s^2), default 9.81
        countercurvature_gain: Dimensionless gain opposing gravity, range [0, 5]
        countercurvature_orientation: Direction of growth relative to gravity

        # Numerical
        random_seed: For reproducibility, default 1337
    """

    # Coupling strengths
    chi_kappa: float = field(default=0.0, metadata={"unit": "m", "range": (0.0, 0.1)})
    chi_E: float = field(default=0.0, metadata={"unit": "dimensionless", "range": (-0.5, 0.5)})
    chi_C: float = field(default=0.0, metadata={"unit": "dimensionless", "range": (-0.5, 1.0)})
    chi_f: float = field(default=0.0, metadata={"unit": "N·m", "range": (0.0, 0.2)})

    # Material properties
    E0: float = field(default=1e9, metadata={"unit": "Pa"})
    C0: float = field(default=1e6, metadata={"unit": "N·s/m"})
    kappa_gen_baseline: float = field(default=0.0, metadata={"unit": "1/m"})
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

    # Gravitation / countercurvature
    g_magnitude: float = field(default=9.81, metadata={"unit": "m/s^2", "range": (0.0, 50.0)})
    countercurvature_gain: float = field(
        default=0.0, metadata={"unit": "dimensionless", "range": (0.0, 5.0)}
    )
    countercurvature_orientation: Literal["against_gravity", "with_gravity"] = (
        "against_gravity"
    )

    # Numerical
    random_seed: int = 1337

    def __post_init__(self):
        """Validate parameter ranges after initialization."""
        self._validate_ranges()

    def _validate_ranges(self):
        """Check parameters are within physical bounds."""
        for field_name, field_obj in self.__dataclass_fields__.items():
            if "range" in field_obj.metadata:
                value = getattr(self, field_name)
                min_val, max_val = field_obj.metadata["range"]
                if not (min_val <= value <= max_val):
                    raise ValueError(
                        f"{field_name} = {value} out of range [{min_val}, {max_val}]"
                    )

        # Additional physical constraints
        if self.E0 <= 0:
            raise ValueError(f"E0 must be positive, got {self.E0}")
        if self.length <= 0:
            raise ValueError(f"length must be positive, got {self.length}")
        if self.n_nodes < 2:
            raise ValueError(f"n_nodes must be >= 2, got {self.n_nodes}")
        if self.countercurvature_orientation not in {"against_gravity", "with_gravity"}:
            raise ValueError(
                "countercurvature_orientation must be 'against_gravity' or 'with_gravity'"
            )

    def get_s_array(self) -> NDArray[np.float64]:
        """
        Generate spatial coordinate array.

        Returns:
            1D array of length n_nodes spanning [0, length]
        """
        return np.linspace(0, self.length, self.n_nodes)

    def to_dict(self) -> Dict[str, Any]:
        """Export parameters as dictionary."""
        return {
            field_name: getattr(self, field_name)
            for field_name in self.__dataclass_fields__.keys()
        }

    def to_json(self, filepath: str):
        """
        Export parameters to JSON file.

        Args:
            filepath: Output JSON path
        """
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


@dataclass
class ModelState:
    """
    Immutable state vector for IEC model at one spatial configuration.

    Contains all spatial fields and metadata for complete provenance tracking.

    Attributes:
        s: Spatial coordinates (m), shape (n_nodes,)
        theta: Deflection angle (rad), shape (n_nodes,)
        kappa: Realized curvature (1/m), shape (n_nodes,)
        kappa_target: Target curvature from IEC-1 (1/m), shape (n_nodes,)
        E_field: Effective Young's modulus from IEC-2 (Pa), shape (n_nodes,)
        C_field: Damping coefficient from IEC-2 (N·s/m), shape (n_nodes,)
        M_active: Active moment from IEC-3 (N·m), shape (n_nodes,)
        I_field: Coherence field (dimensionless), shape (n_nodes,)

        solver: Solver name used to generate this state
        timestamp: ISO format timestamp of computation
        git_sha: Git commit SHA (if available)
        params: Original IECParameters used
    """

    s: NDArray[np.float64]
    theta: NDArray[np.float64]
    kappa: NDArray[np.float64]
    kappa_target: NDArray[np.float64]
    E_field: NDArray[np.float64]
    C_field: NDArray[np.float64]
    M_active: NDArray[np.float64]
    I_field: NDArray[np.float64]

    solver: str = "unknown"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    git_sha: Optional[str] = field(default_factory=get_git_sha)
    params: Optional[IECParameters] = None

    def __post_init__(self):
        """Validate state consistency."""
        arrays = [self.s, self.theta, self.kappa, self.kappa_target,
                  self.E_field, self.C_field, self.M_active, self.I_field]

        # Check all arrays have same length
        lengths = [len(arr) for arr in arrays]
        if len(set(lengths)) != 1:
            raise ValueError(f"Inconsistent array lengths: {lengths}")

        # Check for NaN/Inf
        for name, arr in zip(
            ["s", "theta", "kappa", "kappa_target", "E_field", "C_field", "M_active", "I_field"],
            arrays
        ):
            if not np.all(np.isfinite(arr)):
                raise ValueError(f"{name} contains NaN or Inf values")

    def compute_metrics(self) -> Dict[str, float]:
        """
        Compute derived quantities from state.

        Returns:
            Dictionary with:
            - wavelength_mm: Dominant wavelength (mm)
            - amplitude_deg: Peak-to-peak amplitude (degrees)
            - node_drift_mm: Mean node drift from baseline (mm)
            - max_curvature: Maximum curvature magnitude (1/m)
            - rms_curvature: RMS curvature (1/m)
        """
        # Use module-level functions defined below
        wavelength_mm = compute_wavelength(self.s, self.theta)
        amplitude_deg = compute_amplitude(self.theta)

        # Node positions (simplified - compare to zero-coupling baseline)
        nodes = compute_node_positions(self.s, self.theta)
        if len(nodes) > 0:
            # Drift relative to uniform spacing
            expected_spacing = self.s[-1] / (len(nodes) + 1) if len(nodes) > 0 else 0
            node_drift_mm = np.std(np.diff(nodes) - expected_spacing) * 1000 if len(nodes) > 1 else 0
        else:
            node_drift_mm = 0.0

        return {
            "wavelength_mm": wavelength_mm if wavelength_mm else 0.0,
            "amplitude_deg": amplitude_deg,
            "node_drift_mm": node_drift_mm,
            "max_curvature": float(np.max(np.abs(self.kappa))),
            "rms_curvature": float(np.sqrt(np.mean(self.kappa**2))),
        }

    def to_csv(self, filepath: str):
        """
        Export spatial fields to CSV.

        Args:
            filepath: Output CSV path
        """
        import pandas as pd

        df = pd.DataFrame({
            "s_m": self.s,
            "theta_rad": self.theta,
            "kappa_per_m": self.kappa,
            "kappa_target_per_m": self.kappa_target,
            "E_Pa": self.E_field,
            "C_Ns_per_m": self.C_field,
            "M_active_Nm": self.M_active,
            "I_dimensionless": self.I_field,
        })

        df.to_csv(filepath, index=False, float_format="%.6e")

    def to_json(self, filepath: str):
        """
        Export metadata and summary statistics to JSON.

        Args:
            filepath: Output JSON path
        """
        metrics = self.compute_metrics()

        metadata = {
            "solver": self.solver,
            "timestamp": self.timestamp,
            "git_sha": self.git_sha,
            "n_nodes": len(self.s),
            "length_m": float(self.s[-1]),
            "metrics": metrics,
        }

        if self.params is not None:
            metadata["parameters"] = self.params.to_dict()

        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2)


# Utility functions for backward compatibility
def compute_wavelength(s: NDArray[np.float64], theta: NDArray[np.float64]) -> Optional[float]:
    """
    Compute dominant wavelength from angle profile using zero-crossings.

    Args:
        s: Spatial coordinates (m)
        theta: Angle profile (rad)

    Returns:
        Wavelength in mm, or None if cannot determine
    """
    theta_centered = theta - np.mean(theta)
    sign_changes = np.diff(np.sign(theta_centered))
    zero_crossings = np.where(sign_changes != 0)[0]

    if len(zero_crossings) < 2:
        return None

    distances = np.diff(s[zero_crossings])
    wavelength_m = 2.0 * np.mean(distances)
    return wavelength_m * 1000.0  # Convert to mm


def compute_amplitude(theta: NDArray[np.float64]) -> float:
    """
    Compute peak-to-peak amplitude.

    Args:
        theta: Angle profile (rad)

    Returns:
        Amplitude in degrees
    """
    amplitude_rad = np.max(theta) - np.min(theta)
    return np.rad2deg(amplitude_rad)


def compute_node_positions(
    s: NDArray[np.float64], theta: NDArray[np.float64], threshold: float = 0.01
) -> NDArray[np.float64]:
    """
    Find node positions (points of minimal displacement/angle).

    Args:
        s: Spatial coordinates (m)
        theta: Angle profile (rad)
        threshold: Relative threshold for node detection

    Returns:
        Array of node positions (m)
    """
    theta_centered = theta - np.mean(theta)
    theta_abs = np.abs(theta_centered)

    local_min_idx = []
    for i in range(1, len(theta_abs) - 1):
        if theta_abs[i] < theta_abs[i - 1] and theta_abs[i] < theta_abs[i + 1]:
            if theta_abs[i] < threshold * np.max(theta_abs):
                local_min_idx.append(i)

    return s[local_min_idx] if local_min_idx else np.array([])
