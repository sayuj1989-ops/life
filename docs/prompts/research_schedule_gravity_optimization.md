# AI Prompt: Research Schedule for "Gravity as an Optimization Process"

**Role:** You are a Principal Investigator in Theoretical Biology and Biomechanics, specializing in the physics of morphogenesis. You are proficient in both computational modeling (Python, PyElastica) and experimental design (mechanobiology).

**Context:**
We have established a theoretical framework where spinal alignment is viewed as a **Gradient Descent Optimization process**.
*   **The Cost Function ($U_{CC}$):** The organism minimizes the Total Potential Energy (Gravity + Elasticity - Information).
*   **The Gradient:** Mechanosensors (PIEZO2) detect the error between the current shape and the genetic "Reference Metric".
*   **The Optimizer:** The system updates shape via Differential Growth (Slow) and Muscle Tone (Fast).
*   **The Learning Rate Scheduler:** The Circadian Clock (BMAL1) modulates the sensitivity of the tissue to mechanical signals ("Spinal Jetlag" hypothesis).
*   **The Failure Mode:** Scoliosis is a "Local Minimum" or "Exploding Gradient" caused by sensory noise or feedback delays.

**Objective:**
Create a detailed **12-Week Research Schedule** to test and validate this "Gradient Descent" hypothesis, specifically focusing on the integration of **Gravity Theories** (The Bio-Gravitational Number $\mathcal{B}_g$ and Spinal Jetlag).

**Requirements:**

1.  **Structure:** Divide the schedule into three 4-week phases:
    *   **Phase 1: Computational Proof-of-Concept.** Focus on `PyElastica` simulations, defining the "Cost Function" explicitly, and simulating "Optimization Failure" (Scoliosis).
    *   **Phase 2: The "Spinal Jetlag" Simulation.** Integrate a time-dependent "Learning Rate" (Circadian Clock) into the model. What happens if the clock desynchronizes from the gravity vector?
    *   **Phase 3: Experimental Validation Design.** Outline specific wet-lab experiments (e.g., "Test T_Clock") to validate the computational predictions.

2.  **Key Theoretical Integrations:**
    *   **The Bio-Gravitational Number ($\mathcal{B}_g$):** Ensure the schedule includes a task to calculate this dimensionless number for different species/conditions.
    *   **Vector-Scalar Mismatch:** Design a simulation scenario where the "Scalar" signal (pressure) is high but the "Vector" signal (gravity) is zero (Microgravity).

3.  **Deliverables:** For each week, specify:
    *   **Focus:** The main topic.
    *   **Task:** Specific code to write or experiment to design.
    *   **Hypothesis:** What specific theoretical component is being tested.

4.  **Tone:** rigorously scientific, ambitious, yet operationally grounded in the current codebase (referencing `pyelastica_bridge.py`, `formalism_01.md`).

**Output Format:**
Please provide the response as a Markdown document with a summary, the 12-week schedule table, and a "Risk Assessment" section for potential theoretical bottlenecks.
