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

# Wiki 统一入口

> wiki 子系统唯一导航入口（仓库级入口见 `README.md`）
> 最后更新：2026-04-12

## 控制文件

- [[purpose]]：定义目标、范围与演进方向
- [[schema]]：定义结构、字段、命名、流程与质量约束
- [[index]]：当前统一导航入口
- [[log]]：记录操作时间线（ingest/query/lint/backfill）

## 执行入口

- [[知识库工作台]]：全库共享执行台
- [[知识库来源与专题摄取索引]]：ingest 入口
- [[知识库问答与研究工作流]]：query 入口
- [[知识库输出回流工作流]]：backfill 入口
- [[知识库维护检查索引]]：lint 维护入口
- [[知识库操作记录索引]]：操作记录与追踪入口

## 主题入口

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
- [[Vibe-Coding总索引]]

## 区域入口

- `wiki/sources/` - 来源卡层（入口：[[wiki/sources/index]]）
- `wiki/indexes/` - 索引层（入口：[[wiki/indexes/index]]）
- `wiki/concepts/` - 概念层（入口：[[wiki/concepts/index]]）
- `wiki/entities/` - 实体层（入口：[[wiki/entities/index]]）
- `wiki/comparisons/` - 对比层（入口：[[wiki/comparisons/index]]）
- `wiki/queries/` - 查询沉淀层（入口：[[wiki/queries/index]]）

## 使用说明

- 本页只承担导航与执行入口，不承载字段规范与流程细则；规则统一维护在 [[schema]]。
- 新增稳定页面后，至少更新一个主题总索引，并补到本页对应入口区块。
- `wiki/` 仅放结构化知识页；原始资料统一放在 `raw/`。
