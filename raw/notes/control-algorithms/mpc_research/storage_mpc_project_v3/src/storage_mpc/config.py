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
    lambda_peak: float
    lambda_dev: float


@dataclass
class ForecastNoiseConfig:
    load_sigma: float
    buy_price_sigma: float
    pv_sigma: float
    plan_sigma: float


@dataclass
class ProjectConfig:
    simulation_horizon: int
    mpc_horizon: int
    dt_hours: float
    use_mutual_exclusion_binary: bool
    enable_peak_penalty: bool
    enable_deviation_penalty: bool
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
        mpc_horizon=data["mpc_horizon"],
        dt_hours=data["dt_hours"],
        use_mutual_exclusion_binary=data["use_mutual_exclusion_binary"],
        enable_peak_penalty=data["enable_peak_penalty"],
        enable_deviation_penalty=data["enable_deviation_penalty"],
        battery=BatteryConfig(**data["battery"]),
        market=MarketConfig(**data["market"]),
        weights=WeightsConfig(**data["weights"]),
        random_seed=data["random_seed"],
        forecast_noise=ForecastNoiseConfig(**data["forecast_noise"]),
    )
