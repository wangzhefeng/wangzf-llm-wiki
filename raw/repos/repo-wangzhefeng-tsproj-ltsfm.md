---
source_type: repo
source_url: https://github.com/wangzhefeng/tsproj_ltsfm
source_local_path: raw/repos/tsproj_ltsfm
created_at: 2026-04-12
topics:
  - 时间序列预测
  - 时序基础模型
  - 大模型
related_concepts:
  - 时序基础模型
  - 大语言模型时间序列预测
  - 零样本预测
status: inbox
---

# tsproj_ltsfm 仓库入口笔记

## 仓库信息

- 仓库名：`tsproj_ltsfm`
- 仓库地址：https://github.com/wangzhefeng/tsproj_ltsfm
- README 入口：`README.md`
- 主要用途：围绕时间序列基础模型（Time-MoE 和 Sundial）开展方法调研、脚本接入和实验管理，提供统一的时间序列基础模型评测框架。

## 仓库要解决的问题

- 系统化调研和集成前沿时间序列基础模型（Time-MoE, Sundial）。
- 提供统一的时间序列基础模型评测接口，支持零样本预测、长期预测等任务。
- 实现“两级实验”策略：本地开发机进行代码验证，A100服务器进行大规模实验。

## 关键入口

- 仓库总入口：`README.md`
- 主要目录结构：
  - `pretrain_models/`：预训练模型副本（TimeMoE-50M, TimeMoE-200M, sundial-base-128m）
  - `scripts/`：运行脚本，按模型分类（Time-MoE, Sundial）
  - `results/`：实验结果记录
  - `docs/`：调研报告与文档

## 核心模型

### Time-MoE
- 论文：Time-MoE: Billion-Scale Time Series Foundation Models with Mixture of Experts
- 特点：基于MoE结构的自回归时间序列基础模型，支持50M和200M参数版本
- 应用：长期预测、零样本预测、多数据集统一评测

### Sundial
- 论文：Sundial: A Family of Highly Capable Time Series Foundation Models
- 特点：THUML发布的生成式时间序列基础模型，强调zero-shot forecasting能力
- 应用：概率式样本生成、跨数据集泛化、统一评测

## 实验策略

- **本地开发机**：代码开发、本地smoke test、数据流验证、README命令校验
- **A100 8GPU服务器**：较大checkpoint、较长上下文、较多样本的正式对比实验
- **统一评测接口**：支持滑窗评测，便于不同基础模型的横向比较

## 技术要点

1. **模型适配**：解决官方代码与transformers库的兼容性问题，通过直接自回归前向推理适配
2. **评测标准化**：按“单目标列预测”实现benchmark接口，支持多变量数据集
3. **资源管理**：预训练模型本地副本管理，避免重复下载
4. **实验记录**：结构化保存实验结果，便于分析与复现

## 建议拆分的知识单元

1. 时间序列基础模型评测框架
   - 统一评测接口设计
   - 零样本预测评测流程
   - 多模型横向比较方法

2. Time-MoE模型实践
   - MoE结构在时间序列中的应用
   - 预训练模型加载与推理
   - 长期预测与零样本预测实现

3. Sundial模型实践
   - 生成式时间序列建模
   - 概率式样本生成技术
   - 跨数据集泛化能力评测

4. 大规模实验管理
   - 两级实验策略设计
   - 分布式训练与推理优化
   - 实验结果记录与分析

## 首轮判断

- 该仓库专注于时间序列基础模型的实践与评测，具有前瞻性。
- 提供了完整的模型调研、代码接入和实验管理框架。
- 适合作为时间序列基础模型研究与实践的参考项目。