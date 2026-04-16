---
title: Rubin Causal Model
created: 2026-04-15
updated: 2026-04-15
type: concept
tags:
  - causal-inference
  - 潜在结果
  - RCM
  - 因果模型
sources:
  - wiki/sources/causal-inference/2023-07-09-Yule-Simpson悖论与因果推断基础.md
  - wiki/sources/causal-inference/2023-07-25-因果推断理论框架.md
---

# Rubin Causal Model（鲁宾因果模型）

## 定义

Rubin Causal Model（RCM），由统计学家 Donald Rubin 提出，是因果推断中最重要的理论框架。RCM 基于**潜在结果（Potential Outcomes）**的概念，认为每个单位对于每种可能的处理都有一个潜在的结果，而我们观测到的是其中一个。

## 核心概念

### 潜在结果（Potential Outcomes）

对于每个个体 $i$ 和处理变量 $Z_i \in \{0,1\}$（二值处理），定义：

- $Y_i(1)$：个体 $i$ 接受处理时的潜在结果
- $Y_i(0)$：个体 $i$ 不接受处理时的潜在结果

**关键特性**：两个潜在结果都是确定的数值，但通常我们只能观测其中一个。

### 个体因果作用（Individual Causal Effect）

$$\tau_i = Y_i(1) - Y_i(0)$$

个体因果作用衡量处理对单个个体的效应。

**根本问题**：个体因果作用 $\tau_i$ **不可识别**，因为：
- 当 $Z_i = 1$ 时，我们观测 $Y_i(1)$，但不知道 $Y_i(0)$
- 当 $Z_i = 0$ 时，我们观测 $Y_i(0)$，但不知道 $Y_i(1)$
- 这称为"缺失数据问题"的一个特例

### 观测结果（Observed Outcome）

观测结果是潜在结果的混合：

$$Y_i = Z_i Y_i(1) + (1-Z_i) Y_i(0)$$

### 平均因果作用（Average Causal Effect, ACE）

由于个体效应不可识别，我们转而估计群体平均效应：

$$ACE = E[Y_i(1) - Y_i(0)] = E[Y_i(1)] - E[Y_i(0)]$$

## 可忽略性（Ignorability）

### 定义

在处理变量 $Z$ 和潜在结果 $\{Y(1), Y(0)\}$ 间，若满足：

$$Z \perp \{Y(1), Y(0)\} | X$$

称为**条件可忽略性**。特殊地，当不依赖 $X$ 时，称为**绝对可忽略性**。

### 含义

- 在给定协变量 $X$ 后，处理分配与潜在结果独立
- 不存在未观测的混杂因子
- 处理分配机制不依赖于潜在结果

### 在不同设计中的体现

| 设计 | 可忽略性保证 |
|---|---|
| 完全随机化实验 | $Z \perp \{Y(1), Y(0)\}$ |
| 分组随机化（stratified） | $Z \perp \{Y(1), Y(0)\} \| X$ |
| 观察性研究 | 需要假设（通常不可验证） |

### 在可忽略性下识别 ACE

若可忽略性成立，则：

$$ACE = E[Y_i | Z_i=1] - E[Y_i | Z_i=0]$$

观测差异等于因果效应。

## 平均处理效应（ATE）vs 条件平均处理效应（CATE）

### 平均处理效应（Average Treatment Effect）
$$\text{ATE} = E[Y(1) - Y(0)]$$
总体平均效应，最常见的因果效应度量

### 条件平均处理效应（Conditional ATE）
$$\text{CATE}(x) = E[Y(1) - Y(0) | X = x]$$
给定特征 $x$ 下的平均处理效应，反映异质性

### 异质性处理效应（HTE）
关注处理效应的个体差异，不同个体可能有不同的 $\tau_i$

## Sharp Null vs Weak Null

### Sharp Null Hypothesis（Fisher 框架）
$$H_0: Y_i(1) = Y_i(0) \quad \forall i$$

所有个体的处理效应都为零。在有限样本框架下，潜在结果被视为固定常数。

### Weak Null Hypothesis（Neyman 框架）
$$H_0: E[Y(1)] = E[Y(0)]$$

仅要求群体平均效应为零。在超总体框架下，视为抽样问题。

## RCM 的三层结构

### 1. 定义阶段（Model Specification）
- 明确处理变量、结果变量、协变量
- 定义潜在结果

### 2. 假设阶段（Assumption）
- 可忽略性：$Z \perp \{Y(1), Y(0)\} | X$
- 重叠（Overlap/Positivity）：所有个体都有接受和不接受处理的可能
- SUTVA（Stable Unit Treatment Value Assumption）：个体间无干扰

### 3. 估计阶段（Estimation）
给定假设，选择估计方法：
- 简单差异（Simple Difference）
- 回归调整（Regression Adjustment）
- 倾向评分（Propensity Score）
- 双重机器学习（Double Machine Learning）

## 与 Causal Diagram 的对比

| 维度 | RCM | Causal Diagram |
|---|---|---|
| 出发点 | 潜在结果概念 | 图形化因果关系 |
| 重点 | 估计因果效应 | 识别因果关系 |
| 优势 | 精确、数学严谨 | 澄清假设、直观 |
| 适用 | 处理效应评估 | 假设验证、变量控制 |
| 结合 | DoWhy 框架统一 | 识别 → 估计 |

## 关键假设检验

### 可忽略性（Ignorability）
❌ **不可直接检验**（基于数据）
✓ 需要：领域知识、敏感性分析

### 重叠（Overlap）
✓ **可检验**：检查倾向评分分布是否重叠

$$0 < P(Z=1|X) < 1 \quad \forall X$$

### SUTVA
❌ **通常不可检验**
✓ 需要：研究设计确保

## 常见错误

❌ **错误 1**：认为随机化自动满足所有假设
✓ **正确**：随机化只满足可忽略性，需检查重叠与SUTVA

❌ **错误 2**：混淆观测差异与因果效应
✓ **正确**：只有在可忽略性成立时，二者才相等

❌ **错误 3**：估计个体因果作用
✓ **正确**：个体效应不可识别，应估计平均效应

## 应用示例

### A/B 测试
- 随机分组满足可忽略性
- 可直接计算 ATE = 处理组均值 - 对照组均值

### 观察性研究（如吸烟与肺癌）
- 假设可忽略性（假定已控制所有混杂因子）
- 应用倾向评分匹配、回归调整等方法
- 进行敏感性分析验证假设鲁棒性

## 参考与链接

- [[Causal-Diagram]] — Pearl 因果图框架
- [[Propensity-Score]] — 在观察性研究中应用 RCM
- [[DoWhy-Framework]] — RCM + 因果图的统一实现
- [[2023-07-09-Yule-Simpson悖论与因果推断基础]] — 理论基础来源

**相关概念**：潜在结果、个体因果作用、可忽略性、SUTVA、重叠、反事实推理
