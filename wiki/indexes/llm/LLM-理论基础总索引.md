---
created_at: 2026-04-15
updated_at: 2026-04-15
topics:
  - LLM-理论
  - Transformer
  - Self-Attention
  - 位置编码
related_concepts:
  - Transformer架构
  - Attention机制
  - KV-Cache
  - RoPE
  - Embedding
  - Tokenization
status: summarized
---

# LLM-理论基础总索引

## 总览

LLM 理论基础是构建大语言模型的核心知识体系。本主题深入讲解 Transformer 架构、Self-Attention 机制、位置编码（RoPE/ALiBi）、KV-Cache 等基础概念，以及这些设计如何赋予 LLM 处理长序列、并行计算和高效推理的能力。Transformer 相比 RNN 的主要优势在于完全的并行化，而 Self-Attention 机制使模型能够灵活地建模任意距离的依赖关系。位置编码确保模型能够感知序列中 token 的相对位置，而 KV-Cache 技术则是推理加速的关键。这些理论基础构成了从 BERT、GPT-2 到现代 LLaMA、Claude 等模型的共同基石。

## 核心概念导航

| 概念 | 类型 | 说明 |
|------|------|------|
| [[Transformer架构]] | 架构 | 基于全注意力机制的序列模型，LLM 的基础架构 |
| [[Self-Attention]] | 机制 | 自注意力机制，使模型能捕捉序列内任意位置的依赖关系 |
| [[RoPE]] | 位置编码 | 旋转位置编码，解决长序列推理中的位置外推问题 |
| [[KV Cache]] | 优化技术 | 推理加速技术，通过缓存 K-V 向量减少重复计算 |
| [[Embedding]] | 技术 | Token 嵌入，将离散 token 映射到连续向量空间 |
| [[Tokenization]] | 技术 | 分词，将文本转换为 token 序列的基础处理 |
| [[量化]] | 优化技术 | 模型参数低精度表示，降低显存需求和计算成本 |
| [[多头注意力]] | 机制 | Multi-Head Attention，使注意力并行聚焦不同特征子空间 |
| [[前馈网络]] | 层结构 | Feed-Forward Network，增加非线性和模型容量 |
| [[Layer Normalization]] | 稳定技术 | 层归一化，提高训练稳定性 |

## 来源清单

本索引覆盖 wiki/sources/llm 中标签为 `llm-theory` 的全部来源卡（50 篇）：

| 标题 | 来源类型 | 创建日期 | 关键词 |
|------|---------|---------|--------|
| FastText | web/notes | 2022-04-05 | 词向量、词嵌入 |
| BERT | web/notes | 2022-07-15 | Transformer、掩码语言模型 |
| GPT | web/notes | 2023-03-17 | 自回归、Transformer解码器 |
| LLM 模型--Gemma | web/notes | 2024-03-23 | Gemma、轻量级模型 |
| LLM 架构--RAG | web/notes | 2024-03-23 | 检索增强、向量数据库 |
| LLM 概览 | web/notes | 2024-03-24 | 模型架构、训练流程 |
| LLM 架构--Prompt | web/notes | 2024-04-09 | 提示词工程、上下文学习 |
| LLM 应用--ChatGPT | web/notes | 2024-05-02 | ChatGPT、指令跟随 |
| LLM 模型--Llama | web/notes | 2024-05-02 | LLaMA、开源模型 |
| LLM 框架--LangChain | web/notes | 2024-05-15 | LangChain、Agent框架 |
| GloVe | web/notes | 2024-05-16 | 词向量、矩阵分解 |
| LLM 架构--Agent | web/notes | 2024-06-10 | Agent、工具使用 |
| LLM 评估 | web/notes | 2024-06-10 | 基准测试、性能评估 |
| HuggingFace Transformers | web/notes | 2024-06-15 | Transformers库、预训练模型 |
| LLM 应用--RAG 应用--知识库 | web/notes | 2024-08-03 | RAG应用、知识检索 |
| LLM 应用--模型与API | web/notes | 2024-08-14 | API调用、模型部署 |
| LLM 应用--LLaMA 3 18B | web/notes | 2024-08-15 | LLaMA模型、推理 |
| LLM Embedding | web/notes | 2024-09-23 | 向量表示、相似度 |
| LLM 向量数据库 | web/notes | 2024-09-23 | 向量存储、检索效率 |
| 模型预训练 | web/notes | 2024-09-27 | 预训练流程、数据准备 |
| 字节对编码 BPE | web/notes | 2024-10-16 | 分词、BPE算法 |
| 语言模型 | web/notes | 2024-10-23 | 概率模型、似然估计 |
| 语言模型训练 | web/notes | 2024-10-26 | 训练流程、优化方法 |
| 语言模型架构 | web/notes | 2024-10-26 | Transformer、分词 |
| 语言模型数据 | web/notes | 2024-10-26 | 数据准备、清洗 |
| LLM 微调 | web/notes | 2025-07-05 | 微调方法、LoRA |
| RLHF | web/notes | 2025-07-05 | 强化学习对齐、奖励模型 |

（以上列出前27篇，共50篇来源卡）

## 阅读地图

### 初级（概念入门）

- [[Transformer架构]]（理解 Attention is All You Need 论文）
- [[Self-Attention]]（自注意力机制的直观讲解）
- [[Embedding]]（Token 到向量的映射原理）
- [[Tokenization]]（文本预处理与分词算法）

### 中级（深入理论/工程实践）

- [[RoPE]]（位置编码与长序列扩展）
- [[KV Cache]]（推理优化中的关键技术）
- [[多头注意力]]（并行特征学习）
- [[Layer Normalization]]（训练稳定性设计）

### 高级（前沿研究/最佳实践）

- [[量化]]（模型压缩与显存优化）
- [[长上下文]]（从 4K 到 128K+ tokens 的挑战）
- [[推理部署与量化]]（工业级部署方案）

## 相关索引

- 大语言模型总索引（父索引）
- LLM-预训练总索引（预训练实践入门）
- LLM-后训练总索引（指令微调与对齐）
