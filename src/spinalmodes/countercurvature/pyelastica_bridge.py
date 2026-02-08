"""PyElastica integration layer for countercurvature simulations.

This module provides factory utilities that construct Cosserat rod systems whose rest
curvature, stiffness and active moments are modulated by information fields.  The design
follows the biological countercurvature hypothesis: information gradients act as local
corrections to the mechanical metric, effectively biasing the rod against gravity-driven
modes.

Key Concepts:
- Vector Signal: Stiffness Anisotropy (ECM alignment).
- Scalar Signal: Active Growth/Curvature (Piezo/Ion flux).
- Mismatch: When Vector and Scalar signals dissociate (e.g. Microgravity).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, Type, Dict, Any

import numpy as np
from numpy.typing import NDArray

from .coupling import (
    CounterCurvatureParams,
    compute_active_moments,
    compute_effective_stiffness,
    compute_rest_curvature,
)
from .info_fields import InfoField1D
from .scoliosis_metrics import compute_scoliosis_metrics, ScoliosisMetrics

ArrayF64 = NDArray[np.float64]

# Try to import PyElastica, but make it optional
try:
    import elastica as ea
    PYELASTICA_AVAILABLE = True
except ImportError:
    PYELASTICA_AVAILABLE = False
    # Dummy classes for testing/mocking
    class MockRod:
        def __init__(self, n_elements, length):
            self.n_elems = n_elements
            self.rest_lengths = np.ones(n_elements) * (length / n_elements)
            self.shear_matrix = np.zeros((3, 3, n_elements))
            self.bend_matrix = np.zeros((3, 3, n_elements - 1))
            self.rest_kappa = np.zeros((3, n_elements - 1))
            self.position_collection = np.zeros((3, n_elements + 1))
            self.velocity_collection = np.zeros((3, n_elements + 1))
            self.kappa = np.zeros((3, n_elements - 1))

    class ea:
        class CosseratRod:
            @staticmethod
            def straight_rod(n_elements, base_length, **kwargs):
                return MockRod(n_elements, base_length)
        class NoForces: pass
        class CallBackBaseClass: pass
        class ConstraintBase: pass
        class OneEndFixedBC: pass
        class GravityForces: pass
        class AnalyticalLinearDamper: pass
        class BaseSystemCollection:
            def append(self, *args, **kwargs): pass
            def constrain(self, *args, **kwargs): return self
            def using(self, *args, **kwargs): return self
            def add_forcing_to(self, *args, **kwargs): return self
            def dampen(self, *args, **kwargs): return self
            def collect_diagnostics(self, *args, **kwargs): return self
            def finalize(self): pass
        class Constraints: pass
        class Forcing: pass
        class Damping: pass
        class CallBacks: pass
        class PositionVerlet: pass
        @staticmethod
        def integrate(*args, **kwargs): pass

@dataclass
class SimulationResult:
    time: ArrayF64
    centerline: ArrayF64
    kappa: ArrayF64
    info_field: InfoField1D

    @property
    def curvature(self) -> ArrayF64:
        """Returns the bending curvature (norm of kappa[0,1])."""
        # kappa is (time, n_nodes, 3).
        # We assume d1, d2 are bending, d3 is torsion.
        # Norm of first two components.
        return np.linalg.norm(self.kappa[..., :2], axis=-1)

    @property
    def torsion(self) -> ArrayF64:
        """Returns the torsion (kappa[2])."""
        return self.kappa[..., 2]

    def compute_final_metrics(self) -> Dict[str, float]:
        """Compute scalar metrics for the final state of the simulation.

        Returns:
            Dict containing:
                - max_curvature: Maximum curvature magnitude.
                - max_torsion: Maximum torsion magnitude.
                - end_to_end_distance: Distance between first and last node.
                - S_lat: Lateral scoliosis index (from scoliosis_metrics).
                - cobb_angle: Cobb-like angle (from scoliosis_metrics).
                - z_tip: Tip deflection in Z (vertical).
        """
        if len(self.time) == 0:
            return {}

        # Use final state
        pos = self.centerline[-1] # (n_nodes, 3)
        kappa = self.kappa[-1]    # (n_nodes, 3)

        # Basic geometry
        end_to_end = np.linalg.norm(pos[-1] - pos[0])

        # Curvature/Torsion metrics
        # kappa shape (n_nodes, 3). Bending is first two components.
        bending_mag = np.linalg.norm(kappa[:, :2], axis=1)
        max_curvature = float(np.max(bending_mag))

        torsion_mag = np.abs(kappa[:, 2])
        max_torsion = float(np.max(torsion_mag))

        # Scoliosis metrics
        # Assuming rod is vertical along Z.
        # Longitudinal = Z (index 2).
        # Lateral = X (index 0). Y (index 1) is sagittal depth.
        z_coord = pos[:, 2]
        x_coord = pos[:, 0]

        scol_metrics = compute_scoliosis_metrics(z_coord, x_coord)

        return {
            "max_curvature": max_curvature,
            "max_torsion": max_torsion,
            "end_to_end_distance": float(end_to_end),
            "S_lat": scol_metrics.S_lat,
            "cobb_angle": scol_metrics.cobb_like_deg,
            "z_tip": float(pos[-1, 2]),
            "x_tip": float(pos[-1, 0]),
            "y_tip": float(pos[-1, 1]),
        }

def _check_pyelastica() -> None:
    if not PYELASTICA_AVAILABLE:
        msg = (
            "PyElastica is not installed but is required for this module.\n"
            "Please install it using:\n"
            "  pip install pyelastica\n"
            "Or visit: https://github.com/GazzolaLab/PyElastica"
        )
        raise ImportError(msg)
    else:
        # Consistency check with scripts/check_pyelastica.py
        # Ensure we can access basic attributes to verify full load
        _ = getattr(ea, "__version__", "unknown")

class ActiveMuscleTorques(ea.NoForces):
    """Applies a static distributed active moment (muscle torque)."""
    def __init__(self, torques: ArrayF64):
        super().__init__()
        self.torques = torques  # (3, n_elements)

    def apply_torques(self, system, time: float = 0.0):
        system.external_torques += self.torques

class PinnedBC(ea.ConstraintBase):
    """
    Boundary Condition that pins the position of selected nodes (fixes position)
    but allows free rotation (does not constrain directors).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if not args:
             raise ValueError("PinnedBC requires fixed position argument (passed via constrained_position_idx).")
        self.fixed_position = np.array(args[0])

    def constrain_values(self, *args, **kwargs):
        # Expecting rod as first arg from partial application, but we use *args to be safe
        if args:
            rod = args[0]
            if hasattr(self, 'fixed_position'):
                rod.position_collection[..., 0] = self.fixed_position

    def constrain_rates(self, *args, **kwargs):
         if args:
            rod = args[0]
            rod.velocity_collection[..., 0] = 0.0

class CounterCurvatureRodSystem:
    """
    A PyElastica-based rod system configured for biological counter-curvature simulations.

    This class bridges the information-field theory (IEC) to the Cosserat rod physics engine.
    It maps biological inputs (protein concentrations, ECM organization) to mechanical
    properties like stiffness anisotropy and rest curvature.
    """
    def __init__(
        self,
        rod: ea.CosseratRod,
        info_field: InfoField1D,
        params: CounterCurvatureParams,
        active_torques: Optional[ArrayF64] = None
    ):
        self.rod = rod
        self.info_field = info_field
        self.params = params
        self.n_elements = rod.n_elems
        self.length = np.sum(rod.rest_lengths)
        self.active_torques = active_torques

    @classmethod
    def from_iec(
        cls,
        info: InfoField1D,
        params: CounterCurvatureParams,
        length: float,
        n_elements: int,
        *,
        E0: float = 1e6,
        nu: float = 0.5,
        rho: float = 1000.0,
        radius: float = 0.01,
        kappa_gen: Optional[ArrayF64] = None,
        gravity: float = 9.81,
        base_position: tuple[float, float, float] = (0.0, 0.0, 0.0),
        base_direction: tuple[float, float, float] = (0.0, 0.0, 1.0),
        normal: tuple[float, float, float] = (0.0, 1.0, 0.0),
        stiffness_anisotropy: float = 1.0,
    ) -> "CounterCurvatureRodSystem":
        _check_pyelastica()

        # Create rod
        rod = ea.CosseratRod.straight_rod(
            n_elements=n_elements,
            start=np.array(base_position),
            direction=np.array(base_direction),
            normal=np.array(normal),
            base_length=length,
            base_radius=radius,
            density=rho,
            youngs_modulus=E0,
            shear_modulus=E0 / (2.0 * (1.0 + nu)),
        )

        # Compute effective stiffness E_eff based on information field
        E_eff = compute_effective_stiffness(info, params, E0)

        # Interpolate E_eff to element centers for shear matrix modification
        # s_rod (nodes): [0, ..., L]
        # s_elements (centers): midpoints of nodes
        s_rod = np.linspace(0, length, n_elements + 1)
        s_elements = 0.5 * (s_rod[:-1] + s_rod[1:])
        E_eff_elements = np.interp(s_elements, info.s, E_eff)

        # Scale shear matrix (3, 3, n_elements)
        # Assuming isotropic scaling of shear modulus with Young's modulus
        # shear_matrix ~ G ~ E. So we scale by E_eff_elements / E0
        scaling_shear = E_eff_elements / E0
        for k in range(n_elements):
            rod.shear_matrix[..., k] *= scaling_shear[k]

        # Interpolate E_eff to Voronoi domains (internal nodes) for bend matrix modification
        # Voronoi domains are at s_rod[1:-1]
        s_internal = s_rod[1:-1]
        E_eff_internal = np.interp(s_internal, info.s, E_eff)

        # Scale bend matrix (3, 3, n_elements - 1)
        # bend_matrix ~ E * I. So we scale by E_eff_internal / E0
        scaling_bend = E_eff_internal / E0
        for k in range(n_elements - 1):
            rod.bend_matrix[..., k] *= scaling_bend[k]

        # Apply stiffness anisotropy
        # bend_matrix[0, 0] corresponds to stiffness about d1 (Normal).
        # In this setup (d1=X), this resists Sagittal bending (Y-Z plane).
        # bend_matrix[1, 1] corresponds to stiffness about d2 (Binormal).
        # In this setup (d2=Y), this resists Lateral bending (X-Z plane).
        if stiffness_anisotropy != 1.0:
            rod.bend_matrix[0, 0, :] *= stiffness_anisotropy

        # Set rest curvature
        # kappa_rest is now (3, n_points)
        kappa_rest = compute_rest_curvature(info, params, kappa_gen if kappa_gen is not None else 0.0)

        # PyElastica stores rest_kappa at Voronoi domains (internal nodes)
        # We need to map kappa_rest (defined on info.s) to s_internal
        # We need to interpolate each component: (3, n_points) -> (3, n_elements-1)
        
        rest_kappa = np.zeros((3, n_elements - 1))
        for i in range(3):
            rest_kappa[i, :] = np.interp(s_internal, info.s, kappa_rest[i, :])

        rod.rest_kappa[:] = rest_kappa

        # Compute active moments (scalar field on nodes) if chi_M != 0
        active_torques = None
        if params.chi_M != 0.0:
            M_active_nodes = compute_active_moments(info, params)

            # Interpolate to elements (where external torques are applied)
            M_active_elems = np.interp(s_elements, info.s, M_active_nodes)

            # Create torque vector (3, n_elements)
            # Bending in sagittal plane (x-z) with normal y: torque around y-axis (index 1)
            active_torques = np.zeros((3, n_elements))
            active_torques[1, :] = M_active_elems

        return cls(rod=rod, info_field=info, params=params, active_torques=active_torques)

    def __repr__(self) -> str:
        """Return a string representation of the rod system configuration."""
        # Estimate anisotropy from first element's bend matrix if possible
        anisotropy = 1.0
        if hasattr(self.rod, "bend_matrix") and self.rod.bend_matrix.shape[2] > 0:
            # bend_matrix[0,0] / bend_matrix[1,1]
            # Avoid division by zero
            b00 = self.rod.bend_matrix[0, 0, 0]
            b11 = self.rod.bend_matrix[1, 1, 0]
            if b11 != 0:
                anisotropy = b00 / b11

        return (
            f"<CounterCurvatureRodSystem elements={self.n_elements} "
            f"length={self.length:.2f} "
            f"chi_kappa={self.params.chi_kappa:.2f} "
            f"anisotropy={anisotropy:.2f}>"
        )

    def get_configuration(self) -> Dict[str, Any]:
        """Return a dictionary of the system configuration for logging."""
        # Calculate anisotropy again for the dict
        anisotropy = 1.0
        if hasattr(self.rod, "bend_matrix") and self.rod.bend_matrix.shape[2] > 0:
            b00 = self.rod.bend_matrix[0, 0, 0]
            b11 = self.rod.bend_matrix[1, 1, 0]
            if b11 != 0:
                anisotropy = b00 / b11

        return {
            "n_elements": self.n_elements,
            "length": self.length,
            "chi_kappa": self.params.chi_kappa,
            "chi_tau": self.params.chi_tau,
            "chi_E": self.params.chi_E,
            "chi_M": self.params.chi_M,
            "stiffness_anisotropy": anisotropy
        }

    def run_simulation(
        self,
        final_time: float,
        dt: float,
        *,
        save_every: int = 100,
        gravity: float = 9.81,
        damping_constant: float = 0.5,
        bc_cls: Optional[Type] = None,
        bc_kwargs: Optional[Dict[str, Any]] = None,
        boundary_condition: str = "fixed",
    ) -> SimulationResult:
        _check_pyelastica()

        class CCSystem(ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks):
            pass

        system = CCSystem()
        system.append(self.rod)

        # Constraints
        if bc_cls is not None:
            kwargs = bc_kwargs or {}
            system.constrain(self.rod).using(bc_cls, **kwargs)
        else:
            # Configure based on string description
            if boundary_condition == "fixed":
                system.constrain(self.rod).using(
                    ea.OneEndFixedBC,
                    constrained_position_idx=(0,),
                    constrained_director_idx=(0,)
                )
            elif boundary_condition == "pinned":
                # Pinned: Position fixed at node 0, Directors free
                system.constrain(self.rod).using(
                    PinnedBC,
                    constrained_position_idx=(0,),
                    constrained_director_idx=()
                )
            else:
                raise ValueError(f"Unknown boundary_condition: {boundary_condition}. Use 'fixed' or 'pinned'.")

        # Gravity
        system.add_forcing_to(self.rod).using(ea.GravityForces, acc_gravity=np.array([0.0, 0.0, -gravity]))

        # Active Moments (if any)
        if self.active_torques is not None:
             system.add_forcing_to(self.rod).using(ActiveMuscleTorques, torques=self.active_torques)

        # Damping
        system.dampen(self.rod).using(ea.AnalyticalLinearDamper, damping_constant=damping_constant, time_step=dt)

        # Callback
        class CCCallback(ea.CallBackBaseClass):
            def __init__(self, step_skip, results):
                super().__init__()
                self.every = step_skip
                self.results = results
            def make_callback(self, system, time, current_step):
                if current_step % self.every == 0:
                    self.results["time"].append(time)
                    self.results["centerline"].append(system.position_collection.copy().T)
                    # Save full kappa vector (3, n_elems-1) -> transpose to (n_elems-1, 3)
                    self.results["kappa"].append(system.kappa.copy().T)

        results = {"time": [], "centerline": [], "kappa": []}
        system.collect_diagnostics(self.rod).using(CCCallback, step_skip=save_every, results=results)

        system.finalize()
        timestepper = ea.PositionVerlet()
        ea.integrate(timestepper, system, final_time, int(final_time/dt))

        # Pad kappa to match n_nodes (n_elems + 1)
        # kappa is (time, n_elems-1, 3)
        # We want (time, n_elems+1, 3)
        kappa_raw = np.array(results["kappa"])
        if len(kappa_raw) > 0:
            n_time, n_internal, n_dim = kappa_raw.shape
            padded_kappa = np.zeros((n_time, n_internal + 2, n_dim))
            padded_kappa[:, 1:-1, :] = kappa_raw
            # Edge padding: repeat first/last valid values to avoid zero artifacts
            padded_kappa[:, 0, :] = kappa_raw[:, 0, :]
            padded_kappa[:, -1, :] = kappa_raw[:, -1, :]
        else:
            padded_kappa = np.empty((0, self.n_elements + 1, 3))

        return SimulationResult(
            time=np.array(results["time"]),
            centerline=np.array(results["centerline"]),
            kappa=padded_kappa,
            info_field=self.info_field
        )

__all__ = ["CounterCurvatureRodSystem", "SimulationResult", "PYELASTICA_AVAILABLE", "ActiveMuscleTorques"]
