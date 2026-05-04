---
created_at: 2026-04-06
topics:
- llm
- reinforcement-learning
related_concepts:
- 策略优化
- 群体相对
- 无价值模型
status: summarized
---
# GRPO (Group Relative Policy Optimization)

## 定义

GRPO（群体相对策略优化）是 DeepSeek 于 2024 年提出的一种新型强化学习算法，用于 LLM 对齐和推理训练。

## 核心创新

GRPO 的关键创新是**去除了价值模型**，仅使用群体相对优势：

$$\hat{A}_i = \frac{r_i - \text{mean}(\{r_1, ..., r_G\})}{\text{std}(\{r_1, ..., r_G\})}$$

其中：
- $r_i$ 是第 $i$ 个样本的奖励
- $G$ 是群体大小
- 不需要训练额外的价值模型

## 与 PPO 的对比

| 特性 | PPO | GRPO |
|------|-----|------|
| 价值模型 | 需要 | **不需要** |
| 优势计算 | 基于 TD/GAE | 基于群体相对奖励 |
| 训练复杂度 | 较高（两个模型） | 较低（一个模型） |
| 稳定性 | 依赖价值模型质量 | 更稳定 |
| 内存占用 | 较高 | 较低 |

## 为什么有效

1. **去除价值模型**: 减少训练复杂度和不稳定性
2. **群体归一化**: 通过群体统计消除奖励尺度问题
3. **适合 LLM**: LLM 输出空间巨大，价值模型难以准确估计

## 在 DeepSeek-R1 中的应用

GRPO 是 DeepSeek-R1 推理模型的核心训练方法：
1. **生成多个输出**: 对同一提示生成多个响应
2. **奖励计算**: 使用规则或模型打分
3. **群体归一化**: 计算相对优势
4. **策略更新**: 使用裁剪目标函数更新策略

## 实现要点

```python
# 简化示例
group_rewards = [compute_reward(output) for output in group_outputs]
normalized_rewards = (group_rewards - mean(group_rewards)) / std(group_rewards)
```

## 相关来源

- [[强化学习专题来源]]
- 2026-04-06-DeepSeek关键RL算法GRPO，有人从头跑通了，贡献完整代码
- 2026-04-06-DeepSeek 背后的数学原理：深入探究群体相对策略优化 (GRPO)
- 2026-04-06-Implementing GRPO in TRL
- `2026-04-06-theLMbookGRPO_From_Scratch_Multi_GPU_DataParallel_Qwen_2_5_1_5B_Instruct.ipynb`
- 2026-04-06-PPO→GRPO→DAPO，强化学习一篇通关！

## 相关概念

- [[PPO近端策略优化]]
- [[策略优化]]
- [[奖励模型]]
- [[LLM 对齐]]
