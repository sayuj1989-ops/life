from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


@dataclass(frozen=True)
class IOConfig:
    results_dir: Path
    figures_dir: Path


@dataclass(frozen=True)
class SimulationConfig:
    seed: int
    n_nodes: int
    length: float
    gravity: float


@dataclass(frozen=True)
class MaterialConfig:
    B0: float
    rhoA: float


@dataclass(frozen=True)
class InfoProfileConfig:
    cervical_center: float
    lumbar_center: float
    sigma: float
    thoracic_center: float
    thoracic_sigma: float
    thoracic_depth: float


@dataclass(frozen=True)
class IECConfig:
    chi_kappa: float
    chi_g: float
    chi_E: float
    info_profile: InfoProfileConfig


@dataclass(frozen=True)
class SweepsConfig:
    gravity_values: list[float]
    chi_kappa_values: list[float]


@dataclass(frozen=True)
class FiguresConfig:
    fmt: str
    dpi: int
    n_modes_plot: int


@dataclass(frozen=True)
class BCCConfig:
    io: IOConfig
    simulation: SimulationConfig
    material: MaterialConfig
    iec: IECConfig
    sweeps: SweepsConfig
    figures: FiguresConfig


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


def _as_path(p: Any) -> Path:
    return p if isinstance(p, Path) else Path(str(p))


def load_bcc_config(path: str | Path) -> BCCConfig:
    """Load the primary simulation/figure config."""
    if yaml is None:
        raise RuntimeError("PyYAML is required. Install dependencies via `make deps`.")

    cfg_path = _as_path(path)
    data = yaml.safe_load(cfg_path.read_text())

    io = IOConfig(
        results_dir=_as_path(data["io"]["results_dir"]),
        figures_dir=_as_path(data["io"]["figures_dir"]),
    )

    sim = SimulationConfig(
        seed=int(data["simulation"]["seed"]),
        n_nodes=int(data["simulation"]["n_nodes"]),
        length=float(data["simulation"]["length"]),
        gravity=float(data["simulation"]["gravity"]),
    )
    _require(sim.n_nodes >= 21, "simulation.n_nodes too small")

    mat = MaterialConfig(
        B0=float(data["material"]["B0"]),
        rhoA=float(data["material"]["rhoA"]),
    )

    ip = InfoProfileConfig(
        cervical_center=float(data["iec"]["info_profile"]["cervical_center"]),
        lumbar_center=float(data["iec"]["info_profile"]["lumbar_center"]),
        sigma=float(data["iec"]["info_profile"]["sigma"]),
        thoracic_center=float(data["iec"]["info_profile"]["thoracic_center"]),
        thoracic_sigma=float(data["iec"]["info_profile"]["thoracic_sigma"]),
        thoracic_depth=float(data["iec"]["info_profile"]["thoracic_depth"]),
    )

    iec = IECConfig(
        chi_kappa=float(data["iec"]["chi_kappa"]),
        chi_g=float(data["iec"]["chi_g"]),
        chi_E=float(data["iec"]["chi_E"]),
        info_profile=ip,
    )

    sweeps = SweepsConfig(
        gravity_values=[float(x) for x in data["sweeps"]["gravity"]["values"]],
        chi_kappa_values=[float(x) for x in data["sweeps"]["chi_kappa"]["values"]],
    )

    figs = FiguresConfig(
        fmt=str(data["figures"]["fmt"]).lower(),
        dpi=int(data["figures"]["dpi"]),
        n_modes_plot=int(data["figures"]["n_modes_plot"]),
    )
    _require(figs.fmt in {"png", "pdf"}, "figures.fmt must be 'png' or 'pdf'")

    return BCCConfig(io=io, simulation=sim, material=mat, iec=iec, sweeps=sweeps, figures=figs)


