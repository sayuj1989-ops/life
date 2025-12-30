"""PyElastica integration layer for countercurvature simulations.

This module provides factory utilities that construct Cosserat rod systems whose rest
curvature, stiffness and active moments are modulated by information fields.  The design
follows the biological countercurvature hypothesis: information gradients act as local
corrections to the mechanical metric, effectively biasing the rod against gravity-driven
modes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

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

@dataclass
class SimulationResult:
    time: ArrayF64
    centerline: ArrayF64
    curvature: ArrayF64
    info_field: InfoField1D

def _check_pyelastica() -> None:
    if not PYELASTICA_AVAILABLE:
        raise ImportError("PyElastica is not installed.")

class CounterCurvatureRodSystem:
    def __init__(self, rod: ea.CosseratRod, info_field: InfoField1D, params: CounterCurvatureParams):
        self.rod = rod
        self.info_field = info_field
        self.params = params
        self.n_elements = rod.n_elems
        self.length = np.sum(rod.rest_lengths)

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

        # Set heterogeneous stiffness (simplified: use E0 for now)
        # Set rest curvature
        if kappa_gen is None:
            kappa_gen = np.zeros(info.n_points)
        kappa_rest = compute_rest_curvature(info, params, kappa_gen)
        
        # Interpolate to element centers (n_elements - 1 internal nodes)
        s_voronoi = 0.5 * (info.s[:-1] + info.s[1:])
        kappa_voronoi = np.interp(s_voronoi, info.s, kappa_rest)
        
        # PyElastica rest_kappa has shape (3, n_elements-1)
        rest_kappa = np.zeros((3, n_elements - 1))
        rest_kappa[1, :] = kappa_voronoi[:-1] # Use y-axis for sagittal plane
        rod.rest_kappa[:] = rest_kappa

        return cls(rod=rod, info_field=info, params=params)

    def run_simulation(
        self,
        final_time: float,
        dt: float,
        *,
        save_every: int = 100,
        gravity: float = 9.81,
        damping_constant: float = 0.5,
    ) -> SimulationResult:
        _check_pyelastica()

        class CCSystem(ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks):
            pass

        system = CCSystem()
        system.append(self.rod)

        # Constraints
        system.constrain(self.rod).using(ea.OneEndFixedBC, constrained_position_idx=(0,), constrained_director_idx=(0,))

        # Gravity
        system.add_forcing_to(self.rod).using(ea.GravityForces, acc_gravity=np.array([0.0, 0.0, -gravity]))

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
                    self.results["curvature"].append(np.linalg.norm(system.kappa, axis=0))

        results = {"time": [], "centerline": [], "curvature": []}
        system.collect_diagnostics(self.rod).using(CCCallback, step_skip=save_every, results=results)

        system.finalize()
        timestepper = ea.PositionVerlet()
        ea.integrate(timestepper, system, final_time, int(final_time/dt))

        # Pad curvature to match n_points
        curv = np.array(results["curvature"])
        padded_curv = np.zeros((curv.shape[0], curv.shape[1] + 2))
        padded_curv[:, 1:-1] = curv

        return SimulationResult(
            time=np.array(results["time"]),
            centerline=np.array(results["centerline"]),
            curvature=padded_curv,
            info_field=self.info_field
        )

__all__ = ["CounterCurvatureRodSystem", "SimulationResult", "PYELASTICA_AVAILABLE"]
