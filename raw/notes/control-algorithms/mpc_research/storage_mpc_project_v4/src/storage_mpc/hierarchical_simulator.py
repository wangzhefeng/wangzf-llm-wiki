from __future__ import annotations

from pathlib import Path
import pandas as pd

from .config import ProjectConfig
from .forecaster import LayeredForecaster
from .day_ahead_planner import DayAheadPlanner
from .intra_day_planner import IntraDayPlanner
from .real_time_mpc import RealTimeMPCController


def run_hierarchical_simulation(
    df_actual: pd.DataFrame,
    config: ProjectConfig,
    output_dir: str | Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    output_dir = Path(output_dir)
    forecaster = LayeredForecaster(config)
    day_planner = DayAheadPlanner()
    intra_planner = IntraDayPlanner()
    rt_controller = RealTimeMPCController(config)

    day_load, day_price, day_pv = forecaster.forecast_day_ahead(df_actual)
    day_ahead_plan = day_planner.build_plan(day_load, day_price, day_pv)

    T = len(df_actual)
    batt = config.battery
    soc = batt.soc_init
    p_ch_prev = 0.0
    p_dis_prev = 0.0

    intra_rows = []
    rt_rows = []

    for t in range(T):
        intra_load, intra_price, intra_pv = forecaster.forecast_intra_day(df_actual, t)
        rt_load, rt_price, rt_pv = forecaster.forecast_real_time(df_actual, t)

        day_slice = day_ahead_plan.iloc[t:t + config.intra_day_horizon].copy()
        if len(day_slice) < config.intra_day_horizon:
            last = day_slice.iloc[-1:]
            while len(day_slice) < config.intra_day_horizon:
                day_slice = pd.concat([day_slice, last], ignore_index=True)

        intra_plan = intra_planner.refine_plan(day_slice, intra_load, intra_price, intra_pv)
        intra_rows.append(
            intra_plan.assign(global_time_index=t)
        )

        grid_buy_ref = intra_plan["grid_buy_refined_mw"].to_numpy()[:config.real_time_horizon]
        if len(grid_buy_ref) < config.real_time_horizon:
            pad = [grid_buy_ref[-1]] * (config.real_time_horizon - len(grid_buy_ref))
            grid_buy_ref = list(grid_buy_ref) + pad

        sol = rt_controller.solve(
            soc_current=soc,
            p_ch_prev=p_ch_prev,
            p_dis_prev=p_dis_prev,
            load_forecast_mw=rt_load,
            buy_price_forecast=rt_price,
            pv_forecast_mw=rt_pv,
            grid_buy_ref_mw=grid_buy_ref,
        )

        load_actual = float(df_actual.loc[t, "load_actual_mw"])
        buy_price_actual = float(df_actual.loc[t, "buy_price_actual"])
        sell_price_actual = config.market.sell_price_discount * buy_price_actual
        pv_actual = float(df_actual.loc[t, "pv_actual_mw"])

        p_ch = sol.p_ch_first
        p_dis = sol.p_dis_first
        net_without_grid = p_dis - p_ch + pv_actual
        residual = load_actual - net_without_grid
        p_buy = max(residual, 0.0)
        p_sell = max(-residual, 0.0)

        energy_cost = buy_price_actual * p_buy * config.dt_hours - sell_price_actual * p_sell * config.dt_hours
        plan_track_error = p_buy - float(intra_plan.iloc[0]["grid_buy_refined_mw"])
        plan_track_cost = config.weights.lambda_plan_track * plan_track_error ** 2

        soc_next = soc + (batt.charge_efficiency * config.dt_hours / batt.energy_capacity_mwh) * p_ch             - (config.dt_hours / (batt.discharge_efficiency * batt.energy_capacity_mwh)) * p_dis
        soc_next = min(max(soc_next, batt.soc_min), batt.soc_max)

        rt_rows.append({
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
            "energy_cost": energy_cost,
            "plan_track_cost": plan_track_cost,
            "stage_cost": energy_cost + plan_track_cost,
            "objective_value": sol.objective_value,
        })

        soc = soc_next
        p_ch_prev = p_ch
        p_dis_prev = p_dis

    day_ahead_plan.to_csv(output_dir / "day_ahead_plan.csv", index=False, encoding="utf-8-sig")
    intra_df = pd.concat(intra_rows, ignore_index=True)
    intra_df.to_csv(output_dir / "intra_day_plan_trace.csv", index=False, encoding="utf-8-sig")
    rt_df = pd.DataFrame(rt_rows)
    rt_df.to_csv(output_dir / "real_time_results.csv", index=False, encoding="utf-8-sig")

    return day_ahead_plan, intra_df, rt_df
