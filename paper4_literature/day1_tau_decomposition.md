# Phase 1, Day 1: Decomposition of Proprioceptive Delay ($\tau$)

The macroscopic proprioceptive delay parameter $\tau$ from the inverted pendulum control model in Paper 2 is approximately 200 ms in human standing (parameter derived from Peterka's models of postural control). To link this control-theoretic parameter to molecular genetics, $\tau$ must be decomposed into its serial physiological sub-components:

1. **Peripheral Transduction Delay ($\tau_{trans}$):** The time required for mechanical deformation of the muscle spindle to open mechanosensitive ion channels (e.g., Piezo2) and generate a receptor potential.
   * *Typical duration:* ~1-2 ms.
2. **Afferent Conduction Delay ($\tau_{aff}$):** The time for action potentials to travel along Group Ia/II afferent fibers from the paraspinal muscles to the dorsal horn of the spinal cord. This is heavily dependent on axon diameter and myelination quality.
   * *Typical duration:* ~10-15 ms (assuming 60-120 m/s conduction velocity over ~1 meter).
3. **Spinal Relay Delay ($\tau_{spin}$):** Synaptic processing time within the spinal cord (e.g., Clarke's column) before ascending via the spinocerebellar tracts.
   * *Typical duration:* ~2-5 ms.
4. **Cerebellar Processing Delay ($\tau_{cer}$):** Integration and forward model processing within the cerebellum and supraspinal centers.
   * *Typical duration:* ~50-80 ms.
5. **Efferent Conduction Delay ($\tau_{eff}$):** Conduction of the descending motor command via corticospinal and vestibulospinal tracts to the alpha motor neurons.
   * *Typical duration:* ~15-20 ms.
6. **Neuromuscular Junction (NMJ) Delay ($\tau_{nmj}$):** Synaptic transmission delay at the motor endplate.
   * *Typical duration:* ~1 ms.
7. **Electromechanical Delay ($\tau_{em}$):** The time between the onset of muscle electrical activity (EMG) and the measurable onset of force production (excitation-contraction coupling and stretching of the series elastic component).
   * *Typical duration:* ~30-50 ms.

**Budget:** $\tau_{total} = \tau_{trans} + \tau_{aff} + \tau_{spin} + \tau_{cer} + \tau_{eff} + \tau_{nmj} + \tau_{em} \approx 150-200\text{ ms}$.

Each of these components represents a vulnerability in the control loop. If a genetic variant compromises the efficiency of any single component, the total delay $\tau_{total}$ will increase, potentially crossing the critical threshold during the adolescent growth spurt as modeled in Paper 2.

## References

```bibtex
@inproceedings{Heenan_2011,
  title={Visual and proprioceptive contributions to compensatory and pursuit tracking movements in humans},
  url={http://dx.doi.org/10.1109/iembs.2011.6091839},
  DOI={10.1109/iembs.2011.6091839},
  booktitle={2011 Annual International Conference of the IEEE Engineering in Medicine and Biology Society},
  publisher={IEEE},
  author={Heenan, M. L. and Scheidt, R. A. and Beardsley, S. A.},
  year={2011},
  month=aug,
  pages={7356–7359}
}

@article{Heenan_2014,
  title={Intention tremor and deficits of sensory feedback control in multiple sclerosis: a pilot study},
  volume={11},
  ISSN={1743-0003},
  url={http://dx.doi.org/10.1186/1743-0003-11-170},
  DOI={10.1186/1743-0003-11-170},
  number={1},
  journal={Journal of NeuroEngineering and Rehabilitation},
  publisher={Springer Science and Business Media LLC},
  author={Heenan, Megan and Scheidt, Robert A and Woo, Douglas and Beardsley, Scott A},
  year={2014},
  month=dec
}

@article{Kr_ger_2025,
  title={Experimental physiology Special Issue: ‘Mechanotransduction, muscle spindles and proprioception’},
  volume={110},
  ISSN={1469-445X},
  url={http://dx.doi.org/10.1113/ep093067},
  DOI={10.1113/ep093067},
  number={10},
  journal={Experimental Physiology},
  publisher={Wiley},
  author={Kröger, Stephan},
  year={2025},
  month=jul,
  pages={1383–1388}
}
```
