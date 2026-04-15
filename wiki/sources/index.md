---
created_at: 2026-04-11
topics:
- llm
- shared
related_concepts:
- 知识库来源与专题摄取索引
status: linked
---
# wiki/sources

`wiki/sources/` 负责“来源摘要卡层”，把 `raw/` 的单条原始资料压缩为可检索、可互链的结构化入口。

## 职责

- 每个来源 1 张卡，回答“讲了什么、价值是什么、可连到哪些概念”。
- 每张卡至少链接到对应 `raw/` 原文路径。
- 高价值来源卡应回链到相关 `wiki/concepts/` 或 `wiki/indexes/`。

## 收录范围

- `raw/web|papers|repos|datasets|images|notes` 的来源摘要卡。
- 主题内附件入口页（仅在需要可达性时创建）。

## 不收录范围

- 原始全文（应留在 `raw/`）。
- 长篇综述与阶段总结（应留在 `outputs/syntheses/`）。
- 一次性问答结果（应留在 `outputs/answers/`）。

## 维护流程

1. 先完成 `raw/` 入库。
2. 创建或更新来源卡到 `wiki/sources/<topic>/`。
3. 将来源卡入口补到对应主题索引。
4. 如形成稳定共识，再推动概念页沉淀。

## 主题入口

- [[wiki/sources/data-analysis/index]]
- [[wiki/sources/control-algorithms/index]]
- [[wiki/sources/data-structure-algorithm/index]]
- [[wiki/sources/deep-learning/index]]
- [[wiki/sources/llm-wiki/index]]
- [[wiki/sources/llm/index]]
- [[wiki/sources/machine-learning/index]]
- [[wiki/sources/operations-research/index]]
- [[wiki/sources/reinforcement-learning/index]]
- [[wiki/sources/shared/index]]
- [[wiki/sources/timeseries-analysis/index]]

## 关联入口

- 总入口：[[wiki/index]]
- 规则约束：[[wiki/schema]]
