from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ProjectConfig


def generate_synthetic_data(config: ProjectConfig) -> pd.DataFrame:
    """生成一个可直接用于 MPC 仿真的合成数据集。"""
    T = config.simulation_horizon
    dt = config.dt_hours
    rng = np.random.default_rng(config.random_seed)

    time_index = np.arange(T)
    hour_of_day = (time_index * dt) % 24

    base_load = 20.0 + 4.0 * np.sin(2 * np.pi * (hour_of_day - 7) / 24)
    morning_bump = 2.0 * np.exp(-0.5 * ((hour_of_day - 10) / 2.0) ** 2)
    evening_bump = 3.5 * np.exp(-0.5 * ((hour_of_day - 19) / 2.5) ** 2)
    noise_load = rng.normal(0, 0.35, size=T)
    load_actual = np.clip(base_load + morning_bump + evening_bump + noise_load, 8.0, None)

    base_price = 0.52 + 0.08 * np.sin(2 * np.pi * (hour_of_day - 14) / 24)
    peak_price = 0.20 * np.exp(-0.5 * ((hour_of_day - 19) / 2.5) ** 2)
    valley_price = -0.05 * np.exp(-0.5 * ((hour_of_day - 4) / 2.0) ** 2)
    noise_price = rng.normal(0, 0.01, size=T)
    price_actual = np.clip(base_price + peak_price + valley_price + noise_price, 0.15, None)

    return pd.DataFrame({
        "time_index": time_index,
        "hour_of_day": hour_of_day,
        "load_actual_mw": load_actual,
        "price_actual": price_actual,
    })
