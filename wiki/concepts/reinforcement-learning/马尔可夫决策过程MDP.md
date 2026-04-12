---
created_at: 2026-04-06
topics:
- reinforcement-learning
related_concepts:
- 决策过程
- 马尔可夫性
status: inbox
---
# 马尔可夫决策过程 (MDP)

## 定义

马尔可夫决策过程 (Markov Decision Process, MDP) 是强化学习的数学基础框架，用于建模序列决策问题。

## 核心要素

MDP 由五元组 $(S, A, P, R, \gamma)$ 定义：

- **$S$**: 状态空间 (States)
- **$A$**: 动作空间 (Actions)
- **$P$**: 状态转移概率 $P(s'|s,a)$
- **$R$**: 奖励函数 $R(s,a,s')$
- **$\gamma$**: 折扣因子 $\gamma \in [0, 1]$

## 马尔可夫性

当前状态包含所有历史信息，未来状态仅取决于当前状态和动作：

$$P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_t, a_t, s_{t-1}, a_{t-1}, ...)$$

## 目标

找到最优策略 $\pi^*$ 最大化期望累积奖励：

$$\max E[\sum_{t=0}^{\infty} \gamma^t r_t]$$

## 求解方法

### 值迭代
- 迭代更新值函数
- 收敛到最优值函数

### 策略迭代
- 策略评估 + 策略改进
- 保证收敛到最优策略

### Q-Learning
- 无模型方法
- 学习动作值函数 $Q(s,a)$

## 相关概念

- [[马尔可夫过程 (MP)]]
- [[马尔可夫奖励过程 (MRP)]]
- [[贝尔曼方程]]
- [[策略评估]]
- [[价值迭代]]

## 相关来源

- [[强化学习专题来源]]
- [[2026-04-06-马尔可夫决策过程 - 动手学强化学习]]
- [[2026-04-06-第二章 马尔可夫决策过程 (MDP)]]
- [[2026-04-06-强化学习 david silver]]
- [[2026-04-06-zhouboleiintroRL Intro to Reinforcement Learning (强化学习纲要）]]

## 在强化学习中的地位

MDP 是几乎所有 RL 算法的基础，无论是传统的 Q-Learning、SARSA，还是现代的 PPO、GRPO，都可以归结为求解 MDP 问题。
