import pytest

from spinalmodes.model.solvers.cosserat import available


@pytest.mark.skipif(not available(), reason="PyElastica not installed")
def test_cosserat_bridge_available():
    assert available() is True


import numpy as np
from spinalmodes.model.solvers.cosserat import simulate_cosserat
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.coupling import CounterCurvatureParams

@pytest.mark.skipif(not available(), reason="PyElastica not installed")
def test_simulate_cosserat_metrics():
    # Setup simple parameters
    length = 1.0
    n_elements = 10
    n_points = n_elements + 1
    s = np.linspace(0, length, n_points)
    I = np.ones(n_points) * 0.5
    dIds = np.zeros(n_points)

    info = InfoField1D(s=s, I=I, dIds=dIds)
    iec_params = CounterCurvatureParams(
        chi_kappa=0.0, chi_E=0.0, chi_M=0.0, scale_length=length
    )

    params = {
        "info": info,
        "iec_params": iec_params,
        "length": length,
        "n_elements": n_elements,
        "final_time": 0.1,  # Short simulation for testing
        "dt": 1e-4,
    }

    response = simulate_cosserat(params)

    assert response["ok"] is True
    assert response["reason"] is None

    result = response["result"]
    assert result is not None

    # Check that original fields are still present
    assert "time" in result
    assert "centerline" in result
    assert "curvature" in result
    assert "info_field" in result

    # Check for new performance metrics
    assert "runtime_sec" in result
    assert isinstance(result["runtime_sec"], float)
    assert result["runtime_sec"] >= 0

    assert "peak_memory_mb" in result
    assert isinstance(result["peak_memory_mb"], float)
    assert result["peak_memory_mb"] >= 0

    # Check for clinical and geometric metrics
    # `compute_final_metrics()` returns these
    assert "max_curvature" in result
    assert "max_torsion" in result
    assert "end_to_end_distance" in result
    assert "S_lat" in result
    assert "cobb_angle" in result
    assert "z_tip" in result
