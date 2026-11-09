"""Render the verified, normalized material scenarios with Matplotlib."""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUT = Path(__file__).resolve().parent


def main():
    with (OUT / "recoil_sensitivity.csv").open(newline="") as stream:
        rows = [{key: float(value) for key, value in row.items()}
                for row in csv.DictReader(stream)]
    with (OUT / "recoil_tension_only.csv").open(newline="") as stream:
        tension_rows = [{key: float(value) for key, value in row.items()}
                        for row in csv.DictReader(stream)]
    selected = [row for row in rows if row["load_duration_over_tau"] == 0.1
                and row["unload_duration_over_tau"] == 0.1]
    selected_tension = [row for row in tension_rows
                        if row["load_duration_over_tau"] == 0.1
                        and row["unload_duration_over_tau"] == 0.1]
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 5.8))
    colors = ("#aa3377", "#cc8844", "#4477aa", "#228833", "#555555")
    for fraction, color in zip((0.0, 0.25, 0.5, 0.75, 1.0), colors):
        group = sorted((row for row in selected if row["equilibrium_stiffness_fraction"] == fraction),
                       key=lambda row: row["hold_duration_over_tau"])
        pauses = [row["hold_duration_over_tau"] for row in group]
        axes[0].plot(pauses, [row["net_return_over_loading_work"] for row in group],
                     "o-", color=color, label=f"{fraction:g}")
        axes[1].plot(pauses, [row["complete_cycle_loss_normalized"]/row["loading_work_normalized"]
                             for row in group], "o-", color=color)
    for fraction, color in zip((0.0, 0.25, 0.5, 0.75, 1.0), colors):
        group = sorted((row for row in selected_tension
                        if row["equilibrium_stiffness_fraction"] == fraction),
                       key=lambda row: row["hold_duration_over_tau"])
        pauses = [row["hold_duration_over_tau"] for row in group]
        axes[2].plot(pauses, [row["net_return_over_loading_work_tension_only"]
                             for row in group], "o-", color=color, label=f"{fraction:g}")
    for ax in axes:
        ax.set_xscale("symlog", linthresh=0.25)
        ax.set_xticks((0.0, 0.25, 1.0, 5.0, 20.0), labels=("0", "0.25", "1", "5", "20"))
        ax.set_xlabel("Hold duration / relaxation time (t / τ)")
        ax.grid(alpha=0.25)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].axhline(0, color="black", lw=0.8)
    axes[0].set_ylabel("Net unloading return / loading work")
    axes[0].set_title("A. Signed linear model")
    axes[0].legend(title="Equilibrium stiffness fraction", loc="lower left", fontsize=9)
    axes[1].set_ylabel("Complete-cycle passive loss / loading work")
    axes[1].set_title("B. Energy balance retains all losses")
    axes[2].axhline(0, color="black", lw=0.8)
    axes[2].set_ylim(-0.02, 1.02)
    axes[2].set_ylabel("Net unloading return / loading work")
    axes[2].set_title("C. Tension-only variant (unloading stops at slack)")
    fig.suptitle("Passive recoil: illustrative material model", fontsize=16)
    fig.text(0.5, 0.895, "No human parameters, metabolic savings, or longevity predictions", ha="center", fontsize=11)
    fig.text(0.06, 0.05,
             "Loading and unloading durations = 0.1 τ. Deformation is prescribed; points are computed scenarios.\n"
             "Panel A: signed model permits compression; negative net return means unloading needs net work input.\n"
             "Panel C: the tension-only element unloads only to the slack point; no scenario requires net work input.",
             fontsize=9)
    fig.subplots_adjust(top=0.80, bottom=0.26, left=0.07, right=0.98, wspace=0.26)
    fig.savefig(OUT / "recoil_sensitivity.svg")
    fig.savefig(OUT / "recoil_sensitivity.png", dpi=180)
    plt.close(fig)
    print("Rendered recoil_sensitivity.svg/png from 25 signed and 25 tension-only verified scenarios.")


if __name__ == "__main__":
    main()
