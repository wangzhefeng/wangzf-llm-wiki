---
created_at: 2026-04-16
topics:
- llm
related_concepts:
- 提示词工程
- ReAct
- 上下文工程
status: linked
---
# CoT（Chain-of-Thought）

CoT 是通过在提示中显式要求模型分步推理，来提升复杂问题求解质量的提示策略。

## 核心要点

- 适合数学、规划、逻辑推理等需要中间步骤的问题。
- 价值不在“字数更多”，而在让模型暴露中间判断结构，便于检查和约束。
- 在工程上常与 [[提示词工程]]、结构化输出和结果校验一起使用。

## 相关来源

- [[2026-04-06-Advanced-Prompt-Engineering-Techniques]]
- [[2026-04-06-面向开发者的LLM入门教程]]
