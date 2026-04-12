---
source_type: web
title: "（2024 ICLR）TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting"
author:
  - 
  - "[[的泼墨佛给克呢​​github.com/ddz16/TSFpaper]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
published: 
created: 2026-04-06
description: "清华和ant group在今年发表在ICLR上的一篇文章，也是基于MLP来做时间序列预测任务的。 论文链接：https://openreview.net/pdf?id=7oLshfEIC2代码链接：https://github.com/kwuking/TimeMixerKey Point整个文章的id…"
tags:
  - 
  - "clippings"
source_url: "https://zhuanlan.zhihu.com/p/686772622"
published_at: null
related_concepts: []
---

清华和ant group在今年发表在ICLR上的一篇文章，也是基于 [MLP](https://zhida.zhihu.com/search?content_id=240746147&content_type=Article&match_order=1&q=MLP&zhida_source=entity) 来做时间序列预测任务的。

## 论文链接：

## 代码链接：

## Key Point

整个文章的idea是，对一个原始的时间序列，用不同的频率来采样它，得到的新的序列所蕴含的时域信息是不同的。比如用电量序列，如果以每小时采样，那它就呈现以天为周期的形式；如果以每天采样，那它就可能呈现以周末、节假日相关的波动。因此，如何利用好不同尺度的序列（即用不同频率采样得到的序列）之间的关系，对时序预测任务很重要。这个idea有点类似于 [NHits](https://zhida.zhihu.com/search?content_id=240746147&content_type=Article&match_order=1&q=NHits&zhida_source=entity) 和Scaleformer，这两篇我在之前的知乎文章中有介绍：

[![[raw/assets/attachments/timeseries/v2-bd2c5261acdd3bab27dcb899b713e93e.png]]](https://zhuanlan.zhihu.com/p/573203887)

[![[raw/assets/attachments/timeseries/v2-ed8e30d16217e4434a7fe53e7d3d7085.png]]](https://zhuanlan.zhihu.com/p/535556231)

但不同的是，NHits和Scaleformer都是用单独的block来建模每个尺度序列，先用第一个block处理最粗粒度（采样频率低）的序列，然后进行插值得到更细粒度的序列，输入到下一个block，依此类推，得到最终最细粒度的预测。而本文是 **每个block内部都会处理所有尺度序列（倒是和 [Pyraformer](https://zhida.zhihu.com/search?content_id=240746147&content_type=Article&match_order=1&q=Pyraformer&zhida_source=entity) 中的金字塔attention比较像）** ，此外，还引入了 **序列分解** 的思想和 **尺度间信息流动** 的新方式。

### Architecture

本文提出的TimeMixer的架构如下图

![[raw/assets/attachments/timeseries/v2-0b6cd99d2cd5d9017fc3339ef8eeb4ab_1440w.jpg]]

用简单的话来概述上图就是

1. **Multiscale Time Series** ：首先对输入序列进行不同程序的池化来下采样得到不同尺度的序列。
2. **Past Decomposable Mixing** ：然后将每个尺度的序列都分解为趋势项（trend）和周期项（seasonal）（这里分解方法采用的是 [Autoformer](https://zhida.zhihu.com/search?content_id=240746147&content_type=Article&match_order=1&q=Autoformer&zhida_source=entity) 中的方式，用一个大window size的滑动平均即可）。为了进行尺度间的交互，将每个尺度序列的seasonal项按照从下到上（bottom-up）的方式进行信息融合，将每个尺度序列的trend项按照从上到下（top-down）的方式进行信息融合。
3. **Future Multipredictor Mixing** ：最后，将最后一个block输出的不同尺度的序列都用来预测，把所有尺度的预测结果加起来得到最终预测结果。

### Past-Decomposable-Mixing

尺度间交互是怎么做的呢？作者用两种相反的流动方式来分别处理 **不同尺度的趋势项** 和 **不同尺度的周期项，** 如下图 **：**

![[raw/assets/attachments/timeseries/v2-7b48025c901fd765f964fac3e4fbb0fd_1440w.jpg]]

- 对于 **周期项** ：如上图左侧，下面细粒度的seasonal序列用一个两层的MLP映射到和上面粗粒度的seasonal序列尺度对齐，然后相加即可得到融合后的结果，然后依此类推，把所有尺度的seasonal全部融合一遍。可是为什么要用bottom-up的流动方式呢？作者的原文如下：In seasonality analysis, larger periods can be seen as the aggregation of smaller periods, such as the weekly period of traffic flow formed by seven daily changes, addressing the importance of detailed information in predicting future seasonal variation。我的理解是，细粒度周期本身就包含了粗粒度周期，比如一个每小时采样的序列，周期严格是24，那么用每2小时、每半天、每一天的频率来采样该序列，则周期可以直接推算出来，分别是12，2，1。所以细粒度周期包含的信息多一些，用它来指导粗粒度周期会好一些。
- 对于 **趋势项** ：如上图右侧，其实是和周期项一样的处理方式，唯一的区别是方向是反的，是粗粒度逐渐映射到细粒度的。为什么用top-down的流动方式呢？作者的原文如下：Contrary to seasonal parts, for trend items, the detailed variations can introduce noise in capturing macroscopic trend. Note that the upper coarse scale time series can easily provide clear macro information than the lower level. Therefore, we adopt a top-down mixing method to utilize the macro knowledge from coarser scales to guide the trend modeling of finer scales。我的理解是，越是细粒度，趋势就包含越多的噪声和意想不到的变化，因此需要宏观趋势（粗粒度）来指导微观趋势（细粒度）。

注意，经过上述操作后，每个block得到的输出仍然是多个尺度序列的周期项和趋势项，只不过每个尺度的周期项和趋势项已经融合了其他尺度的信息。然后，把每个尺度的周期项和趋势项相加（趋势周期合并），即可得到每个尺度的未分解序列。再进行一个FFN变换，即可得到下一个block的输入。 **所以，每个block的输入是多个尺度的序列，依次进行趋势周期分解、尺度间交互、趋势周期合并，FFN，输出新的多个尺度的序列** 。

### Future-Multipredictor-Mixing

那么对于最后一个block，它的输出也是多个尺度的序列，所以直接用多个predictor，对每个尺度的序列都映射到和预测范围的长度一致，然后所有尺度的预测结果相加即可得到最终的预测。每个predictor其实就是一个Linear，如下图所示，和Dlinear论文中一样：

![[raw/assets/attachments/timeseries/v2-ec40ab722bf748350d0cce844bdf965c_1440w.jpg]]

## 实验

作者在多变量、单变量、时空预测上均进行了实验，发现TimeMixer均能达到SOTA，并且效率和 [DLinear](https://zhida.zhihu.com/search?content_id=240746147&content_type=Article&match_order=1&q=DLinear&zhida_source=entity) 差不多。

多变量时序预测的结果：

![[raw/assets/attachments/timeseries/v2-0134aaa6260e982d1c9ccdcf105c5c56_1440w.jpg]]

在PEMS几个时空数据集上预测的结果：

![[raw/assets/attachments/timeseries/v2-a90d32c0a2deb4255f5aade925b710d8_1440w.jpg]]

单变量时序预测的结果：

![[raw/assets/attachments/timeseries/v2-a45ee5fc94c92fd63ad2df9e652e091a_1440w.jpg]]

预测效率和DLinear差不多，训练显存占用很小，速度也是非常快的了：

![[raw/assets/attachments/timeseries/v2-a2d63e1a817a064d3067fbecd45754e9_1440w.jpg]]

关于序列分解和尺度间信息融合方式的消融实验，作者发现采用序列分解，然后对分解后的trend和seasonal分别做信息融合效果好，而且，对trend采用top-down的流动方式，对seasonal采用bottom-up的流动方式，效果最好：

![[raw/assets/attachments/timeseries/v2-a1e935187353cbb5a78a8a8a21743dc3_1440w.jpg]]

## Comments

把序列预测里面几个比较有效的思想（多尺度预测，序列分解，尺度间交互）都融到一个模型中了，通过实验结果也能看出来有一定的可解释性。整体采用了纯mlp的架构使得效率很高，接近DLinear。实验很充分，在长短程预测上对比了从多元时序，时空时序以及单元时序的各种场景，并且在统一参数和超参搜索等各种设置下都进行了对比，都基本是SOTA，消融实验也很充分。

还没有人送礼物，鼓励一下作者吧

编辑于 2024-03-13 16:16・浙江[时间序列预测](https://www.zhihu.com/topic/25716601)[深度学习（Deep Learning）](https://www.zhihu.com/topic/19813032)[ICLR2024](https://www.zhihu.com/topic/28591438)[告别加班！用Wyn BI模板复用，5分钟搞定原来1天的活，新手秒变看板大神](https://zhuanlan.zhihu.com/p/1979862684024463789)

[

大家有没有经历过这种绝望？下午快下班时，老板拍拍你说：“小王，明早我要看到一个销售数据分析看板，要直观，要专业！”。 你看着空白的看板工具界面，脑海里已经开始盘算：连接数据源...

](https://zhuanlan.zhihu.com/p/1979862684024463789)