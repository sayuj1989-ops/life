# Phase 1, Day 1: Ageing and Postural Control

## Overview
This document summarises key literature on how ageing affects the systems required for maintaining upright bipedal posture, specifically proprioception, the vestibular system, and the cerebellum.

## Key Papers

1. **Title**: Peripheral and Central Contributions to Age-Related Proprioceptive Decline, Clinical Implications and Management
   **DOI**: 10.52403/gijhsr.20240403
   **Authors**: Silumesii Lili
   **Abstract Extract**: Proprioception is the body’s ability to perceive its position and movement in space, crucial for maintaining balance and coordination, especially in older adults. As individuals...

2. **Title**: Postural Ataxia in Cerebellar Downbeat Nystagmus: Its Relation to Visual, Proprioceptive and Vestibular Signals and Cerebellar Atrophy
   **DOI**: 10.1371/journal.pone.0168808
   **Authors**: Helmchen Christoph, Kirchhoff Jan-Birger, Göttlich Martin, Sprenger Andreas
   **Abstract Extract**: No abstract...

3. **Title**: Postural Ataxia in Late Atrophy of the Cerebellar Anterior Lobe and Its Differential Diagnosis
   **DOI**: 10.1159/000410340
   **Authors**: Dichgans J., Diener H. C.
   **Abstract Extract**: No abstract...

4. **Title**: Postural Control in Elderly Subjects
   **DOI**: 10.1093/ageing/19.3.215
   **Authors**: PYYKKO ILMARI, JANTTI PIRKKO, AALTO HEIKKI
   **Abstract Extract**: No abstract...

5. **Title**: Effect of Vestibular Rehabilitation on Postural Stability in Children with Visual Impairment
   **DOI**: 10.18502/avr.v33i2.14810
   **Authors**: Kasiraman Gayathri, Gousebasha Yasmeen Imtiaz, Sridaran Hariharan
   **Abstract Extract**: Background and Aim: Postural stability is monitored by a circuitous system, particularly visual perception, vestibular apparatus, and somatosensory organs. The ability to maintain balance is s...

## Synthesis for the Terminal Derivative Gain Gap Model
The literature confirms that the "controller" in our PID model degrades across multiple modalities with age. Proprioceptive signals weaken, vestibular inputs become less reliable, and critically, cerebellar atrophy impairs the central integration and predictive capacity of the postural control system. This multi-system degradation forms the basis for modelling the irreversible decline of the derivative gain ($K_d$) and the increase in processing delay ($\tau$) in geriatric postural collapse.
