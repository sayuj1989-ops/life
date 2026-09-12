# Recovery comparators — methods note (kanban t_9f29fa3b)

Synthetic comparison of three reduced models under one declared protocol. Code
`scripts/experiments/recovery_comparators/{models,run_comparators}.py`; all numbers below are from `results.json`
(`generated_utc` inside; runner ≈ 35 s); tests `tests/test_recovery_comparators.py` (11, ≈ 1 s). No clinical
calibration, no AlphaFold input, no change to `manuscript/` or `src/`. Nothing here validates a mechanism.

## 1. Measurable meaning, units, identification

**e, "slow recovery" (1/m):** the signed lateral-curvature deviation that decays after a sustained loading asymmetry
is removed, with time constant 1/(kr+kg) — years at the declared rates. It is therefore *not* the supine/bending
reducible component (a seconds–minutes elastic response, treated as instantaneous in (c) and lumped into κe0 in (a)).
**kr (1/yr)** is identified from ≥ 3 serial standing measurements after a step change in sustained loading (brace
start/stop, end of a persistent asymmetric activity) while measured growth velocity ≈ 0. **kg (1/yr)** from
dp/dt = kg·e with p (regional wedging) and e (total minus wedging) measured separately and growth velocity measured
independently (height velocity); it cannot be read off curvature. **Loading:** b(t) is a dimensionless asymmetry index,
c_load (1/m/yr) converts it; it needs an independent side-to-side load estimate — if b is derived from the curve, (b)
collapses into (c)'s feedback and the comparison is circular. Units: time yr (age 5–20), curvature 1/m, rates 1/yr,
forcing 1/m/yr; (c) constants β 1/MPa, G_m m/yr, c_σ MPa·m, w, h m.

## 2. Models, one protocol

Growth timing is identical: g(t) = `recovery_ratchet.growth_velocity(t)` (peak 1 at 12 y, baseline 0.074);
"ceasing" variant g(t)·½(1−tanh((t−18)/0.25)). Grid 601 points (0.025 yr); switches at 14.0 / 18.0 y are grid points.

| | equations | state / observable |
|---|---|---|
| (a) scalar ratchet, API unchanged | dκp/dt = kg·κe0·kg/(kr+kg), kg = kg_peak·g(t); κe ≡ κe0 | unsigned κp; F = κe0/(κe0+κp) |
| (a′) same law as quadrature | κe0 → κe0·b(t), any g(t); only where the API cannot express a control | matches API on baseline, max\|Δ\| 9.0e-11 |
| (b) signed two-state, API unchanged | de/dt = c_load·b − (kr+kg)e; dp/dt = kg·e − kh·p | e, p signed; F = e/(e+p) |
| (c) stress-modulated growth | dκw/dt = λ(t)(κw + κe0·b), λ = β·G_m_peak·g(t)·c_σ/(w·h) | κw signed; seed κe0·b quasi-static |

(c): per side G = G_m(1 − β(σ − σ_m)) (Stokes 1996, 2006, 2007); Δσ = c_σ·κ_total (declared linear map); the
growth-rate difference βG_m c_σ κ across width w is a wedge-angle rate, and per segment height h a curvature rate.
Sign: the compressed concave side grows slower, so wedging carries the sign of κ_total (the "vicious cycle"). This is a
one-DOF linearisation of the published law, not Stokes's finite-element geometry; any threshold arising there from
geometric nonlinearity is absent here.

**Declared parameters** (order-of-magnitude, not fitted): kr 0.3, kg_peak 1.0 (the ratchet's progressor pair); κe0 0.02;
c_load 0.006 = kr_ref·κe0 so (b) at kg = 0, b = 1 relaxes to κe0 (fixed when kr varies); kh 0.2; **β 1.71 /MPa** =
17.1 % per 0.1 MPa, mean of Stokes et al. 2006 (abstract), swept over its reported 0.92–2.39; G_m_peak 1e-3 m/yr;
c_σ 0.1 MPa·m; w 0.04 m; h 0.025 m → **λ_peak 0.171 /yr**. β, G_m, c_σ, 1/(wh) enter (c) only through λ, so they are
not separately identifiable from curvature. Stokes 2007's apex stresses 0.48/0.81 MPa and 13°→32°/38° over 11–16 y
were *not* used to tune anything.

## 3. Controls (S = κp / p / κw; T = S + recoverable)

| control | (a) / (a′) | (b) kh=0 | (b) kh=0.2 | (c) |
|---|---|---|---|---|
| no growth, zero bias, reversed bias: max\|S\|, max\|T\|, max\|T(b)+T(−b)\| | 0, 0, 0 | 0, 0, 0 | 0, 0, 0 | 0, 0, 0 |
| baseline b≡1: S(20), F(20) | 0.0597, 0.251 | 0.0356, 0.290 | 0.0089, 0.619 | 0.0256, 0.438 |
| F nadir → F(20) | monotone | 0.169 (13.4 y) → 0.290 | 0.244 → 0.619 | monotone |
| unload at 14: S(14); ΔS to 20; (dS/dt)/S at 20 | 0.0533; 0; 0 | 0.0279; +0.0023; 1.3e-3 /yr | 0.0162; −0.0104; −0.21 /yr | 0.0196; +0.0030; +1.26e-2 /yr = λ(20) |
| unload: fraction of T(14⁻) lost by 20 | 0.273 (elastic only) | 0.093 | 0.720 | 0.430 (instant seed loss) |
| unload: e-fold time of the recoverable part | instant | 1.725 y measured, 1.723 y from ∫(kr+kg); 1/(kr+kg(14)) = 1.25 y | same | instant |
| growth ceases at 18: ΔS after 18 | 8e-6 | 8.5e-5 | −0.0035 | 4.9e-5 |
| correction | not expressible (dκp/dt ≥ 0) | reversed load at 14: ΔS −0.0031 via e < 0; after cessation +7e-5 | kh: S(20) 0.0089 vs 0.0356; after unload+cease 0.0057 vs 0.0301 | no autonomous term; reversed load at 14: ΔS −6.9e-5 (κw − κe0 ≈ −0.0005); after cessation +5e-6 |
| zero-mean noise n = 200 (seed 20260912): mean T(20) ± SEM; frac > 0 | (a′) +1.5e-4 ± 1.0e-3; 0.495. **Rectified (a), κe0·\|b\|: +0.0325 ± 0.0007; 1.00** | −1.5e-4 ± 7.3e-5; 0.42 (p 0.03) | — | +1.6e-4 ± 1.0e-3; 0.495 |

(a) as published has no load, growth-history or initial-state argument, so unload / cessation / noise / correction are
`not_expressible` for the API and run on (a′). Noise: Σ_k a_k cos(2πf_k t+φ_k)/√8, a~N(0,1), f~U(0.25,1.5)/yr —
zero-mean, sign-symmetric in law. (b)'s 0.42 is a draw-level fluctuation: the antithetic rerun on −b returns the exact
negatives (max\|T(b)+T(−b)\| = 0), so its expectation is 0.5 by symmetry. Individuals do acquire curves of random sign
(mean\|T(20)\| 0.011 for (a′)/(c), 0.0008 for (b), which low-passes at kr+kg); only rectification manufactures
population handedness.

## 4. Convergence and sensitivity

RK45, (rtol, atol, max_step) (1e-6, 1e-9, ∞) → (1e-8, 1e-11, 0.1) → (1e-10, 1e-13, 0.05): max\|Δ\| vs tightest 1.5e-7 /
5.9e-12 for (a′), 9.1e-8 / 1.9e-12 for (c). (b) pins rtol 1e-10 / atol 1e-12; max_step ∞ → 0.1 → 0.05 gives 5.3e-13 /
5.1e-13. Declared tolerance 1e-9: all pass; API LSODA vs (a′) 9.0e-11. One-at-a-time ×0.5 / ×1.5, relative change of
S(20) (more in `results.json`): (a) kg_peak −62 % / +69 %, kr +20 % / −14 %; (b) kr +25 % / −17 %, kg_peak −30 % / +18 %,
c_load exactly ∓50 % (linear) with F and the recovered fraction unchanged, the recovered fraction most sensitive to
kg_peak (+123 % / −43 %); (c) β −60 % / +91 %, post-unload ΔS −80 % / +184 %. β over its reported range: S(20)/κe0 =
0.56 / 1.28 / 2.17 and post-unload S(20)/S(14) = 1.08 / 1.15 / 1.22 at β = 0.92 / 1.71 / 2.39.

## 5. Imposed vs discriminating

| model | imposed by construction |
|---|---|
| (a) | κp monotone and F monotone falling (rate independent of κp); input is an unsigned amplitude, i.e. rectified; extra event-rate factor ν = kg — the rate is kg/kr × (b)'s quasi-steady rate kg·e_ss, e_ss = kr·κe0/(kr+kg) (S(20) ratio (a)/(b) = 1.68); no threshold at kg = kr; no recovery or reverse term; set accrues at the 0.074 growth baseline indefinitely |
| (b) | linear: zero bias → 0, exact mirror, scales with c_load; e smaller during growth by construction; kh = 0 → p monotone under one-signed load; kh > 0 declared, not derived; no threshold, anatomy or handedness |
| (c) | exponential positive feedback with no threshold whenever β·c_σ > 0 and G_m > 0; quasi-static seed vanishes at unloading; no recovery variable or reverse term — correction only if the net stress asymmetry reverses during remaining growth |

**Discriminating (same protocol, different answers):** (i) after a load step the recoverable part decays over
1/(kr+kg) — years — in (b), instantly in (a′) and (c); (ii) after unloading the structural rate per unit S → 0 in (a)
and (b) (1.3e-3 /yr at 20, still falling) but stays at λ(t) > 0 in (c) (1.26e-2 /yr) while growth continues — with growth
held constant after unloading, (b) → p(14)+kg·e(14)/(kr+kg) and (c) → κw(14)·e^{λΔt}, both pinned by tests; (iii) under
sustained load F has a nadir near PHV then a partial rebound in (b) (0.17 → 0.29), monotone in (a) and (c);
(iv) correction after growth stops exists only with kh > 0 in (b). The "fraction of total recovered" is *not* a
discriminator — (c)'s 0.43 > (b)'s 0.09 is the instantaneous seed. Falling flexibility under sustained load, which all
three produce, discriminates nothing.

## 6. Fairness

Held identical: window, grid, growth timing, the b(t) protocols, the no-growth elastic amplitude κe0 (c_load =
kr_ref·κe0), solver tolerances where the API allows, every observable. Not identical, and could not be: (a) takes a
deviation amplitude, not a load, so at kr ≠ kr_ref it is under a different load and its "recoverer" (kr = 6) has no
fixed-load counterpart in (b) (e → 0.001); (c) has no recovery state, so its elastic response is quasi-static; kg_peak
(1/yr) and G_m_peak (m/yr) are different physical quantities — only growth timing is shared; (c) is a linearisation of
Stokes's law, not his geometry. All magnitudes are set by declared constants and mean nothing clinically.

## 7. Prespecified next empirical test; falsifiers (REVIEW.md §6)

**One test.** Within-patient serial series, ≥ 3 visits at a prespecified 6-month spacing over ≥ 2 years, each measuring
independently (i) a recovery measure — standing minus standardised-unloaded curvature under one declared unloading
protocol (protocols are not interchangeable) and its serial change; (ii) regional vertebral wedging; (iii) height
velocity. Lag prespecified at one visit interval. Recovery-model prediction: deterioration of (i) precedes the increase
of (ii) by that lag, with a positive interaction with (iii), adjusted for baseline Cobb and maturity. Stress-modulated
growth: the wedging increment per interval ∝ current curvature × height velocity, with no incremental contribution from
(i) or its lag. Score by patient-held-out predictive performance and calibration for wedging change against the
geometry/maturity prognosis, never by correlation among quantities sharing inputs. Falsifiers: (a) no added predictive
value of (i) → drop the recovery layer; (b) (i) changes only after (ii) → ordering rejected; (c) the growth interaction
vanishes after maturity/treatment adjustment → kg dependence unsupported; (d) identified 1/(kr+kg) shorter than the
visit interval, or kr, kg outside physiological ranges → e unidentifiable and (b) degenerates to (c); (e) handedness:
none of the three produces it without a bias input (§3), so this design cannot test (e) — open.

## 8. References (verification status 2026-09-12)

- Stokes IAF. Analysis and simulation of progressive adolescent scoliosis by biomechanical growth modulation. *Eur Spine
  J* 2007;16(10):1621–1628. doi:10.1007/s00586-007-0442-7. PMID 17653775, PMC2078290. **Verified** (PubMed, Crossref, abstract).
- Stokes IAF, Aronsson DD, Dimock AN, Cortright V, Beck S. Endochondral growth in growth plates of three species at two
  anatomical locations modulated by mechanical compression and tension. *J Orthop Res* 2006;24(6):1327–1334.
  doi:10.1002/jor.20189. PMID 16705695. **Verified; β and its range are from this abstract.**
- Stokes IAF, Spence H, Aronsson DD, Kilmer N. Mechanical modulation of vertebral body growth. Implications for scoliosis
  progression. *Spine* 1996;21(10):1162–1167. doi:10.1097/00007632-199605150-00007. PMID 8727190. **Verified** (PubMed, abstract).
- Stokes IAF, Burwell RG, Dangerfield PH. Biomechanical spinal growth modulation and progressive adolescent scoliosis — a
  test of the 'vicious cycle' pathogenetic hypothesis. *Scoliosis* 2006;1:16. doi:10.1186/1748-7161-1-16. **Verified via
  Crossref**; the card's PMC1636073 was not confirmed (id-converter returned a different 10.1186/1471-… prefix).
- `manuscript/references.bib` keys, **not edited**: `stokes2006hueter` (doi → Crossref 404; title 0 PubMed hits;
  unverified, possibly not a real record); `stokes2002mechanical` (doi → 404; the 1996 title with 2002 *Spine* 27(22)
  volume/pages; PubMed's only Stokes *Spine* 2002 vol 27 record is 27(24):2801–2805, a classification paper — looks
  conflated); `stokes2006biomechanics` (no DOI/volume, unchecked).

Reproduce from `~/life`: `PYTHONPATH=src:. .venv/bin/python scripts/experiments/recovery_comparators/run_comparators.py`;
`PYTHONPATH=src:. .venv/bin/python -m pytest tests/test_recovery_comparators.py -q`.
