---
source_type: web
title: "（2023 AAAI）N-HiTS: Neural Hierarchical Interpolation for Time Series Forecasting"
author:
  - 
  - "[[的泼墨佛给克呢​​github.com/ddz16/TSFpaper]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://zhuanlan.zhihu.com/p/573203887"
published: 
created: 2026-04-06
description: "论文链接：这是Nbeats作者的又一作品 https://arxiv.org/pdf/2201.12886.pdf可以先了解一下NBEATS模型： 的泼墨佛给克呢：N-BEATS: Neural Basis Expansion Analysis For Interpretable Time Series ForecastingKe…"
tags:
  - 
  - "clippings"
---

目录

收起

论文链接：

Key Points

Main Idea

Multi-Rate Data Sampling

Hierarchical Interpolation

## 论文链接：

这是Nbeats作者的又一作品

可以先了解一下 [NBEATS](https://zhida.zhihu.com/search?content_id=215511750&content_type=Article&match_order=1&q=NBEATS&zhida_source=entity) 模型：

[![[assets/attachments/timeseries/v2-2e903642328d00f8e5744a096ffa1d34.png]]](https://zhuanlan.zhihu.com/p/572850227)

## Key Points

### Main Idea

本文集中在长时间预测（预测范围比较长）任务上如何改进NBEATS。下图是论文的Motivation：

![[assets/attachments/timeseries/v2-0adc058f6f1588223d3466250dfcff7e_1440w.jpg]]

（a）可以看出，随着预测长度（Horizon）的增加，NBEATS的速度变慢、参数量变多，而本文提出的 [N-HiTs](https://zhida.zhihu.com/search?content_id=215511750&content_type=Article&match_order=1&q=N-HiTs&zhida_source=entity) 则缓解了这两个问题。（b）可以看出，随着预测长度（Horizon）的增加，NBEATS的误差变大，这也很好理解，要预测很远的未来的话肯定更难预测，但本文提出的N-HiTs则缓解了这个问题。（c）是论文中的思想，即分层次采样预测后插值的思想，用来缓解上述问题的。

由于有上述问题，本文就设计了几种方案，重定义了NBEATS的架构。下面分别介绍这几种方案。N-HiTs的整体架构如下，和NBEATS差不多，stack和block的结构也用的是NBEATS里面的：

![[assets/attachments/timeseries/v2-c53afff25a4824f77df840d61e6504cf_1440w.jpg]]

### Multi-Rate Data Sampling

说白了就是用下采样（时域上的最大池化）将时间序列采样为多种粒度的序列。采样用的池化层大小越大，则得到的序列更加低频/尺度较大；反之，则是更加高频/尺度较小。但是用了采样之后，得到的这些序列相较于原始序列，都变得更加低频/尺度较大了。利用不同kernel size的池化层，就可以得到不同尺度的序列。其实这种方式作为一种预处理的方式，在时间序列分析中是比较常见的。

这样做的好处也很直观了，下采样之后，序列长度变短了，所以复杂度变低了，效率变高了。此外，也减少了模型参数量，避免了过拟合的风险，又保持了原始的感受野。

### Hierarchical Interpolation

其实这个也很简单，和下采样是正好对应的，在预测结果上又做了个上采样。这可以结合N-HiTs的模型架构图来理解，比如在第一个stack，下采样的kernel size大，所以输入序列更短、尺度更大，预测出来的未来序列也更短，要想得到和期望Horizon一样的长度，就做一个上采样，也就是插值（比如线性插值，二次插值），需要插值很多个点。在最后一个stack，下采样的kernel size小，所以序列更长、尺度更小，预测出来的未来序列也更长，就可以少插值一些。 **所以每个stack实际上都是负责不同尺度的预测，最后把不同尺度的预测序列插值到相同粒度（也就是期望预测Horizon的粒度）然后相加即可** 。可以结合模型图左侧来看，第一个stack因为序列短，尺度大，预测后插值结果就很平滑，更低频一些；而下面的stack则尺度越来越小，插值结果更高频一些。然后具体每个stack的kernel size怎么选取呢，用指数减小的方式即可。

## Comments

思路很简单，没啥分析的必要，下采样输入预测之后再上采样输出。和下面这个文章idea有点撞车，好像都投了NIPS但都没中。

编辑于 2023-03-22 13:42・北京[深度学习（Deep Learning）](https://www.zhihu.com/topic/19813032)[时间序列预测](https://www.zhihu.com/topic/25716601)[时间序列分析](https://www.zhihu.com/topic/19712111)[阿里云 ×OpenClaw 三步极速上手](https://click.aliyun.com/m/1000409721/?spu=biz%3D0%26ci%3D3693408%26si%3De8b7bef9-19f7-4430-8a80-f1017c2cc979%26ts%3D1775469780%26zid%3D1629)

[

无需技术背景！小白也能拥有

](https://click.aliyun.com/m/1000409721/?spu=biz%3D0%26ci%3D3693408%26si%3De8b7bef9-19f7-4430-8a80-f1017c2cc979%26ts%3D1775469780%26zid%3D1629)