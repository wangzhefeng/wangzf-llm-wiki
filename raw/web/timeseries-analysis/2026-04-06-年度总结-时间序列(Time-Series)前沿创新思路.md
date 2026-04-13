---
source_type: web
title: "年度总结 | 时间序列(Time Series)前沿创新思路"
author: 
created_at: 2026-04-06
status: inbox
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
source_url: "https://mp.weixin.qq.com/s/KlwV1o4zO4gKNa-8YxccUw"
published_at: null
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

*2026年1月27日 08:31*

本文站在审稿人视角，系统梳理了时间序列领域近年的关键研究成果，并按创新类型与研究层级，将其分为了四个大类：模型演进、范式创新、高级分析、无监督学习。

这四个创新大类顺应了时间序列从追精度走向强泛化、可解释、少数据依赖的发展趋势，基本上覆盖了当前主流的时间序列创新方向，属于顶会和一区期刊的核心战场。

比如热门的时序+预训练LLM等，都包含在内。目前我已梳理好了243篇前沿成果，顶会顶刊多，且附有相应源码。如果你想发论文，那我建议拿一份当做参考，它可以帮助你快速定位创新点、避免低级拼模型。

![[Image 63.webp|图片]]

**扫码添加小享，** ****回复“时序大合集**** ****”****

免费获取 **全部论文+开源代码**

**![[Image 64.webp|图片]]**

## 核心技术增强与模型演进

这类研究关注的是模型架构本身的创新与改进，是当前论文产出的主流。

热门思路比如Transformer/KAN/Mamba + 时序、频域 + 时序（大类范畴）、LSTM + 时序异常检测（侧重于识别非常规模式）。

#### CT-PatchTST: Channel-Time Patch Time-Series Transformer for Long-Term Renewable Energy Forecasting

**方法：** 论文提出CT-PatchTST模型，基于Transformer架构，通过融合通道注意力与时间注意力的双注意力机制，对多变量时间序列进行处理，同时捕捉通道间相关性与时间依赖性，实现可再生能源的长期高精度预测。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**创新点：**

- 新增通道注意力机制，与时间注意力形成双注意力架构，捕捉多变量时间序列的通道间关联。
- 结合可逆实例归一化、补丁划分与投影预处理，缓解分布偏移，提升特征捕捉能力。
- 针对可再生能源场景优化，整合通道与时间信息，精准建模数据非线性动态模式。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

## 学习范式与框架创新

这类研究关注 “如何更好地训练和应用模型”，是提升性能和应用范围的关键。

热门思路比如时序 + 预训练大模型、迁移学习 + 时序预测、小样本时间序列预测。

#### Chronos: Learning the Language of Time Series

**方法：** 论文提出Chronos框架，通过缩放与量化将时间序列值token化为固定词汇表，基于T5等预训练大模型架构，结合TSMixup数据增强与KernelSynth合成数据训练，实现概率性时间序列预测，在域内和零样本场景均表现优异。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**创新点：**

- 将时间序列通过缩放和量化转化为离散 tokens，直接适配预训练大模型，无需专门修改模型架构。
- 采用 TSMixup 数据增强和 KernelSynth 合成数据，丰富训练数据多样性，提升模型泛化能力。
- 基于预训练大模型构建通用时间序列预测框架，支持域内和零样本预测，还能通过微调进一步优化性能。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**扫码添加小享，** ****回复“时序大合集**** ****”****

免费获取 **全部论文+开源代码**

**![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)**

## 方法论与高级分析

这类研究更偏重理解数据背后的机理和关系，能显著提升论文的理论深度。

比如做可解释性与因果分析，这在金融、医疗、决策科学等领域比较吃香，时序可解释性、时序因果推断都是不错的思路。

#### Optimal Information Retention for Time-Series Explanations

**方法：** 论文提出基于最优信息保留原理的ORTE框架，通过学习二进制掩码过滤冗余信息、对比学习平衡解释完整性与低冗余性、分布对齐保证解释保真度，解决时间序列模型解释中冗余和不完整问题，提升可解释性准确性。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**创新点：**

- 提出最优信息保留原理，从信息论角度明确时间序列解释需满足保真、低冗余、高完整三大准则。
- 设计ORTE框架，通过自适应掩码生成器和改进的直通估计器，精准过滤时间序列中的冗余信息。
- 结合对比学习构建正负样本对，平衡解释的冗余性与完整性，同时对齐黑盒模型预测分布保证解释可信度。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

## 无监督与数据挖掘

这类研究关注从数据本身发现结构，不依赖于预测标签。

比如做无监督聚类，搞应用方面：客户行为分群、故障模式归纳、运动模式识别等。可以考虑时间序列聚类。

#### DUET:DualClustering Enhanced Multivariate Time Series Forecasting

**方法：** 论文提出DUET框架，通过时间维度聚类模块（TCM）将时间序列按分布聚类并适配专属模式提取器，结合频域度量学习与稀疏化的通道软聚类模块（CCM），双维度聚类协同提升多元时间序列预测性能。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**创新点：**

- 通过时间聚类模块将时间序列按分布聚类，为不同聚类配置专属提取器，捕捉异质时间模式。
- 提出通道软聚类策略，在频域学习通道间相关性并生成掩码矩阵，灵活建模通道关联。
- 融合时间聚类与通道聚类的双聚类框架，协同解决时间分布偏移和通道关联复杂问题。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**扫码添加小享，** ****回复“时序大合集**** ****”****

免费获取 **全部论文+开源代码**

**![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)**

继续滑动看下一个

时序人

向上滑动看下一个