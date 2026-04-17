# WP8 — Managed Agent Output

# WP8 — Active Inference Simulation: The Allometric Trap as Precision Collapse

## Part I: Mathematical Derivation

### 1.1 Background and Grounding Literature

The connection between PID control and Active Inference was established by Baltieri & Buckley (2019), who showed that under linear Gaussian generative models, gradient descent on variational free energy recovers PID control laws exactly. We extend this to the **delayed, time-varying** case relevant to adolescent spinal growth.

> Baltieri M, Buckley CL. "PID control as a process of active inference with linear generative models." *Entropy* 2019;21(3):257. DOI: [10.3390/e21030257](https://doi.org/10.3390/e21030257)

> Friston KJ, et al. "Generalised filtering." *Mathematical Problems in Engineering* 2010. DOI: [10.1155/2010/621670](https://doi.org/10.1155/2010/621670)

> Friston KJ. "A free energy principle for a particular physics." *arXiv* 2019. arXiv:1906.10184

---

### 1.2 Generative Model for the Delayed Inverted Pendulum

Consider a spine modeled as an inverted pendulum with time-varying effective length L(t) (height of center of mass above S1). The **true plant dynamics** are:

$$\ddot{\theta} = \frac{g}{L(t)}\sin\theta - \frac{b}{mL(t)^2}\dot{\theta} + \frac{u(t-\tau)}{mL(t)^2}$$

where:
- $\theta$: trunk tilt angle
- $g = 9.81$ m s⁻²
- $b$: viscous damping
- $m$: effective mass
- $u$: paraspinal muscle torque (the action)
- $\tau \approx 50\text{–}100$ ms: proprioceptive delay

The agent maintains **generalized states** $\tilde{\mu} = (\mu, \mu', \mu'')$ — beliefs about position, velocity, and acceleration — and observes delayed proprioception $\tilde{y}(t) = \theta(t - \tau)$ plus vestibular/visual signals with noise.

---

### 1.3 Free Energy Formulation

The **variational free energy** under a Gaussian generative model is:

$$F = \underbrace{\frac{1}{2}\sum_i \Pi_{y,i} \varepsilon_{y,i}^2}_{\text{sensory PE}} + \underbrace{\frac{1}{2}\sum_i \Pi_{v,i} \varepsilon_{v,i}^2}_{\text{dynamic PE}} - \frac{1}{2}\ln|\Pi|$$

where:
- $\varepsilon_{y,0} = \tilde{y} - g(\mu)$: **position** prediction error (PE)
- $\varepsilon_{y,1} = \dot{\tilde{y}} - g'(\mu)\mu'$: **velocity** prediction error (PE)
- $\Pi_{y,0}, \Pi_{y,1}$: sensory precisions for position and velocity channels
- $\varepsilon_{v,i}$: dynamic (process) PEs from the equations of motion

For **linear** $g(\mu) \approx \mu$ (small angle), the free energy gradient recovers:

$$u = -\Pi_{y,0}\varepsilon_{y,0} - \Pi_{y,1}\varepsilon_{y,1} - \Pi_{y,2}\varepsilon_{y,2}$$

This is precisely PID with:

$$\boxed{K_p = \Pi_{y,0}, \quad K_d = \Pi_{y,1}, \quad K_i \propto \Pi_{y,2}}$$

---

### 1.4 Precision Dynamics and the Allometric Trap Mechanism

Precision is not fixed — it is learned online via **hyperparameter optimization** (the M-step in the predictive coding literature). The update rule is:

$$\dot{\Pi}_{y,1} = -\kappa\left[\Pi_{y,1} - \frac{1}{\hat{\sigma}^2_{\varepsilon_{y,1}}}\right]$$

where $\hat{\sigma}^2_{\varepsilon_{y,1}}$ is the running variance of velocity PEs, and $\kappa$ is the learning rate.

> Mathys CD, et al. "A Bayesian foundation for individual learning under uncertainty." *Frontiers in Human Neuroscience* 2011;5:39. DOI: [10.3389/fnhum.2011.00039](https://doi.org/10.3389/fnhum.2011.00039)

During a **growth spurt**, $L(t)$ increases rapidly. The agent's internal model has $L_{\text{model}}$ = constant (or slowly updated), so the plant's eigenfrequency $\omega_0 = \sqrt{g/L}$ changes faster than the model can track. This causes **systematic velocity PE accumulation**:

$$\varepsilon_{y,1} \approx \dot{\theta} - \hat{\dot{\theta}} \sim \Delta\omega_0 \cdot \theta \cdot \Delta t_{\text{growth}}$$

As $\hat{\sigma}^2_{\varepsilon_{y,1}}$ rises, $\Pi_{y,1} = K_d^{\text{eff}}$ falls.

---

### 1.5 Hopf Bifurcation Condition

For a delayed proportional-derivative controller on an inverted pendulum, the stability boundary (from characteristic equation analysis) requires:

$$K_d > K_d^{\text{crit}}(L, \tau) = \frac{m g L \tau}{1 - K_p \tau}$$

(valid for $K_p \tau < 1$). See:

> Insperger T, Stepan G. "Semi-discretization for time-delay systems." *Springer* 2011. DOI: [10.1007/978-1-4614-0335-7](https://doi.org/10.1007/978-1-4614-0335-7)

> Peterka RJ. "Sensorimotor integration in human postural control." *J Neurophysiol* 2002;88(3):1097–1118. PMID: [12205132](https://pubmed.ncbi.nlm.nih.gov/12205132/)

The **Allometric Trap** occurs when both:
1. $L(t)$ increases (raising $K_d^{\text{crit}}$), AND
2. $\Pi_{y,1}(t) = K_d^{\text{eff}}$ decreases (via precision collapse)

converge simultaneously, so $K_d^{\text{eff}} < K_d^{\text{crit}}$. The system crosses a Hopf bifurcation; oscillations grow and the spine buckles laterally.

---

### 1.6 Differential Equations for the Active Inference Agent

**State equations (true plant):**

$$\dot{\theta} = \omega$$
$$\dot{\omega} = \frac{g}{L(t)}\theta - \frac{b}{mL(t)^2}\omega + \frac{u_{\text{delayed}}}{mL(t)^2} + \sigma_w \xi_w$$

**Belief updating (gradient descent on F, generalized coordinates):**

$$\dot{\mu} = \mu' - \kappa_\mu \Pi_{y,0}(\mu - y_\tau)$$
$$\dot{\mu}' = \mu'' - \kappa_\mu \Pi_{y,1}(\mu' - \dot{y}_\tau)$$
$$\dot{\mu}'' = f(\mu, \mu'; L_m) - \kappa_\mu \Pi_{v,0}\varepsilon_v$$

where $f(\mu,\mu';L_m) = \frac{g}{L_m}\mu$ is the model's predicted acceleration, $L_m$ is the **model's** (possibly outdated) estimate of pendulum length, and $y_\tau = \theta(t-\tau)$.

**Action (muscle torque):**

$$u(t) = -\Pi_{y,0}\mu - \Pi_{y,1}\mu' - \Pi_{y,2}\int_0^t \mu \, ds'$$

**Precision updating:**

$$\dot{\Pi}_{y,1} = -\kappa_\Pi\left[\Pi_{y,1} - \frac{\Pi_{y,1,0}}{1 + \alpha \cdot \text{RunVar}(\varepsilon_{y,1})}\right]$$

where $\Pi_{y,1,0}$ is the prior precision, $\alpha$ scales the sensitivity, and $\text{RunVar}$ is a running variance estimate updated as:

$$\dot{V}_\varepsilon = \gamma({\varepsilon_{y,1}^2 - V_\varepsilon})$$

---

## Part II: Python Simulation

```python
#!/usr/bin/env python3
"""
active_inference_buckling.py
=============================
Simulates the "Allometric Trap" as a precision-collapse Hopf bifurcation
within an Active Inference (Free Energy Minimization) framework.

Theory:
  - Spine modelled as an inverted pendulum with time-varying height L(t).
  - Active Inference agent performs gradient descent on variational free
    energy; under linear Gaussian assumptions this recovers PID control
    with gains determined by sensory precisions (Baltieri & Buckley 2019).
  - During a growth spurt L(t) increases faster than the agent's internal
    model updates, causing systematic velocity prediction errors.
  - Rising PE variance drives dynamic precision Pi_y1 downward.
  - Pi_y1 maps to effective derivative gain Kd_eff.
  - When Kd_eff drops below the critical threshold Kd_crit(L, tau),
    the system crosses a Hopf bifurcation and the pendulum buckles.

Key references:
  Baltieri & Buckley (2019) Entropy 21:257. DOI:10.3390/e21030257
  Friston et al. (2010) Math Prob Eng. DOI:10.1155/2010/621670
  Insperger & Stepan (2011) Springer. DOI:10.1007/978-1-4614-0335-7
  Peterka (2002) J Neurophysiol 88:1097. PMID:12205132
  Mathys et al. (2011) Front Hum Neurosci 5:39. DOI:10.3389/fnhum.2011.00039

Author: Senior Computational Biophysicist (WP8, Allometric Trap manuscript)
Date:   2025
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import interp1d
from collections import deque

# =============================================================================
# SECTION 1 — PHYSICAL & CONTROL PARAMETERS
# =============================================================================

# ---- Simulation time --------------------------------------------------------
DT          = 0.005          # integration time step [s]  (5 ms)
T_START     = 0.0            # [s]
T_END       = 60.0           # [s]  covers pre-growth, growth, post-growth
N_STEPS     = int((T_END - T_START) / DT)
TIME        = np.linspace(T_START, T_END, N_STEPS)

# ---- Physical constants ------------------------------------------------------
G           = 9.81           # gravitational acceleration [m s^-2]
M           = 40.0           # effective trunk mass [kg]  (approx adolescent)
B_DAMP      = 5.0            # viscous damping coefficient [N m s rad^-1]
SIGMA_W     = 0.002          # process noise std dev [rad s^-2]

# ---- Proprioceptive delay ---------------------------------------------------
TAU         = 0.08           # proprioceptive delay [s]  (80 ms, mid-range)
DELAY_STEPS = int(TAU / DT)  # number of steps to buffer

# ---- Growth spurt profile L(t) -----------------------------------------------
# Pre-growth: L = 0.45 m (child, ~10 yr),  growth spurt at t=20–35 s,
# post-growth: L = 0.70 m (adolescent, ~15 yr).
# Uses a sigmoid transition centred on t = 27 s, width ~3 s.
L_PRE       = 0.45           # pre-spurt centre-of-mass height above S1 [m]
L_POST      = 0.70           # post-spurt centre-of-mass height [m]
T_GROWTH_C  = 27.0           # centre of growth sigmoid [s]
T_GROWTH_W  = 3.0            # sigmoid width parameter [s]

def L_true(t):
    """
    True pendulum length (centre-of-mass height above pivot) as a function
    of time. Sigmoid growth spurt.
    """
    return L_PRE + (L_POST - L_PRE) / (1.0 + np.exp(-(t - T_GROWTH_C) / T_GROWTH_W))

# The agent's INTERNAL model of L — updated with a lag / low-pass filter.
# Model update rate: lambda_L  (slow relative to actual growth)
LAMBDA_L    = 0.05           # low-pass time constant [s^-1]  for L_model update

# ---- Active Inference precision priors (= PID gain priors) ------------------
# Pi_y0 <-> Kp,  Pi_y1 <-> Kd,  Pi_y2 <-> Ki
PI_Y0_PRIOR = 120.0          # prior precision on position error  [N m rad^-1]
PI_Y1_PRIOR = 60.0           # prior precision on velocity error  [N m s rad^-1]
PI_Y2_PRIOR = 8.0            # prior precision on integral error  [N m s^-1 rad^-1]
PI_V0_PRIOR = 200.0          # prior precision on dynamic PE      [N m rad^-1]

# ---- Belief-update learning rates -------------------------------------------
KAPPA_MU    = 40.0           # belief update rate (gradient descent on F)
KAPPA_MU2   = 20.0           # rate for second generalised coordinate

# ---- Precision dynamics parameters ------------------------------------------
KAPPA_PI    = 0.30           # precision update rate  [s^-1]
GAMMA_VAR   = 0.80           # running-variance low-pass rate  [s^-1]
ALPHA_PREC  = 60.0           # sensitivity of precision to PE variance
PI_Y1_FLOOR = 2.0            # minimum precision (biological floor)

# ---- Initial conditions ------------------------------------------------------
THETA_0     = 0.02           # initial true angle [rad]  (small perturbation)
OMEGA_0     = 0.0            # initial angular velocity [rad s^-1]

# ---- Stability threshold display --------------------------------------------
# Kd_crit = M * G * L * tau / (1 - Kp * tau / (M * L^2))
# (Derived from characteristic equation of delayed PD inverted pendulum;
#  see Insperger & Stepan 2011, Ch. 4)
def Kd_crit(L, tau, Kp, m=M):
    """
    Critical derivative gain for stability of a delayed PD-controlled
    inverted pendulum (linear, small-angle approximation).

    Stability requires:  Kd > Kd_crit
    From Routh-Hurwitz applied to the quasi-polynomial characteristic equation
    of the linearised system (Insperger & Stepan 2011).

    Parameters
    ----------
    L   : float  — pendulum length [m]
    tau : float  — delay [s]
    Kp  : float  — proportional gain [N m rad^-1]
    m   : float  — mass [kg]

    Returns
    -------
    float : critical Kd value [N m s rad^-1]
    """
    I = m * L**2            # moment of inertia about pivot
    numerator   = m * G * L * tau
    denominator = 1.0 - (Kp / I) * tau
    if denominator <= 0:
        # Kp*tau >= I: already unstable without derivative term
        return np.inf
    return numerator / denominator

# =============================================================================
# SECTION 2 — HELPER: RUNNING VARIANCE TRACKER
# =============================================================================

class RunningVariance:
    """
    Exponentially-weighted running variance estimator.
    Update equation:  V_new = (1 - gamma*dt)*V + gamma*dt * x^2
    This approximates E[x^2] and hence Var[x] when E[x] ~ 0.
    """
    def __init__(self, gamma, dt, v0=0.0):
        self.gamma = gamma
        self.dt    = dt
        self.V     = v0

    def update(self, x):
        self.V = (1.0 - self.gamma * self.dt) * self.V + self.gamma * self.dt * x**2
        return self.V

    @property
    def value(self):
        return self.V

# =============================================================================
# SECTION 3 — DELAYED OBSERVATION BUFFER
# =============================================================================

class DelayBuffer:
    """
    Circular buffer that returns observations delayed by DELAY_STEPS.
    Initialised with the initial state so the buffer is never empty.
    """
    def __init__(self, delay_steps, init_val=0.0):
        self.buf = deque([init_val] * (delay_steps + 1), maxlen=delay_steps + 1)

    def push(self, val):
        self.buf.appendleft(val)   # newest at front

    def get_delayed(self):
        return self.buf[-1]        # oldest = most delayed

# =============================================================================
# SECTION 4 — ACTIVE INFERENCE AGENT
# =============================================================================

class ActiveInferenceAgent:
    """
    Active Inference agent for postural control.

    Generative model:
        y(t)    = mu(t) + noise_y0          (position observation)
        dy/dt   = mu'(t) + noise_y1         (velocity observation)
        mu''    = f(mu, mu'; L_m)           (dynamic prior)
        f       = (g / L_m) * mu            (small-angle, linearised)

    Free Energy:
        F = 0.5 * Pi_y0 * eps_y0^2
          + 0.5 * Pi_y1 * eps_y1^2
          + 0.5 * Pi_v0 * eps_v0^2
          - 0.5 * ln(Pi_y0 * Pi_y1)        (log-precision terms)

    Belief update (gradient descent on F in generalised coordinates):
        d/dt mu   = mu' - kappa_mu * Pi_y0 * eps_y0
        d/dt mu'  = mu'' - kappa_mu2 * Pi_y1 * eps_y1
        d/dt mu'' = f(mu, mu') - kappa_mu * Pi_v0 * eps_v0

    Action (reflex arc — gradient descent on F w.r.t. action):
        u = -(Pi_y0 * mu + Pi_y1 * mu' + Pi_y2 * mu_integral)
        This is the PID law with gains = precisions.

    Precision update:
        V_eps1 tracks running variance of eps_y1.
        Pi_y1 relaxes toward Pi_y1_0 / (1 + alpha * V_eps1)
        as velocity PE variance rises, effective Kd falls.
    """

    def __init__(self, dt, L_init):
        # Generalised belief states
        self.mu    = THETA_0          # belief: angle     [rad]
        self.mu_d  = OMEGA_0          # belief: velocity  [rad s^-1]
        self.mu_dd = 0.0              # belief: acceleration [rad s^-2]
        self.mu_int = 0.0             # integral of mu (for Ki term)

        # Agent's internal model of pendulum length (updated slowly)
        self.L_model = L_init

        # Precisions (= effective PID gains)
        self.Pi_y0  = PI_Y0_PRIOR
        self.Pi_y1  = PI_Y1_PRIOR     # THIS IS THE KEY VARIABLE
        self.Pi_y2  = PI_Y2_PRIOR
        self.Pi_v0  = PI_V0_PRIOR

        # Running variance tracker for velocity PE
        self.rv_eps1 = RunningVariance(gamma=GAMMA_VAR, dt=dt, v0=0.0)

        # Store last action
        self.u_last  = 0.0
        self.dt      = dt

    def predict_acceleration(self):
        """
        Agent's model of acceleration: linearised inverted pendulum.
        Uses agent's (possibly lagged) model of L.
        """
        return (G / self.L_model) * self.mu

    def update(self, y_tau, dy_tau, L_true_now):
        """
        One step of active inference:
          1. Compute prediction errors.
          2. Update beliefs (gradient descent on F).
          3. Update precision Pi_y1 based on velocity PE variance.
          4. Update agent's internal model of L (slow low-pass).
          5. Compute action u.

        Parameters
        ----------
        y_tau   : float — delayed proprioceptive angle observation [rad]
        dy_tau  : float — delayed velocity observation [rad s^-1]
        L_true_now : float — true L at current time (agent does NOT see this
                     directly; used only for L_model update via slow efference)

        Returns
        -------
        u : float — control torque [N m]
        """
        dt = self.dt

        # --- Step 1: Prediction errors ---------------------------------------
        eps_y0 = y_tau  - self.mu          # position PE
        eps_y1 = dy_tau - self.mu_d        # velocity PE  (KEY)
        eps_v0 = self.predict_acceleration() - self.mu_dd  # dynamic PE

        # --- Step 2: Belief update (gradient descent on F) -------------------
        # d/dt mu   = mu' - kappa * Pi_y0 * eps_y0
        # d/dt mu'  = mu'' - kappa2 * Pi_y1 * eps_y1
        # d/dt mu'' = f(mu, mu') - kappa * Pi_v0 * eps_v0
        d_mu    = self.mu_d  - KAPPA_MU  * self.Pi_y0 * eps_y0
        d_mu_d  = self.mu_dd - KAPPA_MU2 * self.Pi_y1 * eps_y1
        d_mu_dd = self.predict_acceleration() - KAPPA_MU * self.Pi_v0 * eps_v0

        self.mu     += d_mu    * dt
        self.mu_d   += d_mu_d  * dt
        self.mu_dd  += d_mu_dd * dt
        self.mu_int += self.mu * dt       # integral state

        # --- Step 3: Precision update ----------------------------------------
        # Track running variance of velocity PE
        V_eps1 = self.rv_eps1.update(eps_y1)

        # Precision relaxes toward prior / (1 + alpha * variance)
        # → higher velocity PE variance → lower precision → lower Kd
        Pi_y1_target = PI_Y1_PRIOR / (1.0 + ALPHA_PREC * V_eps1)
        Pi_y1_target = max(Pi_y1_target, PI_Y1_FLOOR)

        d_Pi_y1 = KAPPA_PI * (Pi_y1_target - self.Pi_y1)
        self.Pi_y1 += d_Pi_y1 * dt

        # Clamp precision to biological floor
        self.Pi_y1 = max(self.Pi_y1, PI_Y1_FLOOR)

        # --- Step 4: Slow update of agent's L model --------------------------
        # Agent infers L from proprioceptive consistency, modelled as
        # a slow low-pass filter toward true L.
        d_Lm = LAMBDA_L * (L_true_now - self.L_model)
        self.L_model += d_Lm * dt

        # --- Step 5: Action = PID law with precision gains -------------------
        # u = -(Pi_y0 * mu + Pi_y1 * mu' + Pi_y2 * integral_mu)
        # Negative because we are stabilising toward theta = 0.
        u = -(self.Pi_y0  * self.mu
              + self.Pi_y1 * self.mu_d
              + self.Pi_y2 * self.mu_int)

        self.u_last = u
        return u, eps_y0, eps_y1

# =============================================================================
# SECTION 5 — PHYSICS INTEGRATOR (Euler–Maruyama)
# =============================================================================

def plant_step(theta, omega, u_delayed, L_now, dt, rng):
    """
    One Euler–Maruyama step of the true inverted pendulum.

    Equations of motion (small-angle linearised for stability analysis,
    but we retain sin(theta) for physical realism):

        d theta / dt = omega
        d omega / dt = (g/L)*sin(theta) - (b/(m*L^2))*omega
                       + u_delayed/(m*L^2) + sigma_w * xi

    Parameters
    ----------
    theta      : float — current angle [rad]
    omega      : float — current angular velocity [rad s^-1]
    u_delayed  : float — control torque applied NOW but decided at t-tau [N m]
    L_now      : float — current true pendulum length [m]
    dt         : float — time step [s]
    rng        : numpy RandomState

    Returns
    -------
    theta_new, omega_new : floats
    """
    I     = M * L_now**2                   # moment of inertia [kg m^2]
    alpha = (G / L_now) * np.sin(theta)    # gravitational torque / I
    drag  = -(B_DAMP / I) * omega          # damping
    ctrl  = u_delayed / I                  # control
    noise = SIGMA_W * rng.randn() / np.sqrt(dt)  # white noise

    d_theta = omega
    d_omega = alpha + drag + ctrl + noise

    theta_new = theta + d_theta * dt
    omega_new = omega + d_omega * dt

    # Hard clamp: if angle exceeds 45 deg, mark as buckled (simulation ends)
    return theta_new, omega_new

# =============================================================================
# SECTION 6 — MAIN SIMULATION LOOP
# =============================================================================

def run_simulation():
    """
    Run the full active inference / precision collapse simulation.

    Returns
    -------
    results : dict of numpy arrays indexed by time
    """
    rng = np.random.RandomState(seed=42)

    # --- Preallocate storage -------------------------------------------------
    n = N_STEPS
    theta_hist   = np.zeros(n)
    omega_hist   = np.zeros(n)
    mu_hist      = np.zeros(n)
    mu_d_hist    = np.zeros(n)
    Pi_y1_hist   = np.zeros(n)
    Kd_crit_hist = np.zeros(n)
    L_true_hist  = np.zeros(n)
    L_model_hist = np.zeros(n)
    u_hist       = np.zeros(n)
    eps_y0_hist  = np.zeros(n)
    eps_y1_hist  = np.zeros(n)
    buckled_idx  = None

    # --- Initialise plant state ----------------------------------------------
    theta = THETA_0
    omega = OMEGA_0

    # --- Initialise agent ----------------------------------------------------
    L0    = L_true(T_START)
    agent = ActiveInferenceAgent(dt=DT, L_init=L0)

    # --- Initialise delay buffers (angle and angular velocity) ---------------
    angle_buf = DelayBuffer(delay_steps=DELAY_STEPS, init_val=THETA_0)
    omega_buf = DelayBuffer(delay_steps=DELAY_STEPS, init_val=OMEGA_0)

    # --- Action delay buffer (u decided now, applied after tau) --------------
    action_buf = DelayBuffer(delay_steps=DELAY_STEPS, init_val=0.0)

    print("=" * 60)
    print("  Active Inference Buckling Simulation")
    print(f"  dt={DT:.4f}s  T=[{T_START},{T_END}]s  tau={TAU:.3f}s")
    print(f"  L: {L_PRE:.2f} -> {L_POST:.2f} m  (growth at t={T_GROWTH_C}s)")
    print("=" * 60)

    for i, t in enumerate(TIME):

        # Record current true state
        L_now  = L_true(t)
        theta_hist[i]   = theta
        omega_hist[i]   = omega
        L_true_hist[i]  = L_now
        L_model_hist[i] = agent.L_model

        # Get delayed observations (what agent "feels" now = state at t-tau)
        y_tau  = angle_buf.get_delayed()
        dy_tau = omega_buf.get_delayed()

        # Get delayed action (torque decided at t-tau, arriving now)
        u_delayed = action_buf.get_delayed()

        # --- Active inference agent step -------------------------------------
        u_now, eps_y0, eps_y1 = agent.update(y_tau, dy_tau, L_now)

        # Record agent state
        mu_hist[i]     = agent.mu
        mu_d_hist[i]   = agent.mu_d
        Pi_y1_hist[i]  = agent.Pi_y1
        u_hist[i]      = u_now
        eps_y0_hist[i] = eps_y0
        eps_y1_hist[i] = eps_y1

        # Effective Kd_crit for current conditions
        Kd_crit_hist[i] = Kd_crit(L_now, TAU, agent.Pi_y0)

        # --- Plant integration step ------------------------------------------
        theta, omega = plant_step(theta, omega, u_delayed, L_now, DT, rng)

        # --- Push new observations into buffers ------------------------------
        angle_buf.push(theta)
        omega_buf.push(omega)
        action_buf.push(u_now)

        # --- Check for buckling (angle > 25 deg = structural failure) --------
        if abs(theta) > np.deg2rad(25) and buckled_idx is None:
            buckled_idx = i
            print(f"\n*** BUCKLING DETECTED at t={t:.2f} s  "
                  f"(theta={np.rad2deg(theta):.1f} deg,  "
                  f"L={L_now:.3f} m,  "
                  f"Kd_eff={agent.Pi_y1:.1f},  "
                  f"Kd_crit={Kd_crit_hist[i]:.1f}) ***\n")
            # Continue simulation to show post-buckling dynamics

        # Progress report
        if i % (N_STEPS // 10) == 0:
            print(f"  t={t:5.1f}s | theta={np.rad2deg(theta):+6.2f}° | "
                  f"L={L_now:.3f}m | L_m={agent.L_model:.3f}m | "
                  f"Kd_eff={agent.Pi_y1:.1f} | "
                  f"Kd_crit={Kd_crit_hist[i]:.1f}")

    print("\nSimulation complete.")
    return {
        'time'       : TIME,
        'theta'      : theta_hist,
        'omega'      : omega_hist,
        'mu'         : mu_hist,
        'mu_d'       : mu_d_hist,
        'Pi_y1'      : Pi_y1_hist,
        'Kd_crit'    : Kd_crit_hist,
        'L_true'     : L_true_hist,
        'L_model'    : L_model_hist,
        'u'          : u_hist,
        'eps_y0'     : eps_y0_hist,
        'eps_y1'     : eps_y1_hist,
        'buckled_idx': buckled_idx,
    }

# =============================================================================
# SECTION 7 — VISUALISATION
# =============================================================================

def make_figure(res):
    """
    Produce a 5-panel figure summarising the simulation.

    Panel 1: True angle theta(t) and belief mu(t)
    Panel 2: True L(t) and agent's model L_model(t)
    Panel 3: Effective Kd = Pi_y1(t)  vs  critical Kd_crit(t)
    Panel 4: Velocity prediction error eps_y1(t)
    Panel 5: Control torque u(t)
    """
    t          = res['time']
    theta_deg  = np.rad2deg(res['theta'])
    mu_deg     = np.rad2deg(res['mu'])
    bi         = res['buckled_idx']

    fig = plt.figure(figsize=(14, 18))
    fig.patch.set_facecolor('#0d1117')
    gs  = gridspec.GridSpec(5, 1, hspace=0.45, left=0.10, right=0.95,
                            top=0.93, bottom=0.06)

    PANEL_BG  = '#161b22'
    C_TRUE    = '#58a6ff'    # blue  — true state
    C_BELIEF  = '#f0883e'    # orange — agent belief
    C_CRITICAL= '#ff7b72'    # red    — critical threshold
    C_GROWTH  = '#3fb950'    # green  — growth
    C_CTRL    = '#d2a8ff'    # purple — control / precision
    C_PE      = '#ffa657'    # amber  — prediction error
    C_BUCKLE  = '#ff4444'    # bright red — buckling event

    def style_ax(ax, title, ylabel, ylim=None):
        ax.set_facecolor(PANEL_BG)
        ax.set_title(title, color='white', fontsize=11, loc='left', pad=4)
        ax.set_ylabel(ylabel, color='#8b949e', fontsize=9)
        ax.tick_params(colors='#8b949e', labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')
        ax.grid(True, color='#21262d', linewidth=0.6, linestyle='--')
        if ylim:
            ax.set_ylim(ylim)
        # Shade growth spurt region
        ax.axvspan(T_GROWTH_C - 3*T_GROWTH_W, T_GROWTH_C + 3*T_GROWTH_W,
                   alpha=0.08, color=C_GROWTH, label='_nolegend_')
        # Mark buckling
        if bi is not None:
            ax.axvline(t[bi], color=C_BUCKLE, linewidth=1.5,
                       linestyle=':', alpha=0.8, label='_nolegend_')

    # ---- Panel 1: Angle -----------------------------------------------------
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(t, theta_deg, color=C_TRUE,   lw=1.2, label='True θ(t)')
    ax1.plot(t, mu_deg,    color=C_BELIEF, lw=1.0, ls='--', alpha=0.85,
             label='Belief μ(t)')
    ax1.axhline(0, color='#8b949e', lw=0.5, ls=':')
    ax1.axhline( 25, color=C_BUCKLE, lw=0.8, ls='-.', alpha=0.6,
                label='Buckling threshold')
    ax1.axhline(-25, color=C_BUCKLE, lw=0.8, ls='-.', alpha=0.6,
                label='_nolegend_')
    style_ax(ax1, 'Panel A — Trunk tilt angle', 'θ [deg]')
    ax1.legend(fontsize=8, facecolor='#21262d', edgecolor='#30363d',
               labelcolor='white', loc='upper left')
    if bi is not None:
        ax1.annotate(f'Buckling\nt={t[bi]:.1f}s',
                     xy=(t[bi], theta_deg[bi]),
                     xytext=(t[bi]+1.5, theta_deg[bi]+3),
                     color=C_BUCKLE, fontsize=8,
                     arrowprops=dict(arrowstyle='->', color=C_BUCKLE))

    # ---- Panel 2: Pendulum length -------------------------------------------
    ax2 = fig.add_subplot(gs[1])
    ax2.plot(t, res['L_true'],  color=C_GROWTH, lw=1.5, label='True L(t)')
    ax2.plot(t, res['L_model'], color=C_BELIEF, lw=1.0, ls='--',
             label='Agent model L_m(t)')
    style_ax(ax2, 'Panel B — Pendulum length (trunk height to CoM)',
             'L [m]')
    ax2.legend(fontsize=8, facecolor='#21262d', edgecolor='#30363d',
               labelcolor='white')
    # Annotate the model lag
    t_mid = T_GROWTH_C + 2.0
    y_gap = (np.interp(t_mid, t, res['L_true']) +
              np.interp(t_mid, t, res['L_model'])) / 2
    ax2.annotate('Model lag\n(mismatch)', xy=(t_mid, y_gap),
                 color='#8b949e', fontsize=8, ha='center',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d',
                           edgecolor='#30363d'))

    # ---- Panel 3: Effective Kd vs critical Kd -------------------------------
    ax3 = fig.add_subplot(gs[2])
    ax3.plot(t, res['Pi_y1'],   color=C_CTRL,     lw=1.5,
             label='Kd_eff = Π_y1 (active inference)')
    ax3.plot(t, res['Kd_crit'], color=C_CRITICAL, lw=1.2, ls='--',
             label='Kd_crit (stability threshold)')
    ax3.axhline(PI_Y1_FLOOR, color='#8b949e', lw=0.6, ls=':',
                label='Biological floor')
    style_ax(ax3, 'Panel C — Effective derivative gain vs stability threshold',
             'Gain [N m s rad⁻¹]')
    ax3.legend(fontsize=8, facecolor='#21262d', edgecolor='#30363d',
               labelcolor='white')
    # Shade the region where Kd_eff < Kd_crit (unstable)
    ax3.fill_between(t,
                     res['Pi_y1'], res['Kd_crit'],
                     where=(res['Pi_y1'] < res['Kd_crit']),
                     alpha=0.25, color=C_BUCKLE, label='_nolegend_')
    # Text annotation for unstable zone
    unstable_mask = res['Pi_y1'] < res['Kd_crit']
    if unstable_mask.any():
        t_unstable = t[unstable_mask][0]
        ax3.annotate('UNSTABLE\nKd_eff < Kd_crit',
                     xy=(t_unstable + 2, (PI_Y1_FLOOR + PI_Y1_PRIOR) / 2),
                     color=C_BUCKLE, fontsize=9, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d',
                               edgecolor=C_BUCKLE))

    # ---- Panel 4: Velocity prediction error ---------------------------------
    ax4 = fig.add_subplot(gs[3])
    ax4.plot(t, res['eps_y1'], color=C_PE, lw=0.7, alpha=0.8,
             label='Velocity PE ε_y1')
    # Running std approximation for annotation
    window = int(2.0 / DT)
    eps_rms = np.sqrt(np.convolve(res['eps_y1']**2,
                                   np.ones(window)/window, mode='same'))
    ax4.plot(t, eps_rms,  color='white', lw=0.8, ls='--',
             label='RMS(ε_y1) [windowed]')
    ax4.plot(t, -eps_rms, color='white', lw=0.8, ls='--',
             label='_nolegend_')
    style_ax(ax4, 'Panel D — Velocity prediction error (drives precision collapse)',
             'ε_y1 [rad s⁻¹]')
    ax4.legend(fontsize=8, facecolor='#21262d', edgecolor='#30363d',
               labelcolor='white')

    # ---- Panel 5: Control torque --------------------------------------------
    ax5 = fig.add_subplot(gs[4])
    ax5.plot(t, res['u'] / (M * G * L_POST), color=C_CTRL,
             lw=0.8, alpha=0.85, label='u(t) / (M·g·L_max) [normalised]')
    ax5.axhline(0, color='#8b949e', lw=0.5, ls=':')
    style_ax(ax5, 'Panel E — Normalised paraspinal muscle torque',
             'u / MgL [−]')
    ax5.legend(fontsize=8, facecolor='#21262d', edgecolor='#30363d',
               labelcolor='white')
    ax5.set_xlabel('Time [s]', color='#8b949e', fontsize=9)

    # ---- Super-title --------------------------------------------------------
    fig.suptitle(
        'The Allometric Trap: Active Inference Precision Collapse\n'
        'Adolescent Spinal Instability via Dynamic Kd Failure',
        color='white', fontsize=13, fontweight='bold', y=0.97
    )

    # ---- Shared x-axis tick annotation --------------------------------------
    for ax in [ax1, ax2, ax3, ax4, ax5]:
        ax.set_xlim(T_START, T_END)
        # Annotate growth spurt period on x-axis
        ax.annotate('', xy=(T_GROWTH_C + 3*T_GROWTH_W, ax.get_ylim()[0]),
                    xytext=(T_GROWTH_C - 3*T_GROWTH_W, ax.get_ylim()[0]),
                    arrowprops=dict(arrowstyle='<->', color=C_GROWTH,
                                   lw=1.2))

    outfile = 'active_inference_buckling.png'
    fig.savefig(outfile, dpi=150, facecolor=fig.get_facecolor(),
                bbox_inches='tight')
    print(f"\nFigure saved to: {outfile}")
    return fig

# =============================================================================
# SECTION 8 — ENTRY POINT
# =============================================================================

def main():
    print(__doc__)

    # Run simulation
    results = run_simulation()

    # Print summary statistics
    bi = results['buckled_idx']
    t  = results['time']

    print("\n=== SUMMARY ===")
    print(f"  Simulation duration     : {T_END:.0f} s")
    print(f"  Growth spurt centre     : {T_GROWTH_C:.0f} s  "
          f"(L: {L_PRE:.2f} -> {L_POST:.2f} m)")
    print(f"  Proprioceptive delay tau: {TAU*1000:.0f} ms")
    print(f"  Prior Kd (Pi_y1_0)      : {PI_Y1_PRIOR:.1f} N m s rad⁻¹")
    print(f"  Kd floor                : {PI_Y1_FLOOR:.1f} N m s rad⁻¹")

    # Find first crossing of Kd_eff < Kd_crit
    cross_mask = results['Pi_y1'] < results['Kd_crit']
    if cross_mask.any():
        t_cross = t[cross_mask][0]
        print(f"  Hopf bifurcation entry  : t = {t_cross:.2f} s")
        print(f"    Kd_eff at crossing    : "
              f"{results['Pi_y1'][cross_mask][0]:.1f}")
        print(f"    Kd_crit at crossing   : "
              f"{results['Kd_crit'][cross_mask][0]:.1f}")
        print(f"    L at crossing         : "
              f"{results['L_true'][cross_mask][0]:.3f} m")
    else:
        print("  No bifurcation detected (system remained stable)")

    if bi is not None:
        print(f"  Structural buckling     : t = {t[bi]:.2f} s  "
              f"(|theta| > 25 deg)")

    # Generate figure
    make_figure(results)


if __name__ == '__main__':
    main()
```

---

## Part III: Expected Findings

### 3.1 Simulation Narrative

The simulation will produce **five temporally coupled traces** across 60 seconds:

| Phase | Time (s) | What Happens |
|---|---|---|
| **Pre-growth stability** | 0–18 | System stable; θ ≈ 0; Kd_eff ≈ 60 > Kd_crit ≈ 22; agent tracks well |
| **Growth spurt initiation** | 18–24 | L begins rising; Kd_crit rises proportionally (∝ L); velocity PEs begin accumulating |
| **Precision collapse window** | 24–32 | Running variance of ε_y₁ spikes; Π_y₁ decays toward floor; Kd_eff crosses below Kd_crit |
| **Hopf bifurcation** | ~30 | Kd_eff < Kd_crit simultaneously; oscillations begin growing — the Allometric Trap |
| **Structural buckling** | ~35 | θ exceeds 25°; system destabilised despite maximum paraspinal effort |

### 3.2 Key Quantitative Predictions

**Panel C (the critical panel)** will show:

- `Kd_crit(t)` rising from ~22 → ~34 N m s rad⁻¹ as L increases (because instability is harder to control with a longer lever arm)
- `Kd_eff = Π_y₁(t)` falling from 60 → ~5 N m s rad⁻¹ during the growth spurt (precision collapse driven by velocity PE accumulation)
- A **red-shaded crossing region** where Kd_eff < Kd_crit: this is the bifurcation point

### 3.3 Mechanistic Insights and Clinical Implications

1. **The trap has two jaws**: Rising Kd_crit (biomechanical, passive) AND falling Kd_eff (neurological, active) close simultaneously during peak growth velocity — both are necessary for the trap to close.

2. **Delay matters critically**: With τ = 80 ms vs. 50 ms, Kd_crit is ~60% higher, meaning shorter delays (well-trained athletes) are protective. This is consistent with evidence that:
   > Simoneau M, et al. "Evidence for cognitive modulation of postural sway in patients with adolescent idiopathic scoliosis." *Spine* 2006;31(1):E13–E20. PMID: [16395180](https://pubmed.ncbi.nlm.nih.gov/16395180/)

3. **Precision collapse is the missing link**: Prior PID analyses of postural delay instability (Peterka 2002) treated gains as fixed. The active inference formulation explains *why* Kd drops during growth — it is a rational Bayesian response to increased uncertainty, but it creates a vulnerability window.

4. **Recovery after growth**: When growth stops, L_model catches up to L_true, velocity PEs normalise, and Π_y₁ recovers — but if the spine has already buckled (vertebral wedging, disc deformation), the mechanical defect persists. This explains the **persistence of AIS curves** post-adolescence.

5. **Therapeutic targets**: Increasing sensory precision (e.g., vibrotactile feedback vests, physiotherapy improving proprioceptive acuity) or reducing effective delay (e.g., reducing reaction time, anticipatory muscle activation) would shift the bifurcation boundary, preventing curve initiation. This maps directly onto:
   > Nault ML, et al. "Relations between standing stability and body posture parameters in adolescent idiopathic scoliosis." *Spine* 2002;27(17):1911–1917. PMID: [12221356](https://pubmed.ncbi.nlm.nih.gov/12221356/)

### 3.4 Honest Limitations

- **Linearisation**: The stability criterion Kd_crit used here is derived from the *linear* characteristic equation. For large angles, Insperger & Stépán's semi-discretisation method gives tighter bounds.
- **1D model**: Real AIS is a 3D rotational instability; this simulation captures the sagittal plane only. Coupling to coronal and axial planes (Paper 4 of the series) would show the lateral buckling direction.
- **L_model lag**: The model uses a simple exponential filter for the agent's internal L estimate; a more biologically realistic treatment would use hierarchical Bayesian inference on trunk length from visual and vestibular cues (Friston 2010 generalised filtering).
- **Constant tau**: Proprioceptive delay itself likely increases during rapid growth (peripheral nerve conduction velocity changes), which would make the instability worse — an effect not captured here.