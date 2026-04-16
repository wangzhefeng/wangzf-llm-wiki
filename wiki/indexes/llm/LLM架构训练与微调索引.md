---
created_at: 2026-04-06
updated_at: 2026-04-06
topics:
  - LLM 架构
  - 模型训练
related_concepts:
  - Transformer 架构
  - RLHF
  - 模型量化
status: linked
---

# LLM 架构、训练与微调索引

> 迁移说明：LLM 主题的统一入口是 大语言模型总索引。本页保留“深度学习视角”的训练与微调子索引角色。

## 概述

本索引收录了大语言模型（LLM）架构设计、训练策略、微调方法和评估部署的相关来源。

## 来源卡片

- [[LLM架构训练与微调专题来源]]
- [[LLM架构微调与多模态扩展专题来源]]

## 架构与原理

### 核心架构
- [[The Big LLM Architecture Comparison]] — DeepSeek-V3 到 Gemma 4 架构对比
- [[Understanding and Coding the KV Cache in LLMs from Scratch]] — KV Cache 实现
- [[为什么主流 LLM 都用 RoPE？]] — 旋转位置编码分析

### 从零构建
- [[tiny-llm-zh]] — 从零实现中文小参数量 LLM
- [[Understanding Multimodal LLMs]] — 多模态 LLM 技术

## 训练与微调

### 参数高效微调
- [[Guide to fine-tuning LLMs using PEFT and LoRa]]
- [[Making LLMs even more accessible with bitsandbytes, 4-bit quantization and QLoRA]]
- [[2025-07-05-llm-finetuning]]

### 分布式训练
- [[Training extremely large neural networks across thousands of GPUs]]
- [["real-world" models with DDP]]

## 对齐与后训练

### RLHF 与替代方案
- [[LLM Training: RLHF and Its Alternatives]] — Sebastian Raschka 教程
- [[RLHF and alternatives: ORPO]] — ORPO 方法
- [[GRPO_From_Scratch_Multi_GPU]] — GRPO 多卡实现

### 推理能力
- [[How LLMs learn to reason]] — 后训练策略分析
- [[Why We Think]] — test-time compute 综述

## 评估与部署

- [[Understanding the 4 Main Approaches to LLM Evaluation]]
- [[Evaluate LLMs and RAG]]
- [[Structured LLM outputs]]

## 关键概念

- [[Transformer架构]]
- [[RoPE]]
- [[KV Cache]]
- [[RLHF]]
- [[DPO直接偏好优化]]
- [[模型量化]]
- [[模型微调]]
- [[模型微调]]
- [[注意力机制]]
- [[分布式训练]]

## 方法入口

- 深度学习总索引
- 大语言模型总索引
- 机器学习总索引
- 强化学习总索引
