---
source_type: web
source_path: raw/web/operations-research/2026-04-06-AlphaOPT：用大模型为优化建模构建可进化的“经验知识库”.md
created_at: 2026-04-06
topics:
  - operations-research
related_concepts:
  - LLM与运筹优化
  - 数值优化求解器
status: summarized
---
# AlphaOPT：LLM 优化建模经验知识库来源摘要

- 原文：[[raw/web/operations-research/2026-04-06-AlphaOPT：用大模型为优化建模构建可进化的"经验知识库"]]

## 材料定位

AlphaOPT 是一个将大模型与运筹优化建模结合的框架，核心思想是为 LLM 构建可进化的"建模经验知识库"——类比 AlphaGo 的价值网络，让 LLM 从历史建模成功/失败经验中不断学习，从而提升自动优化建模能力。

## 关键结论

- **核心问题**：LLM 直接做优化建模容易出错（约束遗漏、变量错误、不可行模型），缺乏可积累的建模经验。
- **AlphaOPT 框架**：构建可进化的建模经验知识库（类似 RAG 但专为 OR 定制），存储历史建模案例（成功 + 失败 + 修正路径），LLM 在建模时检索相似案例作为 few-shot 提示。
- **进化机制**：每次求解器执行后反馈结果，自动更新知识库（成功案例强化，失败模式标记）；随时间知识库质量持续提升。
- **与 RAG 的区别**：普通 RAG 仅检索静态知识，AlphaOPT 的知识库随每次建模尝试动态进化。
- **意义**：为"LLM 赋能 OR 建模"方向提供了一套闭环自改进的工程路径。

## related_sources

- [[2026-04-06-LLM与OR融合研究]]
- [[2026-04-06-求解器与大模型融合]]

## missing_context

- AlphaOPT 的具体评测基准和与 ORLM、SIRL 的定量对比未包含。
- 知识库规模、检索方法（向量检索/关键词）的具体实现细节未披露。
