from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ProjectConfig


class LayeredForecaster:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.rng = np.random.default_rng(config.random_seed + 999)

    def forecast(self, df: pd.DataFrame, t: int, horizon: int, noise_scale: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        T = len(df)
        load_pred = []
        price_pred = []
        pv_pred = []
        for k in range(horizon):
            idx = min(t + k, T - 1)
            load_pred.append(max(float(df.loc[idx, "load_actual_mw"]) + self.rng.normal(0, self.config.forecast_noise.load_sigma * noise_scale), 0.0))
            price_pred.append(max(float(df.loc[idx, "buy_price_actual"]) + self.rng.normal(0, self.config.forecast_noise.buy_price_sigma * noise_scale), 0.01))
            pv_pred.append(max(float(df.loc[idx, "pv_actual_mw"]) + self.rng.normal(0, self.config.forecast_noise.pv_sigma * noise_scale), 0.0))
        return np.array(load_pred), np.array(price_pred), np.array(pv_pred)

    def forecast_day_ahead(self, df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return self.forecast(df, 0, self.config.day_ahead_horizon, noise_scale=1.2)

    def forecast_intra_day(self, df: pd.DataFrame, t: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return self.forecast(df, t, self.config.intra_day_horizon, noise_scale=0.8)

    def forecast_real_time(self, df: pd.DataFrame, t: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return self.forecast(df, t, self.config.real_time_horizon, noise_scale=0.5)
