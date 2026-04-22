from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import cvxpy as cp

from .config import ProjectConfig


@dataclass
class MPCSolution:
    p_ch_first: float
    p_dis_first: float
    p_buy_first: float
    p_sell_first: float
    soc_plan: np.ndarray
    objective_value: float


class StorageMPCController:
    def __init__(self, config: ProjectConfig):
        self.config = config

    def solve(
        self,
        soc_current: float,
        p_ch_prev: float,
        p_dis_prev: float,
        load_forecast_mw: np.ndarray,
        buy_price_forecast: np.ndarray,
        pv_forecast_mw: np.ndarray,
    ) -> MPCSolution:
        cfg = self.config
        batt = cfg.battery
        w = cfg.weights
        dt = cfg.dt_hours
        horizon = len(load_forecast_mw)
        sell_price_forecast = cfg.market.sell_price_discount * buy_price_forecast

        soc = cp.Variable(horizon + 1)
        p_ch = cp.Variable(horizon, nonneg=True)
        p_dis = cp.Variable(horizon, nonneg=True)
        p_buy = cp.Variable(horizon, nonneg=True)
        p_sell = cp.Variable(horizon, nonneg=True)

        constraints = [soc[0] == soc_current]
        cost = 0

        for k in range(horizon):
            constraints += [
                soc[k + 1] == soc[k]
                + (batt.charge_efficiency * dt / batt.energy_capacity_mwh) * p_ch[k]
                - (dt / (batt.discharge_efficiency * batt.energy_capacity_mwh)) * p_dis[k],

                p_ch[k] <= batt.charge_power_max_mw,
                p_dis[k] <= batt.discharge_power_max_mw,
                soc[k] >= batt.soc_min,
                soc[k] <= batt.soc_max,

                p_buy[k] - p_sell[k] + p_dis[k] - p_ch[k] + pv_forecast_mw[k] == load_forecast_mw[k],
            ]

            cost += (
                buy_price_forecast[k] * p_buy[k] * dt
                - sell_price_forecast[k] * p_sell[k] * dt
                + w.lambda_soc * cp.square(soc[k] - batt.soc_ref)
                + w.lambda_deg * (p_ch[k] + p_dis[k]) * dt
                + w.lambda_delta_u * (
                    cp.square(p_ch[k] - (p_ch_prev if k == 0 else p_ch[k - 1]))
                    + cp.square(p_dis[k] - (p_dis_prev if k == 0 else p_dis[k - 1]))
                )
            )

        cost += w.lambda_terminal * cp.square(soc[horizon] - batt.soc_ref)
        constraints += [
            soc[horizon] >= batt.soc_min,
            soc[horizon] <= batt.soc_max,
        ]

        prob = cp.Problem(cp.Minimize(cost), constraints)
        prob.solve(solver=cp.OSQP, warm_start=True, verbose=False)

        if prob.status not in ("optimal", "optimal_inaccurate"):
            raise RuntimeError(f"MPC solve failed: {prob.status}")

        return MPCSolution(
            p_ch_first=float(p_ch.value[0]),
            p_dis_first=float(p_dis.value[0]),
            p_buy_first=float(p_buy.value[0]),
            p_sell_first=float(p_sell.value[0]),
            soc_plan=np.array(soc.value).reshape(-1),
            objective_value=float(prob.value),
        )
