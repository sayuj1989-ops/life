"""PyElastica integration layer for countercurvature simulations.

This module provides factory utilities that construct Cosserat rod systems whose rest
curvature, stiffness and active moments are modulated by information fields.  The design
follows the biological countercurvature hypothesis: information gradients act as local
corrections to the mechanical metric, effectively biasing the rod against gravity-driven
modes.
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
    # Dummy classes
    class ea:
        class CosseratRod: pass
        class NoForces: pass
        class CallBackBaseClass: pass
        class OneEndFixedBC: pass
        class GravityForces: pass
        class AnalyticalLinearDamper: pass
        class BaseSystemCollection: pass
        class Constraints: pass
        class Forcing: pass
        class Damping: pass
        class CallBacks: pass
        class PositionVerlet: pass
        class integrate: pass
        class ConstraintBase:
            def __init__(self, **kwargs): pass

@dataclass
class SimulationResult:
    time: ArrayF64
    centerline: ArrayF64
    kappa: ArrayF64
    info_field: InfoField1D

    @property
    def curvature(self) -> ArrayF64:
        """Returns the bending curvature (norm of kappa[0,1])."""
        return np.linalg.norm(self.kappa[..., :2], axis=-1)

    @property
    def torsion(self) -> ArrayF64:
        """Returns the torsion (kappa[2])."""
        return self.kappa[..., 2]

    def compute_final_metrics(self) -> Dict[str, float]:
        """Compute scalar metrics for the final state of the simulation."""
        if len(self.time) == 0:
            return {}

        pos = self.centerline[-1] # (n_nodes, 3)
        kappa = self.kappa[-1]    # (n_nodes, 3)
        end_to_end = np.linalg.norm(pos[-1] - pos[0])
        bending_mag = np.linalg.norm(kappa[:, :2], axis=1)
        max_curvature = float(np.max(bending_mag))
        torsion_mag = np.abs(kappa[:, 2])
        max_torsion = float(np.max(torsion_mag))
        z_coord = pos[:, 2]
        x_coord = pos[:, 0]
        y_coord = pos[:, 1]
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
        raise ImportError(
            "PyElastica is not installed. To install:\n"
            "pip install pyelastica\n"
            "Or see: https://github.com/GazzolaLab/PyElastica"
        )

class ActiveMuscleTorques(ea.NoForces):
    """Applies a static distributed active moment (muscle torque)."""
    def __init__(self, torques: ArrayF64):
        super().__init__()
        self.torques = torques  # (3, n_elements)

    def apply_torques(self, system, time: float = 0.0):
        system.external_torques += self.torques

class PinnedBC(ea.ConstraintBase):
    """Boundary Condition that pins the position of selected nodes but allows free rotation."""
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(**kwargs)
            if 'fixed_position' in kwargs:
                self.fixed_position = np.array(kwargs['fixed_position'])
            elif len(args) > 0:
                self.fixed_position = np.array(args[0])
            else:
                 # Last ditch: check if 'fixed_pos' or similar was passed?
                 raise ValueError("PinnedBC requires 'fixed_position' arg or kwarg.")
        except Exception as e:
            print(f"PinnedBC Init Failed: {e}")
            raise

    def constrain_values(self, system, time):
        system.position_collection[..., 0] = self.fixed_position

    def constrain_rates(self, system, time):
        system.velocity_collection[..., 0] = 0.0

class FixedBC(ea.ConstraintBase):
    """Boundary Condition that pins position and directors (clamped)."""
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(**kwargs)
            if 'fixed_position' in kwargs and 'fixed_directors' in kwargs:
                self.fixed_position = np.array(kwargs['fixed_position'])
                self.fixed_directors = np.array(kwargs['fixed_directors'])
            elif len(args) >= 2:
                self.fixed_position = np.array(args[0])
                self.fixed_directors = np.array(args[1])
            else:
                raise ValueError("FixedBC requires 'fixed_position' and 'fixed_directors'.")
        except Exception as e:
            print(f"FixedBC Init Failed: {e}")
            raise

    def constrain_values(self, system, time):
        system.position_collection[..., 0] = self.fixed_position
        system.director_collection[..., 0] = self.fixed_directors

    def constrain_rates(self, system, time):
        system.velocity_collection[..., 0] = 0.0
        system.omega_collection[..., 0] = 0.0

class CounterCurvatureRodSystem:
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

    def __repr__(self) -> str:
        return (
            f"<CounterCurvatureRodSystem L={self.length:.2f}, n={self.n_elements}, "
            f"params={self.params}>"
        )

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
        s_rod = np.linspace(0, length, n_elements + 1)
        s_elements = 0.5 * (s_rod[:-1] + s_rod[1:])
        E_eff_elements = np.interp(s_elements, info.s, E_eff)

        # Scale shear matrix (3, 3, n_elements)
        scaling_shear = E_eff_elements / E0
        for k in range(n_elements):
            rod.shear_matrix[..., k] *= scaling_shear[k]

        # Interpolate E_eff to Voronoi domains (internal nodes) for bend matrix modification
        s_internal = s_rod[1:-1]
        E_eff_internal = np.interp(s_internal, info.s, E_eff)

        # Scale bend matrix (3, 3, n_elements - 1)
        scaling_bend = E_eff_internal / E0
        for k in range(n_elements - 1):
            rod.bend_matrix[..., k] *= scaling_bend[k]

        # Apply stiffness anisotropy
        if stiffness_anisotropy != 1.0:
            rod.bend_matrix[0, 0, :] *= stiffness_anisotropy

        # Set rest curvature
        kappa_rest = compute_rest_curvature(info, params, kappa_gen if kappa_gen is not None else 0.0)
        rest_kappa = np.zeros((3, n_elements - 1))
        for i in range(3):
            rest_kappa[i, :] = np.interp(s_internal, info.s, kappa_rest[i, :])
        rod.rest_kappa[:] = rest_kappa

        # Compute active moments (scalar field on nodes) if chi_M != 0
        active_torques = None
        if params.chi_M != 0.0:
            M_active_nodes = compute_active_moments(info, params)
            M_active_elems = np.interp(s_elements, info.s, M_active_nodes)
            active_torques = np.zeros((3, n_elements))
            active_torques[1, :] = M_active_elems

        return cls(rod=rod, info_field=info, params=params, active_torques=active_torques)

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
            # Capture initial state for BCs
            pos0 = self.rod.position_collection[..., 0].copy()
            dirs0 = self.rod.director_collection[..., 0].copy()

            # Use keyword arguments for robustness, since debug_bc.py showed it works.
            # AND use custom FixedBC class to be safe.
            # print(f"DEBUG: pos0 shape={pos0.shape}, dirs0 shape={dirs0.shape}")

            if boundary_condition == "fixed":
                system.constrain(self.rod).using(
                    FixedBC,
                    constrained_position_idx=(0,),
                    constrained_director_idx=(0,),
                    fixed_position=pos0,
                    fixed_directors=dirs0
                )
            elif boundary_condition == "pinned":
                system.constrain(self.rod).using(
                    PinnedBC,
                    constrained_position_idx=(0,),
                    constrained_director_idx=(),
                    fixed_position=pos0
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
                    self.results["kappa"].append(system.kappa.copy().T)

        results = {"time": [], "centerline": [], "kappa": []}
        system.collect_diagnostics(self.rod).using(CCCallback, step_skip=save_every, results=results)

        system.finalize()
        timestepper = ea.PositionVerlet()
        ea.integrate(timestepper, system, final_time, int(final_time/dt))

        kappa_raw = np.array(results["kappa"])
        if len(kappa_raw) > 0:
            n_time, n_internal, n_dim = kappa_raw.shape
            padded_kappa = np.zeros((n_time, n_internal + 2, n_dim))
            padded_kappa[:, 1:-1, :] = kappa_raw
        else:
            padded_kappa = np.empty((0, self.n_elements + 1, 3))

        return SimulationResult(
            time=np.array(results["time"]),
            centerline=np.array(results["centerline"]),
            kappa=padded_kappa,
            info_field=self.info_field
        )

__all__ = ["CounterCurvatureRodSystem", "SimulationResult", "PYELASTICA_AVAILABLE", "ActiveMuscleTorques", "PinnedBC", "FixedBC"]
