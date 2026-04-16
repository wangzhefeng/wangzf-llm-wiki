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

`wiki/entities/` 负责“实体层”，沉淀可被多主题复用的人物、组织、社区、团队等对象。

## 职责

- 为反复出现的实体提供统一背景入口。
- 维护“实体-概念-来源”之间的稳定连接。
- 减少同一实体在不同页面的重复介绍与命名漂移。

## 收录范围

- 人物实体（作者、研究者、核心贡献者）。
- 组织与社区实体（团队、机构、开源社区）。
- 在多个主题或来源中反复出现的对象。

## 不收录范围

- 单次提及且不具复用价值的对象。
- 纯概念性内容（应放 `wiki/concepts/`）。

## 维护流程

1. 确认实体在 2+ 来源或主题中重复出现。
2. 建立实体页并补充关联概念与来源入口。
3. 把实体入口补到对应主题总索引。

## 当前实体入口

- 人物：[[entities/Sebastian Raschka]]、[[entities/Jason Brownlee]]
- 组织/社区：[[entities/Datawhale]]、[[entities/PyTorch Contributors]]、[[entities/时序之心]]

## 关联入口

- 总入口：[[index]]
- 规则约束：[[schema]]
