---
source_type: web
title: "【时间序列】TimesBERT: A BERT-Style Foundation Model for Time Series Understanding 论文阅读与分享"
author:
  - 
  - "[[Andy]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://zhuanlan.zhihu.com/p/1894041339106144523?utm_psn=1894857526874456590"
published: 
created: 2026-04-06
description: "笔者的话 作为一名大三的理工科学生，我在入门科研时曾被论文中复杂的公式和术语“劝退”。幸运的是，知乎平台上许多深入浅出的论文解读文章，像一盏盏明灯，帮助我快速理解论文的核心思想和方法论设计。 如今，我…"
tags:
  - 
  - "clippings"
---

目录

收起

笔者的话

背景

主要贡献

具体方法

时间序列嵌入（TIME SERIES EMBEDDING）

预训练 TimesBERT

微调

实验效果

## 笔者的话

　　作为一名大三的理工科学生，我在入门科研时曾被论文中复杂的公式和术语“劝退”。幸运的是，知乎平台上许多深入浅出的论文解读文章，像一盏盏明灯，帮助我快速理解论文的核心思想和方法论设计。

　　如今，我开始尝试用同样的方式解读论文，一方面是希望通过输出倒逼自己更深入地思考。另一方面也希望能为其他刚入门的小伙伴提供一些参考。然而， [时间序列分析](https://zhida.zhihu.com/search?content_id=256283594&content_type=Article&match_order=1&q=%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97%E5%88%86%E6%9E%90&zhida_source=entity) 与大模型预训练本身是快速发展的交叉领域，笔者的知识储备和实践经验仍有诸多不足。 **若您在阅读中发现任何逻辑漏洞、技术误解或表述不清之处，恳请不吝指正** ，这将成为我持续改进的重要动力。

　　需要特别说明的是，论文解读本质上是一种“二手信息”，难免存在个人理解的偏差。 **强烈建议读者结合原文与自身实践辩证参考** ，也欢迎对文中观点展开讨论，共同探索时间序列基础模型的可能性与挑战。

---

**paper link:**

## 背景

  
　　时间序列分析被广泛应用于许多实际应用中，并具有多样化的任务形式，其中 **时间序列预测** 引起了大量关注和研究工作。然而，剩余任务相对关注较少，导致对模型在实际需求方面的能力缺乏全面的探索。这篇论文试图解决时间序列分析中 **时间序列理解** （time series understanding）的问题，特别是对于 **分类、插补缺失值、异常检测** 等任务的支持。

![[assets/attachments/timeseries/v2-e71b9299285d6ac636f57d002a555012_1440w.jpg]]

使用 TimesBERT 可以完成时间序列中的各种任务

　　虽然现有的 GPT 风格模型在时间序列预测等生成任务中表现出色，但它们缺乏利用双向上下文的能力，这对全局理解造成了关键瓶颈。相比之下，BERT在自然语言中表现出任务多样性。

![[assets/attachments/timeseries/v2-19c6e8e7b90222db0e73cac231d4fbf1_1440w.jpg]]

自然语言和时间序列之间的关系：a multivariate time series is worth a multisentence text document

　　作者发现时间序列与自然语言在结构上有令人惊讶的相似之处。  
　　受上述动机的启发，作者提出了 **TimesBERT** ，这是一个基于BERT风格的 [预训练模型](https://zhida.zhihu.com/search?content_id=256283594&content_type=Article&match_order=1&q=%E9%A2%84%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B&zhida_source=entity) ，旨在学习时间序列的通用表示，包括时间模式和变量中心的特征，以支持多种时间序列理解任务。

## 主要贡献

1. 提出将多变量时间序列视为多句文档，揭示了BERT作为预训练模型的优势。
2. 开发了 TimesBERT，包括一个统一的结构化嵌入和一个针对多变量时间序列多粒度结构的功能性标记预测任务，将BERT与时间序列完全对齐。
3. 在包含2600亿个时间点的大规模数据集上对我们的模型进行了预训练，该模型可以适应时间序列分类、插补、异常检测和短期预测任务的最新成果。
![[assets/attachments/timeseries/v2-4308ae9e1eff2eed9b9f1f2120cbb161_1440w.jpg]]

　与BERT的句子对形式化不同，作者为具有任意数量变量的数据实施了一种嵌入方法，并设计了相应的功能标记，以适应时间序列变量固有的不规则性。

## 具体方法

![[assets/attachments/timeseries/v2-4e6900519aae7e465295e26f7f100ec3_1440w.jpg]]

TimesBERT 整体结构图

### 时间序列嵌入（TIME SERIES EMBEDDING）

1. 将时间序列中每个变量按列放置，输入 X 的形状为时间长度 T \* 变量个数 C
2. 分块，将时间序列分为patch，相当于NLP中的token
3. 参考bert模型中 \[cls\]，\[mask\] 和 \[sep\], 引入三个特殊标记：
- **`z[DOM]`** ：全局领域特征的代表，用于分类和趋势预测。类似于 BERT 中的 `[CLS]` 标记，位于输入矩阵 `Z⁰` 的第一行（全局位置）。
- **`z[VAR]`** ：变量级别的分隔与特征聚合，用于跨变量推理。类似于 BERT 中的 \[SEP\] 标记，位于每个变量的末尾（分隔不同变量）。
- **`z[MASK]`** ：局部时间模式的掩码与重建，增强鲁棒性。类似于 BERT 中的 `[MASK]` 标记，但应用于时间序列片段而非文本词元。

　　以上是具体的矩阵变化，我感觉把矩阵画出来会比公式中的符号更加直观，易于理解。

　　采用一个仅编码器的Transformer，具有维度D和L层，作为TimesBERT的主干，将嵌入展平后前向传播。

![[assets/attachments/timeseries/v2-34ed7c0aa5e248ef36dc030e4468e877_1440w.jpg]]

将多变量时间序列看作一句有很多句话的文档

### 预训练 TimesBERT

**任务一：MPM(masked patch modeling)**

　　受 BERT 中使用的 [掩码语言建模](https://zhida.zhihu.com/search?content_id=256283594&content_type=Article&match_order=1&q=%E6%8E%A9%E7%A0%81%E8%AF%AD%E8%A8%80%E5%BB%BA%E6%A8%A1&zhida_source=entity) 任务启发，作者采用了 [掩码补丁建模](https://zhida.zhihu.com/search?content_id=256283594&content_type=Article&match_order=1&q=%E6%8E%A9%E7%A0%81%E8%A1%A5%E4%B8%81%E5%BB%BA%E6%A8%A1&zhida_source=entity) （MPM）为基础模型提供基础理解能力。对于输入标记序列，作者对非功能性标记采用了掩码比例α = 25%。（被选择的patch被z\[MASK\]替换的概率是90%，剩下的patch作者没说如何处理，应该是保持原样，和bert中一样，这是为了缓解 finetune 时候与预训练时候输入不匹配的问题）

![[assets/attachments/timeseries/v2-8ce549174f7b8c0a209964a5293c1112_1440w.jpg]]

任务一：MPM的示意图

**任务二：FTP(FUNCTIONAL TOKEN PREDICTION)**

![[assets/attachments/timeseries/v2-bd4358ca2896c70a549264f8a907efa1_1440w.jpg]]

任务二：FTP的示意图

针对多变量时间序列设计的预训练任务，通过 **变量替换检测** 和 **域分类** 两个子任务联合优化模型：

1. **变量替换检测: 二元交叉熵损失,**随机用另一个数据集中的一个变量替换一个变量，利用变量分隔标记 `z[VAR]` 的输出特征，通过二分类交叉熵损失（ `WVAR` 分类层）识别被替换变量，迫使模型学习跨变量兼容性；
2. **域分类** ： **多类交叉熵损失,**基于全局标记 `z[DOM]` 的输出特征，通过多分类交叉熵损失（ `WDOM` 分类层）预测时间序列所属的数据集领域，增强模型对全局领域特征的捕捉能力。  
	FTP 通过显式建模变量间关系与全局统计特性，弥补了传统掩码建模在跨变量推理和特征聚合上的不足。

最后，训练目标表示如下：

　　训练完成后，保留transformer主干参数，去除任务头参数（比如Wout, Wvar, Wdom）。预训练阶段之后，任务头被移除，而Transformer骨干在微调过程中被调整用于表示提取。这个过程有效地将预训练的骨干与任务设计解耦。

### 微调

在TimesBERT的微调阶段采用可训练的输出层，以适应各种下游数据集。

## 实验效果

![[assets/attachments/timeseries/v2-4f4e6eb8952941b8e65e738bcaa4f025_1440w.jpg]]

五边形战士

![[assets/attachments/timeseries/v2-17730453b849e4ab01e68948134fbb64_1440w.jpg]]

编辑于 2025-04-16 16:01・广东[BERT](https://www.zhihu.com/topic/20743626)[时间序列分析](https://www.zhihu.com/topic/19712111)