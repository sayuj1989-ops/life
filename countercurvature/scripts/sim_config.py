"""Configuration system for Biological Countercurvature simulations."""

import os
import json
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class RodConfig:
    """Rod material and geometric parameters."""
    length: float = 1.0
    discretization: int = 100
    radius: float = 0.01
    density: float = 1000.0
    young_modulus: float = 1e9
    shear_modulus: float = 0.4


@dataclass
class GravityConfig:
    """Gravity parameters."""
    earth_value: float = 9.81
    sweep_range: List[float] = field(default_factory=lambda: [0.01, 0.1, 0.2, 0.5, 1.0])


@dataclass
class IECConfig:
    """Information-Elasticity Coupling parameters."""
    chi_kappa: float = 0.05
    chi_g: float = 0.02
    chi_E: float = 0.1
    sweep_range: List[float] = field(default_factory=lambda: [0.0, 0.01, 0.02, 0.05, 0.1])


@dataclass
class SimulationConfig:
    """Complete simulation configuration."""
    rod: RodConfig = field(default_factory=RodConfig)
    gravity_multiplier: float = 1.0
    iec: IECConfig = field(default_factory=IECConfig)
    random_seed: int = 42

    @classmethod
    def from_dict(cls, config_dict: dict) -> "SimulationConfig":
        """Load configuration from dictionary."""
        return cls(
            rod=RodConfig(**config_dict.get('rod', {})),
            gravity_multiplier=config_dict.get('gravity_multiplier', 1.0),
            iec=IECConfig(**config_dict.get('iec', {})),
            random_seed=config_dict.get('random_seed', 42)
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


def get_default_config() -> SimulationConfig:
    """Get default configuration."""
    return SimulationConfig()
