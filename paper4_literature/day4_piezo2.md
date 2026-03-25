# Day 4: PIEZO2 Deep Dive

## Introduction
PIEZO2 is the primary mechanotransduction ion channel responsible for proprioception and light touch in mammals. It is abundantly expressed in the primary sensory endings of muscle spindles and Golgi tendon organs.

## Role in Mechanotransduction
PIEZO2 forms a massive, three-bladed propeller-like homotrimer in the plasma membrane. Mechanical tension on the membrane pulls the blades, flattening the dome-like structure and opening the central pore.
- **Kinetics**: PIEZO2 opens within microseconds of mechanical stimulation, but it also rapidly inactivates (time constant $\sim$ 5-30 ms). This rapid adaptation is crucial for encoding dynamic changes in muscle length (velocity), which corresponds to the derivative gain ($K_d$) in our control model.
- **Knockout Phenotype**: Humans with loss-of-function PIEZO2 mutations exhibit profound proprioceptive deficits, sensory ataxia, and severe progressive scoliosis (Chesler et al., 2016, NEJM). This provides the most direct link between proprioception and spinal deformity. (See also Woo et al., 2015, DOI: 10.1038/nn.4162).

## Hypothesis for AIS
While complete loss of PIEZO2 is devastating and rare, common functional variants (or variants altering splice isoforms, e.g., Szczot et al., 2018, DOI: 10.1016/j.bpj.2017.11.663) may subtly alter channel kinetics.
If a variant increases the activation time constant (slower opening) or decreases mechanosensitivity (requiring more stretch to open), it will explicitly increase the peripheral transduction delay $\tau_{transduction}$.
Furthermore, if inactivation kinetics are altered, the channel's ability to encode high-frequency velocity signals ($K_d$) is impaired, exacerbating the Derivative Gain Gap.

## Synthesis for Model
$\tau_{transduction}$ is the very first component of the total delay. While its absolute duration is short (1-3 ms), a delay here shifts the entire signal processing cascade. In a rapidly growing adolescent, a delayed PIEZO2 response ($\tau_{transduction}$ increase), combined with slower afferent conduction ($\tau_{afferent}$ increase from GPR126 variants), cumulatively pushes the total $\tau$ past the $\sim$200 ms instability threshold.
