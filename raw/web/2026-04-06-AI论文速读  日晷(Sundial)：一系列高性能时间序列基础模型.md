---
source_type: web
title: "AI论文速读 | 日晷(Sundial)：一系列高性能时间序列基础模型"
author:
  - 
  - "[[NO1WDS”时空探索之旅“ “STLearner”]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://zhuanlan.zhihu.com/p/22292409357"
published: 
created: 2026-04-06
description: "论文标题：Sundial: A Family of Highly Capable Time Series Foundation Models 作者： Yong Liu(刘雍), Guo Qin, Zhiyuan Shi, Zhi Chen, Caiyin Yang, Xiangdong Huang, Jianmin Wang(王建民), Mingsheng Long(…"
tags:
  - 
  - "clippings"
---

目录

收起

摘要

Q: 这篇论文试图解决什么问题？

Q: 有哪些相关研究？

Q: 论文如何解决这个问题？

Q: 论文做了哪些实验？

Q: 总结一下论文的主要内容

**论文标题** ：Sundial: A Family of Highly Capable Time Series Foundation Models

**作者** ： Yong Liu(刘雍), Guo Qin, Zhiyuan Shi, Zhi Chen, Caiyin Yang, Xiangdong Huang, Jianmin Wang(王建民), Mingsheng Long(龙明盛)

**机构** ：清华大学

**论文链接** ： [arxiv.org/abs/2502.0081](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2502.00816)

**Cool Paper** ： [papers.cool/arxiv/2502.](https://link.zhihu.com/?target=https%3A//papers.cool/arxiv/2502.00816)

**TL；DR** ：论文介绍了Sundial，一种新型的时间序列基础模型系列。Sundial通过提出基于流匹配的TimeFlow Loss，解决了时间序列预测中的非确定性和深度模型的局限性问题。模型在包含1万亿时间点的TimeBench数据集上进行预训练，展现了卓越的零样本预测性能。Sundial在多个基准测试中取得了最佳性能，为时间序列预测提供了更可靠和灵活的工具。

**关键词** ：基础模型、零样本预测、流匹配，概率预测，连续/离散 token

![[v2-7d2517309b6caf33b1123de96f1a9971_1440w.jpg]]

### 摘要

本文提出了 **Sundial** ，这是一系列原生、灵活且可扩展的时间序列基础模型。为了预测下一个补丁的分布，提出了基于流匹配的 TimeFlow Loss，这有助于在时间序列上对 [Transformers](https://zhida.zhihu.com/search?content_id=253480717&content_type=Article&match_order=1&q=Transformers&zhida_source=entity) 进行原生预训练，而无需离散词元化（tokenization ）。以任意长度的时间序列为条件，模型无需指定任何先验分布即可进行预训练，并且可以生成多个可能的预测，从而实现除使用参数密度之外的表示学习灵活性。对于时间序列基础模型，利用 Transformers 的最小但关键的改编，并使用 **1 万亿个时间点** 来整理 **TimeBench** ，其中主要包括现实世界的数据集和合成数据。通过 **TimeFlow Loss** 缓解模式崩溃，在 TimeBench 上预训练了一系列 Sundial 模型，这些模型在零样本预测中表现出前所未有的模型容量和泛化性能。除了表现出良好的扩展行为外，Sundial 还在点预测和概率预测基准上实现了新的最先进水平。我们相信，Sundial 的先锋生成范式将促进各种各样的预测场景。

### Q: 这篇论文试图解决什么问题？

![[v2-cfa0c7e0d07c6b682df14caa03390d7b_1440w.jpg]]

原生时序模型在连续词元上学习表示。灵活的基础模型在没有指定先验分布的情况下进行预训练。Sundial为第一个原生且灵活的时间序列基础模型系列

**A**: 这篇论文介绍了Sundial，一个针对时间序列数据的新型基础模型系列。论文试图解决的问题主要集中在以下几个方面：

1. **非确定性预测需求** ：时间序列预测本质上是非确定性的，因此需要生成一系列可能的预测结果以辅助决策。论文强调了生成一系列可能预测的重要性。
2. **深度模型的局限性** ：尽管深度模型在时间序列预测方面取得了令人印象深刻的性能，但它们通常需要针对特定任务在足够多的分布内数据上进行训练。
3. **时间序列基础模型的构建** ：现有的时间序列基础模型研究集中在构建统一、可扩展且开箱即用预测器上，这些预测器展现出接近或有时超过监督方法的零样本（zero-shot）性能。
4. **生成能力与概率预测** ：大多数时间序列基础模型缺乏“生成性”或更具体地说，概率预测能力，这限制了它们在决策中的可靠性。论文提出通过引入生成模型来自然处理预测中的不确定性。
5. **连续值时间序列的表示学习** ：论文指出，连续值时间序列与语言词元（token）之间存在明显区别，可能导致词汇表外问题和粗粒度预测区间。因此，需要一种新的方法来学习连续值时间序列的表示。
6. **预训练分布的灵活性** ：为了学习任意复杂的分布而不发生模式崩溃，论文提出了不采用任何特定概率先验（如单峰高斯或多峰混合模型）的方法，以提高基础模型在大规模语料库上的表示能力。
7. **提高模型容量和泛化性能** ：通过在1万亿时间点的数据集上进行预训练，Sundial模型系列在零样本预测方面展现出前所未有的模型容量和泛化性能。

总的来说，论文旨在通过提出Sundial模型系列，引入基于流匹配的TimeFlow Loss，以及构建包含1万亿时间点的TimeBench数据集，来推动时间序列基础模型的发展，并在各种预测场景中提供更可靠、更灵活的预测能力。

### Q: 有哪些相关研究？

**A**: 根据论文内容，相关研究可以分为以下几个领域：

**时间序列预测** ：

- 统计和深度学习方法的发展，包括理论启发的组件、面向架构的适应和时间序列处理方法。
	- 基础模型（foundation models）的发展，旨在通过预训练解决数据稀缺问题，并在分布外数据上实现良好的泛化性能。

**时间序列基础模型** ：

- 构建大型、通用的时间序列模型，其中Transformer已成为主导架构。
	- 针对时间序列的二维特性和异质性进行的特定适应，包括词元化和优化方法。

**生成模型在时间序列中的应用** ：

- 生成模型在时间序列生成和特定任务预测中的应用。
	- 流匹配（flow-matching）和去噪扩散模型（denoising diffusion models）在连续值模态中的使用。

**概率预测** ：

- 从点预测（point forecasting）向概率预测的转变，以处理预测中的不确定性。

**Transformer架构在时间序列中的应用** ：

- 将Transformer模型适应到时间序列数据，包括处理时间序列数据的特定二维特性和异质性。

具体到论文中提到的一些工作，包括但不限于：

- **Time-MoE** (Shi et al., 2024b)：一个基于Mixture of Experts的大规模时间序列模型。
- **Timer** (Liu et al., 2024a;b)：一个针对时间序列预测优化的Transformer模型。
- **Moirai** (Woo et al., 2024)：一个学习混合分布的概率模型。
- **Chronos** (Ansari et al., 2024)：一个通过离散化时间序列进行预训练的模型，学习灵活的分类分布。
- **LLMTime** ：一个针对时间序列预测优化的大型语言模型。
- **TimesFM** (Das et al., 2023b)：一个基于Transformer的时间序列预测模型。

这些研究构成了Sundial模型的理论和实践基础，并在时间序列预测领域中提供了有价值的见解和技术。

### Q: 论文如何解决这个问题？

![[v2-366ce3e41dc4c802317281daa73fc86f_1440w.jpg]]

Sundial

**A**: 论文通过以下几个关键方法解决了时间序列预测中的问题：

**提出TimeFlow Loss** ：

- 为了在不进行离散化词元化（tokenization）的情况下预训练Transformer模型，并能够进行概率预测，论文提出了TimeFlow Loss。这是一个基于流匹配（flow-matching）的参数化训练目标，允许自回归模型学习每个词元（token）的预测分布，并在推理过程中生成原始预测序列。
![[v2-615c7ba8efdf0926bac07dac1476cc6e_1440w.jpg]]

TimeFlow Loss

**增强Transformer架构** ：

- 论文对Transformer进行了最小但关键的调整，以适应时间序列数据：
- **[Patch Embedding](https://zhida.zhihu.com/search?content_id=253480717&content_type=Article&match_order=1&q=Patch+Embedding&zhida_source=entity)** ：设计了与非整除上下文长度兼容的patch embedding。
		- **[RoPE](https://zhida.zhihu.com/search?content_id=253480717&content_type=Article&match_order=1&q=RoPE&zhida_source=entity) （Rotary Position Embedding）** ：引入位置信息以增强时间因果关系。
		- **[Pre-LN](https://zhida.zhihu.com/search?content_id=253480717&content_type=Article&match_order=1&q=Pre-LN&zhida_source=entity) （Pre-layer Normalization）** ：提高预训练稳定性。
		- **[FlashAttention](https://zhida.zhihu.com/search?content_id=253480717&content_type=Article&match_order=1&q=FlashAttention&zhida_source=entity) 和 [KV Cache](https://zhida.zhihu.com/search?content_id=253480717&content_type=Article&match_order=1&q=KV+Cache&zhida_source=entity)** ：这些是大型基础模型中越来越被强调的部署增强功能。

**构建TimeBench数据集** ：

- 为了探索时间序列基础模型的扩展规律，作者收集和策划了TimeBench，这是一个包含超过 **1万亿时间点** 的大规模数据集，涵盖了 **多个领域** 的数据。
![[v2-a49afffce23107def12c38bc132ff961_1440w.jpg]]

Sundial的预训练语料库TimeBench中的数据源

**实现Sundial模型系列** ：

- 论文介绍了Sundial，这是一个在TimeBench上预训练的高度可扩展的基础模型系列。Sundial模型在点预测和概率预测基准测试中都取得了新的最佳性能。

**生成模型的应用** ：

- 论文通过引入生成模型来实现概率预测，这种方法允许模型自动学习分布，并通过对学习到的表示进行条件化来生成原始预测序列，然后计算其统计数据以进行概率预测。

**零样本学习** ：

- Sundial模型在多个大规模和公认的基准测试中实现了零样本性能的新最佳水平，这表明生成时间序列基础模型是决策的有力工具。

总结来说，论文通过提出新的损失函数、增强Transformer架构、构建大规模数据集，并利用生成模型进行概率预测，解决了时间序列预测中的关键问题，并推动了时间序列基础模型的发展。

### Q: 论文做了哪些实验？

![[v2-7a5b313fdf1f55b671d3b76d2ae5a9fb_1440w.jpg]]

Sundial整体评测结果（性能，效率）

![[v2-54210fea3bf58ecfca1524a4b35954f3_1440w.jpg]]

数据集

**A**: 根据论文内容，作者进行了以下实验来评估Sundial模型的性能和有效性：

**时间序列预测** ：  

- **点预测（Point Forecasting）** ：
- 使用长期预测基准（Time-Series-Library）评估不同模型在不同预测范围下的性能，使用均方误差（MSE）和平均绝对误差（MAE）作为评估指标。
		- 比较Sundial与其他先进的时间序列基础模型的性能。
![[v2-5c5b929708aa9b8ed6442f42fc92adc6_1440w.jpg]]

零样本

- **概率预测（Probabilistic Forecasting）** ：
- 在GIFT-Eval基准测试上进行实验，这是一个综合评估不同时间序列的数据集，覆盖了多个领域和数据特性。
	- 在FEV排行榜上进行评估，这是一个包含27个数据集的概率预测排行榜，用于零样本评估。
![[v2-b096037cb2b84dde25b4540a4db67f38_1440w.jpg]]

GIFT-Eval概率预测

![[v2-c70cac89545d37dbf7498f885150dab3_1440w.jpg]]

FEV概率预测

![[v2-822a80a1ff4b0b2ee89bf1de28f6a93b_1440w.jpg]]

推理时间

**模型扩展性（Scalability）** ：

- 研究模型大小对Sundial性能的影响，通过比较不同大小的Sundial模型在TimeBench上的训练曲线和预测性能。
![[v2-6658f5e219f0b88f171d264ca56d8ae4_1440w.jpg]]

模型扩展性

**TimeFlow Loss的有效性** ：

- 通过与其他训练目标（如MSE Loss和基于去噪扩散的过程的参数化训练目标）进行比较，验证TimeFlow Loss在零样本性能上的有效性。
![[v2-ba0ae256ca57c545996d024c044d6522_1440w.jpg]]

不同损失的零样本预测结果

**模型推理（Model Inference）** ：

- 探讨在推理过程中调整预测质量的不同配置，包括生成预测的数量和流匹配中的采样步骤，以及它们对预测性能和推理速度的影响。
![[v2-ef125969ad5bc535c28a4199444ff039_1440w.jpg]]

生成预测数量和采样步骤

**模型适应性（Model Adaptation）** ：

- 通过对预训练的Sundial模型在FEV排行榜上进行微调，评估模型的知识迁移能力，并与从零开始训练的模型进行比较。
![[v2-b11370cb3f1230621b326913ca2099c3_1440w.jpg]]

从头训练VS零样本VS微调

这些实验全面评估了Sundial模型在不同方面的表现，包括其在点预测和概率预测任务上的性能、模型的扩展性、训练目标的有效性、推理效率和模型的适应性。通过这些实验，作者展示了Sundial模型在时间序列预测任务中的有效性和优越性。

![[v2-d2ab932e1ef3589fb99b374ea0061b3b_1440w.jpg]]

时序基础模型参数对比

**具体示例**

![[v2-870586f8febd4bc71fb4d8260fc727d0_1440w.jpg]]

![[v2-5da388e59fd6c90bd7436b91bc921a44_1440w.jpg]]

- 图10-11 展示了 Sundial (Base) 在 FEV 排行榜上的零样本预测结果。通过生成多个不同初始噪声的预测，计算中位数并绘制 80% 预测区间。这表明 Sundial 模型能够根据历史数据生成多种可能的预测结果，反映出未来时间序列的不确定性，体现了模型在概率预测方面的能力，为决策者提供了更丰富的信息。
![[v2-8de03636f5dc1b14dfef5232ab25feec_1440w.jpg]]

- Sundial (Base) 在长时预测数据集上的零样本预测。展示了不同数据集和不同预测长度下的预测情况，说明 Sundial 在长时预测任务中也能取得较好的效果，生成的预测与输入序列高度相关，且能捕捉到时间序列的趋势和变化，进一步证明了模型的泛化能力和有效性。
![[v2-0d1a85c0e34702a1e6028a5cc80f6edb_1440w.jpg]]

![[v2-a1e4669bf541dff9f721e158cc7c3de0_1440w.jpg]]

- 对比了 Sundial 和采用相同骨干网络但由 MSE 损失预训练的 Transformer 的零样本预测展示。Sundial 作为 **生成式预测器** ，能基于回顾序列预测各种未来可能性；而由 MSE 损失预训练的模型作为确定性预测器，只能输出一个预测。且 MSE 损失预训练的模型在处理大规模预训练时存在局限性，会出现过度平滑的预测，凸显了 Sundial 在预测多样性和处理复杂分布方面的优势。

### Q: 总结一下论文的主要内容

**A**: 论文介绍了Sundial，这是一个针对时间序列数据的新型基础模型家族。以下是论文的主要内容总结：

**问题定义** ：

时间序列预测具有非确定性，需要生成一系列可能的预测结果以辅助决策。

现有的深度模型需要大量特定任务的训练数据，限制了其在数据稀缺情况下的应用。

时间序列基础模型旨在通过预训练解决数据稀缺问题，并在分布外数据上实现良好的泛化性能。

**Sundial模型系列** ：

提出了Sundial，一个原生的、灵活的、可扩展的时间序列基础模型系列。

Sundial模型无需离散化词元，即可在时间序列数据上进行预训练，并生成多个可能的预测结果。

**TimeFlow Loss** ：

为了训练Sundial模型，提出了基于流匹配的TimeFlow Loss，这是一种参数化的训练目标，允许模型学习每个词元的预测分布，并在推理过程中生成原始预测序列。

**Transformer架构的增强** ：

对Transformer进行了最小但关键的调整，包括Patch Embedding、RoPE、Pre-LN、FlashAttention和KV Cache，以适应时间序列数据的特性。

**TimeBench数据集** ：

构建了TimeBench，一个包含超过1万亿时间点的大规模数据集，用于预训练Sundial模型。

**实验评估** ：

在多个大规模和公认的基准测试中评估了Sundial模型，包括点预测和概率预测任务。

Sundial在这些基准测试中取得了新的最佳性能，展现了良好的扩展性和零样本预测能力。

**进一步探索的方向** ：

论文讨论了Sundial模型的局限性，并提出了未来可能的研究方向，包括改进采样策略、多变量时间序列的预训练、输出长度的自适应调整等。

**社会影响** ：

论文讨论了Sundial模型在现实世界应用中的潜在社会影响，强调了其在促进可靠决策和简化预测流程中的价值。

还没有人送礼物，鼓励一下作者吧

编辑于 2025-02-08 16:10・北京[时间序列分析](https://www.zhihu.com/topic/19712111)[人工智能](https://www.zhihu.com/topic/19551275)[机器学习](https://www.zhihu.com/topic/19559450)