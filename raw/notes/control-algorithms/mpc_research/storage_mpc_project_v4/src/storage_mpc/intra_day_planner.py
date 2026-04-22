from __future__ import annotations

import numpy as np
import pandas as pd


class IntraDayPlanner:
    """日内修正器。

    输入：
    - 日前计划片段
    - 更新预测

    输出：
    - 修正后的短期 grid_buy 参考
    - 修正后的短期电池功率参考
    """

    def refine_plan(
        self,
        day_ahead_slice: pd.DataFrame,
        load_pred: np.ndarray,
        price_pred: np.ndarray,
        pv_pred: np.ndarray,
    ) -> pd.DataFrame:
        refined = day_ahead_slice.copy().reset_index(drop=True)

        net_load = np.maximum(load_pred - pv_pred, 0.0)
        batt_ref = refined["p_batt_ref_mw"].to_numpy(copy=True)

        # 简化修正逻辑：若价格更高，则增强放电参考；若价格更低，则增强充电参考
        med = float(np.median(price_pred))
        for i in range(len(batt_ref)):
            if price_pred[i] > med * 1.08:
                batt_ref[i] += 1.0
            elif price_pred[i] < med * 0.92:
                batt_ref[i] -= 1.0

        batt_ref = np.clip(batt_ref, -4.0, 4.0)
        grid_buy_ref = np.maximum(net_load - batt_ref, 0.0)

        refined["load_pred_mw"] = load_pred
        refined["price_pred"] = price_pred
        refined["pv_pred_mw"] = pv_pred
        refined["p_batt_ref_mw"] = batt_ref
        refined["grid_buy_refined_mw"] = grid_buy_ref
        return refined
