# Evidence Note: Vestibular Gain Asymmetry as a Driver of Scoliosis

## Claim
Idiopathic Scoliosis represents a form of "Geometric Hallucination" where the spine curves to minimize prediction error relative to a tilted or noisy vestibular reference frame. This is driven by **Vestibular Gain Asymmetry** in the descending vestibulospinal tracts (specifically the Lateral Vestibulospinal Tract, LVST), which causes persistent asymmetric paraspinal muscle tone.

## Mechanism
1.  **Pathway**: The Vestibular Nuclei (VN) project to paraspinal muscles via the LVST to maintain antigravity tone.
2.  **Defect**: Pialasse et al. (2015) demonstrated that AIS adolescents exhibit significant asymmetry in Vestibular-Evoked Myogenic Potentials (VEMPs), specifically in the sternocleidomastoid (cervical VEMP) and triceps (limb VEMP). This implies a gain mismatch ($\gamma_L \neq \gamma_R$) in the descending command.
3.  **Active Inference**: In the "Biological Counter-Curvature" framework, the spine acts as an inverted pendulum stabilized by active control. If the "Global" vestibular gain is asymmetric, the "Local" proprioceptive loops will drift to a new setpoint (curvature) to zero out the "apparent" error, effectively locking the spine into a curve to satisfy the hallucinated gravity vector.

## Relevance to S-shaped Growth / Scoliosis
This mechanism explains why scoliosis progression is linked to growth: as the spinal column lengthens (increasing moment arm), the error signal from the gain mismatch is amplified. The system compensates by adding a geometric offset (curvature) to balance the torque equation, interpreting the gravitational moment as a "correction" rather than a defect. This aligns with the observation that scoliosis is an "upright" disease (Latimer 2005) dependent on the axial loading vector.

## Support
- **Pialasse et al. (2015)**: "Vestibulospinal function is altered in adolescents with idiopathic scoliosis."
- **Lambert et al. (2009)**: Demonstrates the conservation of these pathways from Xenopus to mammals.
- **H_2025_02_20_Active_Inference**: Previous hypothesis posited that sensory noise drives curvature; this note refines it to specific *Gain Asymmetry*.

## Open Question + Proposed Test
**Question**: Is the vestibular asymmetry primary (causal) or secondary to the spinal deformity (adaptation)?
**Proposed Test**:
- **Test**: Artificial induction of Vestibular Gain Asymmetry via unilateral optogenetic inhibition of the Lateral Vestibular Nucleus (LVN) in wild-type mice.
- **Prediction**: Unilateral inhibition will reduce descending extensor tone on one side, causing the spine to curve *away* from the inhibited side (or towards, depending on cross-over dynamics) to maintain center of mass balance, eventually fixing into a structural curve during growth.
