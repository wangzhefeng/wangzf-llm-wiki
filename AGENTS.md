# AGENTS.md

本文件定义当前仓库的 repo 级协作约束，面向 Codex 及其他通用 AI agent。

目标：让 agent 在 `wangzf_kb` 中稳定遵守 `raw -> wiki -> outputs` 的知识库工作链，而不是每次重新猜目录职责、页面角色和操作顺序。

## 1. 仓库目标

- 这是一个以 Markdown 为中心的个人知识库，不是普通笔记堆积仓库。
- 目标是把网页、论文、仓库、数据集、图片、本地历史文档等原始资料，整理成 LLM 可持续工作的工作域。
- 高价值结果应沉淀为文件，并继续回流到知识库，而不是停留在一次性对话里。

## 2. 默认语言与沟通

- 默认使用简体中文，除非用户明确要求英文。
- 优先直接实施；除非用户明确要求先讨论方案，否则不要只停留在分析。
- 长任务要给简短进度更新，说明正在读什么、改什么、下一步做什么。
- 结尾总结以结果、验证情况、残留风险为主，不写冗长教程。

## 3. 目录职责

- `raw/`：唯一摄取入口，只放原始来源和最小元数据，不写长篇总结。
- `wiki/`：结构化知识层。
- `wiki/sources/`：来源摘要卡，只回答“这份材料讲了什么、价值是什么、连到哪些概念”。
- `wiki/indexes/`：主题总索引、阅读地图、问题地图、来源清单、共享工作台。
- `wiki/concepts/`：概念页、方法页、工具页、人物页。
- `outputs/`：派生结果，不替代 `wiki/`。
- `outputs/answers/`：单次问答结果。
- `outputs/syntheses/`：阶段性综述或专题整理。
- `outputs/slides/`：演示稿。
- `outputs/figures/`：图表、示意图。
- `outputs/logs/`：`ingest / query / lint / backfill` 的时间记录。
- `prompts/`：可复用提示词模板。
- `assets/`：本地附件与通用素材。

## 4. 原始来源类型

`raw/` 中允许的标准来源类型：

- `web`
- `paper`
- `repo`
- `dataset`
- `image`
- `local_note`

对应目录优先使用：

- `raw/web/`
- `raw/papers/`
- `raw/repos/`
- `raw/datasets/`
- `raw/images/`
- `raw/local-notes/`

## 5. 原始文档最小字段

原始网页或原始 Markdown 默认至少保留：

```yaml
---
source_type: web
source_url: https://example.com/article
title: 示例标题
author: 作者名
published_at: 2026-04-05
created_at: 2026-04-05
topics:
  - 知识库维护
related_concepts:
  - 知识库建设方法
status: inbox
---
```

规则：

- `source_type` 必填
- `created_at` 必填
- `topics` 必填，控制在 1 到 3 个
- `related_concepts` 应尽量填写
- 本地文档可省略 `source_url`
- `status` 优先使用：`inbox`、`summarized`、`linked`、`archived`

## 6. 页面生成顺序

任何专题整理、来源沉淀或主题扩写，都优先遵守这个顺序：

1. 先把资料纳入 `raw/`
2. 再生成 `wiki/sources/` 来源卡
3. 再更新 `wiki/indexes/` 总索引、阅读地图、问题入口
4. 最后补 `wiki/concepts/` 概念页

不要跳过来源层直接写概念百科。

## 7. 四类核心操作

### ingest

- 处理新来源
- 先落 `raw/`
- 再补 `wiki/sources/`
- 必要时再更新索引和概念页

### query

- 围绕现有 wiki 做问答、比较、研究、输出
- 先列证据路径，再给判断
- 结果应写入 `outputs/answers/` 或 `outputs/syntheses/`

### lint

- 做知识库健康检查
- 重点看孤页、断链、缺摘要来源、重复概念、附件缺失、输出未回流

### log

- 为 `ingest / query / lint / backfill` 留时间记录
- 记录放在 `outputs/logs/`

## 8. 输出与回流规则

- `outputs/` 只收高价值结果，不当作临时垃圾箱。
- 单轮具体问题写到 `outputs/answers/`
- 多来源阶段性收束写到 `outputs/syntheses/`
- 演示稿写到 `outputs/slides/`
- 图表写到 `outputs/figures/`
- 每次高价值输出完成后，至少做两件事：
  1. 在相关索引页补入口
  2. 如果形成稳定判断或新问题，再回写概念页、索引页或问题地图

## 9. 命名与互链规则

- 原始网页：`YYYY-MM-DD-标题.md`
- 仓库来源：`repo-组织名-仓库名.md`
- 概念页：`概念名.md`
- 输出结果：`YYYY-MM-DD-主题-用途.md`
- 操作记录：`YYYY-MM-DD-主题-动作记录.md`

互链规则：

- 优先使用 Wiki 链接
- 主题页优先互链，不做孤页
- 来源卡应尽量链接到相关概念
- 概念页应能回链到至少 1 个来源卡
- 新增稳定页面后，必要时同步更新总索引、阅读地图、问题地图或工作台入口

## 10. 主题与共享分工

- 知识库方法主题使用：`wiki/indexes/knowledge-base-building/`
- 知识库运维主题使用：`wiki/indexes/knowledge-base-operations/`
- 知识库使用主题使用：`wiki/indexes/knowledge-base-usage/`
- 具体专题（如 `timeseries/`、`operationsresearch/`）优先放各自来源、索引、概念网络。

## 11. 默认行为要求

- 修改前先读上下文，不凭空猜仓库结构。
- 复杂任务至少先读：
  - `README.md`
  - `wiki/index.md`
  - `wiki/SCHEMA.md`
  - `wiki/log.md`
  - 相关主题总索引
  - 必要的来源卡或概念页
- 能本地完成的任务尽量本地完成。
- 不主动修复与当前任务无关的问题。
- 不覆盖、回滚或清理自己未创建的改动。
- 没有用户明确要求时，不主动提交、推送、开 PR。

## 12. 优先入口

方法与结构入口：

- `wiki/index.md`
- `wiki/SCHEMA.md`
- `wiki/indexes/knowledge-base-building/知识库建设方法总索引.md`
- `wiki/indexes/knowledge-base-building/知识库Schema设计.md`

执行入口：

- `wiki/indexes/knowledge-base-operations/知识库工作台.md`
- `wiki/indexes/knowledge-base-building/知识库来源与专题摄取索引.md`
- `wiki/indexes/knowledge-base-usage/知识库问答与研究工作流.md`
- `wiki/indexes/knowledge-base-operations/知识库维护检查索引.md`
- `wiki/indexes/knowledge-base-usage/知识库问题地图.md`
- `wiki/indexes/knowledge-base-operations/知识库操作记录索引.md`

提示词入口：

- `prompts/README.md`
