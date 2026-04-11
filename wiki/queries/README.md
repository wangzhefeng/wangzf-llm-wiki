---
created_at: 2026-04-11
topics:
  - wiki
  - queries
  - llm-wiki
related_concepts:
  - 知识库问答与研究工作流
status: linked
---

# wiki/queries

`wiki/queries/` 存放“可复用问答页 / 研究问题页”：把高频问题固化成可重复运行的查询模板（问题、范围、证据入口、输出格式）。

## 放什么

- 复用价值高的问题：会反复问、或会反复扩展证据
- 明确证据入口：指出要读哪些 `wiki/sources/`、`wiki/concepts/`、`outputs/` 入口

## 不放什么

- 一次性聊天式回答（默认放 `outputs/answers/`，需要复用时再迁入此处）

## 入口

- wiki 总入口：`wiki/index.md`
- schema 约束：`wiki/schema.md`
