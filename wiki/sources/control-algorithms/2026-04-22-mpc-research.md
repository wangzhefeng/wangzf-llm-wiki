---
title: 面向虚拟电厂与电力市场交易算法工程师的MPC调研文档
created: 2026-04-22
type: source
tags: [control-algorithms, mpc, model-predictive-control, virtual-power-plant, electricity-market]
topics: [control-algorithms, mpc]
status: summarized
source_type: notes
source_path: raw/notes/control-algorithms/2026-04-22-mpc_research/2026-04-22-mpc-research.md
related_concepts:
  - MPC
  - 线性MPC
  - 非线性MPC
  - 鲁棒MPC
  - 随机MPC
  - 经济MPC
  - MPC工具库
---

# 2026-04-22-mpc-research

## 讲了什么

面向虚拟电厂与电力市场交易的 MPC 系统调研，覆盖：MPC 核心概念与数学原理、算法家族与工程选型（线性/非线性/鲁棒/随机/经济/分布式/自适应 MPC）、Python 工具库生态（CVXPY/CasADi/Pyomo/do-mpc/GEKKO/MPCPy）、储能调度场景建模、电力市场交易集成、工程实践经验与选型建议。

## 核心价值

- 完整的 MPC 技术分类框架（7 种 MPC 类型对比表）
- Python 工具链三层架构（建模语言/最优控制框架/领域工作流平台）
- 能源场景 MPC 建模示例（储能 SOC/功率约束/经济目标）
- 工程选型决策树：凸 MPC → 场景化随机 MPC → NMPC → MILP
- 与 [[电力市场交易总索引]] 的天然跨主题连接

## 关键结论

> 若目标是快速工程落地，建议先从线性/凸经济 MPC 做主干，再把最关键的不确定性通过场景化、软约束和滚动重优化吸收；若必须显式建模强非线性或高保真储能老化，再引入 CasADi/GEKKO/do-mpc 这类 NMPC 工具栈；若涉及启停、充放互斥、市场报量等离散规则，则应优先把问题整理成 MILP/QP，再使用 Gurobi/CPLEX 等商用求解器。

## 关联概念

- [[MPC算法家族]] — 7 种 MPC 类型详解
- [[MPC数学原理]] — 滚动优化、约束处理、稳定性分析
- [[MPC工具库]] — Python 工具链对比与选型
- [[储能MPC建模]] — 能源场景具体建模方法
