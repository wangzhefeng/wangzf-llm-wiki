---
created_at: 2026-04-11
topics:
  - wiki
  - comparisons
  - llm-wiki
related_concepts:
  - 知识库问答与研究工作流
status: linked
---

# wiki/comparisons

`wiki/comparisons/` 负责“对比层”，将多个候选对象放在统一维度下做长期可复用的结构化比较。

## 职责

- 沉淀模型、方法、工具、方案的横向对比页面。
- 明确评价维度、适用边界与结论条件。
- 为决策型 query 提供可复用证据骨架。

## 收录范围

- 对象数量 >= 2 且评价维度可稳定复用的对比页。
- 与主题索引、概念页、来源卡可形成闭环链接的对比页。

## 不收录范围

- 一次性临时比较（应先放 `outputs/answers/`）。
- 仅有结论、无证据路径或无评价维度的内容。

## 维护流程

1. 明确对比对象与固定评价维度。
2. 建立对比页并补齐来源与概念链接。
3. 将入口挂到对应主题总索引或问题地图。

## 已登记方向

- LLM 推理框架对比：vLLM / TGI / Triton / TensorRT-LLM（待展开）
- 时间序列基础模型对比：Chronos / TimesFM / Moirai / Timer（待展开）
- MILP 求解器对比：Gurobi / CPLEX / SCIP（待展开）

## 关联入口

- 总入口：[[wiki/index]]
- 规则约束：[[wiki/schema]]
