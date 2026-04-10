---
created_at: 2026-04-09
topics:
  - 知识库构建
  - schema
  - llm-wiki
related_concepts:
  - 知识库建设方法
  - 知识库工作台
status: linked
---

# Wiki Schema

## Domain

本库覆盖 AI/ML 研究与工程知识沉淀，重点包含 `llm`、`timeseries`、`operationsresearch`、`machinelearning`、`deeplearning` 等主题。

## Structure

当前仓库采用“兼容 llm-wiki 的轻量映射”：

- `wiki/raw/`：原始来源层（只读，保留原文）
  - `articles/`：网页/文章
  - `papers/`：论文/仓库/数据集等资料
  - `transcripts/`：本地笔记与历史文档
  - `assets/`：图片与附件
- `wiki/sources/`：来源摘要卡（讲材料内容与价值）
- `wiki/indexes/`：主题索引、阅读地图、工作台
- `wiki/concepts/`：概念页与方法页
- `wiki/entities/`：实体页（当前可按需补齐）
- `wiki/comparisons/`：对比分析页（当前可按需补齐）
- `wiki/queries/`：可复用问答页（当前可按需补齐）

## Conventions

- 默认使用 `[[wikilinks]]` 建立页面互链。
- 新增稳定页面后，需补到相应索引入口。
- 原始层文件不做语义改写，修正写入 `sources/concepts/queries`。
- 每次关键操作（ingest/query/lint/backfill）追加到 `wiki/log.md`。

## Frontmatter

### Layer 1 (`wiki/raw/*.md`) 最小字段

```yaml
---
source_type: web | paper | repo | dataset | image | local_note
created_at: YYYY-MM-DD
topics:
  - topic-a
status: inbox
---
```

### Layer 2 (`sources/concepts/entities/comparisons/queries`) 推荐字段

```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: source | concept | entity | comparison | query | summary
tags:
  - tag-a
sources:
  - wiki/raw/articles/xxx.md
---
```

兼容说明：历史页面可继续保留 `created_at/topics/related_concepts/status`，后续增量迁移到统一字段。

## Page Thresholds

- 仅在“2+ 来源共同出现”或“单来源核心主题”时新建概念/实体页。
- 仅当答案具备复用价值时沉淀到 `wiki/queries/`。
- 页面超过约 200 行时考虑拆分。

## Update Policy

- 新信息与旧信息冲突时，保留两者并标注时间与来源。
- 若无法判定真伪，在 lint 报告中标记待人工裁决。

## Session Start (for agents)

每次会话建议先读：

1. `wiki/SCHEMA.md`
2. `wiki/index.md`
3. `wiki/log.md`（最近 20~30 行）
4. 任务相关主题总索引（`wiki/indexes/*/`）
