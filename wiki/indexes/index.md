---
created_at: 2026-04-11
topics:
  - wiki
  - indexes
  - llm-wiki
related_concepts:
  - 知识库工作台
status: linked
---

# wiki/indexes

`wiki/indexes/` 存放“主题索引与导航页”：把分散在 `wiki/sources/` 与 `wiki/concepts/` 的内容组织成可执行的入口（总索引 / 阅读地图 / 工作台 / 问题地图）。

## 放什么

- 主题总索引：该主题下最重要的入口、来源清单、概念网络入口
- 阅读地图：按学习/研究路径组织的阅读顺序
- 工作台：执行型入口（ingest/query/lint/backfill 的入口与清单）
- 问题地图：该主题下的关键问题与待办

## 不放什么

- 不放原始材料（在 `raw/`）
- 不堆一次性问答输出（在 `outputs/`，这里只做链接入口）

## 典型工作流

1. 新来源卡生成后，把入口补到对应主题索引
2. 新概念页稳定后，把概念入口补到主题索引
3. 每次高价值输出回流时，把输出链接挂到合适的索引页

## 入口

- wiki 总入口：`wiki/index.md`
- schema 约束：`wiki/schema.md`
