# Spinal Jetlag Validation Results

This document summarizes the parameter estimates and experimental protocols derived from the theoretical framework to validate the "Spinal Jetlag" hypothesis of Adolescent Idiopathic Scoliosis (AIS).

## 1. Parameter Estimation (Biological Grounding)

The simulation relies on mapping abstract variables to physiological realities. Based on literature, we constrain the model with the following parameters:

*   **Proprioceptive Delay ($\tau$):**
    *   Determined by the conduction velocity of Ia afferents ($v_{nerve}$) and synaptic delays in the spinal cord and cortex.
    *   *Target Range:* $\tau \approx 40-100$ ms.
*   **Spinal Stiffness ($B$):**
    *   Represented by the flexural rigidity ($EI$) of the adolescent spine.
    *   *Target Range:* $EI \approx 1-5$ Nm$^2$.
*   **Growth Velocity ($\dot{L}$):**
    *   The Peak Height Velocity during the adolescent growth spurt.
    *   *Target Range:* $\sim 8-12$ cm/year.
*   **Circadian Phase Shift ($\Delta \phi$):**
    *   The magnitude of left-right asymmetry in clock gene expression (e.g., Per2/Bmal1) in bilateral tissues like somites.
    *   *Target:* A 1-hour phase shift is physically plausible and theoretically sufficient to induce torsional pre-stress.

## 2. Experimental Protocol Design (The "Wet Lab" Plan)

To physically falsify or validate the control theory instability mechanism, we propose the following "Smoking Gun" experiments:

### Protocol A: The "Cooled Ganglion" (Rat Model)

*   **Hypothesis:** Artificially increasing the neural delay $\tau$ in a slow-growing animal will induce a control instability, causing spontaneous scoliosis.
*   **Method:**
    1.  Design a minimal implantable cooling loop (Peltier or microfluidic) targeting the L1-L5 Dorsal Root Ganglia (DRGs).
    2.  Target temperature: 15°C (this slows conduction velocity by approximately 50%).
    3.  Control: Implant the device without active cooling.
    4.  Timeline: Apply cooling for 4 hours/day during peak growth (weeks 4-8).
    5.  Observe for the emergence of a 3D scoliotic curve.

### Protocol B: The "Jetlagged" Zebrafish

*   **Hypothesis:** Asymmetric circadian entrainment between the left and right sides of the body introduces a phase shift $\Delta \phi$, generating torsional pre-stress that converts planar buckling into 3D helical scoliosis.
*   **Method:**
    1.  Use a `Tg(per2:luc)` reporter zebrafish line to visually monitor the clock phase in vivo.
    2.  Chamber Design: Utilize split-tank illumination.
        *   Left side: LD 12:12 (Phase 0).
        *   Right side: LD 12:12 (Phase +4h).
    3.  Confocal Imaging: Measure the vertebral aspect ratio and rotation weekly to track the development of structural torsion.
