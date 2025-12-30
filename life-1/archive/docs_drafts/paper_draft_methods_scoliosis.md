# Methods: Scoliosis Asymmetry Perturbations

## Methods – Thoracic asymmetry perturbation and scoliosis metrics

To probe scoliosis-like symmetry breaking, we introduced a small left–right asymmetry in the model spine. The body axis was discretized as a one-dimensional arc-length coordinate (s \in [0,L]), which we normalized to (\hat{s} \in [0,1]). A localized thoracic bump was defined on this normalized coordinate as

\[
G(\hat{s}) = \exp\left[-\frac{1}{2}\left(\frac{\hat{s} - \hat{s}_0}{\sigma}\right)^2\right],
\]

with center (\hat{s}_0 \approx 0.6) (mid-thoracic levels) and width chosen such that the full width at half maximum spanned approximately 2–3 vertebral levels. In the simplest implementation, an otherwise symmetric information field (I_{\mathrm{sym}}(s)) was perturbed as

\[
I_{\mathrm{asym}}(s) = I_{\mathrm{sym}}(s) + \varepsilon_{\mathrm{asym}} \cdot \Delta I \cdot G(\hat{s}),
\]

where (\Delta I = \max_s I_{\mathrm{sym}}(s) - \min_s I_{\mathrm{sym}}(s)) and (\varepsilon_{\mathrm{asym}}) is a small dimensionless amplitude (typically (\varepsilon_{\mathrm{asym}} \sim 0.05)). In an alternative implementation, a lateral curvature bump (\kappa_{\mathrm{lat}}(s) = \varepsilon_{\mathrm{lat}} G(\hat{s})) was added directly to the coronal component of the Cosserat rod's rest curvature vector, with (\varepsilon_{\mathrm{lat}}) chosen in the range 0.01–0.05 m(^{-1}). Both approaches seeded a controlled, localized asymmetry without otherwise altering the sagittal IEC patterning.

For each simulation, we extracted the coronal-plane centerline coordinates ((z(s), y(s))), where (z) denotes the cranio–caudal axis and (y) the lateral (left–right) direction. A simple lateral scoliosis index was defined as

\[
S_{\mathrm{lat}} = \frac{\max_s |y(s)|}{L_{\mathrm{eff}}},
\]

with (L_{\mathrm{eff}} = \max_s z(s) - \min_s z(s)) the effective longitudinal span. As a Cobb-like angle, we fitted straight lines to the top and bottom fractions of the rod in the ((z,y)) plane using least-squares regression and computed the angle between them. Specifically, linear fits were obtained for the lowest and highest 20% of points; the Cobb-like angle was defined as the absolute difference between the corresponding line orientations. These scoliosis metrics were evaluated for both symmetric ((\varepsilon_{\mathrm{asym}} = 0)) and asymmetric ((\varepsilon_{\mathrm{asym}} > 0)) runs at each point in ((\chi_\kappa, g)) parameter space, and used in combination with the normalized geodesic curvature deviation (\widehat{D}_{\mathrm{geo}}) to classify gravity-dominated, cooperative, and scoliosis-like regimes.

---

## LaTeX Source

```latex
\subsection{Thoracic asymmetry perturbation and scoliosis metrics}

To probe scoliosis-like symmetry breaking, we introduced a small left--right asymmetry in the model spine. The body axis was discretized as a one-dimensional arc-length coordinate $s \in [0,L]$, which we normalized to $\hat{s} \in [0,1]$. A localized thoracic bump was defined on this normalized coordinate as
\begin{equation}
G(\hat{s}) = \exp\left[-\frac{1}{2}\left(\frac{\hat{s} - \hat{s}_0}{\sigma}\right)^2\right],
\end{equation}
with center $\hat{s}_0 \approx 0.6$ (mid-thoracic levels) and width chosen such that the full width at half maximum spanned approximately 2--3 vertebral levels. In the simplest implementation, an otherwise symmetric information field $I_{\mathrm{sym}}(s)$ was perturbed as
\begin{equation}
I_{\mathrm{asym}}(s) = I_{\mathrm{sym}}(s) + \varepsilon_{\mathrm{asym}} \cdot \Delta I \cdot G(\hat{s}),
\end{equation}
where $\Delta I = \max_s I_{\mathrm{sym}}(s) - \min_s I_{\mathrm{sym}}(s)$ and $\varepsilon_{\mathrm{asym}}$ is a small dimensionless amplitude (typically $\varepsilon_{\mathrm{asym}} \sim 0.05$). In an alternative implementation, a lateral curvature bump $\kappa_{\mathrm{lat}}(s) = \varepsilon_{\mathrm{lat}} G(\hat{s})$ was added directly to the coronal component of the Cosserat rod's rest curvature vector, with $\varepsilon_{\mathrm{lat}}$ chosen in the range 0.01--0.05 m$^{-1}$. Both approaches seeded a controlled, localized asymmetry without otherwise altering the sagittal IEC patterning.

For each simulation, we extracted the coronal-plane centerline coordinates $(z(s), y(s))$, where $z$ denotes the cranio--caudal axis and $y$ the lateral (left--right) direction. A simple lateral scoliosis index was defined as
\begin{equation}
S_{\mathrm{lat}} = \frac{\max_s |y(s)|}{L_{\mathrm{eff}}},
\end{equation}
with $L_{\mathrm{eff}} = \max_s z(s) - \min_s z(s)$ the effective longitudinal span. As a Cobb-like angle, we fitted straight lines to the top and bottom fractions of the rod in the $(z,y)$ plane using least-squares regression and computed the angle between them. Specifically, linear fits were obtained for the lowest and highest 20\% of points; the Cobb-like angle was defined as the absolute difference between the corresponding line orientations. These scoliosis metrics were evaluated for both symmetric ($\varepsilon_{\mathrm{asym}} = 0$) and asymmetric ($\varepsilon_{\mathrm{asym}} > 0$) runs at each point in $(\chi_\kappa, g)$ parameter space, and used in combination with the normalized geodesic curvature deviation $\widehat{D}_{\mathrm{geo}}$ to classify gravity-dominated, cooperative, and scoliosis-like regimes.
```

---

## Key Points

1. **Thoracic bump**: Gaussian centered at ŝ₀ ≈ 0.6 (mid-thoracic), FWHM spans 2–3 vertebral levels
2. **Asymmetry formula**: I_asym = I_sym + ε_asym · ΔI · G(ŝ), with ε_asym ~ 0.05
3. **Alternative**: Lateral curvature bump κ_lat(s) = ε_lat G(ŝ), with ε_lat ∈ [0.01, 0.05] m⁻¹
4. **Scoliosis index**: S_lat = max_s |y(s)| / L_eff (dimensionless)
5. **Cobb-like angle**: Angle between linear fits to top and bottom 20% segments in coronal plane
6. **Regime classification**: Based on D̂_geo, S_lat, and Cobb-like angle differences

