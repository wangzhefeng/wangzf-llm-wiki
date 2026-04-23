---
title: MPC数学原理
created: 2026-04-22
type: concept
tags: [control-algorithms, mpc, mpc-mathematics, optimization, constraints, stability]
topics: [control-algorithms, mpc]
status: summarized
sources:
  - raw/notes/control-algorithms/2026-04-22-mpc_research/2026-04-22-mpc-research.md
related_concepts:
  - MPC
  - MPC算法家族
  - MPC工具库
---

# MPC数学原理

## 标准离散时间 MPC 表述

**系统模型**：
$$x_{k+1} = f(x_k, u_k, d_k, \theta), \quad y_k = h(x_k, u_k)$$

**有限时域最优控制问题**（在时刻 $k$ 求解）：
$$\min_{\{u_{k|k},\dots,u_{k+N-1|k}\}} \sum_{i=0}^{N-1} \ell(x_{k+i|k}, u_{k+i|k}) + V_f(x_{k+N|k})$$

**约束条件**：
$$x_{k+i+1|k} = f(x_{k+i|k}, u_{k+i|k}, d_{k+i|k}, \theta)$$
$$(x_{k+i|k}, u_{k+i|k}) \in \mathcal{Z}$$
$$x_{k+N|k} \in \mathcal{X}_f$$

其中：
- $N$：预测时域（horizon）
- $\ell$：阶段代价函数
- $V_f$：终端代价函数
- $\mathcal{Z}$：约束集合（状态 + 输入）
- $\mathcal{X}_f$：终端约束集合

**关键机制**：求得整段最优控制序列后，只把第一步 $u_{k|k}^*$ 下发执行。

## 线性 MPC（QP 形式）

对线性跟踪型 MPC，整理为标准凸 QP：

$$\min_z \frac{1}{2} z^\top H z + g^\top z$$
$$\text{s.t. } Gz \le h, \; Az = b$$

**两种变量组织形式**：
- **Condensed form**：只保留控制序列 $u_{0:N-1}$，变量数少但 Hessian 更密
- **Sparse stage-wise form**：保留完整状态序列 $x_{0:N}$，变量多但利用块带状结构

## 约束分类与处理

### 约束类型

| 类型 | 描述 | 处理方式 |
|------|------|---------|
| **硬约束** | 必须满足（SOC 下界、温度上限） | 直接写入优化问题 |
| **软约束** | 允许短时违反但付出惩罚 | 惩罚函数 + 松弛变量 |
| **耦合约束** | 多变量关系（功率平衡） | 等式约束 |
| **终端约束** | 保证稳定性/经济可行性 | 终端集合 $\mathcal{X}_f$ |

### 储能场景约束示例

**SOC 状态更新**：
$$SOC_{t+1} = SOC_t + \frac{\eta_c P^{ch}_t \Delta t}{E_{cap}} - \frac{P^{dis}_t \Delta t}{\eta_d E_{cap}}$$

**功率平衡**：
$$P^{grid}_t = P^{load}_t - P^{pv}_t + P^{ch}_t - P^{dis}_t$$

**约束集合**：
$$SOC_{min} \le SOC_t \le SOC_{max}$$
$$P^{ch}_t, P^{dis}_t \ge 0, \quad P^{ch}_t \cdot P^{dis}_t = 0 \text{ (互斥)}$$

## 稳定性分析

MPC 从"滚动优化器"变成"控制器"的分水岭是稳定性保证。

### 经典稳定性条件

1. **终端代价**：$V_f(x)$ 是 Lyapunov 函数
2. **终端集合**：$\mathcal{X}_f$ 是闭环正不变集
3. **递归可行性**：保证当前时刻可行 → 未来时刻可行

### 不同 MPC 类型的稳定性机制

| MPC 类型 | 稳定性机制 |
|---------|-----------|
| 跟踪 MPC | 终端约束 + terminal cost |
| 鲁棒 MPC | 不变集 + 管收缩 |
| 随机 MPC | 机会约束 + 概率终端集合 |
| 经济 MPC | Dissipativity + rotated cost / 周期终端 |

## 计算复杂度与实时性

### "足够好 + 足够快"原则

> Rawlings 教材明确指出：不宜执着于把每一次有限时域问题都"解得极其精确"，因为反馈延迟和 CPU 开销本身就会损害闭环性能。

### 复杂度来源

- **线性 QP**：Riccati 递推或带状 KKT，复杂度对 $N$ 近似线性
- **OSQP**：支持 factorization caching + warm start，重复求解极快
- **NLP（NMPC）**：内点法（IPOPT）对初值与尺度敏感，需初值平移、变量归一化、约束软化

## 预测模型类型

| 类型 | 描述 | 适用场景 |
|------|------|---------|
| **机理模型** | 质量/能量守恒、线性化潮流 | 工程设计 |
| **辨识模型** | ARX/状态空间/子空间辨识 | 数据充足 |
| **灰箱/数据驱动** | 机理结构 + 学习模块补偿残差 | 复杂非线性 |

## 核心公式速查

**滚动优化代价函数**：
$$\min \sum_{k=0}^{N-1} \left[ Q \|x_k - x^{ref}\|^2 + R \|u_k\|^2 \right] + P \|x_N - x^{ref}\|^2$$

**储能 MPC 目标函数**：
$$\min \sum_{t=k}^{k+N-1} \left[ c_t P^{grid,+} \Delta t + \lambda_{peak} P^{peak} + \lambda_{smooth}(P^{grid}_t - P^{grid}_{t-1})^2 \right] + \lambda_{soc}(SOC_T - SOC_{target})^2$$

**经济 MPC 目标函数**：
$$\max \sum_{t=k}^{k+N-1} \left( \pi_t^{sell} P_t^{sell} - \pi_t^{buy} P_t^{buy} - C_g(P_t^g) - C_{deg}(P_t^{ch}, P_t^{dis}) \right) \Delta t$$

## 相关概念

- [[MPC]] — MPC 核心概念
- [[MPC算法家族]] — 不同 MPC 类型对比
- [[MPC工具库]] — Python 实现对应
- [[储能MPC建模]] — 能源场景建模示例

## 来源

- [[2026-04-22-mpc-research]]
