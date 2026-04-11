---
created_at: 2026-04-09
topics:
  - 知识库导航
  - index
  - llm-wiki
related_concepts:
  - 知识库工作台
  - 知识库建设方法总索引
status: linked
---

# Wiki Index

> wiki 子系统统一导航入口（与仓库 README 分工互补）
> Last updated: 2026-04-09

## Core Control Files

- [[schema]] - 结构约束、字段规范与会话启动规则
- [[index]] - 当前统一入口页
- [[log]] - 操作时间线（ingest/query/lint/backfill）

## Quick Start

- [[知识库工作台]] - 全库共享操作台
- [[知识库维护检查索引]] - 维护检查入口
- [[知识库来源与专题摄取索引]] - 来源摄取入口
- [[知识库问答与研究工作流]] - query/研究入口
- [[知识库操作记录索引]] - 历史记录入口

## Themes

- [[大语言模型总索引]]
- [[时间序列预测总索引]]
- [[运筹优化算法总索引]]
- [[机器学习总索引]]
- [[数据分析总索引]]
- [[深度学习总索引]]
- [[计算机视觉总索引]]
- [[强化学习总索引]]
- [[控制算法总索引]]
- [[数据结构与算法总索引]]
- [[电力市场交易总索引]]
- [[Vibe Coding总索引]]

## Standard Flow

1. ingest：先把新资料纳入仓库根 `raw/`
2. sources：先补来源摘要卡（`wiki/sources/`）
3. indexes：再更新主题导航（`wiki/indexes/`）
4. concepts：再补概念与方法网络（`wiki/concepts/`）
5. backfill：高价值结果回流到 wiki 入口与相关主题页

## Layer-2 Areas

- `wiki/sources/` - 来源卡层
- `wiki/concepts/` - 概念层
- `wiki/entities/` - 实体层（入口：[[wiki/entities/index]]）
- `wiki/comparisons/` - 对比层（入口：[[wiki/comparisons/index]]）
- `wiki/queries/` - 查询沉淀层（入口：[[wiki/queries/index]]）

## Area READMEs

- [[wiki/README]]（wiki 根说明）
- [[wiki/sources/README]]（wiki/sources 说明）
- [[wiki/concepts/README]]（wiki/concepts 说明）
- [[wiki/entities/README]]（wiki/entities 说明）
- [[wiki/comparisons/README]]（wiki/comparisons 说明）
- [[wiki/queries/README]]（wiki/queries 说明）

## Raw Layer

- `raw/web/`
- `raw/papers/`
- `raw/local-notes/`
- `raw/images/`
- `raw/assets/`

## Common Resources

- [[知识库建设方法总索引]]
- [[知识库运维总索引]]
- [[知识库使用总索引]]
- [[知识库问题地图]]

## Notes

- 本页是“总入口”，不替代现有 `wiki/indexes/*` 的主题导航。
- 本页回答“wiki 内怎么走”；仓库 README 回答“全仓怎么用”。
- 新增稳定页面后，请至少更新对应主题索引与本页相关区块之一。
