---
source_type: repo
source_url: https://github.com/wangzhefeng/tsproj_stat
source_path: raw/repos/repo-wangzhefeng-tsproj-stat.md
created_at: 2026-04-12
topics:
- shared
- timeseries
related_concepts:
- 统计时间序列预测
- ARIMA模型
- 预测框架
status: summarized
---
# 来源卡：tsproj_stat 统计时间序列预测框架

## 这份材料讲了什么

- 原文：`raw/repos/repo-wangzhefeng-tsproj-stat.md`
- 对应仓库：https://github.com/wangzhefeng/tsproj_stat
- 内容：一个基于统计模型（ARIMA / Naive）的时间序列预测框架，提供训练、推理、回测、评估与模型持久化的完整解决方案，包含ARIMA自动选阶、统一模型接口和模块化架构设计。

## 价值是什么

1. **工程化统计预测**：将统计时间序列预测方法（ARIMA）工程化，提供标准化的工作流程和接口。
2. **自动化选阶**：实现ARIMA模型的自动选阶功能，基于网格搜索和AIC/BIC准则选择最优参数。
3. **完整评估体系**：提供回测评估框架，支持多种评估指标（MAE、RMSE、MAPE）和时间序列特定的评估策略。
4. **可扩展架构**：模块化设计便于添加新的统计模型和扩展功能，适合作为统计预测项目的基础框架。
5. **生产就绪**：包含模型持久化、配置管理和单元测试，支持从实验到部署的全流程。

## 连到哪些概念

- [[统计时间序列预测]] - 该框架专注于统计方法的时间序列预测
- [[ARIMA模型]] - 核心实现ARIMA模型及其自动选阶功能
- [[预测框架]] - 提供完整的预测框架设计参考
- [[预测模型评估]] - 包含回测评估系统和多种评估指标
- [[预测工具生态]] - 作为统计预测工具链的一部分

## 关键模块

- **src/ts_forecast_framework/**：核心框架代码
  - `data.py`：数据加载与预处理
  - `persistence.py`：模型保存/加载
  - `evaluation/`：回测评估模块（backtest.py, metrics.py）
  - `inference/`：预测模块（predict.py）
  - `models/`：模型实现（base.py, selection.py, statistical.py）
- **config/**：配置文件管理
- **examples/**：示例脚本
- **tests/**：单元测试套件

## 核心功能

1. **统一模型接口**：所有模型实现`fit`和`predict`方法，提供一致的API。
2. **ARIMA自动选阶**：支持网格搜索结合AIC/BIC准则自动选择最优(p,d,q)参数。
3. **回测评估**：提供完整的回测流程，支持扩展窗口和滑动窗口策略。
4. **模型持久化**：使用pickle序列化保存和加载模型，便于部署和版本管理。
5. **配置驱动**：通过YAML配置文件管理模型超参数和实验设置。

## 使用建议

- 需要快速搭建统计时间序列预测项目时，可直接使用该框架作为起点。
- 进行ARIMA模型实验时，可利用其自动选阶功能简化参数调优。
- 评估统计模型性能时，可参考其回测评估系统和指标计算。
- 开发新的统计预测方法时，可基于其模块化架构进行扩展。

## 局限与注意点

- 目前主要支持ARIMA和Naive模型，其他统计模型需要扩展实现。
- 自动选阶的网格搜索可能计算成本较高，需要合理设置参数范围。
- 框架设计偏向传统统计方法，与机器学习/深度学习的集成需要额外工作。
- 生产环境部署时需要考虑模型更新策略和性能优化。