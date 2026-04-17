---
created_at: 2026-04-11
topics:
  - wiki
  - queries
  - llm-wiki
related_concepts:
  - 知识库问答与研究工作流
status: linked
---

# wiki/queries

`wiki/queries/` 负责“可复用问题层”，把高频问题沉淀为可重复执行的查询入口与证据路径模板。

## 职责

- 固化可复用问题定义（范围、输入、输出结构）。
- 明确证据入口（sources/concepts/indexes/outputs）。
- 连接一次性输出与长期知识资产之间的迁移通道。

## 收录范围

- 会重复出现或需要持续追踪的问题。
- 具备稳定证据入口与可复用输出结构的问题页。

## 不收录范围

- 一次性聊天结果（默认放 `outputs/answers/`）。
- 缺少证据路径或无法复跑的问题描述。

## 维护流程

1. 在 `outputs/answers/` 形成高价值问题结果。
2. 抽象为可复用 query 页并补证据入口。
3. 把 query 入口补到主题索引或问题地图。

## 已沉淀问题

- [[queries/机器学习时间序列预测-知识空白分析]]
- [[queries/运筹优化算法-知识空白分析]]

## 候选迁移


## 关联入口

- 总入口：[[wiki/queries/index]]
- 规则约束：[[schema]]
