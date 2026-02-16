"""Tests for PyElastica protein simulation bridge."""

import pytest
import numpy as np
from spinalmodes.countercurvature.coupling import compute_rest_curvature, CounterCurvatureParams
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation, PYELASTICA_AVAILABLE

def test_kappa_gen_no_inplace_modification():
    """Test that kappa_gen is not modified in place by compute_rest_curvature."""
    n_points = 10
    s = np.linspace(0, 1, n_points)
    I = s
    dIds = np.ones_like(s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    params = CounterCurvatureParams(chi_kappa=1.0)

    # Create a 3xN kappa_gen
    original_kappa = np.zeros((3, n_points))
    original_kappa_copy = original_kappa.copy()

    # Run compute_rest_curvature
    _ = compute_rest_curvature(info, params, original_kappa)

    # Check if original_kappa was modified
    np.testing.assert_array_equal(original_kappa, original_kappa_copy,
                                  err_msg="original_kappa was modified in place!")

@pytest.mark.skipif(not PYELASTICA_AVAILABLE, reason="PyElastica not available")
def test_run_protein_simulation_location_sensitivity():
    """Test that changing info_location_rel affects the simulation result."""

    # Run simulation with location at 0.2
    res_top = run_protein_simulation(
        anisotropy=1.0,
        active_curvature=5.0,
        info_location_rel=0.2,
        duration=0.5, # Short duration for speed
        n_elements=20,
        show_progress=False
    )

    # Run simulation with location at 0.8
    res_bottom = run_protein_simulation(
        anisotropy=1.0,
        active_curvature=5.0,
        info_location_rel=0.8,
        duration=0.5,
        n_elements=20,
        show_progress=False
    )

    assert res_top["success"]
    assert res_bottom["success"]

    # Results should be different because curvature is applied at different heights
    # Specifically, z_tip or max_curvature location might differ, or simply the shape.
    # We can check simple scalar metrics.
    # With gravity, applying curvature high up vs low down has different leverage.

    # With planar forcing (chi_kappa only), the deformation is primarily sagittal (y-axis).
    # Lateral deviation (S_lat) is expected to be near zero for both if anisotropy=1.0.

    # Check sagittal tip deflection (y_tip).
    # Curvature at base (loc=0.2) should cause larger deflection than at tip (loc=0.8).
    y_tip_top = res_top.get("y_tip", 0.0)
    y_tip_bottom = res_bottom.get("y_tip", 0.0)

    # We expect some difference in the sagittal plane
    diff = abs(y_tip_top - y_tip_bottom)
    assert diff > 1e-6, f"Sagittal results for loc=0.2 and loc=0.8 are identical (diff={diff})"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
