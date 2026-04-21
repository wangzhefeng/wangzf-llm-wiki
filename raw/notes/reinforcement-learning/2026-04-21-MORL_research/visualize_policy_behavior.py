"""
visualize_policy_behavior.py
============================
展示 MORL 核心价值：**同一个已训练模型，不同偏好权重 → 不同决策行为**。

从已训练的 Envelope Q-Learner 中:
1. 用不同权重评估同一天（7 月典型工作日）
2. 绘制 4 个子图：SOC 轨迹、电池出力、净购/售电、价格追随
3. 量化对比各策略在当日的 4 个目标维度
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from refined_vpp_env import RefinedVPPEnv, BatteryParams, EnvParams
from numpy_envelope_demo import (
    EnvelopeQLearner, StateDiscretizer, EnvelopeQLConfig, run_training
)


def simulate_day(agent, env, weight, start_day=10):
    """在指定偏好下模拟一天，返回完整轨迹。"""
    obs, info = env.reset(options={"start_day": start_day})
    s_key = agent.disc.discretize(obs)
    records = []
    done = False
    step = 0
    while not done:
        action = agent.act(s_key, weight, epsilon=0.0)  # 贪婪
        obs_next, r_vec, term, trunc, info = env.step(action)
        records.append({
            "step": step,
            "hour": step * 0.25,
            "soc": info["soc"],
            "p_batt_cmd": info["p_batt_cmd"],
            "p_batt_actual": info["p_batt_actual"],
            "price": info["price"],
            "ef": info["ef"],
            "net_export": info["net_export"],
            "r_revenue": r_vec[0],
            "r_co2": r_vec[1],
            "r_deg": r_vec[2],
            "r_risk": r_vec[3],
        })
        s_key = agent.disc.discretize(obs_next)
        done = term or trunc
        step += 1
    return pd.DataFrame(records)


def main():
    print("训练模型...")
    agent, env, _ = run_training(n_episodes=400, verbose_every=100)

    # 选定评估权重
    strategies = [
        ("Profit-Heavy",    np.array([0.70, 0.10, 0.10, 0.10]), "tab:red"),
        ("Balanced",        np.array([0.40, 0.20, 0.25, 0.15]), "tab:blue"),
        ("Battery-Life",    np.array([0.20, 0.10, 0.60, 0.10]), "tab:green"),
        ("Low-Carbon",      np.array([0.30, 0.50, 0.10, 0.10]), "tab:purple"),
    ]

    # 对同一天（7 月中旬）用不同策略模拟
    start_day = 10  # 7 月 11 日
    trajectories = {}
    for name, w, color in strategies:
        traj = simulate_day(agent, env, w, start_day=start_day)
        trajectories[name] = (traj, color, w)

    # ==================================================================
    # 4×1 面板图
    # ==================================================================
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)

    # 1) 电价背景 (所有策略共用)
    price_trace = list(trajectories.values())[0][0]["price"]
    hours = list(trajectories.values())[0][0]["hour"]

    # SOC 轨迹
    ax = axes[0]
    for name, (traj, color, w) in trajectories.items():
        ax.plot(traj["hour"], traj["soc"], color=color, lw=2.0, label=f"{name}")
    ax.set_ylabel("SOC")
    ax.set_title("Battery State of Charge — Same Day, Different Preference Weights")
    ax.axhline(0.1, color="gray", linestyle=":", lw=0.8)
    ax.axhline(0.9, color="gray", linestyle=":", lw=0.8)
    ax.set_ylim(0, 1)
    ax.legend(loc="best", ncol=4, fontsize=10)
    ax.grid(alpha=0.3)

    # 电池出力
    ax = axes[1]
    for name, (traj, color, w) in trajectories.items():
        ax.plot(traj["hour"], traj["p_batt_actual"], color=color, lw=1.5)
    ax.set_ylabel("Battery Power (kW)\n<0 charge, >0 discharge")
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Battery Dispatch Command")
    ax.grid(alpha=0.3)

    # 净购/售电 + 价格
    ax = axes[2]
    for name, (traj, color, w) in trajectories.items():
        ax.plot(traj["hour"], traj["net_export"], color=color, lw=1.2, alpha=0.85)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_ylabel("Net Export (kW)\n<0 buy, >0 sell")
    ax.set_title("Power Exchange with Grid")

    # 第二 y 轴：价格
    ax2 = ax.twinx()
    ax2.fill_between(price_trace.index * 0.25, 0, price_trace.values,
                     alpha=0.12, color="orange", label="Price")
    ax2.set_ylabel("Price (¥/kWh)", color="darkorange")
    ax2.tick_params(axis="y", labelcolor="darkorange")
    ax.grid(alpha=0.3)

    # 累计收益
    ax = axes[3]
    for name, (traj, color, w) in trajectories.items():
        cum_rev = traj["r_revenue"].cumsum()
        ax.plot(traj["hour"], cum_rev, color=color, lw=2.0, label=name)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_ylabel("Cumulative Revenue (¥)")
    ax.set_xlabel("Hour of day")
    ax.set_title("Accumulated Revenue Throughout the Day")
    ax.legend(loc="best", ncol=2, fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_xticks(range(0, 25, 3))

    plt.tight_layout()
    plt.savefig("/home/claude/morl_refined/fig5_policy_behavior.png",
                dpi=110, bbox_inches="tight")
    plt.close()
    print("已保存 fig5_policy_behavior.png")

    # ==================================================================
    # Pareto 散点图 + 权重空间映射
    # ==================================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 收益 vs 电池退化
    ax = axes[0]
    for name, (traj, color, w) in trajectories.items():
        total_rev = traj["r_revenue"].sum()
        total_deg = -traj["r_deg"].sum()
        ax.scatter(total_deg, total_rev, s=200, c=color, edgecolor="black", label=name)
        ax.annotate(
            f"w={w[0]:.1f},{w[1]:.1f},{w[2]:.1f},{w[3]:.1f}",
            (total_deg, total_rev), fontsize=8,
            xytext=(7, 7), textcoords="offset points"
        )
    ax.set_xlabel("Battery Degradation Cost (¥)")
    ax.set_ylabel("Net Revenue (¥)")
    ax.set_title("Pareto Trade-off: Revenue vs Degradation")
    ax.grid(alpha=0.3)
    ax.legend()

    # 收益 vs 碳排
    ax = axes[1]
    for name, (traj, color, w) in trajectories.items():
        total_rev = traj["r_revenue"].sum()
        total_co2 = -traj["r_co2"].sum()
        ax.scatter(total_co2, total_rev, s=200, c=color, edgecolor="black", label=name)
    ax.set_xlabel("CO₂ Cost (¥, monetized)")
    ax.set_ylabel("Net Revenue (¥)")
    ax.set_title("Pareto Trade-off: Revenue vs Carbon")
    ax.grid(alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.savefig("/home/claude/morl_refined/fig6_pareto_scatter.png",
                dpi=110, bbox_inches="tight")
    plt.close()
    print("已保存 fig6_pareto_scatter.png")

    # 汇总
    print("\n策略行为对比（同一天，7 月 11 日）")
    print("-" * 80)
    rows = []
    for name, (traj, color, w) in trajectories.items():
        total_rev = traj["r_revenue"].sum()
        total_co2 = -traj["r_co2"].sum()
        total_deg = -traj["r_deg"].sum()
        total_risk = -traj["r_risk"].sum()
        throughput = traj["p_batt_actual"].abs().sum() * 0.25
        rows.append({
            "Strategy": name,
            "Revenue (¥)":    f"{total_rev:7.1f}",
            "CO2 (¥)":        f"{total_co2:6.1f}",
            "Deg (¥)":        f"{total_deg:6.1f}",
            "Risk":           f"{total_risk:6.2f}",
            "Battery Throughput (kWh)": f"{throughput:6.1f}",
        })
    df_summary = pd.DataFrame(rows)
    print(df_summary.to_string(index=False))
    df_summary.to_csv("/home/claude/morl_refined/policy_comparison_same_day.csv",
                      index=False)
    return agent


if __name__ == "__main__":
    main()
