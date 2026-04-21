"""
milp_oracle.py
==============
VPP 多目标调度的 MILP Oracle 基准（使用 ε-约束法生成 Pareto 前沿）。

作用：
    - 作为 RL 策略的"性能上界"基准（假设完美预测，即已知未来）
    - 用 ε-约束法遍历不同目标权重，生成真实 Pareto 前沿
    - 与 Envelope Q-Learning 的近似 Pareto 前沿对比

注意：
    - MILP 假设全部未来信息已知，实际不可得 → 这是"理论上界"
    - 非线性电池退化被线性化（按功率吞吐近似）
    - 使用开源 PuLP + CBC 求解器

依赖：pip install pulp
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pulp
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class MILPConfig:
    # 电池参数（与 refined_vpp_env 对齐）
    capacity_kwh: float = 400.0
    p_max_kw: float = 100.0
    eta_c: float = 0.95
    eta_d: float = 0.95
    soc_min: float = 0.10
    soc_max: float = 0.90
    init_soc: float = 0.50
    terminal_soc: float = 0.50
    # 退化线性系数（¥/kWh 吞吐）
    deg_coef: float = 0.036   # ≈ capex(1200) / (2 * cycle_life(4000) * 100%DoD * 4hrs)
    # 经济
    carbon_price: float = 0.10
    # 联络线
    grid_import_max_kw: float = 500.0
    grid_export_max_kw: float = 200.0
    dt_hour: float = 0.25


def solve_milp(
    prices: np.ndarray,
    pv: np.ndarray,
    load: np.ndarray,
    ef: np.ndarray,
    cfg: MILPConfig = None,
    eps_constraints: Optional[Dict[str, float]] = None,
    objective: str = "revenue",
    verbose: bool = False,
) -> Dict:
    """
    求解单日 VPP 调度的 MILP。

    objective: "revenue" | "co2" | "deg" | "weighted"
    eps_constraints: 对非主目标施加上限约束（ε-约束法）
        例: {"co2": 50.0, "deg": 60.0}
    """
    if cfg is None:
        cfg = MILPConfig()
    T = len(prices)
    assert len(pv) == len(load) == len(ef) == T

    prob = pulp.LpProblem("VPP_Dispatch", pulp.LpMaximize)

    # 决策变量
    p_charge = [pulp.LpVariable(f"pc_{t}", 0, cfg.p_max_kw) for t in range(T)]
    p_dis = [pulp.LpVariable(f"pd_{t}", 0, cfg.p_max_kw) for t in range(T)]
    soc = [pulp.LpVariable(f"soc_{t}", cfg.soc_min, cfg.soc_max) for t in range(T + 1)]
    p_import = [pulp.LpVariable(f"pi_{t}", 0, cfg.grid_import_max_kw) for t in range(T)]
    p_export = [pulp.LpVariable(f"pe_{t}", 0, cfg.grid_export_max_kw) for t in range(T)]
    # 二进制变量避免同时充放电
    y_charge = [pulp.LpVariable(f"yc_{t}", cat="Binary") for t in range(T)]

    dt = cfg.dt_hour

    # 初始/终端 SOC
    prob += soc[0] == cfg.init_soc
    prob += soc[T] >= cfg.terminal_soc - 0.03   # 允许 ±3% 容差
    prob += soc[T] <= cfg.terminal_soc + 0.03

    # SOC 动力学
    for t in range(T):
        prob += (soc[t + 1] == soc[t]
                 + (p_charge[t] * cfg.eta_c * dt) / cfg.capacity_kwh
                 - (p_dis[t] * dt) / (cfg.capacity_kwh * cfg.eta_d))
        # 互斥约束（充放电不能同时发生）
        prob += p_charge[t] <= cfg.p_max_kw * y_charge[t]
        prob += p_dis[t] <= cfg.p_max_kw * (1 - y_charge[t])

        # 功率平衡: PV + import + dis = load + export + charge
        prob += (pv[t] + p_import[t] + p_dis[t]
                 == load[t] + p_export[t] + p_charge[t])

    # 目标维度
    revenue_expr = pulp.lpSum([
        (prices[t] * p_export[t] - prices[t] * p_import[t]) * dt for t in range(T)
    ])
    co2_expr = pulp.lpSum([
        cfg.carbon_price * ef[t] * p_import[t] * dt for t in range(T)
    ])
    deg_expr = pulp.lpSum([
        cfg.deg_coef * (p_charge[t] + p_dis[t]) * dt for t in range(T)
    ])

    # 应用 ε-约束
    if eps_constraints:
        if "co2" in eps_constraints:
            prob += co2_expr <= eps_constraints["co2"]
        if "deg" in eps_constraints:
            prob += deg_expr <= eps_constraints["deg"]
        if "revenue" in eps_constraints:
            prob += revenue_expr >= eps_constraints["revenue"]

    # 设定主目标
    if objective == "revenue":
        prob += revenue_expr
    elif objective == "co2":
        prob += -co2_expr
    elif objective == "deg":
        prob += -deg_expr
    elif objective == "weighted":
        # 线性加权
        w = eps_constraints or {"w_rev": 1.0, "w_co2": 0.0, "w_deg": 0.0}
        prob += (w.get("w_rev", 1.0) * revenue_expr
                 - w.get("w_co2", 0.0) * co2_expr
                 - w.get("w_deg", 0.0) * deg_expr)
    else:
        raise ValueError(f"未知目标: {objective}")

    # 求解
    solver = pulp.PULP_CBC_CMD(msg=1 if verbose else 0, timeLimit=30)
    status = prob.solve(solver)

    if pulp.LpStatus[status] not in ("Optimal",):
        return {"status": pulp.LpStatus[status]}

    # 抽取解
    sol = {
        "status": "Optimal",
        "revenue": pulp.value(revenue_expr),
        "co2_cost": pulp.value(co2_expr),
        "deg_cost": pulp.value(deg_expr),
        "p_charge": np.array([pulp.value(x) for x in p_charge]),
        "p_discharge": np.array([pulp.value(x) for x in p_dis]),
        "soc": np.array([pulp.value(x) for x in soc]),
        "p_import": np.array([pulp.value(x) for x in p_import]),
        "p_export": np.array([pulp.value(x) for x in p_export]),
    }
    return sol


def generate_pareto_front(
    prices: np.ndarray,
    pv: np.ndarray,
    load: np.ndarray,
    ef: np.ndarray,
    cfg: MILPConfig = None,
    n_points_per_dim: int = 6,
) -> pd.DataFrame:
    """
    用 ε-约束法生成 Pareto 前沿：
    1. 先找每个目标独立最优（端点）
    2. 在其 CO2 和 Degradation 边界的若干 ε 值上，分别求收益最大化
    """
    if cfg is None:
        cfg = MILPConfig()

    print("步骤 1: 求解单目标极值（Pareto 前沿端点）...")
    endpoints = {}
    for obj in ["revenue", "co2", "deg"]:
        sol = solve_milp(prices, pv, load, ef, cfg, objective=obj)
        if sol["status"] == "Optimal":
            endpoints[obj] = sol
            print(f"  {obj}:  rev={sol['revenue']:7.2f}  "
                  f"co2={sol['co2_cost']:6.2f}  deg={sol['deg_cost']:6.2f}")

    # 计算 ε 网格
    co2_min = endpoints["co2"]["co2_cost"]
    co2_max = endpoints["revenue"]["co2_cost"]
    deg_min = endpoints["deg"]["deg_cost"]
    deg_max = endpoints["revenue"]["deg_cost"]

    co2_eps_grid = np.linspace(co2_min, co2_max, n_points_per_dim)
    deg_eps_grid = np.linspace(deg_min, deg_max, n_points_per_dim)

    print(f"\n步骤 2: 扫描 ε-约束网格 ({n_points_per_dim} × {n_points_per_dim} 点)...")
    pareto_pts = []
    for i, co2_eps in enumerate(co2_eps_grid):
        for j, deg_eps in enumerate(deg_eps_grid):
            sol = solve_milp(
                prices, pv, load, ef, cfg,
                objective="revenue",
                eps_constraints={"co2": co2_eps + 1e-3, "deg": deg_eps + 1e-3},
            )
            if sol["status"] == "Optimal":
                pareto_pts.append({
                    "co2_eps":   co2_eps,
                    "deg_eps":   deg_eps,
                    "revenue":   sol["revenue"],
                    "co2_cost":  sol["co2_cost"],
                    "deg_cost":  sol["deg_cost"],
                })

    df = pd.DataFrame(pareto_pts)

    # 保留真正的 Pareto 点（非支配过滤）
    values = df[["revenue", "co2_cost", "deg_cost"]].values
    is_pareto = np.ones(len(values), dtype=bool)
    for i, v in enumerate(values):
        for k, vk in enumerate(values):
            if k == i:
                continue
            # 点 k 支配点 i
            if (vk[0] >= v[0] + 1e-3 and
                vk[1] <= v[1] - 1e-3 and
                vk[2] <= v[2] - 1e-3):
                is_pareto[i] = False
                break
    df["is_pareto"] = is_pareto
    return df


# ======================================================================
# 主函数
# ======================================================================
if __name__ == "__main__":
    print("加载数据...")
    df = pd.read_csv("/home/claude/morl_refined/vpp_year_dataset.csv",
                     parse_dates=["timestamp"])

    # 选一个典型夏季工作日（7 月 15 日, 星期一）
    target_date = pd.Timestamp("2024-07-15").date()
    day_data = df[df["timestamp"].dt.date == target_date].reset_index(drop=True)
    print(f"目标日: {target_date}, {len(day_data)} 步")

    prices = day_data["price_cny_per_kwh"].values
    pv = day_data["pv_kw"].values
    load = day_data["load_kw"].values
    ef = day_data["emission_factor_kg_per_kwh"].values

    cfg = MILPConfig()

    # 1. 生成 MILP Oracle Pareto 前沿
    print("\n" + "=" * 70)
    print("MILP Oracle: ε-约束法 Pareto 前沿")
    print("=" * 70)
    pareto_df = generate_pareto_front(prices, pv, load, ef, cfg, n_points_per_dim=5)
    pareto_df.to_csv("/home/claude/morl_refined/milp_pareto_front.csv", index=False)

    true_pareto = pareto_df[pareto_df["is_pareto"]].copy()
    print(f"\n共 {len(pareto_df)} 解，其中 {len(true_pareto)} 个为 Pareto 最优")
    print("\n前沿摘要:")
    print(true_pareto[["revenue", "co2_cost", "deg_cost"]].describe().round(2))

    # 2. 独立单目标解作为参考
    print("\n" + "=" * 70)
    print("端点策略（独立最优化）")
    print("=" * 70)
    summary_rows = []
    for obj, name in [
        ("revenue", "Revenue-only"),
        ("co2",     "CO2-only"),
        ("deg",     "Deg-only"),
    ]:
        sol = solve_milp(prices, pv, load, ef, cfg, objective=obj)
        summary_rows.append({
            "策略": name,
            "收益 (¥)":   f"{sol['revenue']:7.2f}",
            "碳排 (¥)":   f"{sol['co2_cost']:6.2f}",
            "退化 (¥)":   f"{sol['deg_cost']:6.2f}",
            "电池吞吐 (kWh)": f"{(sol['p_charge'].sum() + sol['p_discharge'].sum()) * 0.25:6.1f}",
        })
    summary_df = pd.DataFrame(summary_rows)
    print(summary_df.to_string(index=False))

    summary_df.to_csv("/home/claude/morl_refined/milp_endpoints.csv", index=False)

    # 3. 可视化
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(12, 5))

    # 3D Pareto 前沿
    ax1 = fig.add_subplot(121, projection="3d")
    pts = true_pareto[["revenue", "co2_cost", "deg_cost"]].values
    ax1.scatter(pts[:, 1], pts[:, 2], pts[:, 0], c=pts[:, 0], cmap="viridis", s=60)
    ax1.set_xlabel("CO₂ Cost (¥)")
    ax1.set_ylabel("Deg Cost (¥)")
    ax1.set_zlabel("Revenue (¥)")
    ax1.set_title("MILP Oracle: 3D Pareto Front")

    # 2D 投影
    ax2 = fig.add_subplot(122)
    non_pareto = pareto_df[~pareto_df["is_pareto"]]
    ax2.scatter(non_pareto["co2_cost"], non_pareto["revenue"],
                alpha=0.3, s=40, c="lightgray", label="Dominated")
    ax2.scatter(true_pareto["co2_cost"], true_pareto["revenue"],
                alpha=0.95, s=80, c="tab:red",
                edgecolor="black", label="Pareto Optimal")
    ax2.set_xlabel("CO₂ Cost (¥)")
    ax2.set_ylabel("Revenue (¥)")
    ax2.set_title("Projected Pareto Front: Revenue vs Carbon")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("/home/claude/morl_refined/fig7_milp_pareto.png",
                dpi=110, bbox_inches="tight")
    plt.close()
    print("\n已保存 fig7_milp_pareto.png")
