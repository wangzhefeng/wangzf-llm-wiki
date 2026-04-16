---
created_at: 2026-04-09
aliases:
  - 知识库Schema设计
topics:
  - 知识库构建
  - schema
  - llm-wiki
related_concepts:
  - 知识库建设方法
  - 知识库工作台
status: linked
---

# Wiki 规则 Schema

## 结构

当前仓库采用 `raw -> wiki -> outputs` 的三层链路，其中 `raw/` 承载“原始层”（外部原件 + 最小元数据），`wiki/` 承载结构化知识层。

- `raw/`：原始来源层（尽量只读，保留原文与最小字段）
  - `web/`：网页/文章
  - `papers/`：论文
  - `repos/`：仓库快照/摘录
  - `datasets/`：数据集快照/摘录
  - `images/`：来源型图像（与某一来源强绑定）
  - `notes/`：本地笔记与历史文档
  - `codex_threads/`：线程沉淀
  - `raw/assets/`：通用附件与非来源型素材（见 `raw/assets/README.md`）
- `wiki/sources/`：来源摘要卡（讲材料内容与价值）
- `wiki/indexes/`：主题索引、阅读地图、工作台
- `wiki/indexes/shared/`：共享执行工作流（ingest/query/backfill/lint 入口）
- `wiki/indexes/llm-wiki/`：知识库建设、运维与使用的主题索引（含总索引、来源清单、阅读地图）
- `wiki/concepts/`：概念页与方法页
- `wiki/entities/`：实体页（当前可按需补齐）
- `wiki/comparisons/`：对比分析页（当前可按需补齐）
- `wiki/queries/`：可复用问答页（当前可按需补齐）

共享层约束：
- `shared` 根目录只放执行页；三主题目录只放定义与导航页。
- `知识库工作台` 是 shared 层统一调度入口。

## 字段

### Layer 1: `raw/**/*.md` 最小字段

```yaml
---
source_type: web | paper | repo | dataset | image | notes
created_at: YYYY-MM-DD
topics:
  - topic-a
status: inbox
---
```

要求：
- `source_type`、`created_at`、`topics` 为必填。
- `topics` 控制在 1 到 3 个，避免过度发散。

### Layer 2: `wiki/sources|concepts|entities|comparisons|queries/**/*.md` 推荐字段

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

兼容说明：历史页面可保留 `created_at/topics/related_concepts/status`，后续增量迁移。

## 命名

- 原始网页：`YYYY-MM-DD-标题.md`
- 仓库来源：`repo-组织名-仓库名.md`
- 概念页：`概念名.md`
- 输出结果：`YYYY-MM-DD-主题-用途.md`
- 操作记录：`YYYY-MM-DD-主题-动作记录.md`

命名例外：
- 模板/清单类文件允许无日期前缀。
- `raw/notes/**/index.md` 允许目录式命名。

## 流程

默认顺序：
1. 资料先落 `raw/`
2. 先补 `wiki/sources/` 来源卡
3. 再更新 `wiki/indexes/` 导航与阅读路径
4. 最后补 `wiki/concepts/` 概念页
5. 高价值输出写入 `outputs/` 并回流索引入口

行为约束：
- 页面互链优先使用 `[[wikilinks]]`。
- 原始层文件不做语义改写，修正写入 `wiki/` 层。
- 每次关键操作（ingest/query/lint/backfill）追加到 `wiki/log.md`。
- 不再单独维护”知识库Schema设计”页面；规则统一在本页维护。

**特别说明**：`wiki/concepts` 层有专独立规则文档 [[CONCEPTS-RULES.md]]，规定了阶段设计、粗细粒度划分、交叉链接维护等规则。当本 schema 与 CONCEPTS-RULES.md 冲突时，CONCEPTS-RULES.md 优先。

## 质量约束

- 仅在“2+ 来源共同出现”或“单来源核心主题”时新建概念/实体页。
- 仅当答案具备复用价值时沉淀到 `wiki/queries/`。
- 页面超过约 200 行时考虑拆分。
- 新增稳定页面后，必须补到至少一个主题索引入口。
- 新信息与旧信息冲突时并存记录，标注时间与来源。

## 会话启动

每次会话建议先读：

1. [[purpose]]
2. [[schema]]
3. [[index]]
4. [[log]]（最近 20~30 行）
5. 任务相关主题总索引（`wiki/indexes/*/`）
