---
source_type: repo
source_url: https://github.com/thuml/Time-Series-Library
source_local_path: raw/repos/Time-Series-Library
title: Time-Series-Library
created_at: 2026-04-11
topics:
  - 时间序列预测
  - 深度学习
related_concepts:
  - 时序基础模型
  - 深度学习时间序列预测
status: summarized
---

# Time-Series-Library 仓库入口笔记

## 仓库信息

- 仓库名：`Time-Series-Library`
- 仓库地址：https://github.com/thuml/Time-Series-Library
- 组织：THUML (清华大学机器学习实验室)
- 主要用途：收集、实现和评测各种深度学习时间序列预测模型，提供统一的代码框架和实验脚本。

## 仓库内容概览

- 模型实现：包括 iTransformer、TimeMixer、Sundial、Timer、OpenLTM 等前沿时间序列模型
- 实验脚本：长期预测、零样本预测等任务的训练和评估脚本
- 数据集处理：ETT、Weather、Electricity 等常用时间序列数据集的加载与预处理
- 统一框架：提供一致的模型接口、训练循环和评估指标

## 关键入口

- 仓库总入口：`README.md`
- 主要目录结构：
  - `models/`：模型实现代码
  - `exp/`：实验脚本
  - `scripts/`：运行脚本
  - `data_provider/`：数据集加载与预处理
  - `layers/`：基础神经网络层
  - `utils/`：工具函数
  - `tutorial/`：教程与示例

## 研究价值

- 代码实现参考：了解最新时间序列模型的 PyTorch 实现细节
- 实验复现：使用统一的框架复现论文结果
- 方法对比：在同一基准下比较不同模型的性能
- 工程实践：学习时间序列预测的工程化实现模式

## 建议拆分的知识单元

1. 模型实现体系
   - iTransformer 实现与原理
   - TimeMixer 系列模型
   - 时序基础模型 (Timer, Sundial, OpenLTM)

2. 实验框架设计
   - 统一的训练/验证/测试流程
   - 多数据集支持
   - 评估指标与结果记录

3. 工程最佳实践
   - 代码组织模式
   - 配置管理
   - 实验可复现性