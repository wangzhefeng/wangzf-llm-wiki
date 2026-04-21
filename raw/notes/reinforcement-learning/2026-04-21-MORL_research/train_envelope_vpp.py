"""
train_envelope_vpp.py
=====================
使用 MORL-Baselines 的 Envelope Q-Learning 在精细 VPP 环境上训练多目标策略。

依赖（本地环境）：
    pip install mo-gymnasium morl-baselines torch wandb

注意：此脚本需要在您本地或带 GPU 的环境运行。本项目沙箱因磁盘限制未安装 torch。

训练流程：
    1. 从 CSV 加载一年的 VPP 数据
    2. 构建精细化 MO 环境，配置 4 个目标
    3. 用 Envelope Q-Learning 训练 ~300k 步（每 episode = 1 天 = 96 步）
    4. 在不同偏好权重下评估，生成 Pareto 前沿近似
    5. 输出评估报告、可视化、保存模型权重
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path

# ---------- 依赖导入 ----------
try:
    import torch
    from morl_baselines.multi_policy.envelope.envelope import Envelope
    from morl_baselines.common.evaluation import (
        eval_mo, policy_evaluation_mo, hypervolume
    )
    HAS_MORL = True
except ImportError as e:
    print(f"[WARN] MORL-Baselines / torch 未安装: {e}")
    print("       请执行: pip install mo-gymnasium morl-baselines torch")
    HAS_MORL = False

from refined_vpp_env import RefinedVPPEnv, BatteryParams, EnvParams


# ======================================================================
# 训练配置
# ======================================================================
CONFIG = {
    "data_path": "/home/claude/morl_refined/vpp_year_dataset.csv",
    "output_dir": "/home/claude/morl_refined/morl_results",
    # 训练超参
    "total_timesteps": 300_000,       # 总步数：300k ≈ 3000 天模拟
    "learning_rate": 3e-4,
    "gamma": 0.99,
    "batch_size": 128,
    "buffer_size": 200_000,
    "net_arch": [256, 256],
    "num_sample_w": 8,                # Envelope 关键超参：每次采样 8 个偏好做 target
    "initial_epsilon": 1.0,
    "final_epsilon": 0.05,
    "epsilon_decay_steps": 150_000,
    "learning_starts": 2_000,
    # 评估
    "ref_point": np.array([-500.0, -200.0, -500.0, -100.0]),  # 超体积参考点
    "eval_weights": [
        ("profit_max",   np.array([1.00, 0.00, 0.00, 0.00])),
        ("balanced",     np.array([0.40, 0.20, 0.25, 0.15])),
        ("low_carbon",   np.array([0.30, 0.50, 0.10, 0.10])),
        ("battery_life", np.array([0.20, 0.10, 0.60, 0.10])),
        ("risk_averse",  np.array([0.25, 0.15, 0.20, 0.40])),
    ],
}


# ======================================================================
# 环境构建
# ======================================================================
def make_env(csv_path: str, split: str = "train"):
    """
    按日期切分：
    - train:  01-01 ~ 10-31 (≈305 天)
    - val:    11-01 ~ 11-30 (≈30 天)
    - test:   12-01 ~ 12-30 (≈30 天)
    """
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    if split == "train":
        df = df[df["timestamp"] < "2024-11-01"].reset_index(drop=True)
    elif split == "val":
        mask = (df["timestamp"] >= "2024-11-01") & (df["timestamp"] < "2024-12-01")
        df = df[mask].reset_index(drop=True)
    elif split == "test":
        df = df[df["timestamp"] >= "2024-12-01"].reset_index(drop=True)

    battery = BatteryParams(
        capacity_kwh=400.0,
        p_max_kw=100.0,
        p_min_kw=-100.0,
        cycle_life_at_100dod=4000.0,
        dod_exponent=1.8,
        capex_per_kwh=1200.0,
    )
    params = EnvParams(
        horizon=96,                    # 1 天一个 episode
        carbon_price=0.10,
        terminal_soc_penalty_weight=1.0,
    )
    env = RefinedVPPEnv(data=df, battery=battery, params=params)
    return env


# ======================================================================
# 训练
# ======================================================================
def train():
    if not HAS_MORL:
        print("无法训练：MORL-Baselines 不可用")
        return

    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")

    # 训练环境与评估环境
    train_env = make_env(CONFIG["data_path"], split="train")
    eval_env = make_env(CONFIG["data_path"], split="val")
    print(f"训练环境 obs_dim={train_env.observation_space.shape[0]}, "
          f"n_actions={train_env.action_space.n}, reward_dim={train_env.reward_dim}")

    # 初始化 Envelope Q-Learning
    agent = Envelope(
        env=train_env,
        learning_rate=CONFIG["learning_rate"],
        gamma=CONFIG["gamma"],
        batch_size=CONFIG["batch_size"],
        buffer_size=CONFIG["buffer_size"],
        net_arch=CONFIG["net_arch"],
        initial_epsilon=CONFIG["initial_epsilon"],
        final_epsilon=CONFIG["final_epsilon"],
        epsilon_decay_steps=CONFIG["epsilon_decay_steps"],
        learning_starts=CONFIG["learning_starts"],
        num_sample_w=CONFIG["num_sample_w"],
        project_name="morl-vpp",
        experiment_name="envelope-vpp-4obj",
        log=False,                    # 设 True 启用 wandb
    )

    # 开训
    agent.train(
        total_timesteps=CONFIG["total_timesteps"],
        eval_env=eval_env,
        ref_point=CONFIG["ref_point"],
        weight=None,                  # None 表示每个 episode 随机采样偏好
    )

    # 保存模型
    model_path = os.path.join(CONFIG["output_dir"], "envelope_final.pt")
    agent.save(model_path)
    print(f"模型已保存到 {model_path}")

    return agent


# ======================================================================
# 评估：不同偏好 → 生成 Pareto 前沿近似
# ======================================================================
def evaluate(agent, split: str = "test", n_episodes: int = 20):
    if not HAS_MORL:
        return

    env = make_env(CONFIG["data_path"], split=split)
    results = []

    for name, w in CONFIG["eval_weights"]:
        returns = np.zeros(env.reward_dim)
        for ep in range(n_episodes):
            ep_return, _, _ = eval_mo(agent, env, w=w)
            returns += ep_return
        returns /= n_episodes
        scalar = float(np.dot(w, returns))

        results.append({
            "strategy": name,
            "weight": w.tolist(),
            "revenue":   float(returns[0]),
            "co2_cost":  -float(returns[1]),
            "degradation": -float(returns[2]),
            "risk":      -float(returns[3]),
            "scalar_utility": scalar,
        })
        print(f"[{name:15s}] 收益={returns[0]:7.1f}  "
              f"碳={-returns[1]:6.1f}  退化={-returns[2]:6.1f}  "
              f"风险={-returns[3]:6.1f}")

    # 保存为 CSV
    df = pd.DataFrame(results)
    out = os.path.join(CONFIG["output_dir"], f"pareto_approximation_{split}.csv")
    df.to_csv(out, index=False)
    print(f"评估结果已保存到 {out}")
    return df


# ======================================================================
# 主流程
# ======================================================================
if __name__ == "__main__":
    agent = train()
    if agent is not None:
        evaluate(agent, split="test", n_episodes=20)
