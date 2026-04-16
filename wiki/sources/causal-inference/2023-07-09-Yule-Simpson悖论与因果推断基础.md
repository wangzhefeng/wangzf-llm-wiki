---
title: Yule-Simpson悖论与因果推断基础
created: 2023-07-09
updated: 2026-04-15
type: source
tags:
  - causal-inference
  - 理论基础
  - 统计方法
sources:
  - raw/notes/causal-inference/2023-07-09-statistics-causal-inference/index.md
---

## 摘要

本文通过 Yule-Simpson 悖论展示了统计中的因果问题，系统介绍了 Rubin Causal Model（RCM）、Fisher/Neyman 分歧与观察性研究中的可忽略性假定。强调因果推断需要在承认数据局限性的前提下，加上足够强的假设才能从关联推导出因果。

## 核心要点

### Yule-Simpson 悖论
- 边际相关性与条件相关性可能反向
- Berkeley 录取率案例：整体上男性录取率高于女性，但按专业分层后女性反而更高
- 反映混杂偏倚（confounding bias）的本质——忽视第三变量可能完全改变结论

### Rubin Causal Model
- 潜在结果（potential outcomes）：$Y_i(1), Y_i(0)$
- 个体因果作用：$Y_i(1) - Y_i(0)$（通常不可观测）
- 平均因果作用（Average Causal Effect, ACE）：在随机化下可识别
- 可忽略性（Ignorability）：$Z \perp \{Y(1), Y(0)\}$ 是关键假定

### Fisher vs Neyman 分歧
- **Fisher Randomization Test**：sharp null（$Y_i(1) = Y_i(0)$ 对所有个体成立），有限样本框架
- **Neyman Repeated Sampling**：测试种群效应，基于置信区间理论
- 适用场景不同：有限总体用 Fisher，超总体推论用 Neyman

### 观察性研究的困局
- 无随机化下难以保证可忽略性
- 烟草与肺癌、健康工人效应等实例说明相关性≠因果性
- 需要：（1）明确假设；（2）敏感性分析；（3）多角度论证

## 概念链接

[[Rubin-Causal-Model]] | [[Yule-Simpson Paradox]] | [[Ignorability]] | [[Causal-Diagram]] | [[Fisher Randomization Test]]

## 原文位置

[[raw/notes/causal-inference/2023-07-09-statistics-causal-inference/index.md]]
