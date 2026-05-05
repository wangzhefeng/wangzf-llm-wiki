---
source_type: repo
source_path: raw/repos/control-algorithm-proj/README.md
title: control-algorithm-proj 仓库入口
created_at: 2026-04-17
topics:
  - control-algorithms
related_concepts:
  - PID 控制
  - 现代控制方法
  - 控制系统基础
status: summarized
---

# control-algorithm-proj 仓库入口来源摘要

## 材料定位

`control-algorithm-proj` 是一个面向控制算法学习与实验的 Python 仓库。它不是单一算法实现，而是把 `PID -> LQR -> MPC / NMPC / iLQR` 组织成一条可运行的学习链，适合作为控制算法主题里的“现代控制工程入口”。

## 核心模块与结构

- `src/pid/`：PID 基础、状态空间 PID、耦合系统 PID
- `src/lqr/`：离散 LQR、增量 LQR 跟踪、iLQR 单车示例
- `src/mpc/`：线性 MPC、跟踪 MPC、CasADi NMPC、单车 NMPC
- `docs/`：控制工程、模糊 PID、工业过程控制相关资料
- `pyproject.toml`：依赖定义，关键栈包括 `numpy / scipy / cvxpy / casadi / matplotlib`

## 关键价值

- 它把当前控制算法主题从“经典控制概念”推进到“现代控制示例仓库”
- 同时覆盖线性与非线性控制、调节与跟踪两类问题
- 每个子目录都自带运行说明，适合从概念页进入代码验证

## 在知识库中的位置

- 属于 `control-algorithms` 主题的 repo 工程来源
- 与 [[PID-控制]] 形成“概念 -> 可运行示例”的对应关系
- 与 [[现代控制方法]] 形成“方法总览 -> 算法示例仓库”的入口关系

## 主要连接概念

- [[控制系统基础]]
- [[PID-控制]]
- [[现代控制方法]]

## 当前局限

- 更偏学习示例，不是生产控制框架
- 自动化测试仍然较弱，重点是可运行演示而不是结果回归
- 文档和代码主要覆盖单体示例，尚未抽象成统一控制库

## 后续可深化方向

1. 补 `LQR / MPC / iLQR / NMPC` 的概念页或方法页细分
2. 把运行指标、求解器与建模差异整理成控制算法对比表
3. 补“控制算法工程实现”专题，沉淀从理论到脚本验证的学习路径
