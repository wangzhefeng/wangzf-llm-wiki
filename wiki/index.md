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

# Wiki 导航索引

> wiki 子系统统一导航入口（与仓库 README 分工互补）
> 最后更新：2026-04-12

## 核心控制文件

- [[schema]] - 结构约束、字段规范与会话启动规则
- [[purpose]] - 目标、范围与演进原则
- [[index]] - 当前统一入口页
- [[log]] - 操作时间线（ingest/query/lint/backfill）

## 快速开始

- [[知识库工作台]] - 全库共享操作台
- [[知识库维护检查索引]] - 维护检查入口
- [[知识库来源与专题摄取索引]] - 来源摄取入口
- [[知识库问答与研究工作流]] - query/研究入口
- [[知识库操作记录索引]] - 历史记录入口

## 主题

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

## 标准流程

1. ingest：先把新资料纳入仓库根 `raw/`
2. sources：先补来源摘要卡（`wiki/sources/`）
3. indexes：再更新主题导航（`wiki/indexes/`）
4. concepts：再补概念与方法网络（`wiki/concepts/`）
5. backfill：高价值结果回流到 wiki 入口与相关主题页

## 第二层区域

- `wiki/sources/` - 来源卡层（入口：[[wiki/sources/index]]）
- `wiki/indexes/` - 索引层（入口：[[wiki/indexes/index]]）
- `wiki/concepts/` - 概念层（入口：[[wiki/concepts/index]]）
- `wiki/entities/` - 实体层（入口：[[wiki/entities/index]]）
- `wiki/comparisons/` - 对比层（入口：[[wiki/comparisons/index]]）
- `wiki/queries/` - 查询沉淀层（入口：[[wiki/queries/index]]）

## Area索引

- [[wiki/sources/index]]（wiki/sources 说明）
- [[wiki/indexes/index]]（wiki/indexes 说明）
- [[wiki/concepts/index]]（wiki/concepts 说明）
- [[wiki/entities/index]]（wiki/entities 说明）
- [[wiki/comparisons/index]]（wiki/comparisons 说明）
- [[wiki/queries/index]]（wiki/queries 说明）

## Wiki层概述

`wiki/` 只放由 `raw/` 编译出来的结构化知识页，不放原始资料。

建议把 `wiki/index.md` 作为“日常入口”，把 `wiki/schema.md` 作为“规则入口”：

- `wiki/index.md`
- `wiki/schema.md`
- `wiki/log.md`

### 当前组织方式

- 第一层按页面角色分为 `sources/`、`indexes/`、`concepts/`
- 第二层按专题拆分为 `timeseries/`、`operationsresearch/`、`knowledge-base/`、`shared/` 等
- `knowledge-base/` 放知识库构建这个独立主题的来源、索引与概念页
- `shared/` 只放全库公共页面与工作台页面

### 约束

- 先生成 `sources/`，再补 `indexes/`，最后沉淀 `concepts/`
- 页面之间尽量使用普通 Markdown 和 Wiki 链接语法互链
- 优先使用名称链接而不是路径链接，减少后续目录迁移成本
- 不把一次性问答结果直接堆进 `wiki/`，高价值输出回流时再补链接

### 推荐命名

- 概念条目：`概念名.md`

## 原始层

- `raw/web/`
- `raw/papers/`
- `raw/local-notes/`
- `raw/images/`
- `raw/assets/`

## 常用资源

- [[知识库建设方法总索引]]
- [[知识库运维总索引]]
- [[知识库使用总索引]]
- [[知识库问题地图]]

## 备注

- 本页是“总入口”，不替代现有 `wiki/indexes/*` 的主题导航。
- 本页回答“wiki 内怎么走”；仓库 README 回答“全仓怎么用”。
- 新增稳定页面后，请至少更新对应主题索引与本页相关区块之一。
