"""
Public API for the countercurvature framework.

This module exposes a minimal, stable surface for users:
- Info fields and IEC→geometry couplings
- Countercurvature metric and geodesic deviation
- PyElastica bridge for 3D rods
- Scoliosis metrics and regime classification

Usage
-----
>>> from spinalmodes.countercurvature import api
>>> info = api.InfoField1D(...)
>>> g_eff = api.compute_countercurvature_metric(info)
>>> D_geo = api.geodesic_curvature_deviation(s, kappa_0, kappa_I, g_eff)
"""

from .info_fields import (
    InfoField1D,
    InfoFieldTimeSeries,
    make_uniform_grid,
)
from .coupling import (
    CounterCurvatureParams,
    compute_rest_curvature,
    compute_effective_stiffness,
    compute_active_moments,
)
from .validation_and_metrics import (
    compute_countercurvature_metric,
    geodesic_curvature_deviation,
)
from .pyelastica_bridge import CounterCurvatureRodSystem
from .scoliosis_metrics import (
    ScoliosisMetrics,
    RegimeThresholds,
    compute_scoliosis_metrics,
    classify_scoliotic_regime,
)

__all__ = [
    "InfoField1D",
    "InfoFieldTimeSeries",
    "make_uniform_grid",
    "CounterCurvatureParams",
    "compute_rest_curvature",
    "compute_effective_stiffness",
    "compute_active_moments",
    "compute_countercurvature_metric",
    "geodesic_curvature_deviation",
    "CounterCurvatureRodSystem",
    "ScoliosisMetrics",
    "RegimeThresholds",
    "compute_scoliosis_metrics",
    "classify_scoliotic_regime",
]
