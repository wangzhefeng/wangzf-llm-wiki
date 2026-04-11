---
created_at: 2026-04-06
topics:
  - 强化学习
related_concepts:
  - 策略优化
  - 优势函数
  - 裁剪
status: inbox
---

# PPO (Proximal Policy Optimization)

## 定义

PPO（近端策略优化）是一种流行的强化学习算法，由 OpenAI 于 2017 年提出。它通过限制策略更新幅度来保证训练稳定性。

## 核心思想

PPO 的关键创新是使用**裁剪目标函数**来防止策略更新过大：

$$L^{CLIP}(\theta) = E_t[\min(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t)]$$

其中：
- $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$ 是概率比
- $\hat{A}_t$ 是优势函数估计
- $\epsilon$ 是裁剪参数（通常 0.1-0.3）

## 为什么有效

1. **On-Policy**: 使用当前策略收集数据
2. **裁剪机制**: 防止策略更新过大，避免训练崩溃
3. **简单易实现**: 相比 TRPO，PPO 更容易实现和调参
4. **样本效率**: 多轮 epoch 更新，提高样本利用率

## 关键组件

### 优势函数 (Advantage Function)

$$A(s,a) = Q(s,a) - V(s)$$

表示在状态 $s$ 执行动作 $a$ 相比平均水平的优势。

### 广义优势估计 (GAE)

$$\hat{A}_t^{GAE} = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}$$

其中 $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ 是 TD 误差。

## PPO-Clip vs PPO-Penalty

| 类型 | 特点 |
|------|------|
| PPO-Clip | 使用裁剪函数，更常用 |
| PPO-Penalty | 使用 KL 散度惩罚 |

## 在 LLM 训练中的应用

PPO 是 RLHF 的核心算法之一：
1. **SFT**: 监督微调基础模型
2. **Reward Model**: 训练奖励模型
3. **PPO**: 使用 PPO 优化策略，最大化奖励
4. **迭代**: 多轮迭代提升模型性能

## 算法演进

- **PPO** (2017): 原始算法
- **GRPO** (2024): DeepSeek 提出，去除价值模型，使用群体相对策略优化
- **DAPO**: 进一步改进的 PPO 变体

## 相关来源

- [[强化学习专题来源]]
- [[2026-04-06-人人都能看懂的RL-PPO理论知识]]
- [[2026-04-06-图解大模型RLHF系列之：人人都能看懂的PPO原理与源码解读]]
- [[2026-04-06-PPO→GRPO→DAPO，强化学习一篇通关！]]
- [[2026-04-06-gaoxiaosSupermariobros-PPO-pytorch rl on super-mario-bros]]

## 相关概念

- [[GRPO (Group Relative Policy Optimization)]]
- [[优势函数]]
- [[On-Policy vs Off-Policy]]
- [[RLHF]]
- [[策略优化]]
