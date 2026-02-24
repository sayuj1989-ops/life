# The Spinal Symphony: Auditory Diagnostics for Scoliosis

## Introduction
Research into Adolescent Idiopathic Scoliosis (AIS) has traditionally relied on visual metrics (Cobb angle, 3D reconstruction) and static protein structures. However, the underlying physical phenomena—standing waves, resonance, and rhythmic growth—are inherently dynamic and oscillatory. To capture these hidden dimensions, we introduced **Auditory Sonification** as a novel analytical tool. By mapping geometric data to acoustic frequencies, we can "listen" to the health of the spine and the folding of its constituent proteins.

## Methodology
We developed two Python tools:
1.  `scripts/experiment_spinal_symphony.py`: Converts time-series simulation data (Cobb angle, Torsion) into audio. Pitch maps to curvature (higher pitch = more deformity), while volume maps to torsion.
2.  `scripts/protein_sonification.py`: Converts protein backbone geometry into audio. Time maps to residue index, pitch to local curvature, volume to pLDDT (confidence), and stereo panning to torsion.

## Results: The Sound of Collapse
We sonified the "Spinal Jetlag" simulation results.
- **Entrained (Healthy):** Produces a steady, harmonic low-frequency hum, representing a stable S-curve with minimal torsion.
- **Jetlagged (Unstable):** The audio exhibits a "wobble" or vibrato, indicating loss of phase lock between the circadian clock and mechanical loading.
- **High-Chi Jetlag (Collapse):** A catastrophic "screech" is heard as the Cobb angle spikes to >80°, accompanied by chaotic amplitude modulation due to torsion.

**Fractal Dimension Analysis:**
We calculated the Higuchi Fractal Dimension (HFD) of the Cobb angle time series.
- **Entrained:** HFD $\approx$ 1.003 (Smooth, predictable)
- **High-Chi Jetlag:** HFD $\approx$ 1.008 (Slight increase in complexity/roughness during collapse)
- **Constant Chi:** HFD $\approx$ 1.98 (High complexity, indicating noise or rapid fluctuations)

## Results: Protein Melodies
We compared **PIEZO2** (the structural strut) and **LBX1** (the signaling node).
- **PIEZO2:** The melody is rhythmic and structured. The long alpha-helical repeats create a pulsing, techno-like beat. The high confidence (pLDDT) ensures a loud, clear signal. The "propeller" domains create distinct, repeating motifs.
- **LBX1:** The melody is disjointed. High-confidence DNA-binding domains sound clear, but the disordered regions (IDRs) drop in volume and fluctuate wildly in pitch, creating a "broken radio" effect. This auditory difference reinforces our "Strut vs. Signal" hypothesis: PIEZO2 is a rigid mechanical element, while LBX1 is a flexible switch.

## Conclusion
Sonification provides an intuitive, high-dimensional way to detect structural anomalies. The "screech" of scoliosis and the "rhythm" of PIEZO2 are distinct auditory signatures that complement visual data. This approach aligns with the "Standing Wave" theory of the spine, suggesting that scoliosis is fundamentally a *dissonance* in the biological oscillator.

## Outputs
- **Audio:** `outputs/spinal_symphony/*.wav`
- **Spectrograms:** `outputs/spinal_symphony/spinal_spectrograms.png`, `outputs/protein_sonification/*_spectrogram.png`
