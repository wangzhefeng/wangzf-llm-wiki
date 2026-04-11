---
source_type: web
title: "TimeMixer++: A General Time Series Pattern Machine for Universal Predictive Analysis"
author:
  - 
  - "[[的泼墨佛给克呢​​github.com/ddz16/TSFpaper]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
published: 
created: 2026-04-06
description: "本文介绍一篇ICLR 2025的高分时间序列分析文章，在openreview上获得了均分8的高分。作者团队就是ICLR 2024中稿文章TimeMixer的原班作者团队，本文也是TimeMixer的改进版本，不仅扩展了任务，性能效果也进一步升级…"
tags:
  - 
  - "clippings"
source_url: "https://zhuanlan.zhihu.com/p/12926871013"
published_at: null
related_concepts: []
---

本文介绍一篇ICLR 2025的高分时间序列分析文章，在openreview上获得了均分8的高分。作者团队就是ICLR 2024中稿文章TimeMixer的原班作者团队，本文也是TimeMixer的改进版本，不仅扩展了任务，性能效果也进一步升级，在所有时序任务上都取得了SOTA的性能，如下图：

![[raw/assets/attachments/timeseries/v2-828b98c7e0ed780ddb1ac6bdcb73fada_1440w.jpg]]

为了读懂这篇文章，我推荐的阅读顺序为TimesNet->TimeMixer和PDF->TimeMixer++，而且恰巧这几篇文章我都有解读过，链接如下：

## 论文链接：

## 代码链接：

## Key Point

本文的目标在于设计一个时序数据通用的骨干网络（论文里称之为time series pattern machine，简称TSPM），可以很有效地进行时序特征的提取，提取好的特征可以用于各种时序任务。所以，关键就是怎么有效地进行时序数据的特征提取？一般来说，时序中经常关注的操作有 **周期趋势分解** 、 **多尺度** 、 **频域分析、多通道相关性** ，这些操作对时序数据来说都至关重要，几乎所有论文都会涉及其中的一类操作或几类。而本文则是四类操作全部都有涉及。

由于TimeMixer++是TimeMixer的改进版本，TimeMixer是做时序预测任务的，TimeMixer++是做通用时序任务的，不过也大差不差了，不同任务用不同head就行。可以先回顾下TimeMixer的结构，然后再看看TimeMixer++在它的基础上做了哪些改进。

### TimeMixer

![[raw/assets/attachments/timeseries/v2-6bbf2d74f64f70a102bf2e2a9d679309_1440w.jpg]]

TimeMixer的结构如上图，用简单的话来概述就是：

1. **Multiscale Time Series** ：首先对输入序列进行不同程序的池化来下采样得到不同尺度的序列。
2. **Past Decomposable Mixing** ：然后将每个尺度的序列都分解为趋势项（trend）和周期项（seasonal）（这里分解方法采用的是 [Autoformer](https://zhida.zhihu.com/search?content_id=251608612&content_type=Article&match_order=1&q=Autoformer&zhida_source=entity) 中的方式，用一个大window size的滑动平均即可）。为了进行尺度间的交互，将每个尺度序列的seasonal项按照从下到上（bottom-up）的方式进行信息融合，将每个尺度序列的trend项按照从上到下（top-down）的方式进行信息融合。这里不同尺度之间信息融合的方式就是直接用 [MLP](https://zhida.zhihu.com/search?content_id=251608612&content_type=Article&match_order=1&q=MLP&zhida_source=entity) 在时间上对齐到相同的尺度然后相加。
3. **Future Multipredictor Mixing** ：最后，将最后一个block输出的不同尺度的序列都用来预测，把所有尺度的预测结果加起来得到最终预测结果。

### TimeMixer++

![[raw/assets/attachments/timeseries/v2-45221b17790a07ab6c79ec0e99ed298b_1440w.jpg]]

TimeMixer++的结构如上图，最核心的改动其实是 **周期趋势分解** 那部分（也就是TimeMixer中的Past Decomposable Mixing模块），从Autoformer的滑动窗口法进化到了TimesNet的二维表示法。下面我将从上图中的（a）（b）（c）（d）（e）结构来依次介绍。

- （a）和TimeMixer一样，还是下采样得到多尺度输入序列，这里采用stride为2的卷积来进行下采样。值得注意的是，这里对最粗粒度的序列（也就是下采样最狠的序列），在通道间进行了一个自注意力操作。这样，TimeMixer++模型相比TimeMixer就增加了 **多通道相关性建模** 这一步 **。**
- （b）这里采用TimesNet的时序二维表示法，将所有尺度的序列都按照 [FFT变换](https://zhida.zhihu.com/search?content_id=251608612&content_type=Article&match_order=1&q=FFT%E5%8F%98%E6%8D%A2&zhida_source=entity) 后的周期分量reshape为二维表示。具体这里二维表示相较于一维序列的优势，在我关于TimesNet的解读中已经详细说明了，在此不再赘述。总之，每个尺度的一维序列都被reshape为了二维的。
- （c）由于二维表示法中，每一行和每一列代表的含义不同。 **每一列代表同一周期内部的一段序列（可以视为周期），每一行代表不同周期内相位相同的那些时间点（可以视为趋势）** ，相关的分析可见我对TimesNet和PDF的解读文章。所以，可以使用 [轴向注意力](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1912.12180) 来分别建模周期和趋势。也就是说，对行级别采用attention得到趋势分量，对列级别采用attention得到周期分量。
- （d）由于这里是二维表示了，所以不能像TimeMixer中采用MLP直接对齐时间尺度来进行不同尺度之间的融合。因此，可采用图像领域中常用的上下采样操作（下采样用2D卷积，上采样用2D transposed卷积）来对齐不同尺度。这里对于趋势和周期分量的不同尺度融合路径也是和TimeMixer一样，一个按照从上到下（top-down）的方式进行信息融合、另一个按照从下到上（bottom-up）的方式。
- （e）最后，把不同分辨率的表征进行加权求和即得到最终每个尺度的表示（注意这里分辨率和尺度不是一个东西。分辨率是指在（b）步骤进行reshape得到二维表征时，用FFT来获取多个主要周期，根据这些主要周期来分别reshape得到多个二维表示，就是不同分辨率了；而尺度则是在下采样时的时域上的不同尺度的序列）。这里加权的权重则是根据FFT时频域中每个周期的幅值来进行softmax得到的。

最后，Output Projection则和TimeMixer里的Future Multipredictor Mixing思路差不多，就是多个尺度用多个head然后再取平均。

## Comments

非常全面的论文了，周期趋势分解、多尺度、频域分析、多通道相关性，把这些时序相关论文的操作全部揉进了模型里。而且实验部分可以看到，TimeMixer++相较于TimeMixer和其他时序模型，在所有任务上都有不错的提升。论文的实验和消融部分做了很多工作，非常充分，详情可见原论文。

编辑于 2024-12-16 17:50・浙江[时间序列预测](https://www.zhihu.com/topic/25716601)[ICLR](https://www.zhihu.com/topic/21503444)[时间序列分析](https://www.zhihu.com/topic/19712111)[用它，免费搭建动态查询系统！](https://zhuanlan.zhihu.com/p/53423212)

[

有用户在后台私信小编，在Excel中如何实现动态查询管理。比如有两个表格，在表A中选择员工姓名，则可查看表B中该员...

](https://zhuanlan.zhihu.com/p/53423212)