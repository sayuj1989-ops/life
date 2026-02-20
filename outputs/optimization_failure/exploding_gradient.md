# Optimization Failure: Exploding Gradient Report

**Date:** 2026-02-20 21:15:56
**Source:** `exploding_gradient.csv`

## Hypothesis

Scoliosis emerges as an 'Exploding Gradient' when the learning rate
(chi_kappa) exceeds structural damping AND sensory noise degrades
gradient fidelity below a critical threshold.

## Mean Cobb Angle by (chi_kappa, sigma_noise)

| chi_kappa | sigma_noise | mean_Cobb | std_Cobb | n_scoliotic |
|-----------|-------------|-----------|----------|-------------|
| 0.00 | 0.000 | 6.92 | 0.00 | 0/8 |
| 0.00 | 0.500 | 6.92 | 0.00 | 0/8 |
| 0.00 | 1.000 | 6.92 | 0.00 | 0/8 |
| 10.00 | 0.000 | 6.99 | 0.00 | 0/8 |
| 10.00 | 0.500 | 7.05 | 0.03 | 0/8 |
| 10.00 | 1.000 | 6.83 | 0.17 | 0/8 |
| 20.00 | 0.000 | 7.18 | 0.00 | 0/8 |
| 20.00 | 0.500 | 6.88 | 0.52 | 0/8 |
| 20.00 | 1.000 | 6.22 | 0.37 | 0/8 |

## Critical Noise Threshold

sigma_c is the noise level at which mean Cobb angle first exceeds 10 degrees.

- chi_kappa = 0.00: no scoliosis onset detected
- chi_kappa = 10.00: no scoliosis onset detected
- chi_kappa = 20.00: no scoliosis onset detected

## Cost Function U_CC Analysis

| chi_kappa | sigma_noise | U_CC (mean) | U_info (mean) | info_gain_ratio |
|-----------|-------------|-------------|---------------|------------------|
| 0.00 | 0.000 | 0.3837 | 0.0000 | 0.0000 |
| 0.00 | 0.500 | 0.3837 | 0.0000 | 0.0000 |
| 0.00 | 1.000 | 0.3837 | 0.0000 | 0.0000 |
| 10.00 | 0.000 | -0.0226 | 0.6657 | 1.0352 |
| 10.00 | 0.500 | -0.0489 | 0.7041 | 1.0730 |
| 10.00 | 1.000 | -0.1179 | 0.8187 | 1.1684 |
| 20.00 | 0.000 | -1.1583 | 2.4353 | 1.9070 |
| 20.00 | 0.500 | -1.1773 | 2.6171 | 1.8230 |
| 20.00 | 1.000 | -1.6315 | 3.3590 | 1.9413 |
