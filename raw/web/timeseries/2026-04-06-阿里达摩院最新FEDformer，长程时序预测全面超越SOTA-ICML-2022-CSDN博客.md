---
source_type: web
title: "阿里达摩院最新FEDformer，长程时序预测全面超越SOTA | ICML 2022-CSDN博客"
author:
  - 
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
published: 
created: 2026-04-06
description: "文章浏览阅读2.9k次，点赞2次，收藏17次。©作者 | Qingsong单位 | 阿里达摩院决策职能实验室论文标题：FEDformer: Frequency Enhanced Decomposed Transformer for Long-term Series Forecasting论文链接：https://arxiv.org/abs/2201.12740代码链接：https://github.com/DAMO..._fedformer代码"
tags:
  - 
  - "clippings"
source_url: "https://blog.csdn.net/c9Yv2cf9I06K2A9E/article/details/125754784"
published_at: null
related_concepts: []
---

![[a1ac8509ed67c68db106726901e21339.gif|74dc48571835f6a4ae234cd11affd1e8.gif]]

**©作者 |** Qingsong

**单位 |** 阿里达摩院决策职能实验室

![[d08fdaec824b25475df4201912fcfaf3.png|87a0a1f5d990c22809d5e4d9cbf56cc8.png]]

**论文标题：**

FEDformer: Frequency Enhanced Decomposed Transformer for Long-term Series Forecasting

**论文链接：**

https://arxiv.org/abs/2201.12740

**代码链接：**

https://github.com/DAMO-DI-ML/ICML2022-FEDformer

**达摩院决策智能实验室：**

https://damo.alibaba.com/labs/decision-intelligence?lang=zh

![[5ede348b22af761e363d0ab8e5bacd3b.png|bdc6581e9feead6294de934ad6e39d41.png]]

### 引言

时间序列预测在众多领域中（例如电力、能源、天气、交通等）都有广泛的应用。时间序列预测问题极具挑战性，尤其是 **长程时间序列预测** （long-term series forecasting）。在长程时间序列预测中，需要根据现有的数据对未来做出较长时段的预测。在部分场景中，模型输出的长度可以达到 1000 以上，覆盖若干周期。该问题对预测模型的精度和计算效率均有较高的要求。且时间序列往往会受到 **分布偏** **移** 和 **噪音** 的影响，使得预测难度大大增加。

![[801dd9020c1248bf7e403142fa427ca7.png|2f2b95f9ad350a1d848eb61a78d92378.png]]

针对时间序列问题，传统的 RNN、LSTM 等 Recurrent 模型，在训练时容易受到梯度消失和爆炸的影响，尤其是面对更加长程的序列时。且这类 Recurrent 的模型无法并行计算，限制了其在大规模问题上的应用。

基于 Transformer 的时间序列预测，通过 **Attention 机制** 捕捉 point-wise 的关系，能够在时序预测中取得较好效果，但仍存在较大不足。Informer、Autoformer 等文章对传统 Attention 机制进行了改进，在提高计算效率的同时能够取得较好的效果。传统 Transformer 为平方复杂度，Autoformer (NeurIPS’21)、Informer (AAAI’21 Best paper)、Reformer (ICLR’2020) 等模型能够达到 log-线性复杂度，而本文作者所提出的 **FEDformer** 因使用了 low-rank approximation 而可以达到线性复杂度，并在精度上大幅超越 SOTA（state-of-the-art）结果。

![[ce5bf425d07772b5ce04d38059a05b9c.png|037d6bf9df827759273673567c1ebce4.png]]

![[5ffba42bd12c2487cbb14d9abb40e5e5.png|3d9064ff34112088c5d421ae6bdea01e.png]]

### 分析

Transformer 在 CV、NLP 等领域取得了很好的效果，但在时间序列预测问题上，情况会更复杂。例如在图片分类问题中，训练集和测试集的图片基本采样自相同的分布。然而在时间序列预测问题中，序列的分布可能随时间轴的推进不断变化，这就需要模型具备更强的 **外推** 能力。如下图所示，因为模型输入（input）和真实值（true）的 **分布** 差异较大，导致模型的预测值（predict）不准确。（分布差异的大小可以通过 Kologrov-Smirnov test 来检验）。

为了解决这个问题，作者提出了两种思路：

1\. 通过 **周期趋势项分解** （seasonal-trend decomposition）降低输入输出的分布差异；

2\. 提出了一种在 **频** **域** 应用 **注意力机制** 的模型结构，以增加对噪声的鲁棒性。

  
![[55d593990a1f3f4bc8b5672e2b2c86ca.png|5fc3723a197d13932a8574bc813e06ef.png]]

![[195277d70a19585869f4e4869578dfdb.png|628733d2250814d1d39c98b34b7d07d5.png]]

### FEDformer

FEDformer 的主体结构（backbone）采用 **编码-解码器结构** ，内部包括四种子模块：频域学习模块（Frequency Enhanced Block）、频域注意力模块（Frequency Enhanced Attention）、周期-趋势分解模块（MOE Decomp）、前向传播模块（Feed Forward）。

**3.1 主体架构**

**![[43222eac61f2465c20d985a5fc8709cc.png|7ada67870a066445ea0593ddb4cd4ed3.png]]**

**FEDformer** 的主体架构采用编码-解码器架构。周期-趋势分解模块（MOE Decomp）将序列分解为周期项（seasonal，S）和趋势线（trend，T）。而且这种分解不只进行一次，而是采用反复分解的模式。

在编码器中，输入经过两个 MOE Decomp 层，每层会将信号分解为 seasonal 和 trend 两个分量。其中，trend 分量被舍弃，seasonal分量交给接下来的层进行学习，并最终传给解码器。

在解码器中，编码器的输入同样经过三个 MOE Decomp 层并分解为 seasonal 和 trend 分量，其中，seasonal 分量传递给接下来的层进行学习，其中通过 **频域** **Attention（Frequency Enhanced Attention）** 层对编码器和解码器的 seasonal 项进行频域关联性学习，trend 分量则进行累加最终加回给 seasonal 项以还原原始序列。

**3.2 频域上的表征学习**

傅立叶变换和逆傅立叶变换可以将信号在时域和频域之间相互转换。一般信号在频域上具有 **稀疏性** ，也就是说，在频域上只需保留很少的点，就能几乎无损的还原出时域信号。保留的点越多，信息损失越少，反之亦然。

![[5c69585926dd262513b073970a2a045b.png|24e2bd9165cd5e63bf15ff560c094281.png]]

虽然无法直接理论证明在 **频域** 上应用各种 **神经网络结构** 能够得到更强的表征能力。但在实验中发现，引入 **频域** 信息可以提高模型的效果，这个现象已经得到近期越来越多论文的证实。

FEDformer 中两个最主要的结构单元的设计灵感正是来源于此。Frequency Enchanced Block（FEB）和 Frequency Enhanced Attention（FEA）具有相同的流程：频域投影 -> 采样 -> 学习 -> 频域补全 -> 投影回时域：

1\. 首先将原始时域上的输入序列投影到频域。

2\. 再在 **频域上进行随机采样** 。这样做的好处在于极大地降低了输入向量的长度进而降低了计算复杂度，然而这种采样对输入的信息一定是有损的。但实验证明，这种损失对最终的精度影响不大。因为一般信号在频域上相对时域更加“稀疏”。且在高频部分的大量信息是所谓“噪音”，这些“噪音”在时间序列预测问题上往往是可以舍弃的，因为“噪音”往往代表随机产生的部分因而无法预测。相比之下，在图像领域，高频部分的“噪音”可能代表的是图片细节反而不能忽略。

3\. 在学习阶段， **FEB** 采用一个全联接层 R 作为可学习的参数。而 **FEA** 则将来自编码器和解码器的信号进行 **cross-attention** 操作，以达到将两部分信号的内在关系进行学习的目的。

4\. **频域补全** 过程与第 2 步 **频域采样** 相对，为了使得信号能够还原回原始的长度，需要对第 2 步采样未被采到的频率点补零。

5\. 投影回时域，因为第 4 步的补全操作，投影回频域的信号和之前的输入信号维度完全一致。

![[189e36f207181ede66368ad185a1e4d4.png|3447c6796dedb077840a52e52439790d.png]]

![[e0254a6a630b8e24768ce2c03ec2ed6f.png|0ff66f2a70fb8eddf3d5b46944965944.png]]

**3.3 低秩近似（low-rank approximation）**

传统 Transformer 中采用的 Attention 机制是平方复杂度，而 **Frequency Enhanced Attention（FEA）** 中采用的 Attention 是线性复杂度，这极大提高了计算效率。因为 **FEA** 在频域上进行了采样操作，也就是说：“无论多长的信号输入，模型只需要在频域保留极少的点，就可以恢复大部分的信息”。采样后得到的小矩阵，是对原矩阵的 **低秩近似** 。作者对 **低秩近似** 与信息损失的关系进行了研究，并通过理论证明，在频域随机采样的 **低秩近似** 法造成的信息损失不会超过一个明确的上界。证明过程较为复杂，有兴趣的读者请参考原文。

**3.4 傅立叶基和小波基**

以上篇幅均基于傅立叶变换进行介绍，同理，小波变换也具有相似的性质，因而可以作为 FEDformer的 一个变种。傅立叶基具有全局性而小波基具有局部性。作者通过实验证明，小波版的 FEDformer 可以在更复杂的数据集上得到更优的效果。但小波版的 FEDformer 运行时间也会更长。

![[cc973b15f76bd73f7375603eca989236.png|402c13565df3f33f7679d6cf0d9313ed.png]]

![[5258a970c6f9ef6c9a4eb85123f7e580.png|0225b44193d598e7e76e4c51b01e1fdc.png]]

### 实验

**4.1 Benchmark实验**

作者在 6 个数据集上进行了模型效果实验，实验数据集包括电力，经济，交通，气象，疾病五个领域，并选取了最新的 Baseline 模型，包括 Autoformer (NeurIPS’21)、Informer (AAAI’21 Best paper)、LogTrans (NeurIPS’2019)、Reformer (ICLR 2020) 等进行对比。FEDformer 在多维时间序列预测实验中相比 SOTA 模型可以取得 14.8% 的提升（如下表） 。在一维时间序列预测实验中相比 SOTA 模型可以取得 22.6% 的提升（详情请见论文）。

![[d4a0ba01f6605dd2871f8bc6826cdd5c.png|2aa84a5b586b726992ead345f6c012b4.png]]

FEDformer 具有较好的鲁棒性，在重复多次进行实验后，最终 MSE 指标在均值较小的同时也能做到方差较小。FEDformer 模型中在 FEB 和 FEA 模块中均具有随机采样的过程。也就是说不同随机种子下得到的 FEDformer 模型所采样得到的频率是不同的。但这种随机性并不会体现在最终效果上，也就是说并不会使模型的鲁棒性有损。

![[c724dc6228c6d7407cbc073f851c9afb.png|4961f0ac52097940587f4bc65264f445.png]]

#### 4.2 基频采样实验

作者通过实验讨论了，在 FEB 和 FEA 模块中，在频域采样保留多少个点对最终效果的影响如何。

![[45d63d2bd57902652c2864558ebf9306.png|45c389f8a222202e33d3a9c9408c78fb.png]]

#### 4.3 模型速度和内存的实验

在不断增加输出长度的条件下，FEDformer 因其线性复杂度而在运行速度和内存占用上增加很少。相比 Transformer（平方复杂度）和 Autoformer/Infomer（log-线性复杂度）具有较大优势。

![[52a07979f58f6305719992867ed45cae.png|4d2b30957271d108be9bc0fd6fcb8df1.png]]

![[c512b47373f010b64c6cd58c00b1896b.png|792c0d5847aa164499e8a1f1d368c099.png]]

### 总结

针对长时间序列预测问题，作者提出了基于频域分解的 FEDformer 模型。大幅提高了预测精度和模型运行效率。作者提出了一种基于傅立叶/小波变换的模块，通过在频域进行固定数量的随机采样，使得模型达到线性复杂度同时提高精度。

作者通过实验证明，在涵盖电力，交通，经济，气象，疾病五个领域的 6 个标准数据集上，FEDformer 可以在多维/一维时间序列预测问题上分别取得 14.8% 和 22.6% 的提升（相比 NeurIPS’21 的 SOTA 模型 Autoformer），并具有良好的鲁棒性。

特别指出的是，我们的方法初步证明了在深度学习网络中利用时序频域信息的有效性。未来，我们将继续探索如何更好的利用时间序列的频域信息来构建网络，在时序预测、异常检测中取得更好的效果。

![[35b9026e4bda3df223cecc228e5e9313.png|outside_default.png]]

**延伸阅读**

![[35b9026e4bda3df223cecc228e5e9313.png|outside_default.png]]

\[1\] \[Time-series Transformer Survey\] Qingsong Wen, Tian Zhou, Chaoli Zhang, Weiqi Chen, Ziqing Ma, Junchi Yan, Liang Sun, “Transformers in Time Series: A Survey,” arXiv preprint arXiv:2202.07125 (2022). Website: https://github.com/qingsongedu/time-series-transformers-review

\[2\] \[KDD’22 Quatformer\] Weiqi Chen, Wenwei Wang, Bingqing Peng, Qingsong Wen, Tian Zhou, Liang Sun, “Learning to Rotate: Quaternion Transformer for Complicated Periodical Time Series Forecasting”, in Proc. 28th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD’22), Washington DC, Aug. 2022.

\[3\] \[KDD’22 Tutorial\] Qingsong Wen, Linxiao Yang, Tian Zhou, Liang Sun, “Robust Time Series Analysis and Applications: An Industrial Perspective,” in the 28th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD’22), Washington DC, USA, Aug. 14-18, 2022. Website: https://qingsongedu.github.io/timeseries-tutorial-kdd-2022/

\[4\] \[IJCAI’22 Tutorial\] Qingsong Wen, Linxiao Yang, Tian Zhou, Liang Sun, “Robust Time Series Analysis: from Theory to Applications in the AI Era,” in the 31st International Joint Conference on Artificial Intelligence (IJCAI 2022), Vienna, Austria, Jul. 23-29, 2022. Website: https://sites.google.com/view/timeseries-tutorial-ijcai-2022

\[5\] \[招聘全职/实习生\] 阿里达摩院DI Lab - 常年招全职/实习生: AI for Time Series, AIOps, XAI等方向 (杭州/西雅图) JD: https://zhuanlan.zhihu.com/p/528948916

**更多阅读**

![[fe2b61306cd1afaaa98d434f3bdda0e1.png|8fc529b8d2c5fef84e7323da8121d3d6.png]]

![[0d363a0d3393d5560f912aa651e177b7.png|84f2fa337bed6d1c6bcd080e8e910282.png]]

![[86015d14abf438004ea92452810cb055.png|1fdf531aa0fe369c0174fccba3b69db5.png]]

![[b6d1d5ddf1c76b7f625e7c11d797b2d2.gif|ae91077c772ba56a0bb3a403360fb727.gif]]

**#投 稿 通 道#**

**让你的文字被更多人看到**

如何才能让更多的优质内容以更短路径到达读者群体，缩短读者寻找优质内容的成本呢？ **答案就是：你不认识的人。**

总有一些你不认识的人，知道你想知道的东西。PaperWeekly 或许可以成为一座桥梁，促使不同背景、不同方向的学者和学术灵感相互碰撞，迸发出更多的可能性。

PaperWeekly 鼓励高校实验室或个人，在我们的平台上分享各类优质内容，可以是 **最新论文解读** ，也可以是 **学术热点剖析** 、 **科研心得** 或 **竞赛经验讲解** 等。我们的目的只有一个，让知识真正流动起来。

📝 **稿件基本要求：**

• 文章确系个人 **原创作品** ，未曾在公开渠道发表，如为其他平台已发表或待发表的文章，请明确标注

• 稿件建议以 **markdown** 格式撰写，文中配图以附件形式发送，要求图片清晰，无版权问题

• PaperWeekly 尊重原作者署名权，并将为每篇被采纳的原创首发稿件，提供 **业内具有竞争力稿酬** ，具体依据文章阅读量和文章质量阶梯制结算

📬 **投稿通道：**

• 投稿邮箱：hr@paperweekly.site

• 来稿请备注即时联系方式（微信），以便我们在稿件选用的第一时间联系作者

• 您也可以直接添加小编微信（ **pwbot02** ）快速投稿，备注：姓名-投稿

![[18a7cd5456206a7aaf9ef432f92367ac.png|1bec8d8acbb038ded3625e304c369148.png]]

**△长按添加PaperWeekly小编**

🔍

现在，在 **「知乎」** 也能找到我们了

进入知乎首页搜索 **「PaperWeekly」**

点击 **「关注」** 订阅我们的专栏吧

·

![[ee5e0484fded9087dc39a66a9971e2e1.jpeg|257e9a27d090f60a6319250f066f0518.jpeg]]