from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import cvxpy as cp

from .config import ProjectConfig


@dataclass
class MPCSolution:
    p_batt_first: float
    p_batt_plan: np.ndarray
    soc_plan: np.ndarray
    objective_value: float


class StorageMPCController:
    """线性储能 MPC 控制器（工程原型版）。"""

    def __init__(self, config: ProjectConfig):
        self.config = config

    def solve(
        self,
        soc_current: float,
        p_prev: float,
        load_forecast_mw: np.ndarray,
        price_forecast: np.ndarray,
    ) -> MPCSolution:
        horizon = len(load_forecast_mw)
        dt = self.config.dt_hours
        batt = self.config.battery
        w = self.config.weights

        soc = cp.Variable(horizon + 1)
        p_batt = cp.Variable(horizon)

        constraints = [soc[0] == soc_current]
        cost = 0

        for k in range(horizon):
            p_grid = load_forecast_mw[k] - p_batt[k]

            cost += (
                price_forecast[k] * p_grid * dt
                + w.lambda_soc * cp.square(soc[k] - batt.soc_ref)
                + w.lambda_u * cp.square(p_batt[k])
                + w.lambda_delta_u * cp.square(p_batt[k] - (p_prev if k == 0 else p_batt[k - 1]))
            )

            constraints += [
                soc[k + 1] == soc[k] - (dt / batt.energy_capacity_mwh) * p_batt[k],
                soc[k] >= batt.soc_min,
                soc[k] <= batt.soc_max,
                p_batt[k] >= batt.power_min_mw,
                p_batt[k] <= batt.power_max_mw,
                p_grid >= 0.0,
            ]

        cost += w.lambda_terminal * cp.square(soc[horizon] - batt.soc_ref)
        constraints += [
            soc[horizon] >= batt.soc_min,
            soc[horizon] <= batt.soc_max,
        ]

        problem = cp.Problem(cp.Minimize(cost), constraints)
        problem.solve(solver=cp.OSQP, warm_start=True, verbose=False)

        if problem.status not in ("optimal", "optimal_inaccurate"):
            raise RuntimeError(f"MPC solve failed with status: {problem.status}")

        return MPCSolution(
            p_batt_first=float(p_batt.value[0]),
            p_batt_plan=np.array(p_batt.value).reshape(-1),
            soc_plan=np.array(soc.value).reshape(-1),
            objective_value=float(problem.value),
        )
