---
source_type: repo
source_url: https://github.com/wangzhefeng/tsproj_stat
source_local_path: raw/repos/tsproj_stat
created_at: 2026-04-12
topics:
  - 时间序列预测
  - 统计模型
related_concepts:
  - 统计时间序列预测
  - ARIMA模型
  - 预测框架
status: inbox
---

# tsproj_stat 仓库入口笔记

## 仓库信息

- 仓库名：`tsproj_stat`
- 仓库地址：https://github.com/wangzhefeng/tsproj_stat
- README 入口：`README.md`
- 主要用途：提供基于统计模型（ARIMA / Naive）的时间序列预测框架，包含训练、推理、回测、评估与模型持久化功能。

## 仓库要解决的问题

- 为统计时间序列预测提供标准化的工程框架，避免重复造轮子。
- 实现ARIMA模型的自动化选阶（AIC/BIC准则）和模型持久化。
- 提供统一的回测评估接口，支持MAE、RMSE、MAPE等指标。
- 建立可扩展的统计模型接口，便于后续添加新的统计预测方法。

## 关键入口

- 仓库总入口：`README.md`
- 主要目录结构：
  - `src/ts_forecast_framework/`：核心框架代码
    - `data.py`：数据加载与预处理
    - `persistence.py`：模型保存/加载
    - `evaluation/`：回测评估模块（backtest.py, metrics.py）
    - `inference/`：预测模块（predict.py）
    - `models/`：模型实现（base.py, selection.py, statistical.py）
  - `config/`：配置文件
  - `examples/`：示例脚本
  - `tests/`：单元测试

## 核心功能

1. **统一模型接口**：所有模型实现`fit`和`predict`方法，提供一致的API。
2. **ARIMA自动选阶**：支持网格搜索结合AIC/BIC准则自动选择最优(p,d,q)参数。
3. **回测评估**：提供完整的回测流程，支持多种评估指标。
4. **模型持久化**：使用pickle序列化保存和加载模型，便于部署。
5. **模块化设计**：数据、模型、评估、持久化模块分离，便于维护和扩展。

## 已实现模型

- **ARIMAForecaster**：基于statsmodels的ARIMA模型，支持自动选阶
- **NaiveForecaster**：朴素预测方法（如持久化预测），作为基线模型

## 技术要点

1. **自动选阶实现**：通过网格搜索遍历可能的(p,d,q)组合，根据信息准则选择最优模型。
2. **回测设计**：支持扩展窗口和滑动窗口回测策略，确保时间序列评估的正确性。
3. **配置管理**：使用YAML配置文件管理模型超参数和实验设置。
4. **测试覆盖**：包含数据加载、模型训练、评估指标、持久化等关键功能的单元测试。

## 建议拆分的知识单元

1. 统计时间序列预测框架设计
   - 统一模型接口模式
   - 模块化架构设计
   - 配置管理与实验设置

2. ARIMA模型实践
   - 自动选阶算法实现
   - 模型训练与预测流程
   - 超参数调优方法

3. 回测评估系统
   - 时间序列回测策略
   - 评估指标计算与比较
   - 结果可视化与报告

4. 模型部署与持久化
   - 模型序列化与反序列化
   - 生产环境部署考虑
   - 版本管理与回滚

## 首轮判断

- 该仓库提供了统计时间序列预测的完整工程框架，具有较高的实用性。
- 代码结构清晰，模块化程度高，便于学习和扩展。
- 适合作为统计时间序列预测项目的基础框架，也可用于教学和原型开发。