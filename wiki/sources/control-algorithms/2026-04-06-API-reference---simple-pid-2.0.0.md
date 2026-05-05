---
source_type: web
source_path: raw/web/control-algorithms/2026-04-06-API-reference-simple-pid-2.0.0.md
title: "API reference - simple-pid 2.0.0"
created_at: 2026-04-06
topics:
  - control-algorithms
related_concepts:
  - PID 控制
status: summarized
---

# 来源卡：API reference - simple-pid 2.0.0

## 这份材料讲了什么

- 原文：`raw/web/control-algorithms/2026-04-06-API-reference-simple-pid-2.0.0.md`
- 来源：https://simple-pid.readthedocs.io/en/latest/reference.html
- 内容：Python `simple-pid` 库（v2.0.0）的完整 API 文档，仅包含一个 `PID` 类
- 核心参数：`Kp`/`Ki`/`Kd`（增益）、`setpoint`（目标值）、`sample_time`（采样间隔，默认 0.01s）、`output_limits`（输出限幅元组）
- 工程特性：
  - `output_limits`：同时防止积分饱和（windup），限制输出在 `[lower, upper]` 区间
  - `proportional_on_measurement`：比例项作用于测量值而非误差，减少设定值跳变时的超调
  - `differential_on_measurement`：微分项作用于测量值（默认 True），避免"微分尖峰"
  - `set_auto_mode(enabled, last_output)`：手动/自动模式切换，从手动无扰切换至自动时传入末次输出
  - `reset()`：清零所有积分项和历史状态，适合切换设定值前调用
  - `components` 属性：返回 (P, I, D) 三项分量，方便调试和可视化
  - `time_fn` 参数：可注入自定义时钟函数，支持仿真场景中的虚拟时间

## 价值是什么

- 提供工程级 PID 实现的最佳实践参考：积分饱和防护、无扰切换、可调试分量输出
- 比教材中的离散 PID 公式更接近生产代码，适合 Python 控制项目直接使用
- `proportional_on_measurement` 和 `differential_on_measurement` 是进阶调优选项，可减少特定系统的超调

## 连到哪些概念

- [[PID-控制]]（实现章节，工程实践部分）

## 相关来源

- [[2024-07-21-控制算法概述-PID与模糊控制]]（理论基础）
