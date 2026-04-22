from __future__ import annotations

import pandas as pd

from .config import ProjectConfig
from .forecaster import NaiveRollingForecaster
from .mpc_controller import StorageMPCController


def run_closed_loop_simulation(df_actual: pd.DataFrame, config: ProjectConfig) -> pd.DataFrame:
    forecaster = NaiveRollingForecaster(config)
    controller = StorageMPCController(config)

    batt = config.battery
    dt = config.dt_hours
    T = len(df_actual)
    N = config.mpc_horizon
    sell_discount = config.market.sell_price_discount

    soc = batt.soc_init
    p_ch_prev = 0.0
    p_dis_prev = 0.0
    rows = []

    for t in range(T):
        load_pred, buy_price_pred, pv_pred = forecaster.forecast(df_actual, t, N)

        sol = controller.solve(
            soc_current=soc,
            p_ch_prev=p_ch_prev,
            p_dis_prev=p_dis_prev,
            load_forecast_mw=load_pred,
            buy_price_forecast=buy_price_pred,
            pv_forecast_mw=pv_pred,
        )

        load_actual = float(df_actual.loc[t, "load_actual_mw"])
        buy_price_actual = float(df_actual.loc[t, "buy_price_actual"])
        sell_price_actual = sell_discount * buy_price_actual
        pv_actual = float(df_actual.loc[t, "pv_actual_mw"])

        p_ch = sol.p_ch_first
        p_dis = sol.p_dis_first
        net_without_grid = p_dis - p_ch + pv_actual
        residual = load_actual - net_without_grid
        p_buy = max(residual, 0.0)
        p_sell = max(-residual, 0.0)

        stage_cost = buy_price_actual * p_buy * dt - sell_price_actual * p_sell * dt

        soc_next = soc + (batt.charge_efficiency * dt / batt.energy_capacity_mwh) * p_ch             - (dt / (batt.discharge_efficiency * batt.energy_capacity_mwh)) * p_dis
        soc_next = min(max(soc_next, batt.soc_min), batt.soc_max)

        rows.append({
            "time_index": int(df_actual.loc[t, "time_index"]),
            "hour_of_day": float(df_actual.loc[t, "hour_of_day"]),
            "load_actual_mw": load_actual,
            "buy_price_actual": buy_price_actual,
            "sell_price_actual": sell_price_actual,
            "pv_actual_mw": pv_actual,
            "soc": soc,
            "soc_next": soc_next,
            "p_charge_mw": p_ch,
            "p_discharge_mw": p_dis,
            "p_buy_mw": p_buy,
            "p_sell_mw": p_sell,
            "objective_value": sol.objective_value,
            "stage_cost": stage_cost,
        })

        soc = soc_next
        p_ch_prev = p_ch
        p_dis_prev = p_dis

    return pd.DataFrame(rows)
