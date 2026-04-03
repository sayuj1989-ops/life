# Phase 1, Day 2: Active Inference and Motor Control

## Overview
This literature review note explores how the free-energy principle (FEP) explains movement, posture, and reflexes, focusing on active inference for motor control.

## Key Papers
- **Adams et al. (2013) "Predictions not commands: active inference in the motor system"** (DOI: 10.1007/s00429-012-0475-5)
- **Baltieri & Buckley (2019) "Active Inference: Computational Models of Motor Control without Efference Copy"** (DOI: 10.32470/ccn.2019.1144-0)

## The Core Concept: Predictions, not Commands
In classical motor control models (including Paper 2's engineering PID), the brain sends a motor command to muscles. Active inference completely inverts this: the brain does not issue motor commands. Instead, it issues *proprioceptive predictions*.

The motor system minimizes prediction errors by *acting on the world* (via classic reflex arcs) to make the sensory input match the prediction. Thus, descending signals from the motor cortex are not forces or torques; they are the desired sensory states.

## The Equilibrium-Point Hypothesis as Active Inference
This framework naturally subsumes the "equilibrium-point hypothesis" (EPH) of motor control. In EPH, the brain specifies an equilibrium position for a limb, and the viscoelastic properties of the muscles (springs and dampers) move the limb to that position.
Under active inference, this equilibrium point is simply the prior expectation (the prediction). Peripheral reflexes act to minimize the mismatch between the actual length of the muscle spindle and the expected length, driving the system to the equilibrium point.

## Relevance to Adolescent Idiopathic Scoliosis (AIS)
1. **Postural Control:** In our framework, upright posture is an expected state. The brain continuously predicts a symmetric, upright alignment.
2. **Growth-induced Misspecification:** When the spine grows rapidly, the physical geometry (the "plant") changes faster than the internal generative model.
3. **Reflex Arc Miscalibration:** The proprioceptive predictions sent to the spinal circuits become systematically mismatched with the new physical reality, analogous to the K_d gain degradation in Paper 2.

## Conclusion for Paper 5
To frame the "derivative gain gap" in active inference terms, we must model how the generative model struggles to update its predictions of generalized coordinates (specifically velocity/acceleration) during rapid structural changes. When predictions of velocity become unreliable, precision weighting must be reduced, mapping perfectly to the drop in K_d.
