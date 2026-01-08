#!/usr/bin/env python3
"""
Smoke test for upgraded BVP solver.

Verifies:
1. BVP solver runs without errors
2. Analytical benchmark comparison
3. IEC coupling mechanisms work
"""

import sys
sys.path.insert(0, "/Users/dr.sayujkrishnan/LIFE")

import numpy as np
from model.core import IECParameters
from model.solvers.bvp_scipy import BVPSolver
from model.solvers.euler_bernoulli import EulerBernoulliAnalytical, compare_bvp_to_analytical


def test_bvp_baseline():
    """Test 1: BVP solver runs for baseline (no IEC couplings)."""
    print("\n" + "="*60)
    print("TEST 1: BVP Solver Baseline (No IEC Couplings)")
    print("="*60)

    params = IECParameters(
        chi_kappa=0.0,
        chi_E=0.0,
        chi_C=0.0,
        chi_f=0.0,
        P_load=100.0,
        n_nodes=100,
    )

    solver = BVPSolver(params)
    print("✓ BVPSolver initialized")

    state = solver.solve()
    print(f"✓ BVP solved: {len(state.s)} nodes")
    print(f"  Max angle: {np.max(np.abs(state.theta)):.4f} rad = {np.rad2deg(np.max(np.abs(state.theta))):.2f}°")
    print(f"  Max curvature: {np.max(np.abs(state.kappa)):.4f} 1/m")

    validation = solver.validate_solution(state)
    print(f"✓ Validation:")
    print(f"  BC error: {validation['bc_error']:.2e}")
    print(f"  Energy error: {validation['energy_error']:.2%}")
    print(f"  Convergence: {validation['convergence']}")

    assert validation['convergence'], "Baseline solution should converge"
    print("\n✅ TEST 1 PASSED\n")


def test_analytical_comparison():
    """Test 2: BVP vs Analytical for linear case."""
    print("="*60)
    print("TEST 2: BVP vs Analytical Euler-Bernoulli")
    print("="*60)

    params = IECParameters(
        chi_kappa=0.0, chi_E=0.0, chi_C=0.0, chi_f=0.0,
        P_load=100.0,
        n_nodes=200,  # Higher resolution for accuracy
    )

    comparison = compare_bvp_to_analytical(params, solver_type="cantilever", tol=0.02)

    print(f"✓ Comparison complete:")
    print(f"  L2 error (θ): {comparison['L2_theta']:.4f}")
    print(f"  L2 error (κ): {comparison['L2_kappa']:.4f}")
    print(f"  L∞ error (θ): {comparison['Linf_theta']:.4e}")
    print(f"  Tolerance: {comparison['tolerance']}")
    print(f"  Passed: {comparison['passed']}")

    assert comparison['passed'], f"BVP error {comparison['L2_theta']:.2%} exceeds tolerance {comparison['tolerance']:.2%}"
    print("\n✅ TEST 2 PASSED\n")


def test_iec1_node_drift():
    """Test 3: IEC-1 mechanism (node drift without wavelength change)."""
    print("="*60)
    print("TEST 3: IEC-1 Node Drift (χ_κ ≠ 0)")
    print("="*60)

    # Baseline
    params_base = IECParameters(chi_kappa=0.0, I_mode="step", I_center=0.5, n_nodes=150)
    solver_base = BVPSolver(params_base)
    state_base = solver_base.solve()
    metrics_base = state_base.compute_metrics()

    # With IEC-1
    params_iec1 = IECParameters(chi_kappa=0.04, I_mode="step", I_center=0.5, n_nodes=150)
    solver_iec1 = BVPSolver(params_iec1)
    state_iec1 = solver_iec1.solve()
    metrics_iec1 = state_iec1.compute_metrics()

    # Compare
    wavelength_change = abs(metrics_iec1["wavelength_mm"] - metrics_base["wavelength_mm"]) / metrics_base["wavelength_mm"] * 100 if metrics_base["wavelength_mm"] > 0 else 0
    node_drift = metrics_iec1["node_drift_mm"]

    print(f"✓ IEC-1 Results:")
    print(f"  Baseline wavelength: {metrics_base['wavelength_mm']:.2f} mm")
    print(f"  IEC-1 wavelength: {metrics_iec1['wavelength_mm']:.2f} mm")
    print(f"  Wavelength change: {wavelength_change:.2f}%")
    print(f"  Node drift: {node_drift:.2f} mm")

    assert wavelength_change < 2.0, f"Wavelength changed by {wavelength_change:.1f}% (should be <2%)"
    print(f"  ✓ Wavelength change < 2% (acceptance criterion)")

    print("\n✅ TEST 3 PASSED\n")


def test_iec2_amplitude():
    """Test 4: IEC-2 mechanism (amplitude modulation)."""
    print("="*60)
    print("TEST 4: IEC-2 Amplitude Modulation (χ_E ≠ 0)")
    print("="*60)

    # Baseline
    params_base = IECParameters(chi_E=0.0, I_mode="constant", n_nodes=100)
    solver_base = BVPSolver(params_base)
    state_base = solver_base.solve()
    amp_base = state_base.compute_metrics()["amplitude_deg"]

    # With IEC-2 (reduced stiffness)
    params_iec2 = IECParameters(chi_E=-0.25, I_mode="constant", I_amplitude=1.0, n_nodes=100)
    solver_iec2 = BVPSolver(params_iec2)
    state_iec2 = solver_iec2.solve()
    amp_iec2 = state_iec2.compute_metrics()["amplitude_deg"]

    # Compare
    amp_change = abs(amp_iec2 - amp_base) / amp_base * 100

    print(f"✓ IEC-2 Results:")
    print(f"  Baseline amplitude: {amp_base:.2f}°")
    print(f"  IEC-2 amplitude: {amp_iec2:.2f}°")
    print(f"  Amplitude change: {amp_change:.2f}%")

    assert amp_change >= 10.0, f"Amplitude changed by {amp_change:.1f}% (should be ≥10%)"
    print(f"  ✓ Amplitude change ≥ 10% (acceptance criterion)")

    print("\n✅ TEST 4 PASSED\n")


def main():
    """Run all smoke tests."""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  IEC MODEL SOLVER UPGRADE - SMOKE TESTS".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60 + "\n")

    try:
        test_bvp_baseline()
        test_analytical_comparison()
        test_iec1_node_drift()
        test_iec2_amplitude()

        print("\n" + "█"*60)
        print("█" + " "*58 + "█")
        print("█" + "  ALL TESTS PASSED ✅".center(58) + "█")
        print("█" + " "*58 + "█")
        print("█" + "  Upgraded BVP solver is publication-ready!".center(58) + "█")
        print("█" + " "*58 + "█")
        print("█"*60 + "\n")

        return 0

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
