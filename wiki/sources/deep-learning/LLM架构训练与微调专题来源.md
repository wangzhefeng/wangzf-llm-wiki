---
source_type: web
title: LLM 架构、训练与微调专题
created_at: 2026-04-06
topics:
- deep-learning
- llm
- shared
related_concepts:
- Transformer 架构
- RoPE
- KV Cache
- RLHF
- 量化
status: summarized
---
# LLM 架构、训练与微调专题

## 来源概述

本专题收纳了关于大语言模型（LLM）架构设计、训练策略、微调方法和评估部署的相关来源。涵盖从架构对比到实际部署的全流程。

## 来源清单

### 架构与原理

| 主题 | 核心内容 | 状态 |
|------|----------|------|
| LLM 架构对比 | DeepSeek-V3 到 Gemma 4 的架构分析 | 待摘要 |
| RoPE 位置编码 | 为什么主流 LLM 都用 RoPE | 待摘要 |
| KV Cache | KV Cache 原理与从零实现 | 待摘要 |
| 从零构建 LLM | TinyLlama、中文 LLM 实现 | 待摘要 |

### 训练与微调

| 主题 | 核心内容 | 状态 |
|------|----------|------|
| PEFT/LoRA | 参数高效微调方法 | 待摘要 |
| 4-bit 量化 | bitsandbytes、QLoRA | 待摘要 |
| 分布式训练 | DDP、多 GPU 训练 | 待摘要 |

### 对齐与后训练

| 主题 | 核心内容 | 状态 |
|------|----------|------|
| RLHF | 人类反馈强化学习 | 待摘要 |
| DPO/ORPO | RLHF 替代方案 | 待摘要 |
| GRPO | 多卡训练实现 | 待摘要 |

### 评估与部署

| 主题 | 核心内容 | 状态 |
|------|----------|------|
| LLM 评估 | 四种评估方法、OpenCompass | 待摘要 |
| vLLM | 高效推理部署 | 待摘要 |

## 关键概念

- Transformer 架构
- RoPE (Rotary Position Embedding)
- KV Cache
- Grouped-Query Attention
- SwiGLU
- RLHF / DPO / ORPO
- 量化 (4-bit, QLoRA)

## 相关链接

- 深度学习总索引
- 机器学习总索引
