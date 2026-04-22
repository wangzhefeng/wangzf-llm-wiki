from __future__ import annotations

import numpy as np
import pandas as pd


class DayAheadPlanner:
    """简化日前计划器。

    这里不追求最复杂求解，而是生成一条比较平滑的日前购电/储能参考轨迹，
    供日内层与实时层跟踪和修正。
    """

    def build_plan(
        self,
        load_pred: np.ndarray,
        price_pred: np.ndarray,
        pv_pred: np.ndarray,
    ) -> pd.DataFrame:
        net_load = np.maximum(load_pred - pv_pred, 0.0)

        # 简单策略：低价时段倾向充电，高价时段倾向放电
        price_threshold_low = np.quantile(price_pred, 0.35)
        price_threshold_high = np.quantile(price_pred, 0.75)

        p_batt_ref = np.zeros_like(price_pred)
        for i, price in enumerate(price_pred):
            if price <= price_threshold_low:
                p_batt_ref[i] = -2.5
            elif price >= price_threshold_high:
                p_batt_ref[i] = 2.5

        grid_buy_plan = np.maximum(net_load - p_batt_ref, 0.0)

        return pd.DataFrame({
            "time_index": np.arange(len(price_pred)),
            "load_pred_mw": load_pred,
            "price_pred": price_pred,
            "pv_pred_mw": pv_pred,
            "p_batt_ref_mw": p_batt_ref,
            "grid_buy_plan_mw": grid_buy_plan,
        })
