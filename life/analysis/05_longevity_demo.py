import matplotlib
matplotlib.use("Agg")
"""Synthetic longevity demo: sit-to-stand frequency vs survival."""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    from lifelines import CoxPHFitter, KaplanMeierFitter
except Exception as e:
    raise SystemExit(
        "lifelines is required for the longevity demo. "
        "Install with: pip install lifelines  (CI uses Makefile: make env)"
    ) from e

from spinalmodes.utils.provenance import write_provenance
from spinalmodes.utils.seeds import set_seed


def synth_cohort(n: int = 10000) -> pd.DataFrame:
    """Generate clearly marked synthetic cohort."""
    age = np.random.normal(60, 12, n).clip(35, 90)
    sit2stand = np.random.poisson(25, n)
    male = np.random.binomial(1, 0.55, n)
    bmi = np.random.normal(24, 3.5, n).clip(17, 38)
    baseline_hazard = 0.01 + 0.0005 * (age - 60) + 0.0002 * (bmi - 24) + 0.002 * male
    hazard = baseline_hazard * np.exp(-0.01 * (sit2stand - 20))
    t = np.random.exponential(1 / hazard)
    cens = np.random.binomial(1, 0.7, n)  # 70% censored
    time = np.minimum(t, 10.0)
    event = (t <= 10.0) * (1 - cens)
    return pd.DataFrame(
        dict(time=time, event=event, age=age, male=male, bmi=bmi, sit2stand=sit2stand)
    )


def main() -> None:
    set_seed(1337)
    df = synth_cohort()
    Path("tables").mkdir(parents=True, exist_ok=True)
    df.to_csv("tables/longevity_synthetic.csv", index=False)

    df["tertile"] = pd.qcut(df["sit2stand"], 3, labels=["low", "mid", "high"])
    km = KaplanMeierFitter()
    plt.figure()
    for g in ["low", "mid", "high"]:
        km.fit(df.loc[df.tertile == g, "time"], df.loc[df.tertile == g, "event"], label=g)
        km.plot(ci_show=False)
    plt.title("SYNTHETIC—ILLUSTRATIVE: Survival by sit-to-stand tertile")
    plt.xlabel("years")
    plt.ylabel("S(t)")
    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig("figures/km_curves.pdf", bbox_inches="tight")

    cph = CoxPHFitter()
    cph.fit(df[["time", "event", "age", "male", "bmi", "sit2stand"]], duration_col="time", event_col="event")
    cph.summary.to_csv("tables/cox_results.csv")
    write_provenance("tables/cox_results.provenance.json", 1337, {"n": len(df)})
    print(cph.summary)


if __name__ == "__main__":
    main()
