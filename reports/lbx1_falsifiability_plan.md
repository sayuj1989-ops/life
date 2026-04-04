# LBX1 Falsifiability Plan

**Date:** 2026-04-04

## Overview
LBX1 has been proposed as a key player in the Biological Countercurvature hypothesis. However, structural analysis indicates low confidence (mean pLDDT 66.9) and only moderate anisotropy (2.27), suggesting its apparent "blockiness" or structural properties may be artifacts of intrinsically disordered regions rather than a true mechanosensory architecture. This document outlines three concrete experiments to definitively falsify the hypothesis that LBX1 acts as a direct, structural mechanosensor.

## Experiment 1: The Conformational Rigidity Assay
**Hypothesis:** If LBX1 functions as a rigid mechanosensor or structural scaffold linking mechanical cues to transcription, its conformation should remain relatively stable and its anisotropy functionally relevant under physiological conditions.
**Assay Design:** Small Angle X-ray Scattering (SAXS) or FRET on purified full-length LBX1 in solution under varying osmotic pressures (mimicking crowding/compression).
**Quantitative Readout:** Radius of gyration ($R_g$) and maximum particle dimension ($D_{max}$) via SAXS; FRET efficiency between terminal tags.
**Expected Direction:** If it acts as a rigid sensor, $R_g$ and $D_{max}$ should remain stable or change predictably with pressure.
**Falsification Threshold:** If LBX1 is highly polymorphic, shows a random coil signature in SAXS, or FRET efficiency indicates extreme structural plasticity lacking a defined stable state, the claim that it operates as a rigid, anisotropic mechanosensor is falsified.

## Experiment 2: Tension-Dependent Nuclear Localization
**Hypothesis:** If LBX1 relays mechanical tension, its nuclear localization or retention should depend on cytoskeletal tension (similar to YAP/TAZ).
**Assay Design:** Culture human myoblasts on substrates of varying stiffness (e.g., 2 kPa vs 50 kPa) or treat with Blebbistatin to abolish cytoskeletal tension.
**Quantitative Readout:** Nuclear/Cytoplasmic ratio of LBX1 via immunofluorescence.
**Expected Direction:** If mechanically linked, nuclear localization should decrease on soft substrates or upon tension ablation.
**Falsification Threshold:** If the LBX1 Nuclear/Cytoplasmic ratio remains constant (variation < 10%) across stiffness gradients and Blebbistatin treatment, it is not tension-gated.

## Experiment 3: Deletion of Predicted Disordered Regions
**Hypothesis:** The low-pLDDT regions of LBX1 are functional sensors requiring specific extended conformations, rather than generic flexible linkers.
**Assay Design:** Create LBX1 mutants with the low-confidence regions (pLDDT < 70) deleted or replaced with an idealized flexible linker (e.g., (Gly-Ser)n) of equal length. Assess downstream transcriptional activity (e.g., via a reporter assay for known LBX1 targets).
**Quantitative Readout:** Relative luciferase activity or target gene mRNA levels (qRT-PCR) compared to wild-type LBX1.
**Expected Direction:** Deletion/replacement should abolish mechanosensitive transcriptional changes.
**Falsification Threshold:** If the (Gly-Ser)n linker mutant fully rescues or maintains wild-type target gene expression patterns under mechanical load, the specific sequence and hypothesized extended architecture of those regions are irrelevant, pointing to a standard flexible tether rather than a specialized mechanosensor.
