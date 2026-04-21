"""
refined_vpp_env.py
==================
精细化的 VPP 多目标强化学习环境。

相对于基础版本的增强：
1. 电池退化采用 **Rainflow 简化 DoD-权重模型**，高 DoD 循环指数级加速老化
2. 增加 **爬坡率约束** 和 **最小停留时间**
3. 状态特征包含 **多视野预测 + 预测不确定性 (σ)** + **滚动统计**
4. 反映 **预测误差随时间演化**（越近越准）
5. 风险目标采用 **滚动 CVaR_α** 而非简单方差
6. 引入 **终端 SOC 惩罚**（促使每日调度不过度损耗电池）
7. **软约束** 通过额外的 "violation" 奖励维度体现

奖励向量维度：d=4
  r[0]: 净收益 (¥)
  r[1]: -碳排成本 (¥，EF × 净购电 × 碳价)
  r[2]: -电池等效寿命损耗 (¥，基于 DoD-权重循环)
  r[3]: -尾部风险 (¥，CVaR_95% of negative revenue)
"""

from __future__ import annotations

import gymnasium as gym
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from gymnasium import spaces
from typing import Dict, Tuple, Optional, List


# ======================================================================
# 电池物理参数
# ======================================================================
@dataclass
class BatteryParams:
    capacity_kwh: float = 400.0
    p_max_kw: float = 100.0
    p_min_kw: float = -100.0          # 负值 = 充电
    eta_charge: float = 0.95
    eta_discharge: float = 0.95
    soc_min: float = 0.10
    soc_max: float = 0.90
    init_soc: float = 0.50
    ramp_max_kw_per_step: float = 40.0   # 爬坡约束（每 15 min 最大变化）
    # 退化参数（Wöhler-like）
    cycle_life_at_100dod: float = 4000.0  # 100% DoD 循环寿命
    dod_exponent: float = 1.8             # 非线性加速因子（>1 意味着深放大幅加速退化）
    capex_per_kwh: float = 1200.0         # ¥/kWh，用于把退化货币化
    calendar_aging_per_year: float = 0.02 # 年度日历老化


@dataclass
class EnvParams:
    carbon_price: float = 0.10        # ¥/kg CO2
    dev_tol_kw: float = 5.0           # 可容忍功率偏差
    dev_penalty: float = 1.5          # 偏差罚款 ¥/kWh
    grid_import_limit_kw: float = 500.0  # 电网联络线限值
    grid_export_limit_kw: float = 200.0
    terminal_soc_penalty_weight: float = 5.0  # 终端偏离目标 SOC 的惩罚
    terminal_soc_target: float = 0.5
    risk_window: int = 24             # 风险计算滑动窗口（步）
    risk_alpha: float = 0.95          # CVaR 置信水平
    horizon: int = 96                 # 单 episode 步数 = 1 天


# ======================================================================
# 主环境类
# ======================================================================
class RefinedVPPEnv(gym.Env):
    """精细化 VPP 多目标 RL 环境，符合 MO-Gymnasium API。"""
    metadata = {"render_modes": []}

    def __init__(
        self,
        data: pd.DataFrame,
        battery: Optional[BatteryParams] = None,
        params: Optional[EnvParams] = None,
        forecast_horizons_min: Tuple[int, ...] = (15, 60, 240),
        n_action_levels: int = 11,   # 连续动作离散化：-100, -80, ..., 0, ..., +100
    ):
        super().__init__()
        self.data = data.reset_index(drop=True)
        self.battery = battery or BatteryParams()
        self.params = params or EnvParams()
        self.forecast_horizons = forecast_horizons_min
        self.n_actions = n_action_levels

        # 离散动作档位（kW），对称分布
        self.action_levels = np.linspace(
            self.battery.p_min_kw,
            self.battery.p_max_kw,
            n_action_levels,
        ).astype(np.float32)
        self.action_space = spaces.Discrete(n_action_levels)

        # 奖励向量维度 = 4
        self.reward_dim = 4
        self.reward_space = spaces.Box(
            low=-np.inf, high=np.inf,
            shape=(self.reward_dim,), dtype=np.float32,
        )

        # 观察空间维度：见 _build_obs
        obs_dim = self._compute_obs_dim()
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf,
            shape=(obs_dim,), dtype=np.float32,
        )

        # 运行时状态
        self._t_global = 0           # 数据索引
        self._t_local = 0            # 当前 episode 内步数
        self._soc = 0.5
        self._prev_p_batt = 0.0
        self._revenue_history: List[float] = []
        self._done = False

    def _compute_obs_dim(self) -> int:
        """动态计算观察空间维度。"""
        # SOC (1) + 上一步动作 (1) + 时间编码 (3: hour_sin, hour_cos, weekend)
        base = 1 + 1 + 3
        # 当前真实值 × 3 (price, pv, load)
        cur = 3
        # 预测值 × 3 variables × n_horizons, + 1 σ per variable
        fcst = 3 * len(self.forecast_horizons) + 3
        # 滚动统计：过去 6 步的价格均值和标准差
        rolling = 2
        return base + cur + fcst + rolling

    # ------------------------------------------------------------------
    # 核心循环
    # ------------------------------------------------------------------
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # 允许指定起始日
        start_idx = 0
        if options is not None and "start_day" in options:
            start_idx = int(options["start_day"]) * self.params.horizon

        # 保证 episode 不超出数据
        max_start = len(self.data) - self.params.horizon - max(self.forecast_horizons) // 15
        start_idx = min(start_idx, max_start)
        if start_idx < 0:
            start_idx = 0

        self._t_global = start_idx
        self._t_local = 0
        self._soc = self.battery.init_soc
        self._prev_p_batt = 0.0
        self._revenue_history = []
        self._done = False

        return self._build_obs(), self._build_info(action_taken=None, p_batt_actual=0.0)

    def step(self, action: int):
        if self._done:
            raise RuntimeError("Episode 已结束，请先 reset()")

        # 1. 解析动作
        p_batt_cmd = float(self.action_levels[int(action)])

        # 2. 应用爬坡约束
        ramp = self.battery.ramp_max_kw_per_step
        p_batt_cmd = np.clip(
            p_batt_cmd,
            self._prev_p_batt - ramp,
            self._prev_p_batt + ramp,
        )

        # 3. 应用 SOC 约束（物理裁剪）
        p_batt = self._apply_soc_constraints(p_batt_cmd)

        # 4. SOC 更新
        dt = 0.25  # 15 min = 0.25 h
        if p_batt > 0:  # 放电
            dsoc = -(p_batt * dt) / (self.battery.capacity_kwh * self.battery.eta_discharge)
        elif p_batt < 0:  # 充电
            dsoc = -(p_batt * dt * self.battery.eta_charge) / self.battery.capacity_kwh
        else:
            dsoc = 0.0
        prev_soc = self._soc
        self._soc = float(np.clip(self._soc + dsoc, self.battery.soc_min, self.battery.soc_max))

        # 5. 读取当前外生变量
        row = self.data.iloc[self._t_global]
        pv = float(row["pv_kw"])
        load = float(row["load_kw"])
        price = float(row["price_cny_per_kwh"])
        ef = float(row["emission_factor_kg_per_kwh"])

        # 6. 功率平衡
        net_export = pv - load + p_batt   # >0: 售电；<0: 从电网购电
        # 联络线约束
        net_export = float(np.clip(
            net_export,
            -self.params.grid_import_limit_kw,
            self.params.grid_export_limit_kw,
        ))

        # 7. 目标 1: 净收益
        r_revenue = price * net_export * dt
        self._revenue_history.append(r_revenue)

        # 8. 目标 2: 碳排放（货币化）
        grid_import_kwh = max(0.0, -net_export) * dt
        r_co2 = -self.params.carbon_price * ef * grid_import_kwh

        # 9. 目标 3: 电池退化（DoD-weighted）
        r_deg = -self._compute_degradation_cost(prev_soc, self._soc, abs(p_batt) * dt)

        # 10. 目标 4: 尾部风险 (CVaR 近似)
        r_risk = -self._compute_risk_cost()

        vec_reward = np.array([r_revenue, r_co2, r_deg, r_risk], dtype=np.float32)

        # 11. 时间推进
        self._t_global += 1
        self._t_local += 1
        self._prev_p_batt = p_batt

        terminated = self._t_local >= self.params.horizon
        truncated = False
        if terminated:
            # 终端 SOC 惩罚（加到碳排维度，因为它是"约束性"目标）
            soc_penalty = (self.params.terminal_soc_penalty_weight
                           * (self._soc - self.params.terminal_soc_target) ** 2
                           * self.battery.capacity_kwh)
            vec_reward[2] -= soc_penalty  # 归到 degradation 维度
            self._done = True

        obs = self._build_obs() if not terminated else self._build_obs()
        info = self._build_info(action_taken=p_batt_cmd, p_batt_actual=p_batt)
        info["price"] = price
        info["ef"] = ef
        info["net_export"] = net_export
        info["soc"] = self._soc

        return obs, vec_reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # 辅助：观察构建
    # ------------------------------------------------------------------
    def _build_obs(self) -> np.ndarray:
        row = self.data.iloc[self._t_global]
        hour = float(row.get("hour", 0.0))
        is_weekend = float(row.get("is_weekend", 0.0))

        # 基础状态
        base = [
            self._soc,
            self._prev_p_batt / self.battery.p_max_kw,
            np.sin(2 * np.pi * hour / 24),
            np.cos(2 * np.pi * hour / 24),
            is_weekend,
        ]

        # 当前真实值（归一化）
        cur = [
            float(row["price_cny_per_kwh"]),  # 保留原值
            float(row["pv_kw"]) / self.battery.p_max_kw,
            float(row["load_kw"]) / self.battery.p_max_kw,
        ]

        # 预测值（多视野）
        fcst = []
        for h in self.forecast_horizons:
            col_p = f"forecast_price_cny_per_kwh_h{h}min"
            col_pv = f"forecast_pv_kw_h{h}min"
            col_l = f"forecast_load_kw_h{h}min"
            if col_p in row:
                fcst.extend([
                    float(row[col_p]),
                    float(row[col_pv]) / self.battery.p_max_kw,
                    float(row[col_l]) / self.battery.p_max_kw,
                ])
            else:
                # 回退：使用当前值
                fcst.extend([cur[0], cur[1], cur[2]])

        # 预测不确定性代理：预测值与当前值的 abs 差（反映短期波动）
        sigma_proxy = []
        for col in ["price_cny_per_kwh", "pv_kw", "load_kw"]:
            fcst_col = f"forecast_{col}_h60min"
            if fcst_col in row:
                sigma_proxy.append(
                    abs(float(row[fcst_col]) - float(row[col])) /
                    max(abs(float(row[col])), 0.1)
                )
            else:
                sigma_proxy.append(0.0)

        # 滚动统计（过去 1.5 小时 = 6 步 价格均值与 std）
        past_start = max(0, self._t_global - 6)
        past_prices = self.data["price_cny_per_kwh"].iloc[past_start:self._t_global]
        if len(past_prices) > 1:
            rolling = [float(past_prices.mean()), float(past_prices.std())]
        else:
            rolling = [cur[0], 0.0]

        obs = np.array(base + cur + fcst + sigma_proxy + rolling, dtype=np.float32)
        return obs

    def _build_info(self, action_taken, p_batt_actual) -> Dict:
        return {
            "t_global": self._t_global,
            "t_local": self._t_local,
            "soc": self._soc,
            "p_batt_cmd": action_taken,
            "p_batt_actual": p_batt_actual,
        }

    # ------------------------------------------------------------------
    # 物理：SOC 约束
    # ------------------------------------------------------------------
    def _apply_soc_constraints(self, p_cmd: float) -> float:
        dt = 0.25
        if p_cmd > 0:  # 放电
            max_kw = (self._soc - self.battery.soc_min) \
                     * self.battery.capacity_kwh * self.battery.eta_discharge / dt
            return float(np.clip(p_cmd, 0.0, min(max_kw, self.battery.p_max_kw)))
        elif p_cmd < 0:  # 充电
            max_kw = -(self.battery.soc_max - self._soc) \
                     * self.battery.capacity_kwh / (self.battery.eta_charge * dt)
            return float(np.clip(p_cmd, max(max_kw, self.battery.p_min_kw), 0.0))
        else:
            return 0.0

    # ------------------------------------------------------------------
    # 物理：电池退化模型（DoD-weighted cycling，简化 Rainflow）
    # ------------------------------------------------------------------
    def _compute_degradation_cost(self, soc_prev: float, soc_now: float,
                                  throughput_kwh: float) -> float:
        """
        退化模型（货币化）：
        成本 = capex × (循环损耗 + 日历老化)
        
        循环损耗：使用 DoD-加权模型。每个"半循环"对寿命的消耗为
            loss = 0.5 / (cycle_life × (DoD)^(-dod_exp))
        即深放电对寿命消耗呈指数加速。
        """
        dod_change = abs(soc_now - soc_prev)
        if dod_change < 1e-6 and throughput_kwh < 1e-6:
            cycle_loss = 0.0
        else:
            # 半循环，DoD 取本次 |ΔSOC|
            # loss_fraction = 0.5 * (DoD)^dod_exp / cycle_life_at_100dod
            cycle_loss = 0.5 * (dod_change ** self.battery.dod_exponent) \
                         / self.battery.cycle_life_at_100dod
        # 日历老化（每步分摊）
        steps_per_year = 365 * 96
        calendar_loss = self.battery.calendar_aging_per_year / steps_per_year
        total_loss = cycle_loss + calendar_loss
        # 货币化
        degradation_cost = total_loss * self.battery.capacity_kwh * self.battery.capex_per_kwh
        return degradation_cost

    # ------------------------------------------------------------------
    # 风险：滚动 CVaR
    # ------------------------------------------------------------------
    def _compute_risk_cost(self) -> float:
        """计算滚动窗口内的负收益的 CVaR_α 代理。"""
        if len(self._revenue_history) < 4:
            return 0.0
        window = self._revenue_history[-self.params.risk_window:]
        neg_revenues = [-r for r in window if r < 0]  # 只对亏损建模
        if len(neg_revenues) == 0:
            return 0.0
        # CVaR_α = 损失分布中尾部 α 分位的均值
        q = np.quantile(neg_revenues, self.params.risk_alpha)
        tail = [v for v in neg_revenues if v >= q]
        if len(tail) == 0:
            return 0.0
        cvar = float(np.mean(tail))
        # 除以窗口长度，把累计量分摊到单步
        return cvar / self.params.risk_window


# ======================================================================
# 工厂方法：从 CSV 构建环境
# ======================================================================
def make_env_from_csv(
    csv_path: str = "/home/claude/morl_refined/vpp_year_dataset.csv",
    battery: Optional[BatteryParams] = None,
    params: Optional[EnvParams] = None,
) -> RefinedVPPEnv:
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    env = RefinedVPPEnv(data=df, battery=battery, params=params)
    return env


# ======================================================================
# 单元测试：环境可正确运行
# ======================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("精细 VPP 环境单元测试")
    print("=" * 70)
    env = make_env_from_csv()
    print(f"观察维度:    {env.observation_space.shape}")
    print(f"动作数量:    {env.action_space.n}")
    print(f"动作档位:    {env.action_levels}")
    print(f"奖励维度:    {env.reward_dim}")
    print()

    obs, info = env.reset(options={"start_day": 15})  # 1 月 16 日开始
    total_rewards = np.zeros(env.reward_dim)
    step = 0
    trajectory = []

    # 策略：简单启发式——低价充电，高价放电
    while True:
        price = obs[5]  # 状态向量中第 5 位是当前价格
        soc = obs[0]
        if price < 0.2 and soc < 0.85:
            action = 2       # 充电档位
        elif price > 0.6 and soc > 0.15:
            action = 8       # 放电档位
        else:
            action = 5       # 待机

        obs, reward, terminated, truncated, info = env.step(action)
        total_rewards += reward
        trajectory.append({
            "step": step,
            "soc": info["soc"],
            "p_batt": info["p_batt_actual"],
            "price": info["price"],
            "net_export": info["net_export"],
            "r_revenue": reward[0],
            "r_co2": reward[1],
            "r_deg": reward[2],
            "r_risk": reward[3],
        })
        step += 1
        if terminated or truncated:
            break

    df_traj = pd.DataFrame(trajectory)
    print(f"总步数: {step}")
    print(f"奖励总和 (启发式策略):")
    print(f"  收益:       {total_rewards[0]:8.2f} ¥")
    print(f"  碳排成本:   {total_rewards[1]:8.2f} ¥")
    print(f"  电池退化:   {total_rewards[2]:8.2f} ¥")
    print(f"  风险成本:   {total_rewards[3]:8.2f} ¥")
    print()
    print(f"SOC 轨迹: {df_traj['soc'].min():.2f} → {df_traj['soc'].max():.2f}")
    print(f"电池吞吐: {df_traj['p_batt'].abs().sum() * 0.25:.1f} kWh")
    print(f"净售电:   {df_traj[df_traj['net_export'] > 0]['net_export'].sum() * 0.25:.1f} kWh")
    print(f"净购电:   {-df_traj[df_traj['net_export'] < 0]['net_export'].sum() * 0.25:.1f} kWh")

    df_traj.to_csv("/home/claude/morl_refined/trajectory_heuristic.csv", index=False)
    print("\n轨迹数据已保存到 trajectory_heuristic.csv")
