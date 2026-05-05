---
source_type: web
source_path: raw/web/power-market-trading/2026-04-16-pvlib python — pvlib python 0.15.0 documentation.md
title: pvlib python — pvlib python 0.15.0 documentation
author: pvlib python contributors
published_at: null
created_at: 2026-04-16
topics:
  - power-market-trading
related_concepts:
  - 风光储测算
status: summarized
---

# 来源卡：pvlib python documentation

- 原文：[[raw/web/power-market-trading/2026-04-16-pvlib python — pvlib python 0.15.0 documentation.md]]
- 来源平台：Read the Docs
- 角色定位：光伏出力建模工具文档

## 这份材料讲了什么

这份文档介绍了 `pvlib python` 这个开源光伏建模工具箱，重点在于如何用标准化的物理模型模拟光伏系统性能。与本主题直接相关的能力包括：

1. **站点建模**：位置、时区、海拔等站点参数初始化
2. **太阳与辐照度计算**：太阳位置、辐照度分解与转换
3. **温度与组件模型**：组件温度、逆变器和系统参数建模
4. **功率计算链路**：从气象输入到交流功率输出的整套计算流程
5. **示例与规范**：提供示例、命名规范与版本化引用方式，适合作为工程实现参考

## 价值是什么

- 为“风光储测算算法方案”中的光伏模块提供了标准工具底座
- 它不是电力市场规则资料，但能把“绿电出力能力”从经验估算提升为可复现的模型计算
- 在做绿电直连测算、新能源自发自用分析、交易策略压力测试时，可作为光伏出力模拟的首选工具入口

## 连到哪些概念

- [[风光储测算]] — 光伏出力模拟的工具基础
