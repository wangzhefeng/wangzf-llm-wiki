---
title: 储能MPC项目工程版（v1）
created: 2026-04-22
type: source
tags: [control-algorithms, mpc, energy-storage, cvxpy, osqp]
topics: [control-algorithms, mpc, energy-storage]
status: summarized
source_type: notes
source_path: raw/notes/control-algorithms/2026-04-22-mpc_research/storage_mpc_project/README.md
related_concepts:
  - 储能MPC建模
  - 线性MPC
  - CVXPY
  - OSQP
---

# storage_mpc_project (v1)

## 讲了什么

储能 Model Predictive Control 工程项目（v1），使用 CVXPY + OSQP 构建线性二次型 MPC 控制器，面向能源/电力算法工程师设计。核心功能：负荷预测序列输入、电价预测序列输入、储能 SOC 约束、功率约束、功率平滑项、终端 SOC 惩罚。

## 核心价值

- 工程级储能 MPC 实现模板
- CVXPY + OSQP 组合的完整 QP 建模示例
- SOC 状态转移方程：$SOC_{k+1} = SOC_k - \frac{\Delta t}{E} u_k$
- 目标函数包含：购电成本 + SOC 惩罚 + 控制平滑项 + 终端惩罚
- 完整的仿真数据生成、控制器、滚动仿真、可视化流程

## 关键接口

```python
# MPC 控制器核心
python scripts/run_simulation.py
# 输出: simulation_results.csv, soc_trajectory.png, power_dispatch.png
```

## 关联概念

- [[2026-04-22-mpc-research]]
- [[储能MPC建模]]
- [[MPC工具库]]
