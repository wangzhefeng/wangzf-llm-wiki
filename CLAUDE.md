# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 主规范

本仓库唯一主规范为 [AGENTS.md](AGENTS.md)。若本文件与 `AGENTS.md` 冲突，以 `AGENTS.md` 为准。

## 仓库定位

这是一个面向 LLM 持续工作的 Markdown 知识库，主链路为 `raw -> wiki -> outputs`，核心任务为 `ingest / query / lint / backfill`。没有代码构建、测试或 lint 命令——所有"操作"均是 Markdown 文件的读写与整理。

## 架构总览

```
raw/          原始来源层（只放原件 + 最小 frontmatter，尽量只读）
  web/        网页/文章
  papers/     论文
  repos/      仓库快照
  datasets/   数据集快照
  local-notes/   本地笔记与历史文档
  codex_threads/ 线程沉淀
  assets/        通用附件素材

wiki/         结构化知识层
  sources/    来源摘要卡（讲材料内容与价值）
  indexes/    主题总索引与阅读地图
    shared/   共享执行工作流（ingest/query/backfill/lint 入口）
  concepts/   概念页、方法页
  entities/   实体页（人物、组织等）
  comparisons/ 对比分析页
  queries/    可复用问答页

outputs/      派生结果（答案、综述、演示稿、图表、操作日志）
prompts/      可复用提示词模板
```

## 五个控制文件（必须优先读）

| 文件 | 职责 |
|---|---|
| `README.md` | 仓库级入口：结构、快速开始、主题入口 |
| `wiki/index.md` | wiki 唯一导航入口：控制文件、执行入口、主题入口 |
| `wiki/purpose.md` | 目标、关键问题、范围、演进方向 |
| `wiki/schema.md` | 结构、字段、命名、流程、质量约束（**唯一规则源**） |
| `wiki/log.md` | append-only 操作时间线 |

**复杂任务开始前，至少读这 5 个文件。**

## 四类核心操作

| 操作 | 动作 | 结果落点 |
|---|---|---|
| `ingest` | 纳入新来源 | `raw/` → `wiki/sources/` → 更新索引 |
| `query` | 问答与研究 | `outputs/answers/` 或 `outputs/syntheses/` |
| `lint` | 健康检查 | 孤页、断链、缺摘要、重复概念 |
| `backfill` | 高价值输出回流 | `outputs` → `wiki/indexes` → `wiki/concepts` |

## 页面生成顺序（强制）

1. 先落 `raw/`（含最小 frontmatter）
2. 再生成 `wiki/sources/` 来源卡
3. 再更新 `wiki/indexes/` 索引与阅读地图
4. 最后补 `wiki/concepts/` 概念页

**不可跳过来源层直接写概念页。**

## Frontmatter 最小字段（raw 层）

```yaml
---
source_type: web | paper | repo | dataset | image | local_note
created_at: YYYY-MM-DD
topics:
  - topic-a          # 1-3 个
related_concepts:    # 应尽量填写
  - 相关概念名
status: inbox        # inbox | summarized | linked | archived
---
```

## 命名规则

- 原始网页：`YYYY-MM-DD-标题.md`
- 仓库来源：`repo-组织名-仓库名.md`
- 概念页：`概念名.md`
- 输出结果：`YYYY-MM-DD-主题-用途.md`
- 操作记录：`YYYY-MM-DD-主题-动作记录.md`

## 执行入口速查

- 摄取任务：`wiki/indexes/shared/知识库来源与专题摄取索引.md`
- 问答研究：`wiki/indexes/shared/知识库问答与研究工作流.md`
- 输出回流：`wiki/indexes/shared/知识库输出回流工作流.md`
- 维护检查：`wiki/indexes/shared/知识库维护检查索引.md`
- 全局调度：`wiki/indexes/shared/知识库工作台.md`

## 默认行为

- 默认使用简体中文。
- 修改前先读上下文，不凭空猜结构。
- 不主动修复与当前任务无关的问题。
- 无用户明确要求时，不提交、推送、开 PR。
- 高价值输出完成后，至少在相关索引页补入口，并在 `wiki/log.md` 追加记录。
