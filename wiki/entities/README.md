---
created_at: 2026-04-11
topics:
  - wiki
  - entities
  - llm-wiki
related_concepts:
  - 知识库Schema设计
status: linked
---

# wiki/entities

`wiki/entities/` 存放“实体页”：人物、组织、公司、产品、论文作者群、数据集发布方等可被多处引用的对象。

## 何时使用

- 一个实体在多个主题/来源中重复出现，需要统一背景与引用入口
- 需要把“实体—概念—来源”关系稳定化，便于检索与对比

## 页面建议包含

- 基本信息（简洁）
- 关键关联：相关概念页、代表来源卡、重要时间点

## 入口

- wiki 总入口：`wiki/index.md`
- schema 约束：`wiki/schema.md`
