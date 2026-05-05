---
created: 2026-04-16
updated: 2026-04-16
type: concept
tags:
  - deep-learning
  - llm
  - inference
sources:
  - wiki/concepts/llm/推理部署与量化.md
status: linked
---

# KV Cache

KV Cache 是推理阶段缓存 Key/Value 张量以避免重复计算的常见优化技术。

## 入口说明

- LLM 推理语境见 [[推理部署与量化]]
- 架构上下文见 [[Transformer架构]]
- 与位置扩展相关的讨论见 [[RoPE旋转位置编码]]
