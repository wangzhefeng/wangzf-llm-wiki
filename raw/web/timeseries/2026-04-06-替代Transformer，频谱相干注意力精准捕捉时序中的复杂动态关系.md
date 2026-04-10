---
author:
- null
- '[[TSer]]'
created: 2026-04-06
created_at: 2026-04-06
description: null
published: null
source: https://mp.weixin.qq.com/s/_H4ODSnQAPwTaut9WyIpgA
source_type: web
status: inbox
tags:
- null
- clippings
title: 替代Transformer，频谱相干注意力精准捕捉时序中的复杂动态关系
topics:
- 大语言模型
- 深度学习
---

## AAAI 2026 Oral | 替代Transformer，频谱相干注意力精准捕捉时序中的复杂动态关系

原创 TSer *2026年1月26日 20:02*

**点击名片**  

关注并星标

**TSer**

**扫下方二维码** **，加入时序人学术星球**

**参与算法讨论，获取前沿资料**

**已有** **540+** **同学加入交流学习**  

**文末有优惠券~**

![[Image 81.webp|图片]]

针对多变量时间序列预测中难以有效建模变量间复杂动态关系的痛点，作者提出了一种名为 Sonnet（Spectral Operator Neural Network） 的新型神经网络架构。

该模型并没有单纯依赖传统的 Transformer 架构，而是结合了可学习的小波变换和基于 Koopman 算子的谱分析理论。其核心创新在于提出了一种多变量相干注意力机制（Multivariable Coherence Attention, MVCA），利用谱相干性来精准捕捉变量间的依赖关系。

实验结果表明，Sonnet 在47个预测任务中的34个任务上取得了最佳性能，相比最强基线模型平均降低了2.2%的 MAE；同时，MVCA 模块作为一个通用组件，能够替换现有深度学习模型中的朴素注意力层，在困难任务上平均降低10.7%的误差。

![[Image 82.webp|图片]]

【论文标题】

Sonnet: Spectral Operator Neural Network for Multivariable Time Series Forecasting

【论文地址】

https://arxiv.org/abs/2505.15312

【论文源码】

https://github.com/ClaudiaShu/Sonnet

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**论文背景**

在时序预测领域，多变量预测与多变量输出预测有所区别：前者侧重于利用多个外生变量来辅助预测单一目标变量（如利用温度、湿度、气压预测特定地点的降雨量），后者则是同时预测多个变量。

尽管 Transformer 架构在捕捉长序列的时间依赖性方面表现出色，但在处理多变量预测时存在明显的短板：

- 变量间关系建模困难：朴素的 Transformer 应用往往难以有效解耦和利用外生变量与目标变量之间随时间变化的复杂非线性关系。
- 注意力机制的局限：传统的注意力机制主要关注序列层面的相似性，缺乏对物理机制或频域相干性的考量，导致在引入外生变量时噪声干扰大，甚至出现性能倒退。

为了解决这些问题，作者引入了谱理论，特别是 Koopman 算子理论，旨在将非线性动力系统映射到线性空间中进行处理，从而更本质地捕捉变量间的协同演化关系。

**论文方法**

Sonnet 的整体架构设计紧密围绕“频域特征提取”与“谱动力学建模”展开，主要包含以下关键技术：

**01**

**可学习的小波变换**

不同于固定的傅里叶变换（FFT），Sonnet 在输入端采用了可学习的小波变换。

- 优势：FFT 丢失了时间信息，而小波变换能同时保留时域和频域的局部特征。
- 机制：模型通过学习小波系数，能够自适应地处理非平稳信号，为后续的谱分析提供更鲁棒的特征表示。

**02**

**Koopman算子谱分析**

论文利用 Koopman 算子理论来线性化复杂的非线性动力学系统。

- 原理：将数据映射到一个潜在空间，在该空间中，系统的演化可以近似为线性的。
- 实现：Sonnet 通过学习一个线性算子（矩阵），在谱模态（Spectral Modes）上推演未来的状态。这使得模型能够清晰地分离出系统的长期趋势和周期性波动，保证了预测的稳定性。

**03**

**多变量相干注意力机制（MVCA）**

这是论文的核心创新点，MVCA 旨在替代传统的缩放点积注意力。

- 核心思想：利用谱相干性作为度量标准。
- 计算方式：MVCA 不计算时域上的点积，而是计算外生变量与目标变量在频域上的相干程度。
- 物理意义：如果两个变量在特定频率上具有高相干性，说明它们之间存在强物理耦合。MVCA 据此动态分配权重，让模型“自动聚焦”于那些真正驱动目标变化的关键外生变量，同时抑制噪声变量的干扰。

**实验分析与结果**

为了验证 Sonnet 的有效性，作者构建并开源了一个涵盖不同气候条件（伦敦、纽约、香港、开普敦、新加坡）的气象数据集，主要任务是利用周围区域的气候指标作为外生变量，预测特定位置的850hPa温度（T850）。

**01**

**主实验性能**

在总共47个不同的预测任务中，Sonnet 在34个任务上取得了 SOTA 性能。与当前最具竞争力的基线模型相比，Sonnet 的平均绝对误差（MAE）降低了约 2.2%。这一结果证明了谱算子方法在处理复杂气象动力学方面的优势。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**02**

**消融研究**

作者尝试将现有的深度学习模型（如基于 Transformer 的基线模型）中的原始注意力层替换为 MVCA 模块。

实验结果显示：

- MVCA 的通用性：替换后，原有模型的性能得到了显著提升。
- 抗噪能力：在最具挑战性的预测任务（通常意味着噪声大、关系复杂）中，MVCA 带来的 MAE 下降达到了惊人的 10.7%。

这证明了 MVCA 不仅仅是 Sonnet 的一个组件，更是一个可以“即插即用”的强力模块，能有效修复传统注意力机制在多变量依赖建模上的缺陷。

**03**

**长短期预测能力**

实验还特别采用了针对目标步长的评估方式（即关注 t+H 时刻的准确性而非1到 H 的平均），结果显示 Sonnet 在长跨度预测上保持了优异的稳定性，验证了其捕捉长期动力学特征的能力。

**总结**

该工作的最大贡献在于跳出了“堆叠Transformer层数”的传统思路，转而从谱动力学的角度重新审视多变量时序预测问题。其提出的 MVCA 模块为多变量场景下的信息融合提供了一个具有物理可解释性的新范式。

对于从事气象预测、能源管理、金融量化等依赖多变量分析的复杂时序任务的研究者而言，Sonnet 提供了一个极具价值的新基准和设计思路。

**扫下方二维码，加入时序人学术星球**

**星球专注于时间序列领域的知识整理，前沿追踪**

**提供** **论文合集** **、视频课程、问答服务** **等资源**

**已有** **540+** **同学加入交流学习**

**价格随着内容丰富而上涨，早入早享优惠~**

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

时间序列学术前沿系列持续更新中 ⛳️

后台回复" **讨论** "，加入讨论组一起交流学习 🏃

**往期推荐阅读**

[AAAI 2026 | 时间序列相关论文盘点（附原文源码）](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507600&idx=1&sn=ad10ea55e291d13820e5ae6d9a1bd45b&scene=21#wechat_redirect)

[AAAI 2026 | TimeMosaic：时间序列真的“均匀”吗？](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507572&idx=1&sn=e42a9935924b61ff77c309f5445ebd29&scene=21#wechat_redirect)

[综述 | 从信号到语义：基于人类认知视角的时间序列可解释性综述](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507557&idx=1&sn=7e64a7a617c8e8b6a76db49f7c5735ad&scene=21#wechat_redirect)

[AAAI 2026 | CONFETTI：多维时序分类任务下的反事实解释新 SOTA，多目标优化提升！](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507528&idx=1&sn=a4f9b93f7f92f30751704300894091a9&scene=21#wechat_redirect)

[AAAI 2026 | APN：越简单越高效，重新审视不规则时间序列预测的基础方法](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507515&idx=1&sn=709479586b092c44a5cc57a8920a381b&scene=21#wechat_redirect)

[D2Vformer：一个可实现任意位置任意长度时序预测的深度学习模型](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507468&idx=1&sn=8e46d9070964216c2da5bb7038e5ec3d&scene=21#wechat_redirect)

[AAAI 2026 Oral | 零样本、高精度、低开销：高效利用视觉语言模型检测时序异常](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507350&idx=1&sn=b442d44f60df809459cafe3196a0ab7d&scene=21#wechat_redirect)

[年度总结 | 2025 时间序列领域前沿技术进展](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507349&idx=1&sn=3df85ce4388951cec6dbe2c769fd5b22&scene=21#wechat_redirect)

[综述 | 一文读懂「生物信号 (Biosignal) 大模型」的全景图景](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507263&idx=1&sn=bf0aa06dc3e159e5bf57f8a9fd97cdce&scene=21#wechat_redirect)

[NeurIPS 2025 | ScatterAD：作用于时序异常检测的“时态-拓扑”散射表示方法](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507169&idx=1&sn=0727b65cc082e418befefe6b3ba3d1d9&scene=21#wechat_redirect)

[NeurIPS 2025 | 有选择性的 Patch，提升分块技术在时序预测中的性能](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507058&idx=1&sn=4f5da921b2ef49103ad6b5714cb901cd&scene=21#wechat_redirect)

[NeurIPS 2025 | 全局对齐 Loss 提升高缺失率时间序列补全效果](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247507007&idx=1&sn=33eb8e63533536d0f16d3378dfb3f340&scene=21#wechat_redirect)

[NeurIPS 2025 | 比 attention 计算更高效，正交线性 Olinear 显著提升时序预测性能](https://mp.weixin.qq.com/s?__biz=Mzg3NDUwNTM3MA==&mid=2247506986&idx=1&sn=72f043bf1c42dc4fa00c7755acb0d06c&scene=21#wechat_redirect)

**觉得不错，那就点个推荐和赞吧**

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

继续滑动看下一个

时序人

向上滑动看下一个