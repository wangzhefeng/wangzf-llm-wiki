from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ProjectConfig


class NaiveRollingForecaster:
    """简单滚动预测器占位实现，可替换成真实 TS 模型。"""

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.rng = np.random.default_rng(config.random_seed + 1000)

    def forecast(self, df: pd.DataFrame, t: int, horizon: int) -> tuple[np.ndarray, np.ndarray]:
        T = len(df)
        load_pred = []
        price_pred = []

        for k in range(horizon):
            idx = min(t + k, T - 1)
            load_hat = float(df.loc[idx, "load_actual_mw"]) + self.rng.normal(
                0, self.config.forecast_noise.load_sigma
            )
            price_hat = float(df.loc[idx, "price_actual"]) + self.rng.normal(
                0, self.config.forecast_noise.price_sigma
            )
            load_pred.append(max(load_hat, 0.0))
            price_pred.append(max(price_hat, 0.01))

        return np.array(load_pred), np.array(price_pred)
