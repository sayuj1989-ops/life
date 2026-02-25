"""Proprioceptive Feedback Mechanism.

This module implements the "Proprioceptive Lag" hypothesis, which posits that
rapid growth during adolescence increases the neural transmission delay (tau propto L)
beyond the stability margin of the spinal postural control loop.

It provides a DelayedFeedbackTorques class that applies a correcting moment
based on the curvature state from a past time t - tau.
"""

from dataclasses import dataclass
from collections import deque
from typing import Optional, Tuple
import numpy as np

try:
    import elastica as ea
    PYELASTICA_AVAILABLE = True
except ImportError:
    PYELASTICA_AVAILABLE = False
    # Mock for type checking or simple fallback
    class ea:
        class NoForces:
            def apply_torques(self, system, time: float = 0.0): pass

@dataclass
class ProprioceptiveParams:
    """Parameters for the proprioceptive feedback loop.

    Attributes:
        delay: Time delay (tau) in seconds.
        gain: Proportional gain (Kp) in Nm/rad (actually Nm per unit curvature).
              Negative feedback implies Kp > 0 (restoring force).
              Torque M = -Kp * kappa(t - tau).
    """
    delay: float = 0.0
    gain: float = 0.0

class DelayedFeedbackTorques(ea.NoForces):
    """Applies a delayed proportional feedback torque based on curvature.

    Mechanism:
    1. Stores history of curvature kappa(t).
    2. At time t, retrieves kappa(t - delay).
    3. Computes restoring torque M = -gain * kappa(t - delay).
    4. Maps internal node curvature to element torques.
    """
    def __init__(self, params: ProprioceptiveParams, dt: float):
        super().__init__()
        self.params = params
        self.dt = dt

        # Buffer size: delay / dt
        # We need at least 1 step
        self.buffer_size = max(1, int(params.delay / dt)) if dt > 0 else 1

        # Circular buffer for history
        # Stores tuples (time, kappa_state)
        # kappa_state shape: (3, n_elems - 1)
        # Use a slightly larger buffer to ensure we cover the delay
        self.history = deque(maxlen=self.buffer_size + 10)

    def _get_delayed_kappa(self, current_time: float) -> Optional[np.ndarray]:
        """Retrieve kappa at time t - delay."""
        target_time = current_time - self.params.delay

        if target_time <= 0:
            # If requested time is before start, return straight (zero curvature)
            # or the earliest state if we want to be continuous.
            # Assuming straight initial condition is safer.
            return None

        # Find closest state in history
        # Deque is sorted by time (monotonic).
        # We want the value closest to target_time.

        best_kappa = None
        min_dt = float('inf')

        # Since we append new items to the right, old items are on the left.
        # Iterate from left (oldest) to find the match.
        for t, k in self.history:
            dt_val = abs(t - target_time)
            if dt_val < min_dt:
                min_dt = dt_val
                best_kappa = k
            else:
                # If error starts increasing, we've passed the optimal point
                # (since time is monotonic)
                break

        return best_kappa

    def apply_torques(self, system, time: float = 0.0):
        # 1. Record current state
        # system.kappa is (3, n_elems - 1). We must copy it.
        if hasattr(system, "kappa"):
            current_kappa = system.kappa.copy()
            self.history.append((time, current_kappa))
        else:
            return

        # 2. Retrieve delayed state
        delayed_kappa = self._get_delayed_kappa(time)

        if delayed_kappa is None:
            # No history yet (t < delay), assume straight (kappa=0) -> No torque
            return

        # 3. Compute Restoring Torque at Internal Nodes
        # Torque M = -gain * kappa
        # Gain can be scalar or array. Assuming scalar for now.
        # This opposes the curvature, trying to straighten the rod.
        torque_internal = -self.params.gain * delayed_kappa # (3, n_elems - 1)

        # 4. Map Internal Torques to Elements
        # Internal nodes are between elements.
        # element i has internal node i-1 (left) and i (right).
        # n_elems = N. internal nodes = N-1.
        # kappa[k] is at Voronoi domain k (between elem k and k+1).

        n_elems = system.n_elems
        torque_elem = np.zeros((3, n_elems))

        # Interior elements (1 to N-2)
        # elem k (where k=1..N-2) has neighbors kappa[k-1] and kappa[k]
        # Average the moment from the two adjacent voronoi domains
        torque_elem[:, 1:-1] = 0.5 * (torque_internal[:, :-1] + torque_internal[:, 1:])

        # Boundary elements
        # Elem 0: right neighbor is kappa[0].
        torque_elem[:, 0] = 0.5 * torque_internal[:, 0]

        # Elem N-1: left neighbor is kappa[N-2].
        torque_elem[:, -1] = 0.5 * torque_internal[:, -1]

        # 5. Apply
        system.external_torques += torque_elem
