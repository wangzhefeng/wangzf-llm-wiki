---
author:
- '[[时序之心]]'
created: 2026-04-10
description: PyRregular开源34个数据集基准，找不规则时序方向baseline的可以直接抄作业
published: null
source: https://mp.weixin.qq.com/s/_h6SMNWEhpvbeGU8wwlSQw
tags:
- clippings
title: PyRregular开源34个数据集基准，找不规则时序方向baseline的可以直接抄作业
topics:
- 时间序列
source_type: local_note
created_at: 2026-04-10
---
原创 时序之心 *2026年4月10日 14:43*

现实世界中的时间序列数据常因采样不均、观测缺失、长度不一等问题而呈现“不规则”性，这给医疗、交通、气象等领域的分析带来了巨大挑战。

针对此问题，本文解析的两篇论文从不同角度给出了解决方案。第一篇由 **意大利比萨大学** 提出的 **PyRregular** 框架，旨在建立统一的 **不规则时间序列** 处理标准与分类基准；第二篇提出的 **APN** 模型，则聚焦于 **预测任务** ，通过创新的自适应分块聚合机制，在保证精度的同时大幅提升计算效率。二者分别从“标准化基准”与“高效建模”两个层面推动了该领域的发展。

我把两篇论文的核心资料整理好了： **34个数据集清单+不规则类型标注表，以及不规则时间序列精选论文合集** ，感兴趣的可以自取，希望能帮到你~

![图片](https://mmbiz.qpic.cn/sz_mmbiz_gif/Dxic0cdJa3wlAA4uBN6OySXAEVRyKLT2Lm6W6fpAkR2Ibpiaanib2zgCAHLjzPHr1qo8KlYVWrOxP5cbntqGaLSUxqpL1c5LZEtM5ys71rI68o/640?wx_fmt=gif&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

扫码添加小助手回复“B181”

免费获取全部资料

## 一、论文1：PYRREGULAR: A UNIFIED FRAMEWORK FOR IRREGULAR TIME SERIES, WITH CLASSIFICATION BENCHMARKS（意大利比萨大学）

### 方法：

PyRregular 提出了一套处理不规则时间序列的统一框架。它首先定义了三种独立的 **不规则性** 类型： **不均匀采样** 、 **部分观测** 和 **参差不齐** 。框架的核心是将数据转换为基于 **COO稀疏张量** 的通用数组格式，并利用 xarray 库存储时间戳，从而实现高效存储与操作。最终，该框架可无缝对接多种现有分类库。

### 创新点：

1. **首个标准化基准** ：发布了首个包含34个数据集的 **不规则时间序列分类** 标准化仓库，并基于此对12种来自不同领域的分类器进行了全面的基准测试。
2. **统一数据表示** ：提出了一种结合稀疏张量与时间戳的统一数组格式，有效区分了“部分观测”和“参差不齐”导致的缺失值，解决了现有格式无法同时处理各类不规则性的痛点。
3. **关键发现** ：基准测试结果显示，原本为规则时间序列设计的 **ROCKET** 方法在不规则数据上表现最佳，且 **LightGBM** 等简单基线模型在性能和效率上优于许多复杂深度学习模型。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

- 论文链接：https://arxiv.org/pdf/2505.06047

## 二、论文2：Rethinking Irregular Time Series Forecasting: A Simple yet Effective Baseline（华东师范大学）

### 方法：

论文提出 APN 框架。核心是 **时间感知分块聚合模块** ，该模块为每个通道独立学习动态的“软窗口”，并通过 **加权平均** 策略直接聚合窗口内的原始观测值，从而将不规则序列转换为规则、高质量的 **分块表示** 。随后，一个轻量级的查询模块汇总历史信息，最后通过一个 **浅层MLP** 进行预测。

### 创新点：

1. **自适应分块策略** ：摒弃了传统固定长度的“硬分割”方法，创新性地提出 **自适应软分块** 机制。通过为每个分块学习动态的左右边界，使模型能灵活适应局部信息密度的变化，并保证每个观测点都对所有分块有贡献，避免信息丢失。
2. **高效轻量架构** ：将处理不规则性的复杂性“前加载”到 TAPA 模块，使得后续的聚合与预测模块可以极简化。实验证明，APN 在 **PhysioNet** 等多个真实数据集上的预测精度超越了现有最先进方法，同时显著降低了GPU内存、参数量和运行时间。
3. **避免插值偏差** ：与现有通过插值填补缺失值的方法不同，APN 的加权聚合策略直接使用原始观测数据，避免了插值可能引入的 **数据失真** ，保证了信息保真度。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

- 论文链接：https://arxiv.org/pdf/2505.11250

扫码添加小助手回复“B181”

免费获取全部资料

作者提示: 个人观点，仅供参考

继续滑动看下一个

时序之心

向上滑动看下一个