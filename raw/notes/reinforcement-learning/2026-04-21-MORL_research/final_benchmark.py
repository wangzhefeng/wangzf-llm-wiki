"""
final_benchmark.py
==================
综合对比：MORL (Envelope Q-Learning) vs MILP Oracle vs 规则基线

统一评估集：7 月 15 日（夏季典型工作日）
评估维度：收益、碳成本、电池退化

产出图：Pareto 前沿对比 + 差距量化
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from refined_vpp_env import RefinedVPPEnv, BatteryParams, EnvParams
from numpy_envelope_demo import run_training
from visualize_policy_behavior import simulate_day
from milp_oracle import solve_milp, MILPConfig


# ======================================================================
# 规则基线：启发式 + 完美前瞻
# ======================================================================
def rule_based_policy(env, weight, start_day=14):
    """
    简单 TOU 规则策略：
    - 低价 (<0.2 ¥): 充电
    - 高价 (>0.55 ¥): 放电
    - 其他：待机
    """
    obs, info = env.reset(options={"start_day": start_day})
    total = np.zeros(env.reward_dim)
    done = False
    while not done:
        price = obs[5]  # 当前价格
        soc = obs[0]
        if price < 0.2 and soc < 0.85:
            action = 2  # 充电档
        elif price > 0.55 and soc > 0.15:
            action = 8  # 放电档
        else:
            action = 5  # 待机
        obs, r_vec, term, trunc, info = env.step(action)
        total += r_vec
        done = term or trunc
    return total


def no_battery_policy(env, start_day=14):
    """对照组：完全不用电池。"""
    obs, _ = env.reset(options={"start_day": start_day})
    total = np.zeros(env.reward_dim)
    done = False
    while not done:
        obs, r_vec, term, trunc, _ = env.step(5)  # 动作 5 = 待机
        total += r_vec
        done = term or trunc
    return total


def main():
    # 加载数据
    df_all = pd.read_csv("/home/claude/morl_refined/vpp_year_dataset.csv",
                        parse_dates=["timestamp"])
    target_date = pd.Timestamp("2024-07-15").date()
    day_data = df_all[df_all["timestamp"].dt.date == target_date].reset_index(drop=True)

    print("=" * 70)
    print("VPP 调度算法综合对比（2024-07-15 典型夏季日）")
    print("=" * 70)

    # =================================================================
    # 1. MILP Oracle: 完美信息下的 Pareto 前沿
    # =================================================================
    print("\n[1] MILP Oracle (完美信息上界)")
    cfg = MILPConfig()
    prices = day_data["price_cny_per_kwh"].values
    pv = day_data["pv_kw"].values
    load = day_data["load_kw"].values
    ef = day_data["emission_factor_kg_per_kwh"].values

    milp_pts = []
    # 用线性加权扫描权重空间
    weight_grid = [
        (1.0, 0.0, 0.0),
        (0.8, 0.1, 0.1),
        (0.6, 0.2, 0.2),
        (0.5, 0.3, 0.2),
        (0.4, 0.3, 0.3),
        (0.3, 0.5, 0.2),
        (0.3, 0.2, 0.5),
        (0.2, 0.1, 0.7),
        (0.1, 0.1, 0.8),
    ]
    for w_rev, w_co2, w_deg in weight_grid:
        sol = solve_milp(
            prices, pv, load, ef, cfg,
            objective="weighted",
            eps_constraints={"w_rev": w_rev, "w_co2": w_co2, "w_deg": w_deg},
        )
        if sol["status"] == "Optimal":
            milp_pts.append({
                "method": "MILP",
                "w": (w_rev, w_co2, w_deg),
                "revenue": sol["revenue"],
                "co2":     sol["co2_cost"],
                "deg":     sol["deg_cost"],
            })
            print(f"  w=({w_rev:.1f},{w_co2:.1f},{w_deg:.1f})  "
                  f"rev={sol['revenue']:7.2f}  "
                  f"co2={sol['co2_cost']:6.2f}  "
                  f"deg={sol['deg_cost']:6.2f}")

    # =================================================================
    # 2. MORL (Envelope Q-Learning) 在多个权重下的表现
    # =================================================================
    print("\n[2] Envelope Q-Learning (MORL, 实际学到的策略)")
    print("    训练中...")
    agent, train_env, _ = run_training(n_episodes=500, verbose_every=500)

    # 在同一天用不同权重评估
    morl_pts = []
    morl_weights = [
        ("Profit",       np.array([1.0, 0.0, 0.0, 0.0])),
        ("Profit-Heavy", np.array([0.7, 0.1, 0.1, 0.1])),
        ("Balanced",     np.array([0.5, 0.25, 0.15, 0.1])),
        ("Low-Carbon",   np.array([0.3, 0.5, 0.1, 0.1])),
        ("Eco-Balance",  np.array([0.3, 0.3, 0.3, 0.1])),
        ("Deg-Averse",   np.array([0.2, 0.1, 0.6, 0.1])),
        ("Battery-Save", np.array([0.1, 0.1, 0.7, 0.1])),
    ]
    start_day_idx = day_data.index[0] // 96  # 7 月 15 日在训练数据中的天索引

    # 用训练环境构建评估（训练数据是 7 月）
    # 找到 7 月 15 日 在 7 月数据中的索引 (7月1日 = 0)
    day_in_july = 14
    for name, w in morl_weights:
        traj = simulate_day(agent, train_env, w, start_day=day_in_july)
        rev = traj["r_revenue"].sum()
        co2 = -traj["r_co2"].sum()
        deg = -traj["r_deg"].sum()
        morl_pts.append({
            "method": "MORL",
            "strategy": name,
            "w": tuple(w),
            "revenue": rev,
            "co2": co2,
            "deg": deg,
        })
        print(f"  {name:15s}  rev={rev:7.1f}  co2={co2:6.1f}  deg={deg:6.1f}")

    # =================================================================
    # 3. 规则基线
    # =================================================================
    print("\n[3] Rule-based Baseline (TOU 启发式)")
    rule_return = rule_based_policy(train_env, None, start_day=day_in_july)
    print(f"  rev={rule_return[0]:7.1f}  co2={-rule_return[1]:6.1f}  deg={-rule_return[2]:6.1f}")

    print("\n[4] No-battery Baseline (完全不调度电池)")
    no_bat = no_battery_policy(train_env, start_day=day_in_july)
    print(f"  rev={no_bat[0]:7.1f}  co2={-no_bat[1]:6.1f}  deg={-no_bat[2]:6.1f}")

    # =================================================================
    # 4. 可视化对比
    # =================================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ax = axes[0]
    # MILP 前沿
    mx = [p["co2"] for p in milp_pts]
    my = [p["revenue"] for p in milp_pts]
    ax.scatter(mx, my, s=180, marker="s", c="tab:red", alpha=0.7,
               edgecolor="black", label="MILP Oracle (perfect info)")
    # 连接 MILP 点形成前沿
    milp_sorted = sorted(milp_pts, key=lambda p: p["co2"])
    ax.plot([p["co2"] for p in milp_sorted],
            [p["revenue"] for p in milp_sorted],
            "r--", alpha=0.5, lw=1.5)

    # MORL 策略
    mox = [p["co2"] for p in morl_pts]
    moy = [p["revenue"] for p in morl_pts]
    ax.scatter(mox, moy, s=150, marker="o", c="tab:blue", alpha=0.7,
               edgecolor="black", label="MORL (Envelope Q-Learning)")
    for p in morl_pts:
        ax.annotate(p["strategy"], (p["co2"], p["revenue"]),
                    fontsize=7, xytext=(6, 4), textcoords="offset points")

    # 基线
    ax.scatter([-rule_return[1]], [rule_return[0]], s=220, marker="X",
               c="tab:green", edgecolor="black", label="Rule-based (TOU)")
    ax.scatter([-no_bat[1]], [no_bat[0]], s=220, marker="D",
               c="tab:orange", edgecolor="black", label="No-battery")

    ax.set_xlabel("CO₂ Cost (¥)")
    ax.set_ylabel("Revenue (¥)")
    ax.set_title("Revenue vs Carbon Trade-off\n2024-07-15 (Summer Weekday)")
    ax.legend()
    ax.grid(alpha=0.3)

    # 右图：收益 vs 退化
    ax = axes[1]
    ax.scatter([p["deg"] for p in milp_pts],
               [p["revenue"] for p in milp_pts],
               s=180, marker="s", c="tab:red", alpha=0.7,
               edgecolor="black", label="MILP Oracle")
    ax.plot(sorted([p["deg"] for p in milp_pts]),
            [p["revenue"] for p in sorted(milp_pts, key=lambda x: x["deg"])],
            "r--", alpha=0.5, lw=1.5)
    ax.scatter([p["deg"] for p in morl_pts],
               [p["revenue"] for p in morl_pts],
               s=150, marker="o", c="tab:blue", alpha=0.7,
               edgecolor="black", label="MORL")
    for p in morl_pts:
        ax.annotate(p["strategy"], (p["deg"], p["revenue"]),
                    fontsize=7, xytext=(6, 4), textcoords="offset points")
    ax.scatter([-rule_return[2]], [rule_return[0]], s=220, marker="X",
               c="tab:green", edgecolor="black", label="Rule-based (TOU)")
    ax.scatter([-no_bat[2]], [no_bat[0]], s=220, marker="D",
               c="tab:orange", edgecolor="black", label="No-battery")
    ax.set_xlabel("Battery Degradation (¥)")
    ax.set_ylabel("Revenue (¥)")
    ax.set_title("Revenue vs Battery Degradation Trade-off")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("/home/claude/morl_refined/fig8_final_comparison.png",
                dpi=110, bbox_inches="tight")
    plt.close()
    print("\n已保存 fig8_final_comparison.png")

    # =================================================================
    # 5. 量化差距
    # =================================================================
    print("\n" + "=" * 70)
    print("量化差距: MORL vs MILP Oracle")
    print("=" * 70)
    # 对于"纯收益最大化"场景
    milp_best_rev = max(p["revenue"] for p in milp_pts)
    morl_profit_rev = next(
        p["revenue"] for p in morl_pts if p["strategy"] == "Profit-Heavy"
    )
    rule_rev = rule_return[0]
    no_bat_rev = no_bat[0]

    print(f"  MILP 最优收益（完美信息）: {milp_best_rev:7.2f} ¥")
    print(f"  MORL Profit-Heavy 策略:    {morl_profit_rev:7.2f} ¥")
    print(f"  TOU 规则策略:              {rule_rev:7.2f} ¥")
    print(f"  不调度电池:                {no_bat_rev:7.2f} ¥")
    print()

    gap_morl = (milp_best_rev - morl_profit_rev)
    improvement = morl_profit_rev - no_bat_rev
    milp_improvement = milp_best_rev - no_bat_rev
    recovery_ratio = improvement / milp_improvement if milp_improvement > 0 else 0

    print(f"  MORL 回收可获收益比例: {recovery_ratio * 100:.1f}%")
    print(f"    (即 MORL 抓到了 MILP Oracle 所能获得收益提升的 {recovery_ratio*100:.1f}%)")
    print()
    print("  备注：")
    print("  - MILP 假设完美知道未来 96 步所有外生变量")
    print("  - MORL 只用当前观察 + 滚动预测（预测含噪声）")
    print("  - 用更多训练步数、更大网络（神经网络版）可进一步缩小差距")

    # 保存汇总
    all_rows = []
    for p in milp_pts:
        all_rows.append({"method": "MILP", "strategy": f"w={p['w']}",
                         "revenue": p["revenue"], "co2": p["co2"], "deg": p["deg"]})
    for p in morl_pts:
        all_rows.append({"method": "MORL", "strategy": p["strategy"],
                         "revenue": p["revenue"], "co2": p["co2"], "deg": p["deg"]})
    all_rows.append({"method": "Rule", "strategy": "TOU",
                     "revenue": rule_return[0], "co2": -rule_return[1], "deg": -rule_return[2]})
    all_rows.append({"method": "NoBat", "strategy": "baseline",
                     "revenue": no_bat[0], "co2": -no_bat[1], "deg": -no_bat[2]})

    pd.DataFrame(all_rows).to_csv("/home/claude/morl_refined/final_benchmark.csv",
                                  index=False)


if __name__ == "__main__":
    main()
