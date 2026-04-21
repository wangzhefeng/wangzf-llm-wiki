"""
numpy_envelope_demo.py
======================
用纯 NumPy 手写的 Envelope Q-Learning 简化实现，无 torch 依赖。

适用场景：快速验证环境设计、理解算法核心数学。不适合生产。
核心数学逻辑与 Yang 等 (NeurIPS 2019) 原论文一致：

    Q 值形式：Q(s, w) ∈ R^(A × d)
    Envelope 目标：
        (a*, w*) = argmax_{a', w'} w^T Q(s', a'; w')
        y = r + γ · Q(s', a*; w*)   [作为向量]

本实现为了可读性做了以下简化：
    - 状态离散化为哈希桶（tile coding 近似）
    - 使用显式字典存储 Q 值而非神经网络
    - 偏好采样数 N_w = 4

尽管是玩具级实现，在设计得当的小环境上能快速收敛并展示 Pareto 前沿。
"""

import numpy as np
import pandas as pd
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Tuple, List
import pickle

from refined_vpp_env import RefinedVPPEnv, BatteryParams, EnvParams


# ======================================================================
# 状态离散化：Tile Coding 简化版
# ======================================================================
class StateDiscretizer:
    """把连续观察离散化为哈希桶，用于表格 Q 学习。"""

    def __init__(self, bins_config: Dict[int, Tuple[float, float, int]]):
        """
        bins_config: {obs_idx: (low, high, n_bins)}
        """
        self.bins_config = bins_config

    def discretize(self, obs: np.ndarray) -> tuple:
        key_parts = []
        for idx, (low, high, n_bins) in self.bins_config.items():
            x = np.clip(obs[idx], low, high)
            b = int((x - low) / (high - low + 1e-9) * n_bins)
            b = min(b, n_bins - 1)
            key_parts.append(b)
        return tuple(key_parts)


# ======================================================================
# Envelope Q-Learning (表格版, 纯 NumPy)
# ======================================================================
@dataclass
class EnvelopeQLConfig:
    lr: float = 0.1
    gamma: float = 0.98
    epsilon_start: float = 1.0
    epsilon_end: float = 0.05
    epsilon_decay_episodes: int = 200
    num_sample_w: int = 4             # 每步采样的候选偏好数量
    num_target_update_samples: int = 8
    lambda_homo: float = 0.0          # 标量损失权重（演示用 0，仅用向量更新）


class EnvelopeQLearner:
    """表格版 Envelope Q-Learning。"""

    def __init__(self, n_actions: int, reward_dim: int,
                 discretizer: StateDiscretizer,
                 config: EnvelopeQLConfig = None):
        self.n_actions = n_actions
        self.reward_dim = reward_dim
        self.disc = discretizer
        self.cfg = config or EnvelopeQLConfig()

        # Q[state_key, action_idx] -> 向量 shape (reward_dim,)
        # 为了支持"以偏好为条件"的查询，我们存储不带偏好的 Q 向量
        # 并在查询时对偏好做标量化
        self.Q: Dict[Tuple, np.ndarray] = defaultdict(
            lambda: np.zeros((self.n_actions, self.reward_dim))
        )
        self._rng = np.random.default_rng(0)

    # ------------------------------------------------------------------
    # 核心：Envelope 目标计算
    # ------------------------------------------------------------------
    def _envelope_target(self, s_key: tuple, w: np.ndarray,
                         sample_ws: np.ndarray) -> np.ndarray:
        """
        核心数学：对 (a', w') 联合取 argmax w^T Q(s', a'; w')
        返回整个向量 Q 作为目标。

        因为我们是表格法，Q 不显式依赖 w'，所以 w' 的枚举退化为
        寻找在不同 w' 下最优的 a' 的集合，然后在这个集合中对 w 标量化最大化。
        """
        q_vec = self.Q[s_key]                      # shape (A, d)
        # 对每个候选 w_j ∈ sample_ws 找到它偏爱的动作 a_j
        scalarized = sample_ws @ q_vec.T           # (N_w, A)
        best_actions_per_w = np.argmax(scalarized, axis=1)  # (N_w,)
        candidate_q_vecs = q_vec[best_actions_per_w]         # (N_w, d)

        # 在当前查询 w 下从候选集选出最好的
        scalar_under_w = candidate_q_vecs @ w      # (N_w,)
        best_idx = int(np.argmax(scalar_under_w))
        return candidate_q_vecs[best_idx]          # (d,)

    # ------------------------------------------------------------------
    # 动作选择：ε-贪婪 w.r.t. w^T Q(s, a)
    # ------------------------------------------------------------------
    def act(self, s_key: tuple, w: np.ndarray, epsilon: float) -> int:
        if self._rng.random() < epsilon:
            return int(self._rng.integers(self.n_actions))
        q_vec = self.Q[s_key]                      # (A, d)
        scalarized = q_vec @ w                     # (A,)
        return int(np.argmax(scalarized))

    # ------------------------------------------------------------------
    # 更新
    # ------------------------------------------------------------------
    def update(self, s_key, action, reward_vec, s_next_key, done, w):
        # 采样一组候选偏好 (包括当前 w)
        sample_ws = self._sample_weights(self.cfg.num_sample_w - 1)
        sample_ws = np.vstack([w, sample_ws])

        if done:
            target_vec = reward_vec
        else:
            env_target = self._envelope_target(s_next_key, w, sample_ws)
            target_vec = reward_vec + self.cfg.gamma * env_target

        # 向量 TD 更新
        q_old = self.Q[s_key][action]
        self.Q[s_key][action] = q_old + self.cfg.lr * (target_vec - q_old)

    def _sample_weights(self, n: int) -> np.ndarray:
        """Dirichlet(1, ..., 1) 采样权重，得均匀分布的单纯形点。"""
        return self._rng.dirichlet(np.ones(self.reward_dim), size=n)


# ======================================================================
# 训练循环
# ======================================================================
def run_training(n_episodes: int = 300, verbose_every: int = 25):
    """
    在 VPP 环境上训练 Envelope Q-Learning（小规模 demo）。
    """
    # 1. 构建环境（取一小段数据加速训练）
    df = pd.read_csv("/home/claude/morl_refined/vpp_year_dataset.csv",
                     parse_dates=["timestamp"])
    # 用 7 月份（典型夏季高光伏）做训练
    df_july = df[(df["timestamp"] >= "2024-07-01") &
                 (df["timestamp"] < "2024-08-01")].reset_index(drop=True)
    print(f"训练数据：{len(df_july)} 行 (7 月)")

    battery = BatteryParams(capacity_kwh=400.0, p_max_kw=100.0, p_min_kw=-100.0)
    params = EnvParams(horizon=96, carbon_price=0.10, terminal_soc_penalty_weight=0.5)
    env = RefinedVPPEnv(data=df_july, battery=battery, params=params)

    # 2. 状态离散化：只取关键维度
    # obs[0]=SOC, obs[1]=prev_p, obs[5]=price, obs[6]=pv/norm, obs[7]=load/norm
    # obs[8]=forecast_price_15min, obs[9]=forecast_pv, obs[10]=forecast_load
    discretizer = StateDiscretizer({
        0: (0.0, 1.0, 6),           # SOC 分 6 档
        2: (-1.0, 1.0, 4),          # hour_sin
        3: (-1.0, 1.0, 4),          # hour_cos
        5: (-0.2, 1.5, 8),          # 当前价格
        6: (0.0, 1.5, 4),           # PV/norm
    })

    # 3. 算法
    cfg = EnvelopeQLConfig(
        lr=0.15,
        gamma=0.98,
        epsilon_start=1.0,
        epsilon_end=0.08,
        epsilon_decay_episodes=int(n_episodes * 0.7),
        num_sample_w=6,
    )
    agent = EnvelopeQLearner(
        n_actions=env.action_space.n,
        reward_dim=env.reward_dim,
        discretizer=discretizer,
        config=cfg,
    )

    # 4. 主训练循环
    history = []
    rng = np.random.default_rng(123)

    for ep in range(n_episodes):
        # 每个 episode 随机一个偏好
        w_ep = rng.dirichlet(np.ones(env.reward_dim))

        # 随机起始日（7月内）
        start_day = rng.integers(0, 30)
        obs, info = env.reset(options={"start_day": start_day})
        s_key = discretizer.discretize(obs)

        epsilon = max(
            cfg.epsilon_end,
            cfg.epsilon_start - (cfg.epsilon_start - cfg.epsilon_end)
            * ep / cfg.epsilon_decay_episodes
        )

        ep_reward_vec = np.zeros(env.reward_dim)
        done = False
        steps = 0
        while not done:
            action = agent.act(s_key, w_ep, epsilon)
            obs_next, r_vec, term, trunc, info = env.step(action)
            s_next_key = discretizer.discretize(obs_next)
            done = term or trunc

            agent.update(s_key, action, r_vec, s_next_key, done, w_ep)

            s_key = s_next_key
            ep_reward_vec += r_vec
            steps += 1

        history.append({
            "ep": ep,
            "w": w_ep,
            "return_vec": ep_reward_vec,
            "scalar_return": float(np.dot(w_ep, ep_reward_vec)),
            "epsilon": epsilon,
            "n_states_seen": len(agent.Q),
        })

        if (ep + 1) % verbose_every == 0:
            recent = history[-verbose_every:]
            avg_scalar = np.mean([h["scalar_return"] for h in recent])
            avg_rev = np.mean([h["return_vec"][0] for h in recent])
            avg_co2 = np.mean([h["return_vec"][1] for h in recent])
            avg_deg = np.mean([h["return_vec"][2] for h in recent])
            print(f"Ep {ep + 1:3d}  ε={epsilon:.2f}  "
                  f"|states|={len(agent.Q):4d}  "
                  f"avg scalar={avg_scalar:7.1f}  "
                  f"revenue={avg_rev:6.1f}  "
                  f"co2={avg_co2:5.1f}  "
                  f"deg={avg_deg:5.1f}")

    return agent, env, history


# ======================================================================
# 评估：在固定偏好下推断 Pareto 前沿近似
# ======================================================================
def evaluate_pareto(agent, env, weights_list, n_episodes=10, seed=999):
    rng = np.random.default_rng(seed)
    results = []
    for name, w in weights_list:
        acc = np.zeros(env.reward_dim)
        for _ in range(n_episodes):
            start_day = rng.integers(0, 25)
            obs, _ = env.reset(options={"start_day": start_day})
            s_key = agent.disc.discretize(obs)
            done = False
            ep_vec = np.zeros(env.reward_dim)
            while not done:
                action = agent.act(s_key, w, epsilon=0.0)   # 贪婪
                obs_next, r_vec, term, trunc, info = env.step(action)
                s_key = agent.disc.discretize(obs_next)
                done = term or trunc
                ep_vec += r_vec
            acc += ep_vec
        acc /= n_episodes
        results.append({
            "strategy": name,
            "weight": w,
            "avg_return_vec": acc,
            "avg_scalar": float(w @ acc),
        })
    return results


# ======================================================================
# 主函数
# ======================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Envelope Q-Learning Demo（纯 NumPy 表格法）")
    print("=" * 70)

    agent, env, history = run_training(n_episodes=400, verbose_every=50)

    print("\n" + "=" * 70)
    print("Pareto 前沿近似评估")
    print("=" * 70)
    eval_weights = [
        ("profit_only",   np.array([1.0, 0.0, 0.0, 0.0])),
        ("profit_heavy",  np.array([0.7, 0.1, 0.1, 0.1])),
        ("balanced",      np.array([0.4, 0.2, 0.25, 0.15])),
        ("low_carbon",    np.array([0.3, 0.5, 0.1, 0.1])),
        ("battery_life",  np.array([0.2, 0.1, 0.6, 0.1])),
        ("risk_averse",   np.array([0.25, 0.15, 0.20, 0.40])),
    ]
    results = evaluate_pareto(agent, env, eval_weights, n_episodes=5)

    print(f"\n{'策略':18s} | {'收益':>8s} | {'碳排成本':>9s} | {'电池退化':>9s} | {'风险':>7s}")
    print("-" * 72)
    for r in results:
        v = r["avg_return_vec"]
        print(f"{r['strategy']:18s} | {v[0]:8.1f} | {-v[1]:9.1f} | "
              f"{-v[2]:9.1f} | {-v[3]:7.2f}")

    # 保存
    df_results = pd.DataFrame([
        {
            "strategy": r["strategy"],
            "w0_revenue": r["weight"][0],
            "w1_co2": r["weight"][1],
            "w2_deg": r["weight"][2],
            "w3_risk": r["weight"][3],
            "revenue": r["avg_return_vec"][0],
            "co2_cost": -r["avg_return_vec"][1],
            "deg_cost": -r["avg_return_vec"][2],
            "risk_cost": -r["avg_return_vec"][3],
        } for r in results
    ])
    out_path = "/home/claude/morl_refined/pareto_approximation.csv"
    df_results.to_csv(out_path, index=False)
    print(f"\n已保存到 {out_path}")

    # 保存训练历史
    df_history = pd.DataFrame([
        {"ep": h["ep"], "scalar_return": h["scalar_return"],
         "r_revenue": h["return_vec"][0], "r_co2": h["return_vec"][1],
         "r_deg": h["return_vec"][2], "r_risk": h["return_vec"][3],
         "epsilon": h["epsilon"], "w0": h["w"][0], "w1": h["w"][1],
         "w2": h["w"][2], "w3": h["w"][3]}
        for h in history
    ])
    df_history.to_csv("/home/claude/morl_refined/training_history.csv", index=False)
