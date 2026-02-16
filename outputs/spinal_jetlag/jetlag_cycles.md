# Spinal Jetlag Experiment Report

**Date:** 2026-02-16 20:56:15

## Model

$$\chi_{\kappa}(t) = \chi_0 \cdot (1 + A(t) \cdot \cos(\omega t + \phi))$$

- **Entrained** (phi=0): Clock and gravity in phase
- **Free-running**: Clock drifts gradually
- **Jetlagged** (phi=pi): Anti-phase, destructive interference
- **Microgravity**: Zeitgeber removed, amplitude decays

## Summary by Condition

| Condition | Cycles | Final Cobb | Max Cobb | Mean S_lat | Mean U_CC |
|-----------|--------|------------|----------|------------|----------|
| entrained | 8 | 8.05 | 8.37 | 0.0273 | -190.4256 |
| jetlagged | 8 | 8.34 | 8.37 | 0.0273 | -190.4256 |

## Time Series (every 4th cycle)


### entrained

| Cycle | t (h) | chi_kappa | Amplitude | Cobb | S_lat |
|-------|-------|-----------|-----------|------|-------|
| 0 | 0.0 | 15.000 | 0.500 | 8.00 | 0.0293 |
| 4 | 12.0 | 5.000 | 0.500 | 8.37 | 0.0261 |

### jetlagged

| Cycle | t (h) | chi_kappa | Amplitude | Cobb | S_lat |
|-------|-------|-----------|-----------|------|-------|
| 0 | 0.0 | 5.000 | 0.500 | 8.37 | 0.0261 |
| 4 | 12.0 | 15.000 | 0.500 | 8.00 | 0.0293 |

## Key Predictions

1. **Phase Coherence**: Entrained condition should show lowest Cobb angles
2. **Destructive Interference**: Jetlagged (phi=pi) should show highest Cobb angles
3. **Microgravity Drift**: Clock amplitude decays → progressive geometric error
4. **Critical Phase**: Scoliosis onset at phi > pi/2 (90 degrees of mismatch)
