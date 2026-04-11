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

# Wiki 模式

## 领域

本库覆盖 AI/ML 研究与工程知识沉淀，重点包含 `llm`、`timeseries`、`operationsresearch`、`machinelearning`、`deeplearning` 等主题。

## 结构

当前仓库采用 `raw -> wiki -> outputs` 的三层链路，其中 `raw/` 承载“原始层”（外部原件 + 最小元数据），`wiki/` 承载结构化知识层。

- `raw/`：原始来源层（尽量只读，保留原文与最小字段）
  - `web/`：网页/文章
  - `papers/`：论文
  - `repos/`：仓库快照/摘录
  - `datasets/`：数据集快照/摘录
  - `images/`：来源型图像（与某一来源强绑定）
  - `local-notes/`：本地笔记与历史文档
  - `codex_threads/`：线程沉淀
  - `raw/assets/`：通用附件与非来源型素材（见 `raw/assets/README.md`）
- `wiki/sources/`：来源摘要卡（讲材料内容与价值）
- `wiki/indexes/`：主题索引、阅读地图、工作台
- `wiki/concepts/`：概念页与方法页
- `wiki/entities/`：实体页（当前可按需补齐）
- `wiki/comparisons/`：对比分析页（当前可按需补齐）
- `wiki/queries/`：可复用问答页（当前可按需补齐）

## 约定

- 默认使用 `[[wikilinks]]` 建立页面互链。
- 新增稳定页面后，需补到相应索引入口。
- 原始层文件不做语义改写，修正写入 `sources/concepts/queries`。
- 每次关键操作（ingest/query/lint/backfill）追加到 `wiki/log.md`。

### 命名例外

raw 层命名约定默认是“原始网页：`YYYY-MM-DD-标题.md`”。但以下类型允许例外（不强制日期前缀）：

- 模板/清单类文件（例如线程总结模板、历史文档清单）。
- 仓库来源卡：允许使用 `repo-组织名-仓库名.md`。
- 目录式条目：`raw/local-notes/**/index.md` 保持目录结构即可。

## 前置元数据

### Layer 1 (`raw/**/*.md`) 最小字段

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
  - raw/web/xxx.md
---
```

兼容说明：历史页面可继续保留 `created_at/topics/related_concepts/status`，后续增量迁移到统一字段。

## 页面阈值

- 仅在“2+ 来源共同出现”或“单来源核心主题”时新建概念/实体页。
- 仅当答案具备复用价值时沉淀到 `wiki/queries/`。
- 页面超过约 200 行时考虑拆分。

## 更新策略

- 新信息与旧信息冲突时，保留两者并标注时间与来源。
- 若无法判定真伪，在 lint 报告中标记待人工裁决。

## 会话启动（给代理）

每次会话建议先读：

1. [[purpose]]（目标与意图）
2. [[schema]]（结构规则）
3. [[index]]（导航入口）
4. [[log]]（最近 20~30 行）
5. 任务相关主题总索引（`wiki/indexes/*/`）
