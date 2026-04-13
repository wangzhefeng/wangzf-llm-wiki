---
author:
- null
- '[[王世宇]]'
created: 2026-04-06
created_at: 2026-04-06
description: 蚂蚁集团和清华大学联合推出纯MLP架构模型TimeMixer，在时序预测上的性能和效能全面超越Transformer模型。
source_type: web
status: inbox
tags:
- null
- clippings
title: 时序预测双飞轮，全面超越Transformer，纯MLP模型实现性能效能齐飞
source_url: https://mp.weixin.qq.com/s/d7fEnEpnyW5T8BN08XRi7g
published_at: null
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

王世宇 *2024年6月25日 19:14*

点击上方蓝字，关注我们

**作者简介：** 王世宇，蚂蚁集团算法专家，在AI创新技术部NextEvo主要负责时序算法研究方向，主导时序预测平台建设和时序算法创新研发和架构工作，推动预测与决策联动的双引擎能力。在ICLR, IJCAI, KDD, AAAI, WSDM, ICDM, DASFAA等顶级会议发表多篇论文。  

**导读**

在数据驱动的时代，时序预测成为了许多领域中不可或缺的一部分。从金融市场的波动预测到智能制造中的设备故障预警，时序数据分析的准确性和效率直接影响着决策的质量和速度。

近年来，Transformer模型因其在自然语言处理(NLP)和计算机视觉(CV)中的卓越表现，引起了广泛关注。然而，Transformer在处理时序数据时存在一定的局限性，如计算复杂度高、对长序列数据处理不够高效等问题。

![[Image 75.webp|图片]]

**为了解决这些问题，近期蚂蚁集团和清华大学联合推出一种纯MLP架构的模型TimeMixer，在时序预测上的性能和效能两方面全面超越了Transformer模型，实现时序预测双飞轮。**

结合对时序趋势周期特性的分解以及多尺度混合的设计模式，不仅在长短程预测性能上大幅提升，而且基于纯MLP架构实现了接近于线性模型的极高效率，实现预测性能和模型效能齐飞。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**论文地址：**

https://openreview.net/pdf?id=7oLshfEIC2

**ARXIV地址：**

https://arxiv.org/abs/2405.14616v1

**论文代码：**

https://github.com/kwuking/TimeMixer

**论文概述**

TimeMixer是一种全新的时序预测模型，采用了纯多层感知机（MLP）架构，彻底摒弃了复杂的自注意力机制。该模型通过引入可分解的多尺度混合机制，在保持高精度预测的同时，大幅降低了计算复杂度和训练时间。

- **核心观察—History Extraction历史信息抽取：** 鉴于季节和趋势成分在时间序列中表现出明显不同的特征，并且时间序列的不同尺度反映了不同的属性，在细粒度的微观尺度上季节性特征更加明显，而在粗粒度的宏观尺度上趋势特征更加明显，因此，有必要在不同尺度上分离季节性和趋势成分。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)
- **核心观察—Future Prediction未来预测：** 整合不同尺度的预测得到最终的预测结果，不同尺度表现出互补的预测能力。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**模型框架**

TimeMixer模型采用了一个多尺度混合架构，旨在解决时间序列预测中的复杂时间变化问题。该模型主要采用全MLP（多层感知机）架构，由过去可分解混合Past Decomposable Mixing (PDM) 和未来多预测器混合Future Multipredictor Mixing (FMM) 两大块构成，能够有效利用多尺度序列信息。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)
- **Past Decomposable Mixing：** PDM负责提取过去的信息并将不同尺度上的季节性和趋势组分分别混合。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

PDM以季节和趋势混合为动力，将详细的季节信息由细到粗逐步聚合，并利用较粗尺度的先验知识深入挖掘宏观趋势信息，最终实现过去信息提取中的多尺度混合。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)
- **Future Multipredictor Mixing：** 请注意，未来多重预测器混合 (FMM) 是多个预测器的集合，其中不同的预测器基于不同尺度的过去信息，使 FMM 能够集成混合多尺度序列的互补预测功能。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**实验效果**

为了验证TimeMixer的性能，我们在包含长程预测，短程预测，多元时序预测以及具有时空图结构的18组基准数据集上进行了实验，包括电力负荷预测、气象数据预测和股票价格预测等。 **实验结果表明，TimeMixer在多个指标上全面超越了当前最先进的Transformer模型，具体表现如下：**

- **预测精度：** 在所有测试的数据集上，TimeMixer均表现出更高的预测精度。以电力负荷预测为例，TimeMixer相比于Transformer模型，平均绝对误差（MAE）降低了约15%，均方根误差（RMSE）降低了约12%。
- **计算效率：** 得益于MLP结构的高效计算特性，TimeMixer在训练时间和推理时间上均显著优于Transformer模型。实验数据显示，在相同硬件条件下，TimeMixer的训练时间减少了约30%，推理时间减少了约25%。
- **模型可解释性：** 通过引入Past Decomposable Mixing和Future Multipredictor Mixing技术，TimeMixer能够更好地解释不同时间尺度上的信息贡献，使得模型的决策过程更加透明和易于理解。
- **泛化能力：** 在多个不同类型的数据集上进行测试，TimeMixer均表现出良好的泛化能力，能够适应不同的数据分布和特征。这表明TimeMixer在实际应用中具有广泛的适用性。
- **长程预测：** 为了确保模型比较的公平性，使用标准化参数进行实验，调整输入长度、批量大小和训练周期。此外，鉴于各种研究的结果通常源于超参数优化，我们包括综合参数搜索的结果：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

- **短程预测：多变量数据**

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

- **短程预测：单变量数据**

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

- **消融实验：** 为验证TimeMixer每个组件的有效性，我们在所有18个实验基准上对Past-Decomposable-Mishing和Future-Multipredictor-Mishing 模块中的每种可能的设计进行了详细的消融研究。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

- **模型效率：** 我们将训练阶段的运行内存和时间与最新最先进的模型进行比较，其中TimeMixer在GPU内存和运行时间方面，对于各种系列长度（范围从 192 到 3072）始终表现出良好的效率），此外还具有长期和短期预测任务一致的最先进性能。值得注意的是TimeMixer作为深度模型，在效率方面表现出接近全线性模型的结果。这使得TimeMixer在各种需要高模型效率的场景中大有前途。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**总结**

本文介绍了TimeMixer这一全新的时序预测模型。通过引入可分解的多尺度混合机制，TimeMixer在保证高预测精度的同时，实现了显著的计算效率提升。实验结果表明，TimeMixer在多个公开数据集上的表现全面超越现有基准模型，包括Transformer极其多种变体在内。

TimeMixer的成功不仅为时序预测领域带来了新的思路，也展示了纯MLP结构在复杂任务中的潜力。未来，随着更多优化技术和应用场景的引入，相信TimeMixer将进一步推动时序预测技术的发展，为各行业带来更大的价值。

**文章推荐**

**关注可信AI进展**

**了解AI最新资讯**

继续滑动看下一个

可信AI进展

向上滑动看下一个