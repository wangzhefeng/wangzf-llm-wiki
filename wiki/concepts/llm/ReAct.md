---
created_at: 2026-04-16
topics:
- llm
- vibe-coding
related_concepts:
- Agent智能体
- 提示词工程
- 上下文工程
status: linked
---
# ReAct

ReAct 是把推理（Reasoning）与行动（Acting）交替组织起来的 Agent 基本范式，常用于搜索、工具调用和多步任务执行。

## 核心要点

- 让模型先写出当前判断，再触发工具，再根据观察继续下一步。
- 优点是过程可解释、容易插入人工检查点，也便于失败回放。
- 局限是上下文开销较大，对工具反馈质量敏感，因此常与 [[上下文工程]] 一起设计。

## 相关来源

- [[2026-04-06-Advanced-Prompt-Engineering-Techniques]]
- [[2026-04-06-Agents Companion]]
