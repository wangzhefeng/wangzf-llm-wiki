---
created_at: 2026-04-11
updated: 2026-04-16
topics:
  - llm
  - shared
status: active
---
# wiki/concepts/llm

本目录存放大语言模型相关概念、方法与工具的稳定页面。

## 核心概念页（Tier 1，8 个）

1. [[大语言模型]] — 基于 Transformer 的大规模语言模型总览
2. [[Transformer架构]] — 支撑高效并行序列处理的核心神经架构
3. [[预训练]] — 从海量无标注文本学习语言表示的预训练框架
4. [[后训练]] — 含监督微调与人类反馈强化学习的后训练框架
5. [[LLM 理论体系]] — 解释 LLM 如何学习与表示知识的理论基础
6. [[LLM 对齐]] — 使 LLM 输出与人类价值观对齐的方法框架
7. [[llm-arch]] — Transformer 架构变体（编码器-解码器、仅解码器等）
8. [[llm-app]] — 基于 LLM 构建应用的框架与模式（提示、集成）

## 方法级概念页（Tier 2，33 个）

### 提示与上下文
9. [[提示词工程]] — 设计有效提示词引导 LLM 行为的技术
10. [[上下文工程]] — 结构化上下文窗口以提升 LLM 性能的方法

### 微调与参数高效方法
11. [[模型微调]] — 将预训练模型适配特定任务的微调技术
12. [[Guide to fine-tuning LLMs using PEFT and LoRa]] — 参数高效微调方法（PEFT/LoRA）

### 量化与推理优化
13. [[模型量化]] — 降低模型体积与延迟的量化技术（4位、8位量化）
14. [[Making LLMs even more accessible with bitsandbytes, 4-bit quantization and QLoRA]] — 量化实践实现
15. [[推理部署与量化]] — 推理优化与部署策略
16. [[vLLM]] — 使用分页注意力的高吞吐 LLM 推理引擎
17. [[Understanding and Coding the KV Cache in LLMs from Scratch]] — KV 缓存优化

### 检索增强生成
18. [[rag]] — 检索增强生成：整合外部知识源的 LLM 框架
19. [[RAG检索增强生成]] — 知识检索框架（中文版）

### 评估
20. [[LLM 评估]] — LLM 综合评估框架
21. [[大语言模型评估]] — LLM 评估方法
22. [[Evaluate LLMs and RAG]] — LLM 与 RAG 系统的评估方法
23. [[Understanding the 4 Main Approaches to LLM Evaluation]] — 评估方法的系统分类

### 训练方法
24. [[InstructGPT]] — 使用 RLHF 的指令微调 GPT 变体
25. [[LLM Training: RLHF and Its Alternatives]] — 训练方法（RLHF 与替代方案）

### 多模态
26. [[多模态 LLM]] — 处理多种模态的 LLM（视觉、文本、音频）
27. [[Understanding Multimodal LLMs]] — 多模态模型设计技术与挑战

### 智能体与应用
28. [[Agent智能体]] — 使 LLM 能够执行行动与使用工具的智能体系统

### 嵌入与位置编码
29. [[Embedding]] — 从语言模型学习的文本/词元密集向量表示
30. [[RoPE (Rotary Position Embedding)]] — 现代 LLM 中使用的旋转位置编码
31. [[为什么主流 LLM 都用 RoPE？]] — RoPE 相对于其他方法的优势分析

### 其他技术与工具
32. [[Structured LLM outputs]] — 将 LLM 输出约束为结构化格式的技术
33. [[llm-models]] — 具体 LLM 模型实例及其特征
34. [[llm-framework]] — LLM 开发与部署的软件框架
35. [[LLM工程框架]] — 生产环境 LLM 系统的工程框架
36. [[tiny-llm-zh]] — 小规模中文语言模型
37. [[The Big LLM Architecture Comparison]] — 不同 LLM 架构对比
38. [[How LLMs learn to reason]] — LLM 推理能力分析
39. [[NLP任务]] — 自然语言处理任务与基准
40. [[LLM + OR]] — LLM 与运筹研究方法的结合
41. [[claude_code]] — Claude Code 功能与能力文档

## 入口建议

- **快速入门**：从 [[大语言模型]] 和 [[Transformer架构]] 建立整体认知
- **训练路径**：[[预训练]] → [[后训练]] → [[LLM 对齐]]
- **应用开发**：从 [[llm-app]] 和 [[提示词工程]] 入手
- **工程部署**：参考 [[推理部署与量化]]、[[vLLM]]、[[RAG检索增强生成]]
