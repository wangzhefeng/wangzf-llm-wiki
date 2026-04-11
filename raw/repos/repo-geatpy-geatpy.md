---
source_type: repo
source_url: https://github.com/geatpy-dev/geatpy
source_local_path: raw/repos/geatpy
title: geatpy
created_at: 2026-04-12
topics:
  - 运筹优化算法
  - 进化算法
  - 启发式优化
related_concepts:
  - 遗传算法
  - 粒子群优化
  - 数值优化求解器
status: inbox
---

# geatpy 仓库入口笔记

## 仓库信息

- 仓库名：`geatpy`
- 仓库地址：https://github.com/geatpy-dev/geatpy
- 组织：geatpy-dev
- 主要用途：高性能进化算法工具箱，提供遗传算法、差分进化、粒子群优化等多种进化算法的Python实现，支持多目标优化、约束优化等复杂场景。

## 仓库内容概览

- 算法实现：包括遗传算法(GA)、差分进化(DE)、粒子群优化(PSO)、模拟退火(SA)等主流进化算法
- 多目标优化：NSGA-II、NSGA-III、MOEA/D等多目标进化算法实现
- 约束处理：多种约束处理技术，包括罚函数法、可行性规则等
- 并行计算：支持多进程、多线程并行计算，加速大规模优化问题求解
- 可视化工具：提供进化过程、帕累托前沿等可视化功能

## 关键入口

- 仓库总入口：`README.md`
- 主要目录结构：
  - `geatpy/`：核心算法实现
  - `examples/`：示例代码与使用教程
  - `docs/`：文档与API参考
  - `tests/`：单元测试

## 在运筹优化主题中的定位

- geatpy是启发式算法主线的重要工具实现
- 填补了Python生态中高性能进化算法框架的空白
- 与Gurobi、CPLEX等数学规划求解器形成互补：前者擅长连续、非线性、多模态问题，后者擅长线性、整数规划等结构化问题

## 建议拆分的知识单元

1. 进化算法工具箱对比
   - geatpy vs. DEAP vs. pymoo
   - 性能特点与适用场景

2. 多目标优化实践
   - NSGA-II在geatpy中的实现与调参
   - 帕累托前沿分析与决策

3. 工程集成模式
   - 如何将geatpy集成到现有优化流程
   - 与数学规划求解器的混合求解策略