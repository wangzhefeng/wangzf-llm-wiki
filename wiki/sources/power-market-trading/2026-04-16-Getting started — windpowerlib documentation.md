---
source_type: web
source_path: raw/web/power-market-trading/2026-04-16-Getting started — windpowerlib  documentation.md
title: Getting started — windpowerlib documentation
author: windpowerlib contributors
published_at: null
created_at: 2026-04-16
topics:
  - power-market-trading
related_concepts:
  - 风光储测算
status: summarized
---

# 来源卡：windpowerlib documentation

- 原文：[[raw/web/power-market-trading/2026-04-16-Getting started — windpowerlib  documentation.md]]
- 来源平台：Read the Docs
- 角色定位：风机出力建模工具文档

## 这份材料讲了什么

这份文档是 `windpowerlib` 的入门说明，核心是如何利用风机参数、天气数据和功率曲线计算风电机组或风场的出力。与本主题相关的点主要有：

1. **风机对象建模**：支持内置机型库或自定义功率曲线
2. **基础仿真链路**：利用天气数据、轮毂高度和机型参数计算风机出力
3. **风场与集群建模**：不仅支持单机，也支持风场和机群级别的模拟
4. **样例与数据源**：提供示例脚本、笔记本与 turbine library 的调用方式

## 价值是什么

- 为“风光储测算算法方案”中的风机出力模拟模块提供标准工具支撑
- 它让风电容量配置不再只依赖经验小时数，而是可以建立在功率曲线与天气输入之上
- 在电力交易主题里，它主要服务于绿电直连测算、新能源出力评估与交易情景建模，不承担市场规则解释功能

## 连到哪些概念

- [[风光储测算]] — 风机出力模拟的工具基础
