from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ProjectConfig


def generate_synthetic_data(config: ProjectConfig) -> pd.DataFrame:
    T = config.simulation_horizon
    dt = config.dt_hours
    rng = np.random.default_rng(config.random_seed)

    time_index = np.arange(T)
    hour_of_day = (time_index * dt) % 24

    base_load = 18.0 + 3.5 * np.sin(2 * np.pi * (hour_of_day - 7) / 24)
    morning_bump = 2.0 * np.exp(-0.5 * ((hour_of_day - 10) / 2.0) ** 2)
    evening_bump = 4.0 * np.exp(-0.5 * ((hour_of_day - 19) / 2.4) ** 2)
    load_noise = rng.normal(0, 0.35, size=T)
    load_actual = np.clip(base_load + morning_bump + evening_bump + load_noise, 6.0, None)

    buy_price = 0.50 + 0.07 * np.sin(2 * np.pi * (hour_of_day - 14) / 24)
    buy_price += 0.18 * np.exp(-0.5 * ((hour_of_day - 19) / 2.5) ** 2)
    buy_price -= 0.05 * np.exp(-0.5 * ((hour_of_day - 4) / 1.8) ** 2)
    buy_price += rng.normal(0, 0.01, size=T)
    buy_price = np.clip(buy_price, 0.12, None)

    pv_profile = 5.5 * np.exp(-0.5 * ((hour_of_day - 12) / 2.6) ** 2)
    pv_profile += rng.normal(0, 0.15, size=T)
    pv_actual = np.clip(pv_profile, 0.0, None)

    return pd.DataFrame({
        "time_index": time_index,
        "hour_of_day": hour_of_day,
        "load_actual_mw": load_actual,
        "buy_price_actual": buy_price,
        "pv_actual_mw": pv_actual,
    })
