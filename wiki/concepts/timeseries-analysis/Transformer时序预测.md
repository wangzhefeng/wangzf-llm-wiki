---
created_at: 2026-04-06
topics:
- timeseries
related_concepts:
- 多尺度建模
- 频率分解
status: inbox
---
# Transformer 时序预测

## 定义

将 Transformer 架构应用于时间序列预测任务的方法和技术。

## 核心挑战

- **长序列问题**: 传统 Transformer 在长序列上计算复杂度高
- **非平稳性**: 时间序列统计特性随时间变化
- **多尺度特征**: 时序数据包含不同时间尺度的模式

## 主要架构演进

### 早期工作
- **Informer** (AAAI 2021): ProbSparse 自注意力，降低复杂度
- **Autoformer**: 分解架构，分解趋势和季节成分

### Transformer 变体
- **iTransformer**: 倒置 Transformer，在特征维度做注意力
- **Scaleformer** (ICLR 2023): 迭代多尺度细化
- **TimesNet** (ICLR 2023): 时序 2D 变化建模

### 其他架构
- **N-BEATS/N-HiTS**: 基于 MLP 的层次架构
- **TimeMixer** (ICLR 2024): 多尺度混合方法
- **TimeKAN**: 基于 KAN 的时序预测

### 基础模型
- **TimesFM** (Google): 时序基础模型
- **Sundial** (ICML 2025): 时序基础模型家族

## 关键技术

- **注意力机制优化**: ProbSparse、局部注意力
- **频率分解**: 将序列分解为不同频率成分
- **多尺度建模**: 捕获不同时间尺度的依赖
- **位置编码**: 适应时序数据的位置表示

## 相关来源

- [[时间序列预测深度学习专题来源]]
- [[时间序列预测深度学习论文索引]]

## 相关概念

- [[多尺度建模]]
- [[频率分解]]
- [[时序基础模型]]
- [[注意力机制]]
