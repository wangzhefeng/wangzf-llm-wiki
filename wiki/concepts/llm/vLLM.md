---
created_at: 2026-04-16
topics:
- llm
related_concepts:
- 推理部署与量化
- 长上下文
- KV Cache
status: linked
---
# vLLM

vLLM 是面向大模型在线推理的高吞吐推理引擎，代表性能力是连续批处理和分页注意力（PagedAttention）。

## 核心要点

- 通过更细粒度地管理 KV Cache，显著提升多请求场景下的吞吐率。
- 适合需要高并发、长上下文和动态请求调度的服务端推理。
- 与 [[推理部署与量化]] 的关系是：vLLM 是具体引擎实现，而后者讨论更宽的部署与显存优化策略。

## 相关来源

- [[2026-04-06-LLM推理框架：11-款主流大模型推理引擎汇总]]
- [[2026-04-06-Understanding-and-Coding-the-KV-Cache-in-LLMs-from-Scratch]]
