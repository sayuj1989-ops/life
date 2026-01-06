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

        # Set rest curvature
        if kappa_gen is None:
            kappa_gen = np.zeros(info.n_points)
        kappa_rest = compute_rest_curvature(info, params, kappa_gen)

        # PyElastica stores rest_kappa at Voronoi domains (internal nodes)
        # We need to map kappa_rest (defined on info.s) to s_internal
        kappa_internal = np.interp(s_internal, info.s, kappa_rest)
        
        # PyElastica rest_kappa has shape (3, n_elements-1)
        rest_kappa = np.zeros((3, n_elements - 1))
        rest_kappa[1, :] = kappa_internal # Use y-axis for sagittal plane
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
    ) -> SimulationResult:
        _check_pyelastica()

        class CCSystem(ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks):
            pass

        system = CCSystem()
        system.append(self.rod)

        # Constraints
        if bc_cls is None:
            # Default to OneEndFixedBC
            system.constrain(self.rod).using(
                ea.OneEndFixedBC,
                constrained_position_idx=(0,),
                constrained_director_idx=(0,)
            )
        else:
            kwargs = bc_kwargs or {}
            system.constrain(self.rod).using(bc_cls, **kwargs)

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
        else:
            padded_kappa = np.empty((0, self.n_elements + 1, 3))

        return SimulationResult(
            time=np.array(results["time"]),
            centerline=np.array(results["centerline"]),
            kappa=padded_kappa,
            info_field=self.info_field
        )

__all__ = ["CounterCurvatureRodSystem", "SimulationResult", "PYELASTICA_AVAILABLE", "ActiveMuscleTorques"]
