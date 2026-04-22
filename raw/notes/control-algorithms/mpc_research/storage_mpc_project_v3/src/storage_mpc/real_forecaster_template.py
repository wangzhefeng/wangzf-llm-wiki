from __future__ import annotations

import numpy as np


class RealForecasterTemplate:
    """真实预测器接口模板。

    你可以在这里接入自己的模型，例如：
    - 负荷预测模型
    - 电价预测模型
    - 光伏预测模型
    - 日前/日内计划生成模型

    统一输出长度为 horizon 的 4 个序列：
    1. load_pred
    2. buy_price_pred
    3. pv_pred
    4. grid_buy_plan_pred
    """

    def forecast(self, features: dict, horizon: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        raise NotImplementedError("请在此接入你自己的真实预测模型。")
