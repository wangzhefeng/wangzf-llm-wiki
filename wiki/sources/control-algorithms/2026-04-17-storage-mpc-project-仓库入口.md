---
source_type: repo
source_path: raw/repos/storage_mpc_project/README.md
title: storage_mpc_project 仓库入口
created_at: 2026-04-17
topics:
  - control-algorithms
related_concepts:
  - 现代控制方法
  - 风光储测算
  - 电力交易优化建模
status: summarized
---

# storage_mpc_project 仓库入口来源摘要

## 材料定位

`storage_mpc_project` 是一个面向能源场景的储能 MPC 工程模板。它把 `Forecasting -> Optimization -> Control` 组织成最小可运行闭环，重点展示如何用 `cvxpy` 在储能调度问题里实现滚动优化控制。

## 核心模块与结构

- `src/storage_mpc_project/mpc_controller.py`：MPC 核心优化建模
- `battery.py / simulator.py / forecasting.py`：电池状态、滚动仿真与预测接口
- `metrics.py / plotting.py`：结果评估与可视化
- `data/sample_day.csv`：最小样例数据
- `outputs/`：示例运行结果与图像

## 关键价值

- 它是控制算法主题中的“能源场景 MPC 模板”
- 明确展示储能控制问题里的状态、动作、目标函数和约束组织方式
- 适合作为控制算法与电力市场交易主题之间的跨主题工程接口

## 在知识库中的位置

- 主归属是 `control-algorithms` 主题的工程模板来源
- 通过 [[电力交易优化建模]] 与 `power-market-trading` 主题建立跨主题连接
- 在 [[现代控制方法]] 下作为“场景化 MPC”实例落位

## 主要连接概念

- [[现代控制方法]]
- [[电力交易优化建模]]
- [[风光储测算]]

## 当前局限

- 更偏单储能控制模板，不覆盖完整多市场交易机制
- 样例数据是演示级，不代表真实市场数据
- 重点是控制闭环跑通，不是复杂随机优化或多资源联合调度框架

## 后续可深化方向

1. 与 `ele-trading` 的结算与场景模块做更明确的分工对照
2. 补“储能 MPC 与电力交易优化”的方法桥接说明
3. 引入真实预测接口或多资源扩展时，再沉淀更细的工程专题页
