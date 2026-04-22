from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ProjectConfig


class NaiveRollingForecaster:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.rng = np.random.default_rng(config.random_seed + 1000)

    def forecast(self, df: pd.DataFrame, t: int, horizon: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        T = len(df)
        load_pred = []
        buy_price_pred = []
        pv_pred = []

        for k in range(horizon):
            idx = min(t + k, T - 1)
            load_hat = float(df.loc[idx, "load_actual_mw"]) + self.rng.normal(0, self.config.forecast_noise.load_sigma)
            price_hat = float(df.loc[idx, "buy_price_actual"]) + self.rng.normal(0, self.config.forecast_noise.buy_price_sigma)
            pv_hat = float(df.loc[idx, "pv_actual_mw"]) + self.rng.normal(0, self.config.forecast_noise.pv_sigma)

            load_pred.append(max(load_hat, 0.0))
            buy_price_pred.append(max(price_hat, 0.01))
            pv_pred.append(max(pv_hat, 0.0))

        return np.array(load_pred), np.array(buy_price_pred), np.array(pv_pred)
