---
author:
- null
- '[[时序之心]]'
created: 2026-04-06
created_at: 2026-04-06
description: 本文介绍了一项在 ICLR 2025 发表的最新研究成果。
source_type: web
status: inbox
tags:
- null
- clippings
title: TIMEMIXER++：通用时序预测新SOTA，全面超越Transformer！
topics:
- 大语言模型
- 时间序列
source_url: https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486524&idx=1&sn=ba81479a7b9b52af1e80cf8f2e5e853c&scene=21&poc_token=HLyF02mjC6tJvy-KqC-WppWyEKeLHWOxaX-qR9Gd
published_at: null
related_concepts: []
---

## ICLR 2025 | TIMEMIXER++：通用时序预测新SOTA，全面超越Transformer！

原创 时序之心 *2025年8月7日 10:34*

本文介绍了一项在 ICLR 2025 发表的最新研究成果。该研究提出了TIMEMIXER++，这是一种通用的时序模式机器，旨在通过强大的表示和模式提取能力，在广泛的时间序列任务中表现出色。

传统模型常常难以捕捉跨越不同任务的通用模式。为解决此问题，TIMEMIXER++ 独创性地将一维时间序列转换为二维的多分辨率时间图像，并在图像的潜在空间中利用双轴注意力来解耦季节性和趋势性模式。随后，通过多尺度和多分辨率混合机制，模型能自适应地聚合不同尺度和周期的信息，从而提取出与任务高度相关的复杂模式。实验表明， **TIMEMIXER++ 在八项主流的时间序列分析任务中均取得了SOTA性能，全面超越了现有的通用及任务专用模型。**

另外，我整理了 **ICLR 2025时间序列相关论文合集** ，感兴趣的自取~

关注“时序之心”回复“C276”

免费领取ICLR 2025时间序列论文+源码

![[Image 107.webp|Benchmarking model performance]]

Benchmarking model performance

【论文标题】TIMEMIXER++: A GENERAL TIME SERIES PATTERN MACHINE FOR UNIVERSAL PREDICTIVE ANALYSIS

【论文链接】https://arxiv.org/abs/2410.16032

【代码链接】 https://github.com/kwuking/TimeMixer

## 研究背景

时间序列分析在天气预报、医疗诊断、金融预测等众多领域至关重要。一个核心挑战是开发一种能够处理多种任务的通用模型架构，即时序模式机器。现有的方法各有局限：

- **RNN-based** 模型难以捕捉长期依赖。
- **TCN-based** 模型虽然高效，但其固定的感受野限制了对长距离模式的建模。
- **Transformer-based** 模型虽然擅长捕捉长距离依赖，但时间序列数据中多种周期在同一时间点重叠的特性，使得将其有效“token化”变得困难，从而限制了模型充分捕捉相关时间结构的能力。

此外，不同的时间序列任务对模型的表示能力有不同的要求。根据 CKA 相似度分析所示，预测和分类等任务受益于层间一致的表示（高 CKA），而插补和异常检测等任务则需要更多样化的分层表示（低 CKA）。这种矛盾给设计一个真正通用的 TSPM 带来了巨大挑战。

为了解决这些问题，本文提出了 TIMEMIXER++，一个旨在通过处理多尺度和多周期动态性来捕捉通用、任务自适应模式的 TSPM。

## 核心贡献

本研究贡献可总结如下：

- 提出TIMEMIXER++，一个通用的时间序列分析模型，通过将时间序列转换为多分辨率时间图像，实现了在时间和频率双域上的高效模式提取。
- 设计了时间图像分解、多尺度混合和多分辨率混合等一系列创新机制。这些机制协同工作，首先利用双轴注意力解耦时间图像中的季节和趋势模式，然后跨尺度和周期自适应地聚合这些模式。
- TIMEMIXER++ 在八个不同基准的时间序列分析任务上均取得了新的SOTA性能，持续优于现有的通用模型和任务专用模型，标志着下一代 TSPM 发展迈出了重要一步。

## 方法解析

![The framework of TIMEMIXER++](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

The framework of TIMEMIXER++

上图为 TIMEMIXER++ 方法的整体框架。它采用了一个标准的 Encoder-Only 架构，主要由输入投影、一堆 MixerBlock 和输出投影三部分组成。其核心思想是，在每个 MixerBlock 中，将多尺度的一维时间序列输入转化为二维的时间图像，然后进行分解、混合与聚合。

### 多尺度时间序列

首先，通过步长为2的一维卷积对原始输入时间序列进行多次下采样，从而得到一个包含 M+1 个不同尺度的时间序列集合 。这为后续的多尺度分析奠定了基础。

### MixerBlock

MixerBlock 是 TIMEMIXER++ 的核心，它包含四个关键步骤，旨在从多尺度、多周期数据中提取全面的模式。

#### 1\. 多分辨率时间成像

在每个 MixerBlock 的开始，模型首先对最粗糙尺度 的时间序列进行傅里叶变换，找出幅度最高的 Top-K 个频率，这些频率对应着数据中最主要的 K 个周期。然后，对于每一个尺度 的序列 ，模型使用这 K 个周期将其重塑为 K 个二维的“时间图像” 。在这些图像中，行代表周期内的不同时间点，列代表跨越不同周期的同一时间点。

#### 2\. 时间图像分解

时间序列模式天然是嵌套的。为了精细化地解耦这些模式，模型对每个时间图像应用双轴注意力。 列轴注意力：沿列的方向计算注意力，用于捕捉季节性模式。 行轴注意力：沿行的方向计算注意力，用于提取趋势性模式。 通过这种方式，模型可以将每个时间图像分解为一个季节性图像和一个趋势性图像。

#### 3\. 多尺度混合

分解后，模型需要整合不同尺度的信息。 对于季节性模式，模型采用从细到粗的方式，使用带残差连接的 2D 卷积进行分层混合。因为长周期的季节性通常是短周期季节性的组合。 对于趋势性模式，模型采用从粗到细 的方式，使用 2D 转置卷积进行混合。因为粗糙尺度更能捕捉全局趋势，可以指导精细尺度上的趋势建模。

#### 4\. 多分辨率混合

最后，对于每个尺度 ，模型需要将从 K 个不同分辨率中提取的模式聚合起来。模型使用之前 FFT 得到的各频率分量的幅度作为权重，对 K 个处理后的模式进行加权求和，得到该尺度最终的表示。这个过程是自适应的，因为它根据数据本身的周期特性来决定不同分辨率的重要性。

### 输入与输出投影

在进入 MixerBlock 栈之前，模型通过一个输入投影层对不同尺度的序列进行通道混合与嵌入。经过 L 个 MixerBlock 处理后，模型得到多尺度的表示。由于不同尺度捕捉的模式不同，模型为每个尺度都设置一个独立的预测头，并将它们的输出进行集成，得到最终的预测结果。这种设计增强了模型的任务自适应能力。

## 实验验证

![Long-term forecasting results](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Long-term forecasting results

如上方的雷达图所示，TIMEMIXER++ 在八项全面的时间序列分析任务中均展现出卓越的性能，持续超越了27个先进的基线模型。

**长期预测** ：在包含 ETT、Weather、Traffic 等8个数据集的长期预测任务中，TIMEMIXER++ 表现出色。例如，在挑战性的 Solar-Energy 数据集上，其 MSE 和 MAE 分别比次优模型低 6.0% 和 9.2%。

**短期预测** ：在 M4 单变量预测竞赛数据集上，TIMEMIXER++ 的 SMAPE 指标比 iTransformer 降低了 9.7%。在 PeMS 多变量交通流量预测任务中，其 MAE 比 PatchTST 降低了 30.8%，展示了其在处理高维数据上的强大能力。

**其他任务** ：在插补任务中，TIMEMIXER++ 的 MSE 比次优模型 TimesNet 平均降低 25.7%。在分类任务中，准确率达到 75.9%，超过 TimesNet 2.3%。在异常检测任务中，F1-score 达到 87.47%，超过 Anomaly Transformer 6.62%。这些结果充分证明了 TIMEMIXER++ 作为一个通用时序模式机器的强大泛化能力和鲁棒性。

## 总结

本文提出了 TIMEMIXER++，一个为通用预测分析设计的时序模式机器。通过创新的多分辨率时间成像、基于双轴注意力的模式分解以及多尺度/多分辨率混合技术，TIMEMIXER++ 能够无缝地在不同层级上融合和提取信息，展现出强大的表示能力。全面的实验评估证明，TIMEMIXER++ 在各类时间序列任务中一致地优于现有模型，为构建下一代通用时间序列分析工具奠定了坚实的基础。 **一言概括之，TIMEMIXER++ 将时序分析从“一维思考”提升到“二维图像化”的层次，通过解耦和分层聚合，实现了对复杂时序模式的深度理解。**

扫码添加小助手回复“C276”

免费获取全部论文资料

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

---

---

相关推荐

[ACL 2025精选：时间序列论文精华速览！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486516&idx=1&sn=e2596c7b20965db60c67be9ac6031dc8&scene=21#wechat_redirect)

[ICML 2025 | A2P模型精准预测时间序列未来异常点！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486516&idx=2&sn=47ca77273f1994090df08f34106feee1&scene=21#wechat_redirect)

[时序预测新思路：频域乘法替代时域卷积，计算量骤降！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486478&idx=1&sn=9c2e9e7dc45ab1e4a8010d0498b6a702&scene=21#wechat_redirect)

[小波变换+时序预测：AI 搞定非平稳信号，2025 顶会思路这不来了！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486467&idx=1&sn=6da2980bb4a6cf1e72f1fd8d6b34e9f3&scene=21#wechat_redirect)

[ICML 2025 | 在神经科学中生成动态因果图假设：利用观测时间序列的生成因子模型！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486445&idx=1&sn=b6c1921719c948e46bd9c627fc810a4a&scene=21#wechat_redirect)

[GAN颠覆时序建模！TimeGAN让数据增强更智能！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486456&idx=1&sn=b8722d6a595fc6045a2a0d101938a60c&scene=21#wechat_redirect)

[ICML 2025 | 深度剖析时序 Transformer：为何有效，瓶颈何在？](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486418&idx=1&sn=02d4a0fcbd9b1373f6514831e08a4bc4&scene=21#wechat_redirect)

[ICLR 2025 | ROSE：基于频率分解的通用时序预测新突破！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486399&idx=2&sn=5a16f8b1688dffc10ddd585b2b42694b&scene=21#wechat_redirect)

[2025 | 时间序列232篇顶会论文汇总（附原文源码）！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486337&idx=1&sn=15669fd74a88cba25080a75324627012&scene=21#wechat_redirect)

注：本公众号发布的内容仅用于信息传递与知识分享，不保证绝对准确，也不构成专业建议。因使用内容造成的任何损失，我们概不负责。 若公众号含外部链接，链接内容及运营不受我们控制，由此产生的风险和损失，读者自行承担。此外，原创内容版权归本号所有，未经授权禁止商用。因不可抗力、技术故障等致内容异常，本号同样免责。阅读即视为同意本声明，如有疑问，欢迎联系。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

作者提示: 个人观点，仅供参考

阅读原文

继续滑动看下一个

时序之心

向上滑动看下一个