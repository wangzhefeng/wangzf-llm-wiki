---
author:
- null
- '[[Yong Liu]]'
- '[[Tengge Hu]]'
- '[[Haoran Zhang]]'
- '[[Haixu Wu]]'
- '[[Shiyu Wang]]'
- '[[Lintao Ma]]'
- '[[Mingsheng Long]]'
created: 2026-04-06
created_at: 2026-04-06
description: iTransformer通过反转其组件操作的维度，重新定位了用于多元时间序列预测的标准Transformer架构。它将每个变量的完整时间序列视为一个标记，并在变量之间应用自注意力，从而在多个数据集上实现了最先进的性能，同时有效利用了长回溯窗口。
source_type: web
status: inbox
tags:
- null
- clippings
title: iTransformer：倒置Transformer在时间序列预测中卓有成效
source_url: https://www.alphaxiv.org/zh/overview/2310.06625v4
published_at: 2024-03-14
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

## 概述

iTransformer 对 Transformer 架构如何应用于多元时间序列预测进行了根本性的重新构想。这项工作没有修改 Transformer 的核心组件，而是提出反转这些组件操作的维度，将单个时间序列变量视为 token，而不是时间点。

![[img-0.jpeg|Performance comparison]] *图1：显示不同数据集上归一化MSE性能的雷达图，展示了iTransformer相对于现有方法（包括Transformer、PatchTST、TimesNet、DLinear和FEDformer）的持续优越性。*

## 问题陈述与动机

传统的基于Transformer的预测器在应用于多元时间序列数据时面临几个基本挑战。传统方法将每个时间戳视为一个 token，将来自同一时间点的多个变量嵌入到单个时间表示中。这种设计选择导致了几个问题：

**低效的表示学习** ：当具有不同物理意义的多个变量融合到一个时间 token 中时，所产生的表示会失去每个变量的个体特征。这种“变量混合表示”使得难以捕获不同时间序列之间有意义的关系。

**可扩展性限制** ：自注意力相对于序列长度的二次复杂度（ $O(T^2)$ ）使得利用更长的历史上下文在计算上难以承受，这与更多历史数据应提高预测准确性的统计直觉相悖。

**有限的可解释性** ：在数值时间点上计算的注意力图缺乏语义意义，使得难以理解模型学习到了关于变量关系和时间依赖性的哪些内容。

## 方法论：倒置架构

iTransformer 的核心创新在于其维度倒置策略。该架构完全颠覆了传统范式，不再是在时间维度上应用注意力，在变量维度上应用前馈网络。

![[img-1.jpeg|Architectural comparison]] *图2：传统Transformer视图（上）与iTransformer视图（下）的比较，展示了倒置架构如何将单个变量的整个时间序列视为 token。*

### 变量分词

对于一个多元时间序列 $X \in \mathbb{R}^{T \times N}$ （其中 $T$ 表示时间步， $N$ 表示变量），iTransformer 首先将输入转置为 $X \in \mathbb{R}^{N \times T}$ 。然后，每一行（代表单个变量的完整时间序列）被嵌入为一个变量 token：

$$
h_n = \text{MLP}(X_{:,n})
$$

其中 $h_n \in \mathbb{R}^D$ 表示第 $n$ 个变量完整时间序列的嵌入表示。

### 重新利用的组件

**用于多元相关性的自注意力** ：自注意力机制作用于 $N$ 个变量 token，而不是 $T$ 个时间 token。这使得模型能够捕获不同变量之间的相关性：

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

其中 $Q$ 、 $K$ 和 $V$ 均源自变量 token 表示，使注意力复杂度变为 $O(N^2)$ 而非 $O(T^2)$ 。

**用于序列表示的前馈网络** ：FFN 独立处理每个变量 token，学习提取单个时间序列中的复杂时间模式：

$$
\text{FFN}(h_n) = W_2 \sigma(W_1 h_n + b_1) + b_2
$$

这种设计利用了 FFN 学习非线性变换的能力，以捕获每个变量历史中复杂的时序动态。

![[img-3.jpeg|详细架构]] *图3：详细的iTransformer架构，展示了(a)嵌入过程，(b)多元注意力机制，(c)前馈处理，以及(d)归一化策略。*

## 实验结果与分析

实验评估表明iTransformer在多个具有挑战性的基准测试中表现出有效性。该模型在七个真实世界数据集中持续取得最先进的性能，特别是在高维时间序列上表现出色。

### 性能比较

![[img-4.jpeg|泛化结果]] *图4：iTransformer与通道独立（CI）策略在不同数据集上的泛化性能比较，显示在使用仅20%可用变量时表现出卓越性能。*

结果表明，iTransformer的倒置框架持续改进了各种Transformer变体：

- 对于Vanilla Transformer，平均MSE降低了38.9%
- 对于Reformer，提升了36.1%
- 对于Informer，增强了28.5%
- 对于Flowformer，提升了16.8%

### 历史数据的有效利用

![[img-5.jpeg|回溯窗口分析]] *图5：不同回溯窗口长度的性能比较，展示了iTransformer有效利用更长历史上下文的能力，而其他方法往往性能下降。*

与传统基于Transformer的预测器在较长回溯窗口下表现不佳不同，iTransformer随着更多历史数据的可用性显示出改进的性能。这验证了使用MLP处理单个变量内时间信息的设计选择。

### 可解释性分析

倒置架构通过有意义的注意力可视化提供了增强的可解释性。注意力图揭示了模型如何捕获多元相关性，其中浅层关注输入相关性，而深层则与未来关系对齐。

![[img-6.jpeg|注意力分析]] *图6：预测性能（MSE）与表示质量（CKA相似性）之间的关系，以及显示不同层多元相关性的注意力分数可视化。*

## 意义与影响

### 理论贡献

iTransformer挑战了Transformer本质上不适合时间序列预测的普遍假设。通过证明问题不在于Transformer组件本身，而在于它们的传统应用方式，这项工作为时间数据架构设计提供了新的视角。

### 实际影响

**可扩展性** ： $O(N^2)$ 的注意力复杂度使得该方法特别适用于变量数量可控但时间序列较长的场景——这在许多实际应用中很常见。

**泛化能力** ：该模型处理不同数量输入变量的能力为构建能够在不同时间序列领域和维度之间泛化的基础模型开辟了可能性。

**效率** ：灵活的架构允许高效的训练策略，例如每批次随机抽样变量子集，显著减少了高维数据集的内存需求。

### 未来方向

维度倒置的成功预示了几个有前景的研究方向：

1. **增强嵌入** ：在变量令牌创建过程中，结合更复杂的时序嵌入（例如，卷积或循环组件）。
2. **跨领域应用** ：探索倒置框架在预测之外的不同时间序列领域（如异常检测和分类）中的表现。
3. **基础模型开发** ：利用其泛化能力，构建用于时间序列分析的大规模预训练模型。

iTransformer 代表了时间序列 Transformer 架构思维的一次范式转变，它表明有时最有效的创新来自于重新审视基本假设，而不是增加复杂性。它对时间序列预测中长期存在的问题提供了优雅的解决方案，结合了强大的实证结果和增强的可解释性，使其成为该领域的重要贡献。

[注意力就是你所需要的一切](https://alphaxiv.org/abs/1706.03762)

这是首次提出Transformer架构的奠基性论文。iTransformer模型直接使用了原始Transformer的固有组件，例如自注意力机制和前馈网络，但将其应用于时间序列数据的倒置维度，因此这项引用具有根本重要性。

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. NeurIPS, 2017.

[Transformer 在时间序列预测中有效吗？](https://alphaxiv.org/abs/2205.13504)

这篇论文是iTransformer的主要启发，因为它通过展示简单的线性模型可以超越复杂的Transformer架构，直接质疑了它们的有效性。iTransformer的作者引用了这项工作，将其研究定位为一种回应，旨在证明当Transformer架构被正确地应用于时间序列数据时，它们确实有效。

Ailing Zeng, Muxi Chen, Lei Zhang, and Qiang Xu. Are transformers effective for time series forecasting? AAAI, 2023.

[时间序列，64个词足矣——基于Transformer的长期预测](https://alphaxiv.org/abs/2211.14730)

本文介绍了PatchTST，这是一种将时间序列分块标记化的先进模型。iTransformer的作者将他们基于变量的标记化描述为“分块的极端情况”，从而建立了直接的概念联系。PatchTST在整个实验中也被用作一个关键的高性能基线模型，突出了其作为比较基准的重要性。

Yuqi Nie, Nam H Nguyen, Phanwadee Sinthong, and Jayant Kalagnanam. A time series is worth 64 words: Long-term forecasting with transformers. ICLR, 2023.

Autoformer：基于自相关的分解Transformer用于长期时间序列预测

Autoformer是一个有影响力的基于Transformer的模型，代表了时间序列预测的传统方法，而iTransformer对其提出了批评。它在时间标记上应用了注意力机制，iTransformer认为这种范式并非最优。本论文经常被用作基线，以证明所提出的倒置架构的优越性。

Haixu Wu, Jiehui Xu, Jianmin Wang, and Mingsheng Long. Autoformer: Decomposition transformers with Auto-Correlation for long-term series forecasting. NeurIPS, 2021.

Crossformer: 利用跨维度依赖的Transformer用于多元时间序列预测

Crossformer 被引作一个代表性模型，它通过修改 Transformer 架构及其组件，试图同时捕捉跨时间和跨变量的依赖关系。iTransformer 的作者将他们使用原生组件在倒置维度上的方法，与 Crossformer 的方法进行对比，使其成为架构设计选择的一个关键比较点。

Yunhao Zhang and Junchi Yan. Crossformer: Transformer utilizing cross-dimension dependency for multivariate time series forecasting. ICLR, 2023.