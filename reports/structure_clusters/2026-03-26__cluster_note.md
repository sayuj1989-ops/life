# Cluster Analysis Report: Cilia Scaffold and Mechanotransduction

**Date**: 2026-03-26

## Cluster Members
- **IFT88** (Representative Member)

## Shared Properties
Based on K-means clustering of AlphaFold-derived structural metrics, Cluster 4 is uniquely characterized by:
- **Anisotropy Index**: 7.86 (Moderately high, indicating an elongated or rod-like structure).
- **Elongation**: 2.61.
- **Predicted Domain Segments**: 3.00.
- **pLDDT Mean**: 76.35 (Good confidence).
- **Disorder Fraction Proxy**: 0.23.
- **Top Pathways Enriched**: Cilia (1), Mechanotransduction (1).

## Hypothesized Mechanical Role
Given the high anisotropy and elongation, combined with the pathway enrichment for Cilia and Mechanotransduction, it is hypothesized that **IFT88** acts as a critical **cilia scaffold** and **flow sensor**. The elongated structure suggests it forms a structural 'backbone' or 'tension rod' within the primary cilium, transmitting mechanical forces (like fluid shear stress or gravity-induced bending) directly to the base of the cilium to trigger downstream mechanotransduction signaling pathways.

## Concrete Test
**Hypothesis**: If IFT88 provides the essential structural anisotropy required for primary cilia to act as flow/gravity sensors, then its depletion will result in a loss of directional mechanosensing without necessarily abolishing the cilium completely.

**Experiment**: Perform siRNA knockdown of IFT88 in patient-derived or wild-type osteoblasts cultured in a parallel-plate flow chamber.
- **Readout**: Measure the realignment of the actin cytoskeleton and the directional migration of the cells in response to bidirectional fluid flow.
- **Expected Result**: IFT88-depleted cells will fail to orient themselves or migrate against the fluid flow compared to control cells, demonstrating a loss of directional mechanosensing.
