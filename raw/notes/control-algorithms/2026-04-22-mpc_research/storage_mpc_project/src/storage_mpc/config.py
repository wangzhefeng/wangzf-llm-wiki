from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class BatteryConfig:
    energy_capacity_mwh: float
    power_min_mw: float
    power_max_mw: float
    soc_init: float
    soc_min: float
    soc_max: float
    soc_ref: float


@dataclass
class WeightsConfig:
    lambda_soc: float
    lambda_u: float
    lambda_delta_u: float
    lambda_terminal: float


@dataclass
class ForecastNoiseConfig:
    load_sigma: float
    price_sigma: float


@dataclass
class ProjectConfig:
    simulation_horizon: int
    mpc_horizon: int
    dt_hours: float
    battery: BatteryConfig
    weights: WeightsConfig
    random_seed: int
    forecast_noise: ForecastNoiseConfig


def load_config(config_path: str | Path) -> ProjectConfig:
    path = Path(config_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return ProjectConfig(
        simulation_horizon=data["simulation_horizon"],
        mpc_horizon=data["mpc_horizon"],
        dt_hours=data["dt_hours"],
        battery=BatteryConfig(**data["battery"]),
        weights=WeightsConfig(**data["weights"]),
        random_seed=data["random_seed"],
        forecast_noise=ForecastNoiseConfig(**data["forecast_noise"]),
    )
