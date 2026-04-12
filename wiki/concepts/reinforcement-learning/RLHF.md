---
created_at: 2026-04-09
topics:
- llm
- reinforcement-learning
related_concepts:
- 奖励模型
- DPO直接偏好优化
- 策略优化
status: linked
---
# RLHF

## 定义

RLHF（Reinforcement Learning from Human Feedback）是利用人类反馈构造奖励信号，再通过强化学习优化模型行为的对齐方法。

## 核心流程

1. 监督微调得到基础策略模型。
2. 基于人类偏好比较训练奖励模型。
3. 使用 PPO 等策略优化方法更新模型，使输出更符合人类偏好。

## 为什么归到强化学习主题

- 它的关键增量不只是“人类标注”，而是把偏好反馈转成奖励信号，再进入策略优化。
- 方法链路直接连接奖励模型、策略优化、PPO、DPO、GRPO 等强化学习/偏好优化方法。
- 在知识库里，它更适合作为“LLM 对齐中的强化学习方法入口”。

## 与 DPO 的关系

- RLHF 是经典多阶段流程，需要奖励模型和 RL 优化。
- DPO 试图保留偏好优化目标，同时去掉显式奖励模型与 RL 训练环节。

## 相关来源

- [[强化学习专题来源]]
- [[raw/web/reinforcement-learning/2026-04-06-图解大模型RLHF系列之：人人都能看懂的PPO原理与源码解读]]
- [[2026-04-06-LLM Training RLHF and Its Alternatives]]
- [[raw/web/llm-pre-training/2026-04-06-我的RLHF实践记录~]]

## 相关概念

- [[奖励模型]]
- [[PPO (Proximal Policy Optimization)]]
- [[DPO直接偏好优化]]
- [[策略优化]]

