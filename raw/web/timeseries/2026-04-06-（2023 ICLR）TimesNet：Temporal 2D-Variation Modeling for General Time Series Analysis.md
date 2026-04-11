---
source_type: web
title: "（2023 ICLR）TimesNet：Temporal 2D-Variation Modeling for General Time Series Analysis"
author:
  - 
  - "[[的泼墨佛给克呢​​github.com/ddz16/TSFpaper]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
published: 
created: 2026-04-06
description: "论文链接：TimesNet: Temporal 2D-Variation Modeling for General Time Series...本文中了2023 ICLR，是清华软院龙明盛老师组的文章，一如既往的Solid。本文的作者就是Autoformer的作者，所以本文的很多思想都延…"
tags:
  - 
  - "clippings"
source_url: "https://zhuanlan.zhihu.com/p/604100426"
published_at: null
related_concepts: []
---

## 论文链接：

[![[raw/assets/attachments/timeseries/v2-f379b46dfcd21ef4f1edea0f5ad81a0c_ipico.jpg]]](https://link.zhihu.com/?target=https%3A//openreview.net/forum%3Fid%3Dju_Uqw384Oq)

本文中了2023 ICLR，是清华软院龙明盛老师组的文章，一如既往的Solid。本文的作者就是Autoformer的作者，所以本文的很多思想都延续了Autoformer。Autoformer在知乎有作者团队官方的解析，如下：

[![[raw/assets/attachments/timeseries/v2-28048dd6074ba09a33c1985b5f557e06.jpg]]](https://zhuanlan.zhihu.com/p/385066440)

**不同于Autoformer只集中于时间序列预测，本文提出的TimesNet是一个通用的时间序列神经网络骨干，可处理各种不同的时间序列任务，如最常见的任务：预测、分类、异常检测等等** 。其实几乎所有的时间序列预测模型也可以当做是通用骨干，比如Autoformer， [Informer](https://zhida.zhihu.com/search?content_id=222376207&content_type=Article&match_order=1&q=Informer&zhida_source=entity) ， [FEDformer](https://zhida.zhihu.com/search?content_id=222376207&content_type=Article&match_order=1&q=FEDformer&zhida_source=entity) ， [Preformer](https://zhida.zhihu.com/search?content_id=222376207&content_type=Article&match_order=1&q=Preformer&zhida_source=entity) 这些Transformer-based模型中只采用Encoder就相当于是一个时间序列的特征提取器，区别在于它们捕获时序依赖性的方式不同。比如Autoformer是用Auto-Correlation，Informer中的概率稀疏Attention，FEDformer的频域Attention，Preformer中的Multi-Scale Segment-Correlation。还有那些MLP-based模型比如 [DLinear](https://zhida.zhihu.com/search?content_id=222376207&content_type=Article&match_order=1&q=DLinear&zhida_source=entity) 也可以当做是通用骨干，它是直接采用线性层权重来表示时序依赖性。

## Key Points

### 1D变2D

这是本文的核心。大部分现有方法都是作用于时间序列的时间维度，捕获时序依赖性。实际上，现实时间序列一般都有多种模式，比如不同的周期，各种趋势，这些模式混杂在一起。如果直接对原始序列的时间维度来建模，真正的时序关系很可能隐藏在这些混杂的模式中，无法被捕获。考虑到： **现实世界的时间序列通常具有多周期性，比如每天周期、每周周期、每月周期；而且，每个周期内部的时间点是有依赖关系的（比如今天1点和2点），不同的相邻周期内的时间点也是有依赖关系的（比如今天1点和明天1点），作者提出将1D的时间维度reshape成2D的，** 示意图如下。下图左侧的时间序列具有三个比较显著的周期性（Period 1、Period 2、Period 3），将其reshape成三种不同的2D-variations，2D-variations的每一列包含一个时间段（周期）内的时间点，每一行包含不同时间段（周期）内同一阶段的时间点 **。变成2D-variations之后，就可以采用2D卷积等方式来同时捕获时间段内部依赖和相邻时间段依赖** 。

![[raw/assets/attachments/timeseries/v2-f4c3befcbf9d3acdf2fbeb91af6e29d5_1440w.jpg]]

那么怎么确定时间序列中的周期性呢？采用 [傅里叶变换](https://zhida.zhihu.com/search?content_id=222376207&content_type=Article&match_order=1&q=%E5%82%85%E9%87%8C%E5%8F%B6%E5%8F%98%E6%8D%A2&zhida_source=entity) 。给时间序列做傅里叶变换后，主要的周期会呈现对应的高幅值的频率分量。设定超参数k，然后只取top k个最大的幅值对应的频率分量，即可得到top k个主要的周期，这和Autoformer中的处理类似。具体操作如下图，左侧是确定top k个周期，在此只画了三个，然后将1D的时间序列reshape成3种不同的2D-variations（不能整除的可以用padding），对这三种2D-variations用2D卷积进行处理之后再聚合结果即可。

![[raw/assets/attachments/timeseries/v2-035520ad6c4a80488a9f63bdaf38fff2_1440w.jpg]]

一般来说，对于一个多变量时间序列 ，其中 是变量维数， 是长度，虽然它是一个2D tensor，但作者将其称为是1D的，这是因为在时间维度上来看是1D的。可以通过上图中这种方式，先算出主要周期和频率，再根据主要周期和频率将时间维度上是1D的时间序列reshape成k个2D-variations。注意，对于 个变量，最终算得的主要周期是所有变量的主要周期的平均，这也说明输入的多变量时间序列中包含的不同单变量时间序列的周期模式需要相似。最后，第i个2D-variations即是 ，其中 和 分别表示第i个周期和频率，它们的关系如下式：

![[raw/assets/attachments/timeseries/v2-9680e4a8e5f87a8a44728c5a5cbff1eb_1440w.jpg]]

### TimesBlock

得到k个2D-variations之后该怎么处理呢？本文提出了TimesBlock，每层TimesBlock又分为两步。 **首先是要先对这些2D-variations分别用2D卷积（可以是ResNet、ConvNeXt等）或者其他的视觉骨干网络（比如Swin，Vit）处理；其次将k个处理后的结果再聚合起来。**

对于第一步，本文采用了一种参数高效的Inception block。Inception block是GoogleNet中的模块，包含多个尺度的2D卷积核。如下图左侧蓝色区域，处理k个2D-variations的Inception block是参数共享的。因此，模型整体的参数量不会随着超参数k的增大而增大，因此本文将其称为参数高效的Inception block（Parameter-efficient Inception block）。

![[raw/assets/attachments/timeseries/v2-778f08ed6121523b0ed8a43e3d383bfd_1440w.jpg]]

对于第二步，在处理完k个2D-variations之后，需要将其展平回1D-variations，并截断到原始长度 （这对应于前面不能整除时使用padding的情况，相当于把多余的padding给去掉）。总之，得到k个变换回去的1D-variations之后，该如何聚合这k个结果呢？如上图右侧所示，也是延续Autoformer的思路，根据傅里叶变换后频率周期对应的赋值大小来加权聚合，幅值大的证明该频率周期的分量越显著也越重要，给它较大的聚合权重，幅值小的则相反。直接用softmax归一化这些幅值 ，然后将归一化后幅值作为加权权重来聚合上面得到的k个1D-variations即可：

![[raw/assets/attachments/timeseries/v2-5dfea4dfed77491f91350660ce85c811_1440w.jpg]]

### 实验结果

作者在五种时间序列任务上做了实验，充分对比了一些其他的时间序列骨干。五边形战士：

![[raw/assets/attachments/timeseries/v2-5f119cc7bb1d06ba61151e6d766abf22_1440w.jpg]]

作者也用了不同的视觉骨干来处理2D-variations：

![[raw/assets/attachments/timeseries/v2-4e10a31806052dd69cb69720caf7ee39_1440w.jpg]]

在长时间序列预测上的效果：

![[raw/assets/attachments/timeseries/v2-10aeab02eb26fd7380296d4849aa75d1_1440w.jpg]]

## Comments

文章真的写的很好，idea很清晰合理，实验很充分效果也很不错，在长时间序列预测上超越了很多很先进的Transformer-based模型和MLP-based模型。有些新中2023 ICLR的论文在长时间序列预测上的效果非常差，甚至是一些时序预测任务上中了oral的文章，写的花里胡哨，创新性也没有特别显著，常看这个领域的基本看一遍那些文章就知道大概啥水平，效果也不能打，根本不实用。

发布于 2023-02-07 10:36・北京[ICLR 2023](https://www.zhihu.com/topic/26350446)[时间序列分析](https://www.zhihu.com/topic/19712111)[卷积神经网络（CNN）](https://www.zhihu.com/topic/20043586)[靠自己写了半年，论文2区总不过，找辅导真的有用吗？靠谱吗？](https://zhuanlan.zhihu.com/p/1910344894683289061)

[

这个问题我曾经想过无数次。 我一开始也很抗拒找人辅导论文，总觉得“自己学术的事，自己搞才硬气”，但事实是我靠自己写了半年，投了三家都被拒，一度以为自己没救了。 我是工科背景，...

](https://zhuanlan.zhihu.com/p/1910344894683289061)