---
source_type: repo
source_url: https://github.com/wangzhefeng/tsproj_ltsfm
source_path: raw/repos/repo-wangzhefeng-tsproj-ltsfm.md
created_at: 2026-04-12
topics:
- llm
- timeseries
related_concepts:
- 时序基础模型
- 大语言模型时间序列预测
- 零样本预测
status: summarized
---
# 来源卡：tsproj_ltsfm 时间序列基础模型评测框架

## 这份材料讲了什么

- 原文：`raw/repos/repo-wangzhefeng-tsproj-ltsfm.md`
- 对应仓库：https://github.com/wangzhefeng/tsproj_ltsfm
- 内容：一个专注于时间序列基础模型（Time-MoE 和 Sundial）的方法调研、脚本接入和实验管理框架，提供统一的时间序列基础模型评测接口，支持零样本预测、长期预测等任务。

## 价值是什么

1. **前沿模型实践**：系统化集成当前最先进的时间序列基础模型（Time-MoE, Sundial），提供可复现的实践代码。
2. **统一评测框架**：设计标准化的评测接口，支持不同基础模型在相同基准下的横向比较。
3. **工程化实验管理**：实现“两级实验”策略，分离本地开发与大规模服务器实验，提高研究效率。
4. **零样本预测能力评估**：专注于时间序列基础模型的zero-shot forecasting能力评测，反映模型泛化性能。
5. **预训练模型管理**：提供预训练模型的本地副本管理，避免重复下载，加速实验进程。

## 连到哪些概念

- [[时序基础模型]] - 该框架专注于时间序列基础模型的实践与评测
- [[大语言模型时间序列预测]] - Time-MoE和Sundial均采用类似语言模型的自回归生成方式
- [[零样本预测]] - 重点评测模型的zero-shot forecasting能力
- [[预测工具生态]] - 作为时间序列预测工具链的一部分，提供基础模型评测能力

## 关键模块

- **pretrain_models/**：预训练模型副本目录（TimeMoE-50M, TimeMoE-200M, sundial-base-128m）
- **scripts/**：运行脚本，按模型分类组织
- **results/**：实验结果记录与存储
- **docs/**：模型调研报告与技术文档

## 核心模型

### Time-MoE
- 基于Mixture of Experts结构的时间序列基础模型
- 支持50M和200M参数版本
- 自回归生成方式，适合长期预测任务

### Sundial
- THUML发布的生成式时间序列基础模型
- 强调zero-shot forecasting能力
- 概率式样本生成，支持不确定性量化

## 使用建议

- 研究时间序列基础模型时，可参考该框架的模型调研和实现方式。
- 进行基础模型对比实验时，可使用其统一评测接口确保公平比较。
- 管理大规模时间序列实验时，可借鉴其两级实验策略和资源管理方法。
- 需要零样本预测能力评估时，可参考其评测流程和指标设计。

## 局限与注意点

- 目前主要支持Time-MoE和Sundial两个模型，其他基础模型可能需要扩展。
- 大模型推理对计算资源要求较高，需要GPU支持。
- 评测接口目前按“单目标列预测”实现，多变量预测需要适配。
- 框架仍处于活跃开发中，接口可能变化。