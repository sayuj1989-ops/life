"""Metrics computation for Biological Countercurvature simulations."""

import numpy as np
from typing import Tuple
from dataclasses import dataclass


@dataclass
class RodMetrics:
    """Container for computed rod simulation metrics."""
    E_bend: float
    E_shear: float
    E_stretch: float
    E_total: float
    E_gravity: float
    curvature_mean: float
    curvature_std: float
    curvature_max: float
    curvature_min: float
    inflection_count: int
    tip_deflection: float
    end_sag: float
    c_shape_score: float
    s_shape_score: float
    D_geo: float
    D_geo_hat: float
    lateral_deviation_max: float
    cobb_angle_estimate: float
    centerline_x: np.ndarray = None
    centerline_y: np.ndarray = None
    centerline_z: np.ndarray = None
    curvature_profile: np.ndarray = None
    arc_length: np.ndarray = None


def compute_curvature(centerline: np.ndarray, window: int = 3) -> Tuple[np.ndarray, np.ndarray]:
    """Compute local curvature from centerline."""
    diffs = np.diff(centerline, axis=0)
    segment_lengths = np.linalg.norm(diffs, axis=1)
    arc_length = np.concatenate([[0.0], np.cumsum(segment_lengths)])
    tangent = diffs / (segment_lengths[:, np.newaxis] + 1e-12)
    tangent = np.vstack([tangent[0:1], tangent, tangent[-1:]])
    curvature = np.zeros(len(arc_length))
    for i in range(1, len(arc_length) - 1):
        dT = tangent[i+1] - tangent[i-1]
        ds = arc_length[i+1] - arc_length[i-1]
        curvature[i] = np.linalg.norm(dT) / (ds + 1e-12)
    return curvature, arc_length


def compute_mode_shape_discriminator(centerline: np.ndarray) -> Tuple[float, float]:
    """Characterize rod shape as C-shaped or S-shaped."""
    curvature, _ = compute_curvature(centerline)
    curvature_sign = np.sign(curvature)
    sign_changes = np.sum(np.abs(np.diff(curvature_sign)) > 0)
    
    if sign_changes >= 2:
        return 0.0, 1.0  # S-shaped
    elif sign_changes == 1:
        return 0.5, 0.5
    else:
        return 1.0, 0.0  # C-shaped


def compute_metrics_from_simulation(centerline: np.ndarray, 
                                    centerline_passive: np.ndarray = None,
                                    bending_stiffness: float = 1.0,
                                    rod_density: float = 1000.0,
                                    gravity: float = 9.81) -> RodMetrics:
    """Compute complete metrics set from simulation output."""
    curvature, arc_length = compute_curvature(centerline)
    
    if centerline_passive is None:
        s = arc_length / arc_length[-1]
        centerline_passive = np.column_stack([
            np.zeros_like(s),
            -s * (1 - s),
            np.zeros_like(s)
        ])
    
    # Energy
    ds = arc_length[1] - arc_length[0] if len(arc_length) > 1 else 1.0
    E_bend = 0.5 * bending_stiffness * np.trapz(curvature**2, dx=ds)
    E_gravity = -rod_density * gravity * np.mean(centerline[:, 2])
    E_shear = 0.1 * E_bend
    E_stretch = 0.05 * E_bend
    E_total = E_bend + E_shear + E_stretch + E_gravity
    
    # Curvature stats
    curvature_stats = {
        'mean': np.mean(curvature),
        'std': np.std(curvature),
        'max': np.max(curvature),
        'min': np.min(curvature),
        'inflections': int(np.sum(np.abs(np.diff(np.sign(curvature))) > 0))
    }
    
    # Shape characterization
    c_score, s_score = compute_mode_shape_discriminator(centerline)
    
    # Geodesic deviation
    diff = centerline - centerline_passive
    distances = np.linalg.norm(diff, axis=1)
    D_geo = np.sqrt(np.mean(distances**2))
    curvature_passive, _ = compute_curvature(centerline_passive)
    passive_squared = np.mean(curvature_passive**2)
    D_geo_hat = D_geo / (np.sqrt(passive_squared) + 1e-12)
    
    # Scoliosis metrics
    lateral_dev = np.max(np.abs(centerline[:, 0]))
    dx = centerline[-1, 0] - centerline[0, 0]
    dy = centerline[-1, 1] - centerline[0, 1]
    cobb_angle = np.degrees(np.arctan2(dx, dy)) if dy != 0 else 0.0
    
    # Endpoints
    tip_deflection = np.linalg.norm(centerline[-1, :2] - centerline[0, :2])
    end_sag = centerline[-1, 2] - centerline[0, 2]
    
    return RodMetrics(
        E_bend=float(E_bend),
        E_shear=float(E_shear),
        E_stretch=float(E_stretch),
        E_total=float(E_total),
        E_gravity=float(E_gravity),
        curvature_mean=float(curvature_stats['mean']),
        curvature_std=float(curvature_stats['std']),
        curvature_max=float(curvature_stats['max']),
        curvature_min=float(curvature_stats['min']),
        inflection_count=curvature_stats['inflections'],
        tip_deflection=float(tip_deflection),
        end_sag=float(end_sag),
        c_shape_score=float(c_score),
        s_shape_score=float(s_score),
        D_geo=float(D_geo),
        D_geo_hat=float(D_geo_hat),
        lateral_deviation_max=float(lateral_dev),
        cobb_angle_estimate=float(abs(cobb_angle)),
        centerline_x=centerline[:, 0],
        centerline_y=centerline[:, 1],
        centerline_z=centerline[:, 2],
        curvature_profile=curvature,
        arc_length=arc_length
    )
