---
created_at: 2026-04-06
topics:
  - 强化学习
  - LLM 对齐
related_concepts:
  - 偏好优化
  - 奖励模型
  - 直接优化
status: inbox
---

# DPO (Direct Preference Optimization)

## 定义

DPO（直接偏好优化）是一种简化 LLM 对齐的方法，由 Rafailov 等人于 2023 年提出。它直接优化偏好数据，无需单独的奖励模型和 RL 优化。

## 核心思想

DPO 的关键洞察是**奖励函数和策略之间存在一一映射**，可以直接从偏好数据优化策略：

$$\mathcal{L}_{DPO} = -E[\log \sigma(\beta \log \frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)})]$$

其中：
- $y_w$: 偏好的输出
- $y_l$: 不偏好的输出
- $\pi_{ref}$: 参考模型（通常是 SFT 模型）
- $\beta$: 温度参数

## 与 RLHF 的对比

| 特性 | RLHF | DPO |
|------|------|-----|
| 奖励模型 | 需要训练 | **不需要** |
| RL 优化 | PPO 等复杂算法 | **直接优化** |
| 训练流程 | 多阶段（SFT→RM→PPO） | **单阶段** |
| 计算复杂度 | 高 | **低** |
| 实现难度 | 复杂 | **简单** |
| 性能 | 强 | **相当或更好** |

## 为什么有效

1. **简化流程**: 去除奖励模型训练和 RL 优化
2. **稳定**: 直接优化偏好数据，避免 RL 的不稳定性
3. **高效**: 计算成本显著低于 RLHF
4. **理论保证**: 有坚实的优化理论基础

## 训练流程

1. **SFT**: 监督微调基础模型（与 RLHF 相同）
2. **收集偏好数据**: 对同一提示生成多个输出，人工标注偏好
3. **DPO 优化**: 直接使用 DPO 损失函数优化策略
4. **迭代**: 可选多轮 DPO 提升性能

## 变体

- **IPO**: Identity Preference Optimization
- **KTO**: Kahneman-Tversky Optimization
- **ORPO**: Odds Ratio Preference Optimization
- **SPIN**: Self-Play Fine-Tuning

## 相关来源

- [[强化学习专题来源]]
- [[2026-04-06-Direct Preference Optimization (DPO)]]
- [[2026-04-06-人人都能看懂的DPO数学原理]]
- [[2026-04-06-面试问了DPO算法，答得稀烂~]]
- `2026-04-06-deep-learning-pytorch-huggingfacetrainingscriptsdporun_dpo.py`

## 相关概念

- [[RLHF]]
- [[偏好优化]]
- [[奖励模型]]
- [[LLM 对齐]]
- [[ORPO]]
