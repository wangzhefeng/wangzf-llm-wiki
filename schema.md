---
created_at: 2026-04-18
aliases:
  - Wiki 规则 Schema
  - 知识库Schema设计
topics:
  - 知识库构建
  - schema
  - llm-wiki
related_concepts:
  - 知识库建设方法
  - 知识库工作台
status: active
---

# LLM Wiki 规则 Schema

## 定位

本文件是当前仓库的唯一规则入口，定义：

- 目录结构与分层边界
- frontmatter 与命名约束
- 主题命名规范
- 日志与 lint 的唯一输出口
- 默认执行顺序与会话启动顺序

当前固定三条单一出口：

- 操作日志唯一出口：`wiki/log.md`
- 审查报告唯一出口：`wiki/log_lint.md`
- 规则入口唯一出口：`schema.md`

## 目录结构约定

当前仓库采用 `raw -> wiki -> outputs` 的三层链路，其中 `raw/` 承载原始层，`wiki/` 承载结构化知识层，`outputs/` 承载派生结果层。

- `raw/`：原始来源层（尽量只读，保留原文与最小字段）
  - `web/`：网页/文章
  - `papers/`：论文
  - `repos/`：仓库快照/摘录
  - `datasets/`：数据集快照/摘录
  - `images/`：来源型图像
  - `notes/`：本地笔记与历史文档
  - `assets/`：通用附件与非来源型素材
- `wiki/sources/`：来源摘要卡
- `wiki/indexes/`：主题总索引、阅读地图、问题地图、工作台、维护清单
- `wiki/indexes/shared/`：跨主题执行工作流
- `wiki/concepts/`：概念页与方法页
- `wiki/entities/`：实体页
- `wiki/comparisons/`：对比分析页
- `wiki/queries/`：可复用问题页
- `wiki/log.md`：append-only 操作时间线
- `wiki/log_lint.md`：最新 lint / health 审查主报告
- `outputs/answers/`：单次问答结果
- `outputs/syntheses/`：阶段性综述
- `outputs/slides/`：演示稿
- `outputs/figures/`：图表与示意图

共享层约束：

- `wiki/indexes/shared/` 根目录只放执行页
- 三主题目录只放定义与导航页
- `知识库工作台` 是统一调度入口

当前正式重编译范围：

- `raw/web/**`
- `raw/repos/repo-*.md`
- `raw/notes/**`

范围说明：

- `raw/repos/` 的正式编译对象是 `repo-*.md` 仓库入口卡
- `raw/repos/**` 下镜像仓库中的 `README.md`、`AGENTS.md`、`CONTRIBUTING.md` 等文件默认只作为背景证据，不逐文件下沉为 `wiki/sources/`
- `raw/notes/**` 是标准编译对象，不再视作边缘历史材料

## 字段约束

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

- `source_type`、`created_at`、`topics` 为必填
- `topics` 控制在 1 到 3 个

### Layer 2: `wiki/**/*.md` 推荐字段

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
status: linked
---
```

兼容说明：

- 历史页面可暂保留 `created_at/topics/related_concepts/status`
- 目录导航页允许使用 `status: active`

来源卡补充契约：

- `wiki/sources/**/*.md` 推荐显式保留 `source_path`
- `source_path: raw/...` 表示单一原始来源
- `source_path:` 列表表示聚合来源卡
- `source_path` 的值必须全部是 `raw/` 相对路径，不得写成本地绝对路径

## 命名约束

- 原始网页：`YYYY-MM-DD-标题.md`
- 仓库来源：`repo-组织名-仓库名.md`
- 概念页：`概念名.md`
- 输出结果：`YYYY-MM-DD-主题-用途.md`
- 审查报告：固定为 `wiki/log_lint.md`
- 操作日志：固定追加到 `wiki/log.md`

命名例外：

- 模板/清单类文件允许无日期前缀
- `raw/notes/**/index.md` 允许目录式命名

## 主题命名规范

活跃主题与规范 slug：

| slug | 中文主题 | 历史别名 / 说明 |
|---|---|---|
| `causal-inference` | 因果推断 | 无 |
| `control-algorithms` | 控制算法 | 无 |
| `deep-learning` | 深度学习 | 历史上出现过 `deep-learning-theory`、`deeplearning` |
| `feature-engineering` | 特征工程 | 从原 `machinelearning` 拆出 |
| `llm` | 大语言模型 | 历史上曾拆分 `llm-theory`、`llm-pre-training`、`llm-post-training` |
| `llm-wiki` | 大语言模型知识库 | 历史上出现过 `knowledge-base`、`llm-knowledge-base` |
| `machine-learning` | 机器学习 | 历史上出现过 `machinelearning`、更细粒度监督/无监督拆分 |
| `nlp` | 自然语言处理 | 无 |
| `operations-research` | 数学优化算法 / 运筹学 | 历史上出现过 `operationsresearch` |
| `power-market-trading` | 电力市场交易 | 无 |
| `reinforcement-learning` | 强化学习 | 无 |
| `statistics-theory` | 统计学理论 | 历史上出现过 `statistics` |
| `timeseries-analysis` | 时间序列分析 | 历史上出现过 `timeseries` |
| `vibe-coding` | Vibe Coding | 无 |

已删除或不再新增的旧主题：

- `agent-dev`
- `computer-vision`
- `data-analysis`
- `data-structure-algorithm`
- `tools`
- `programming-tools`
- `others`

命名规则：

- 新增 `topics` / `tags` / 目录 slug 一律使用上表规范名
- 历史 `source_path`、原文回链和日志记录允许保留旧 raw 路径，不作为当前命名漂移错误
- 不再新增 `knowledge-base-*`、`llm-theory`、`llm-pre-training`、`llm-post-training` 作为正式主题 slug

## outputs 规范

`outputs/` 只放围绕当前知识库生成的派生结果，不放原始来源，也不替代 `wiki/`。

目录职责：

- `answers/`：单次问答结果
- `syntheses/`：阶段性综述或专题整理
- `slides/`：Marp 幻灯片或演示稿
- `figures/`：图表、示意图、流程图说明

约束：

- 输出优先写成可回看、可回链的 Markdown 或图表文件
- 高价值输出完成后，必须回链到相关 `wiki/` 页面
- `outputs/` 不再承担日志唯一出口职责
- lint 主报告不再写入 `outputs/answers/`

## 日志与审查规范

### 日志规范

- 所有 ingest / query / lint / backfill / task 统一追加到 `wiki/log.md`
- `wiki/log.md` 保持 append-only
- 不再在旧日志目录下按天新建操作记录文件
- 历史上出现的旧日志目录路径只允许作为历史事实出现在旧日志正文中

统一日志格式：

- 标题格式：`## [YYYY-MM-DD] action | subject`
- 动作类型：`ingest`、`update`、`query`、`lint`、`backfill`、`archive`、`task`

### lint / health 报告规范

- 最新 lint / health 主报告统一写入 `wiki/log_lint.md`
- 该文件覆盖更新，不按日期滚动复制
- 健康检查过程动作与修复动作仍记录在 `wiki/log.md`

## 默认流程

默认顺序：

1. 资料先落 `raw/`
2. 先补 `wiki/sources/` 来源卡
3. 再更新 `wiki/indexes/` 导航与阅读路径
4. 最后补 `wiki/concepts/` 概念页
5. 高价值输出写入 `outputs/`
6. 将关键动作追加到 `wiki/log.md`
7. 将最新审查结果覆盖到 `wiki/log_lint.md`

行为约束：

- 页面互链优先使用 `[[wikilinks]]`
- 原始层文件不做语义改写，修正写入 `wiki/` 层
- lint 基线除目录、字段和相对链接外，还应检查旧主题命名残留
- 标准执行顺序固定为：`基线盘点 -> 修断链 -> 重编译 sources -> 刷新 indexes/concepts -> 更新流程文档 -> 复验与日志收尾`

## 质量约束

- 仅在“2+ 来源共同出现”或“单来源核心主题”时新建概念/实体页
- 仅当答案具备复用价值时沉淀到 `wiki/queries/`
- 页面超过约 200 行时考虑拆分
- 新增稳定页面后，必须补到至少一个主题索引入口
- 新信息与旧信息冲突时并存记录，标注时间与来源
- `health` 中的 warning 允许作为边界项保留，但必须在 `wiki/log_lint.md` 中写明类型、原因和后续策略

## 会话启动

每次会话建议先读：

1. [[schema]]
2. [[purpose]]
3. [[wiki/index]]
4. [[log]]（最近 20~30 行）
5. [[log_lint]]
6. 任务相关主题总索引（`wiki/indexes/*/`）
