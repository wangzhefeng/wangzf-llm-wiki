---
created_at: 2026-04-11
topics:
  - wiki
  - sources
  - llm-wiki
related_concepts:
  - 知识库来源与专题摄取索引
status: linked
---

# wiki/sources

`wiki/sources/` 存放“来源摘要卡”（source card），用于把 `raw/` 的单条来源压缩成可检索、可互链的结构化入口。

## 放什么

- 每个来源 1 张卡：回答“这份材料讲什么、价值是什么、与哪些概念相关、下一步怎么用”。
- 卡片应尽量链接到：
  - 对应 `raw/` 原文（或原件路径）
  - 相关 `wiki/concepts/` 概念页
  - 相关 `wiki/indexes/` 主题入口（必要时）

## 不放什么

- 不放原始全文（原文应在 `raw/`）
- 不放长篇综述（阶段性综述放 `outputs/syntheses/`，再回流链接）

## 典型工作流

1. ingest：先把材料落到 `raw/`
2. 为该来源创建/更新来源卡：写入 `wiki/sources/<topic>/...md`
3. 如形成稳定复用价值：再回写 `wiki/indexes/`（导航）与 `wiki/concepts/`（概念）

## 命名建议

- 优先沿用原始来源文件名或 slug，保证可追溯。

## 入口

- wiki 总入口：`wiki/index.md`
- schema 约束：`wiki/schema.md`

## Topics

- [[wiki/sources/analysis/README]]
- [[wiki/sources/computervision/README]]
- [[wiki/sources/control_algorithms/README]]
- [[wiki/sources/data_structure_algorithm/README]]
- [[wiki/sources/deeplearning/README]]
- [[wiki/sources/knowledge-base/README]]
- [[wiki/sources/llm/README]]
- [[wiki/sources/machinelearning/README]]
- [[wiki/sources/operationsresearch/README]]
- [[wiki/sources/reinforcementlearning/README]]
- [[wiki/sources/shared/README]]
- [[wiki/sources/timeseries/README]]
