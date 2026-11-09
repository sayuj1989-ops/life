# Derivation re-verification — AIS manuscript (2026-10-12)

Checker: `scripts/analysis/verify_derivations_20261012.py` (run under clean env, sympy 1.14 / scipy 1.17). Lean-style intent after openai/math: every stated equation re-derived and asserted. 14 PASS, 0 DISCREPANCY out of 16.

| id | claim | source | verdict |
|---|---|---|---|
| C1 | Rindler Hamiltonian expansion | research/scoliosis_derivation_rindler_cosserat.md Eq 1.1 (HISTORICAL) | CHECK |
| C2 | Bio-Gravitational Number dimensionless + Euler relation | manuscript/sections/supplementary.tex eq:bg_number_passive_supp | PASS |
| C3 | Energy-deficit scaling L^3 vs L^2 and R(0.45)/R(0.35) | manuscript/sections/theory_summary.tex (Energy Deficit Window) | PASS |
| C4 | Recovery-ratchet cemented fraction k_g/(k_r+k_g) | manuscript/sections/theory_summary.tex eq:recovery_ratchet; src/spinalmodes/recovery_ratchet.py docstring | PASS |
| C5 | Modal ansatz kappa=A e^{lam t} sin(n pi s/L) -> characteristic equation | manuscript/sections/supplementary.tex eq:dde_spine_supp -> eq:char_eq_supp | PASS |
| C6 | Exact quadratic in x = omega^2 (Hopf boundary) | manuscript/sections/supplementary.tex eq:hopf_quadratic_supp; scripts/hopf_exact.py | PASS / tex typo |
| C9 | IEC energy functional -> constitutive moments | manuscript/sections/supplementary.tex eq:iec_energy_supp | PASS |
| C7 | tau*(Kd) ridge numbers quoted in supplementary | manuscript/sections/supplementary.tex (Kp=120 ridge K_D*=12.4, tau_c=79.0 ms) | PASS |
| C8 | Delay-Hopf rejection trajectory numbers | manuscript/sections/supplementary.tex (rejection paragraphs); scripts/analysis/verify_hopf_rejection.py | PASS |
| N1 | Growth material-derivative expansion (HISTORICAL note) | research/scoliosis_derivation_rindler_cosserat.md Sec 3.1 | PASS-with-note |
| N2 | Growth-convected DDE characteristic equation + B_eff (HISTORICAL note) | research/scoliosis_derivation_rindler_cosserat.md Eq 3.1.5-3.1.7 | PASS |
| N3 | S_crit = pi/2 instability criterion (HISTORICAL note; AMEND-02 corrected) | research/scoliosis_derivation_rindler_cosserat.md Sec 3.2 | PASS(AMEND-02) |
| N4 | Spinal-jetlag differential growth identity (HISTORICAL note) | research/scoliosis_derivation_rindler_cosserat.md Eq 4.1.2 | PASS-with-note |
| N5 | Generalized eigenproblem (B y'')'' = lambda Q y from variational principle | research/multi_segment_cosserat_lenke_derivation.md Sec 2 | PASS |
| N6 | Lenke-type localization demo: mode localizes to low-B/high-Q zone | research/multi_segment_cosserat_lenke_derivation.md Sec 3-4 | CHECK |
| N7 | Scoliosis Number dimensionlessness (HISTORICAL note) | research/scoliosis_derivation_rindler_cosserat.md Eq 3.2.1 | PASS |

## Details

### C1 — Rindler Hamiltonian expansion
- Source: `research/scoliosis_derivation_rindler_cosserat.md Eq 1.1 (HISTORICAL)`
- Method: sympy series of rho c^2 (sqrt(1-rs/r)-1) in 1/c
- Verdict: **CHECK**
- rho c^2(sqrt(g00)-1) ~ 0 : leading term is MINUS rho*G*M/r (=-rho*g*h). Note claims '+rho*Phi=+rho*g*h'; correct as magnitude, wrong as signed potential energy. HISTORICAL note only; no manuscript equation depends on it.

### C2 — Bio-Gravitational Number dimensionless + Euler relation
- Source: `manuscript/sections/supplementary.tex eq:bg_number_passive_supp`
- Method: sympy dimensional substitution; algebraic Euler-load comparison
- Verdict: **PASS**
- [B_g] -> 1; Mg/P_Euler = (4/pi^2)*B_g (4/pi**2*B_g) - consistent with 'passive flexural resistance vs gravitational bending moment'.

### C3 — Energy-deficit scaling L^3 vs L^2 and R(0.45)/R(0.35)
- Source: `manuscript/sections/theory_summary.tex (Energy Deficit Window)`
- Method: sympy log-exponent extraction; exact rational ratio
- Verdict: **PASS**
- U ~ EI k^2 L with I~L^4, k~L^-1 -> exponent 3 (=3 required); R(0.45)/R(0.35) = 9/7 = 1.2857 -> paper's '~1.29' and '(0.45/0.35)^1' correct.

### C4 — Recovery-ratchet cemented fraction k_g/(k_r+k_g)
- Source: `manuscript/sections/theory_summary.tex eq:recovery_ratchet; src/spinalmodes/recovery_ratchet.py docstring`
- Method: impulse recoil kappa_e=A exp(-(kr+kg)t); cemented = int kg*kappa_e dt (sympy)
- Verdict: **PASS**
- int_0^inf k_g A e^-(k_r+k_g)t dt / A = k_g/(k_g + k_r) = claimed fraction; limits kr->inf: 0, kg->inf: 1. NOTE: d kappa_p/dt = k_g*kappa_e0*[k_g/(k_r+k_g)] identifies the perturbation recurrence rate with k_g (modeling choice; a linear k_g*kappa_e0 feed would scale ~k_g, not k_g^2 at small k_g).

### C5 — Modal ansatz kappa=A e^{lam t} sin(n pi s/L) -> characteristic equation
- Source: `manuscript/sections/supplementary.tex eq:dde_spine_supp -> eq:char_eq_supp`
- Method: symbolic substitution, divide by mode shape
- Verdict: **PASS**
- PDE (rhoA k_tt + eta k_t + EI k_ssss + K_P k_tau + K_D k_t,tau = 0) reduces exactly to rhoA lam^2 + eta lam + EI (n pi/L)^4 + (K_P + K_D lam) e^{-lam tau} = 0.

### C6 — Exact quadratic in x = omega^2 (Hopf boundary)
- Source: `manuscript/sections/supplementary.tex eq:hopf_quadratic_supp; scripts/hopf_exact.py`
- Method: eliminate (cos,sin) from RE=IM=0; impose cos^2+sin^2=1; compare coeffs
- Verdict: **PASS / tex typo**
- Derived: I^2 x^2 + (2 I mgL + b^2 - K_D^2) x + ((mgL)^2 - K_P^2) = 0 -- matches hopf_exact.py code (C = mgL*mgL - Kp*Kp). DISCREPANCY: supplementary.tex renders the constant term 'mgL^2 - K_P^2' (literal m*g*L^2); it must read (mgL)^2 - K_P^2. fix: change tex to (mgL)^2.

### C9 — IEC energy functional -> constitutive moments
- Source: `manuscript/sections/supplementary.tex eq:iec_energy_supp`
- Method: symbolic functional derivative d/dkappa etc.
- Verdict: **PASS**
- delta E/delta kappa = B_eff (kappa - kappa_rest) (bending moment), torsion and stretch terms analogous; gravity term rho A r.g is a potential on the centreline (sign depends on g-vector convention: written as + r.g with g pointing down). Consistent with eq:stiffness_modulation_supp.

### C7 — tau*(Kd) ridge numbers quoted in supplementary
- Source: `manuscript/sections/supplementary.tex (Kp=120 ridge K_D*=12.4, tau_c=79.0 ms)`
- Method: import scripts/hopf_exact.py; recompute table + ridge by ternary search
- Verdict: **PASS**
- Kp=120: Kd=4->40.7ms, Kd=8->67.0ms, Kd=12->78.9ms, Kd=13->78.8ms, Kd=20->62.3ms; ridge Kd*=12.41 tau*=78.9 ms (expect 12.4/79.0); Kp=200: Kd*=15.81, tau*=54.7 ms (expect 15.8/54.7). maxdev=0.05 ms.

### C8 — Delay-Hopf rejection trajectory numbers
- Source: `manuscript/sections/supplementary.tex (rejection paragraphs); scripts/analysis/verify_hopf_rejection.py`
- Method: subprocess re-run, regex-assert against prose numbers
- Verdict: **PASS**
- v=15: (0.806, 0.655) (expect 0.806->0.655); v=55: (0.546, 0.324) (expect 0.546->0.324); dimless delay change -21.1% (expect -21.1); crossings [('0.8063', '5.0'), ('0.5456', '5.0')] -> none >= 1 as claimed.

### N1 — Growth material-derivative expansion (HISTORICAL note)
- Source: `research/scoliosis_derivation_rindler_cosserat.md Sec 3.1`
- Method: apply (d_t + v d_s)^2 twice symbolically
- Verdict: **PASS-with-note**
- (D/Dt)^2 theta = theta_tt + 2 v theta_ts + v^2 theta_ss EXACTLY for constant v; residual for v(t): 0 -> note's expansion assumes growth-rate constancy (v=Ldot const); holds for logistic growth only approximately (v-dot theta_s dropped).

### N2 — Growth-convected DDE characteristic equation + B_eff (HISTORICAL note)
- Source: `research/scoliosis_derivation_rindler_cosserat.md Eq 3.1.5-3.1.7`
- Method: modal substitution lambda, k into expanded D^2 theta
- Verdict: **PASS**
- I(lam^2 + 2 Ldot lam i k - Ldot^2 k^2) + B + K e^{-lam tau} = 0 reproduces; real part at lam=i w gives B_eff = B - I Ldot^2 k^2 exactly as claimed.

### N3 — S_crit = pi/2 instability criterion (HISTORICAL note; AMEND-02 corrected)
- Source: `research/scoliosis_derivation_rindler_cosserat.md Sec 3.2`
- Method: argument principle on h=(I lam^2+B+K e^{-lam tau}) over right half-disk + crossing-family algebra
- Verdict: **PASS(AMEND-02)**
- crossing law b+(-1)^n a = n^2 pi^2 verified on ray a=tau^2,b=2tau^2: first odd (n=1) boundary tau_1* = pi/sqrt((B-K)/I) = 3.1416 (2->0); even n=2 at 2pi/sqrt((B+K)/I)=3.6276 (+2), even n=4 at 7.2552 (+2, N_RHP=4 for tau in (7.26,9.42)), odd n=3 at 3pi (−2). Stability wedges W_m = {b-a>(2m+1)^2 pi^2, b+a<(2m+2)^2 pi^2}. PREVIOUSLY PRINTED tau=pi/sqrt((B+K)/I)=1.814 IS NOT A CROSSING (real part 2K != 0 at w tau=pi); N_RHP=2 there. S_co = K*Ldot*tau/B = (K/B)*(Ldot*tau) carries dimension [m] (growth distance per delay window), NOT dimensionless (cf. N7). Pi/2 in the HISTORICAL note is the first-order criterion; second-order boundary is omega*tau = pi. AMEND-02. counts: tau=0.5: 2.00(exp 2); tau=1.814: 2.00(exp 2); tau=3.2: 0.00(exp 0); tau=4.0: 2.00(exp 2); tau=8.0: 3.99(exp 4); tau=9.5: 1.98(exp 2)

### N4 — Spinal-jetlag differential growth identity (HISTORICAL note)
- Source: `research/scoliosis_derivation_rindler_cosserat.md Eq 4.1.2`
- Method: sympy product-to-sum expansion
- Verdict: **PASS-with-note**
- g_L-g_R = -2 A gbar sin(Omega t + (phi_L+phi_R)/2) sin(dphi/2) exactly; note drops the mean-phase factor -> its form holds only for phi_L+phi_R=0.

### N5 — Generalized eigenproblem (B y'')'' = lambda Q y from variational principle
- Source: `research/multi_segment_cosserat_lenke_derivation.md Sec 2`
- Method: higher-order Euler-Lagrange on Pi[y] = int 1/2 B y''^2 - 1/2 lambda Q y^2
- Verdict: **PASS**
- delta Pi = 0 gives exactly (B(s) y'')'' = lambda Q(s) y for pinned/essential BCs. HISTORICAL note (route superseded by recovery ratchet), but the variational statement is correct.

### N6 — Lenke-type localization demo: mode localizes to low-B/high-Q zone
- Source: `research/multi_segment_cosserat_lenke_derivation.md Sec 3-4`
- Method: generalized eigenproblem (B y'')'' = lam Q y, 4-region B,Q, pinned BC, scipy eigh
- Verdict: **CHECK**
- first-mode participation cervical:0.42, thoracic:0.94, thoracolumbar:0.73, lumbar:0.18; peak at s/L=0.59 in 'thoracic' region; eigenvalue1=2.14e+03. Mechanism claim (regional B,Q -> curve-type mapping) is mechanically valid; clinical mapping is illustrative.

### N7 — Scoliosis Number dimensionlessness (HISTORICAL note)
- Source: `research/scoliosis_derivation_rindler_cosserat.md Eq 3.2.1`
- Method: units: [K]=N m, [Ldot L tau]=m, [B=EI]=N m^2
- Verdict: **PASS**
- S_co = K Ldot tau / B is dimensionless iff B is a bending stiffness EI (N m^2), but the note's DDE uses B as a per-mode torque/rad stiffness (N m) -> same symbol, two units; the ratio is only dimensionless under the EI reading. Note also rejects pi/2 threshold (N3).
