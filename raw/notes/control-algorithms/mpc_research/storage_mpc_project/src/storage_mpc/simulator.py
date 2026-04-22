from __future__ import annotations

import pandas as pd

from .config import ProjectConfig
from .forecaster import NaiveRollingForecaster
from .mpc_controller import StorageMPCController


def run_closed_loop_simulation(
    df_actual: pd.DataFrame,
    config: ProjectConfig,
) -> pd.DataFrame:
    controller = StorageMPCController(config)
    forecaster = NaiveRollingForecaster(config)

    T = len(df_actual)
    N = config.mpc_horizon
    dt = config.dt_hours
    batt = config.battery

    soc = batt.soc_init
    p_prev = 0.0
    rows = []

    for t in range(T):
        load_pred, price_pred = forecaster.forecast(df_actual, t, N)

        solution = controller.solve(
            soc_current=soc,
            p_prev=p_prev,
            load_forecast_mw=load_pred,
            price_forecast=price_pred,
        )

        p_batt = solution.p_batt_first
        load_actual = float(df_actual.loc[t, "load_actual_mw"])
        price_actual = float(df_actual.loc[t, "price_actual"])
        p_grid = max(load_actual - p_batt, 0.0)
        stage_cost = price_actual * p_grid * dt

        soc_next = soc - (dt / batt.energy_capacity_mwh) * p_batt
        soc_next = min(max(soc_next, batt.soc_min), batt.soc_max)

        rows.append({
            "time_index": int(df_actual.loc[t, "time_index"]),
            "hour_of_day": float(df_actual.loc[t, "hour_of_day"]),
            "load_actual_mw": load_actual,
            "load_forecast_mw": float(load_pred[0]),
            "price_actual": price_actual,
            "price_forecast": float(price_pred[0]),
            "soc": soc,
            "soc_next": soc_next,
            "p_batt_mw": p_batt,
            "p_grid_mw": p_grid,
            "objective_value": solution.objective_value,
            "stage_cost": stage_cost,
        })

        soc = soc_next
        p_prev = p_batt

    return pd.DataFrame(rows)
