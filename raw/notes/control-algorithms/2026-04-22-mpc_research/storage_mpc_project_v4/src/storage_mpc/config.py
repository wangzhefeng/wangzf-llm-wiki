from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class BatteryConfig:
    energy_capacity_mwh: float
    charge_power_max_mw: float
    discharge_power_max_mw: float
    charge_efficiency: float
    discharge_efficiency: float
    soc_init: float
    soc_min: float
    soc_max: float
    soc_ref: float


@dataclass
class MarketConfig:
    sell_price_discount: float


@dataclass
class WeightsConfig:
    lambda_soc: float
    lambda_deg: float
    lambda_delta_u: float
    lambda_terminal: float
    lambda_plan_track: float


@dataclass
class ForecastNoiseConfig:
    load_sigma: float
    buy_price_sigma: float
    pv_sigma: float


@dataclass
class ProjectConfig:
    simulation_horizon: int
    day_ahead_horizon: int
    intra_day_horizon: int
    real_time_horizon: int
    dt_hours: float
    battery: BatteryConfig
    market: MarketConfig
    weights: WeightsConfig
    random_seed: int
    forecast_noise: ForecastNoiseConfig


def load_config(config_path: str | Path) -> ProjectConfig:
    path = Path(config_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return ProjectConfig(
        simulation_horizon=data["simulation_horizon"],
        day_ahead_horizon=data["day_ahead_horizon"],
        intra_day_horizon=data["intra_day_horizon"],
        real_time_horizon=data["real_time_horizon"],
        dt_hours=data["dt_hours"],
        battery=BatteryConfig(**data["battery"]),
        market=MarketConfig(**data["market"]),
        weights=WeightsConfig(**data["weights"]),
        random_seed=data["random_seed"],
        forecast_noise=ForecastNoiseConfig(**data["forecast_noise"]),
    )
