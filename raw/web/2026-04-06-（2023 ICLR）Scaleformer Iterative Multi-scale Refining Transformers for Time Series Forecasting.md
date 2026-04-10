---
source_type: web
title: "（2023 ICLR）Scaleformer: Iterative Multi-scale Refining Transformers for Time Series Forecasting"
author:
  - 
  - "[[的泼墨佛给克呢​​github.com/ddz16/TSFpaper]]"
created_at: 2026-04-06
topics:
  - 大语言模型
status: inbox
source: "https://zhuanlan.zhihu.com/p/535556231"
published: 
created: 2026-04-06
description: "论文链接https://arxiv.org/pdf/2206.04038.pdf代码链接https://github.com/BorealisAI/scaleformerKey PointsMulti-scale Framework将时间序列利用不同采样率进行采样（平均池化），得到不同尺度。低级尺度具有更…"
tags:
  - 
  - "clippings"
---

目录

收起

论文链接

代码链接

Key Points

Multi-scale Framework

Cross-scale Normalization

Loss Function

## 论文链接

## 代码链接

## Key Points

### Multi-scale Framework

将时间序列利用不同采样率进行采样（平均池化），得到不同尺度。低级尺度具有更大的采样率，更平滑，是低频信息；高级尺度具有更小的采样率，保留更多细节信息、高频信息。先预测低级尺度的结果，再将其上采样后送入更高级尺度作为高级尺度的解码器的输入，是一种从粗到细的预测策略。

![[v2-08d182a1d4d6c349910b69cf42a1b8d6_1440w.jpg]]

逐级预测的idea的示意图

![[v2-e287270597449acea84f36572a26aa4b_1440w.jpg]]

具体架构

### Cross-scale Normalization

编码器的输入和解码器的输入存在数据分布偏移。一方面是这两者分别来源于look-back window和horizon window，数据分布本身就存在偏移；另一方面，高级尺度的解码器输入是由低级尺度的输出上采样得到的，不同尺度分布也不一样（如下图右），这又带来了跨尺度偏移。因此，将编码器的输入和解码器的输入整体求平均后，都减掉均值，再输入到模型中。

![[v2-32fad0b3bf3a731dd92a23f0f5ef14eb_1440w.jpg]]

左侧是用与不用cross-scale normalization的对比，右侧是不同尺度数据的分布

### Loss Function

用新的自适应loss（别人已经提出来了）来替换MSE loss来训练模型。

![[v2-1fde81ebbca1ce76fdac9f12fc742156_1440w.jpg]]

新的训练loss

## Comments

从粗到细的预测策略看起来挺work也挺直观，但每一个尺度都分配一个预测模型属实有点浪费。虽然作者说了可以去掉复杂度最高的最高级的尺度（因为高级尺度采样率小，序列更长，复杂度更高），直接从第二高级的尺度插值得到预测结果，但我觉得有点牵强。

编辑于 2023-02-09 13:17・北京[深度学习（Deep Learning）](https://www.zhihu.com/topic/19813032)[Transformer](https://www.zhihu.com/topic/20746363)[时间序列预测](https://www.zhihu.com/topic/25716601)[阿里云 ×OpenClaw 三步极速上手](https://click.aliyun.com/m/1000409721/?spu=biz%3D0%26ci%3D3693408%26si%3Dc6d090ba-3f6e-4bb1-8816-dbf70d29ac37%26ts%3D1775469780%26zid%3D1629)

[

无需技术背景！小白也能拥有

](https://click.aliyun.com/m/1000409721/?spu=biz%3D0%26ci%3D3693408%26si%3Dc6d090ba-3f6e-4bb1-8816-dbf70d29ac37%26ts%3D1775469780%26zid%3D1629)