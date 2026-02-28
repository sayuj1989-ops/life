# Spinal Jetlag Experiment Report

**Date:** 2026-02-27 21:34:49

## Model

$$\chi_{\kappa}(t) = \chi_0 \cdot (1 + A(t) \cdot \cos(\omega t + \phi))$$

- **Entrained** (phi=0): Clock and gravity in phase
- **Free-running**: Clock drifts gradually
- **Jetlagged** (phi=pi): Anti-phase, destructive interference
- **Microgravity**: Zeitgeber removed, amplitude decays

## Summary by Condition

| Condition | Cycles | Final Cobb | Max Cobb | Mean S_lat | Mean U_CC |
|-----------|--------|------------|----------|------------|----------|
| entrained | 28 | 8.05 | 16.61 | 0.0913 | -0.1138 |
| phase_shift_45 | 12 | 10.80 | 16.27 | 0.1766 | -0.1751 |
| phase_shift_90 | 12 | 8.51 | 16.61 | 0.1766 | -0.1751 |
| jetlagged | 28 | 8.34 | 16.61 | 0.0913 | -0.1138 |
| microgravity | 12 | 11.76 | 15.09 | 0.1154 | -0.4418 |
| microgravity_jetlag | 12 | 13.97 | 16.23 | 0.1153 | -0.4245 |
| constant_chi | 12 | 9.11 | 9.11 | 0.1713 | -0.1329 |
| high_chi_jetlag | 12 | 8.44 | 44.84 | 0.2704 | -1.6032 |

## Time Series (every 4th cycle)


### entrained

| Cycle | t (h) | chi_kappa | Amplitude | Cobb | S_lat |
|-------|-------|-----------|-----------|------|-------|
| 0 | 0.0 | 15.000 | 0.500 | 11.10 | 0.2089 |
| 4 | 8.0 | 7.500 | 0.500 | 12.10 | 0.1591 |
| 8 | 16.0 | 7.500 | 0.500 | 12.10 | 0.1591 |
| 0 | 0.0 | 15.000 | 0.500 | 8.00 | 0.0293 |
| 4 | 12.0 | 5.000 | 0.500 | 8.37 | 0.0261 |
| 0 | 0.0 | 15.000 | 0.500 | 8.00 | 0.0293 |
| 4 | 12.0 | 5.000 | 0.500 | 8.37 | 0.0261 |

### phase_shift_45

| Cycle | t (h) | chi_kappa | Amplitude | Cobb | S_lat |
|-------|-------|-----------|-----------|------|-------|
| 0 | 0.0 | 13.536 | 0.500 | 9.14 | 0.1967 |
| 4 | 8.0 | 5.170 | 0.500 | 16.27 | 0.1550 |
| 8 | 16.0 | 11.294 | 0.500 | 8.45 | 0.1799 |

### phase_shift_90

| Cycle | t (h) | chi_kappa | Amplitude | Cobb | S_lat |
|-------|-------|-----------|-----------|------|-------|
| 0 | 0.0 | 10.000 | 0.500 | 9.11 | 0.1713 |
| 4 | 8.0 | 5.670 | 0.500 | 15.31 | 0.1553 |
| 8 | 16.0 | 14.330 | 0.500 | 10.03 | 0.2031 |

### jetlagged

| Cycle | t (h) | chi_kappa | Amplitude | Cobb | S_lat |
|-------|-------|-----------|-----------|------|-------|
| 0 | 0.0 | 5.000 | 0.500 | 16.61 | 0.1549 |
| 4 | 8.0 | 12.500 | 0.500 | 8.51 | 0.1887 |
| 8 | 16.0 | 12.500 | 0.500 | 8.51 | 0.1887 |
| 0 | 0.0 | 5.000 | 0.500 | 8.37 | 0.0261 |
| 4 | 12.0 | 15.000 | 0.500 | 8.00 | 0.0293 |
| 0 | 0.0 | 5.000 | 0.500 | 8.37 | 0.0261 |
| 4 | 12.0 | 15.000 | 0.500 | 8.00 | 0.0293 |

### microgravity

| Cycle | t (h) | chi_kappa | Amplitude | Cobb | S_lat |
|-------|-------|-----------|-----------|------|-------|
| 0 | 0.0 | 15.000 | 0.500 | 12.90 | 0.1213 |
| 4 | 8.0 | 7.883 | 0.423 | 13.44 | 0.1140 |
| 8 | 16.0 | 8.208 | 0.358 | 13.18 | 0.1135 |

### microgravity_jetlag

| Cycle | t (h) | chi_kappa | Amplitude | Cobb | S_lat |
|-------|-------|-----------|-----------|------|-------|
| 0 | 0.0 | 5.000 | 0.500 | 16.23 | 0.1206 |
| 4 | 8.0 | 12.117 | 0.423 | 11.68 | 0.1138 |
| 8 | 16.0 | 11.792 | 0.358 | 11.67 | 0.1133 |

### constant_chi

| Cycle | t (h) | chi_kappa | Amplitude | Cobb | S_lat |
|-------|-------|-----------|-----------|------|-------|
| 0 | 0.0 | 10.000 | 0.000 | 9.11 | 0.1713 |
| 4 | 8.0 | 10.000 | 0.000 | 9.11 | 0.1713 |
| 8 | 16.0 | 10.000 | 0.000 | 9.11 | 0.1713 |

### high_chi_jetlag

| Cycle | t (h) | chi_kappa | Amplitude | Cobb | S_lat |
|-------|-------|-----------|-----------|------|-------|
| 0 | 0.0 | 10.000 | 0.500 | 9.11 | 0.1713 |
| 4 | 8.0 | 25.000 | 0.500 | 44.84 | 0.3303 |
| 8 | 16.0 | 25.000 | 0.500 | 44.84 | 0.3303 |

## Key Predictions

1. **Phase Coherence**: Entrained condition should show lowest Cobb angles
2. **Destructive Interference**: Jetlagged (phi=pi) should show highest Cobb angles
3. **Microgravity Drift**: Clock amplitude decays → progressive geometric error
4. **Critical Phase**: Scoliosis onset at phi > pi/2 (90 degrees of mismatch)
