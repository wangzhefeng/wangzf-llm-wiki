---
created_at: 2026-04-11
topics:
- reinforcement-learning
related_concepts:
  - 长上下文优化
  - 稀疏注意力
  - 模型架构创新
status: summarized
source_path: raw/web/reinforcement-learning/2026-04-06-Deepseek新发布的DSA，太炸裂了！.md
---
# 来源卡：2026-04-06-Deepseek新发布的DSA，太炸裂了！

## 这份材料讲了什么

DeepSeek-V3.2-Exp 技术报告解读。核心内容：
- **模型架构**：新增 DeepSeek Sparse Attention（DSA）稀疏注意力机制，基于 Lightning Indexer 组件
- **长上下文优化**：在 128K token 上下文下推理成本下降 50%+，支持低成本持续学习
- **Lightning Indexer**：核心创新组件，计算 query token 与前文 token 的索引分数，筛选关键 token，采用 MQA 模式与 FP8 精度
- **训练流程**：Dense Warm-up Stage（参数初始化与对齐）→ Sparse Training Stage（细粒度 token 选择）→ Post-Training（沿用已有流水线）

## 价值是什么

深入解读大模型长上下文处理的最新工程优化方向。DSA 稀疏注意力机制代表了降低长序列成本的实践案例，对理解现代 LLM 架构设计与工程化思路有重要参考价值。特别适合关注大模型工程优化与成本节约方向的研究者。

## 连到哪些概念

- [[强化学习总索引]]（工程实践）
- [[LLM架构训练与微调索引]]（模型架构优化）
