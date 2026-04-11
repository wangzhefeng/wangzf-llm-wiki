---
title: "百度/中科大等联合发布：TimeFound-超越谷歌TimesFM的时序基础模型，零样本泛化能力惊人！"
author:
  - "[[时序之心]]"
published:
created: 2026-04-11
description: "百度/中科大等联合发布 | TimeFound：超越谷歌TimesFM的时序基础模型，零样本泛化能力惊人！"
tags:
  - "clippings"
source_type: web
created_at: 2026-04-11
topics:
  - "clippings"
status: inbox
source_url: "https://mp.weixin.qq.com/s/4zopxtf3hq_Rlb8HSENmwA"
published_at: null
related_concepts: []
---
原创 时序之心 *2026年1月26日 10:41*

在人工智能涉足的各个领域中， **时间序列预测（Time Series Forecasting）** 一直是一个极其重要但又充满挑战的方向，它广泛应用于能源管理、金融分析、气象预报等关键行业。过去，研究人员主要依赖深度学习模型，但这些模型通常需要针对特定领域的大量数据进行训练，一旦换个场景，模型就失效了，这就是所谓的“泛化能力”差。更棘手的是，现实中很多场景根本没有足够的数据来重新训练模型。

为了解决这个难题，本论文受到大语言模型的启发，提出了名为 **TimeFound** 的 **基础模型（Foundation Model）** 。该模型采用了一种独特的 **多分辨率分块（Multi-resolution Patching）** 策略，能够同时捕捉时间序列中不同尺度的变化规律。通过在海量数据上进行预训练，TimeFound 实现了强大的 **零样本（Zero-shot）** 预测能力，即不需要针对新数据进行训练就能直接进行精准预测，在多个实验中表现优于当前最先进的同类模型。

另外我整理了时间序列+LLM(2024-2025年)相关论文，感兴趣的自取哦~(科研人专属物资见文末)

关注“时序之心”回复“C826”

免费领取 **时间序列+LLM相关论文合集**

## 一、论文基本信息

![[raw/assets/attachments/Image.webp|图片]]

**论文标题：** TimeFound: A Foundation Model for Time Series Forecasting

**作者姓名：** Congxi Xiao, Jingbo Zhou, Yixiong Xiao, Xinjiang Lu, Le Zhang, Hui Xiong

**作者单位/机构：** 百度研究院商业智能实验室（Business Intelligence Lab, Baidu Research）、中国科学技术大学、香港科技大学（广州）

**论文链接：** https://arxiv.org/pdf/2503.04118

## 二、主要贡献与创新

1. 提出了TimeFound模型，采用 **编码器-解码器（Encoder-Decoder）** 架构，结合历史上下文理解与未来因果预测。
2. 设计了 **多分辨率分块** 策略，通过不同大小的切片处理数据，有效适应不同领域的频率和尺度特征。
3. 基于大规模真实与合成时间序列语料库，训练了2亿和7.1亿参数量的两个版本基础模型。
4. 在24个未见过的跨领域数据集上进行了零样本评估，证明了模型在短长期预测中的卓越泛化能力。

## 三、研究方法与原理

TimeFound模型的核心思路是：将时间序列看作一种特殊的“语言”，通过将数据切分成不同粗细粒度的“块”，让模型既能看清细节波动又能把握整体趋势，从而实现通用的预测能力。

![Figure 1.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 1.

### 1\. 输入模块：多分辨率分块与投影

模型首先需要处理来自不同领域的原始数据。为了统一数据分布，TimeFound首先对输入序列进行标准化处理（Standard Scaling）。随后，论文引入了核心创新点： **多分辨率分块** 。与以往固定大小分块的方法不同，该策略考虑到不同领域的数据（如每分钟的股票和每小时的气温）具有完全不同的动态特性。

假设输入的时间序列上下文为 ，模型定义了一组不同的分块大小 。对于第 种分块尺寸 ，序列被划分为 个块。为了将这些块映射到潜在空间，模型使用了 个独立的映射器（Projector），每个映射器由两层多层感知机（MLP）构成。

为了处理填充（Padding）等特殊情况，模型还引入了点级掩码（Point-level Mask） ，它与分块一起被送入映射器。对于第 种分辨率下的第 个分块 和对应的掩码 ，其潜在嵌入表示 计算如下：

其中 表示拼接操作。

### 2\. 补丁嵌入融合（Patch Embedding Integration）

经过多分辨率分块后，我们得到了 组不同长度的嵌入向量序列。因为分块大小不同，导致序列长度不一致（块越大，序列越短），无法直接输入到后续网络中。为了解决这个问题，论文提出了一种 **上采样（Upsampling）** 对齐策略。

模型以分块数量最多（即分辨率最高、块最小）的那一组 为基准，将其他较粗粒度的分块序列进行复制扩展。对于第 组中的每个分块嵌入 ，它会被复制 次。对齐后的序列表示为 ：

最后，将所有对齐后的组在对应位置上的嵌入向量相加，得到最终融合了多尺度信息的输入序列 ：

这种设计巧妙地保留了不同时间尺度下的语义信息，同时为Transformer提供了统一的输入格式。

### 3\. 主干网络：Transformer 模块

TimeFound 采用了 T5 模型的编码器-解码器架构作为主干。

**编码器** 部分使用双向注意力机制，允许模型在处理历史数据时查看整个上下文，从而深入理解历史趋势。 **解码器** 部分则严格采用因果注意力机制（Causal Attention），确保在生成预测时只能看到当前时刻之前的信息，符合时间序列预测的逻辑。同时，解码器通过交叉注意力（Cross-Attention）机制与编码器的输出进行交互，利用历史信息来指导未来的生成。

### 4\. 输出模块与预测

解码器的输出经过一个输出模块（Output Module）转化为未来的预测值。该模块同样由两层 MLP 构成。假设解码器输出的最后一个分块表示为 ，模型预测下一个分块 的公式为：

值得注意的是，输出的分块大小 可以大于输入的分块大小，这有利于加速长序列的生成。

除了点预测，模型还支持概率预测。通过添加一个额外的预测头，模型可以输出分位数预测结果。对于感兴趣的分位数集 （例如十分位数），损失函数包含了 **分位数损失（Quantile Loss）** 。

### 5\. 训练目标

模型的预训练采用了 **教师强制（Teacher Forcing）** 策略，即在训练时将真实的未来标签作为解码器的输入。总损失函数 由两部分组成：衡量点预测准确性的均方误差损失（MSE）和衡量概率分布准确性的分位数损失（QL）。

其中 MSE 损失计算如下：

通过这种混合损失训练，TimeFound 既能给出精确的数值预测，也能给出置信区间，增强了其实用性。

## 四、实验设计与结果分析

为了验证 TimeFound 的有效性，研究团队采用了极为严格的评估标准。预训练数据使用了包含能源、金融、天气等多个领域的真实数据集以及部分通过高斯过程生成的合成数据。模型分为 **TimeFound-Base (2亿参数)** 和 **TimeFound-Large (7.1亿参数)** 两个版本。

### 对比实验：标准零样本评估

在这一部分，实验评估了模型在24个未参与预训练的数据集上的表现。评估指标采用 MASE（平均绝对缩放误差）和 sMAPE（对称平均绝对百分比误差）。对比模型包括 Google 的 TimesFM 和亚马逊的 Chronos 等顶尖基础模型。

![Table 3.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Table 3.

实验结果显示，TimeFound 在绝大多数数据集上都取得了领先或极具竞争力的成绩。特别是在综合所有数据集的几何平均指标上， **TimeFound 取得了最佳性能** （MASE 指标最低）。这表明，相比于其他模型可能只在特定类型数据上表现好，TimeFound 的多尺度设计让它在面对任何陌生领域的数据时，都能保持稳定的高水准预测。

### 对比实验：长序列滚动验证

为了进一步测试模型在长周期预测中的稳定性，实验在四个经典的电力变压器温度数据集（ETT）上进行了 **滚动验证（Rolling Validation）** 。预测长度涵盖了从96到720个时间点。

![Table 4.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Table 4.

如表4所示，TimeFound 在长序列预测任务中表现尤为出色。随着预测长度的增加（例如到达720点），其他模型（特别是基于点预测的 Chronos）的误差显著上升，这是因为点预测容易产生误差累积。而 TimeFound 凭借基于分块（Patch-based）的建模方式和多分辨率特性，在长周期预测中依然保持了较低的误差， **在所有设置下均优于对比基线** 。

## 五、论文结论与评价

### 总结

本文提出了 TimeFound，一个面向时间序列预测的通用基础模型。通过创新的多分辨率分块策略和强大的编码器-解码器 Transformer 架构，该模型成功解决了单一尺度难以适应多领域数据特征的痛点。实验证明，TimeFound 在完全未见过的真实世界数据集中，无论是短期还是长期预测，都展现出了超越现有最先进模型（如 TimesFM 和 Chronos）的零样本泛化能力。这项研究为构建通用的“时间序列预测大模型”提供了坚实的理论和实践基础。

### 优点

1. **多尺度适应性强** ：多分辨率分块设计非常巧妙，从数学原理上保证了模型能够同时捕捉高频细节和低频趋势，这对于处理来源复杂的通用时间序列至关重要。
2. **长序列预测稳定** ：相比于逐点预测的模型，TimeFound 采用的分块自回归生成方式显著减少了长距离预测时的误差累积，使其在长周期任务中优势明显。
3. **架构通用性** ：模型不仅支持确定性的点预测，还能输出概率分布（分位数），这在风险管理等实际应用中非常具有价值。

### 缺点

1. **推理计算成本** ：虽然多分辨率融合提升了精度，但相比于单一分块，这种设计在推理阶段涉及多组映射和上采样操作，可能会增加一定的计算开销和内存占用。
2. **依赖数据对齐** ：在上采样过程中采用了简单的复制策略来对齐不同分辨率的块，这种硬性的对齐方式可能在某些剧烈变化的边界处引入由于“块效应”导致的不平滑，虽然文中提到效果很好，但理论上存在更平滑的插值优化空间。
3. **通道独立性限制** ：模型目前主要针对单变量预测（对多变量采用通道独立处理），这虽然提高了泛化性，但可能忽略了多变量之间潜在的复杂相关性（如股票价格与交易量之间的关系）。

扫码添加小助手回复“C826”

免费获取全部论文资料

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

---

**🎁 科研人专属物资 · 免费补给**

为了帮大家理清全年的投稿时间线，我们特别制作了 **“2026科研日历鼠标垫”** 和 **“学术通勤帆布袋”** 。不做虚的，只送实用的工具。

- **选品一：全功能鼠标垫** 印有全年CCF会议时间轴，抬头就能看DDL，治愈拖延症。扫码还能直通内部学术交流群，获取大佬经验。
- **选品二：大容量帆布袋** 尺寸40\*34cm，不仅能装下电脑和论文，简约设计也让通勤更轻松。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**🚀 领取指南（请仔细阅读）**

本活动真实有效，限量500份，手慢无。

- **第一步：** 扫描下方二维码。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)
- **第二步：** 后台回复关键词 **【鼠标垫】** 获取参与链接。
- **注意事项：**
- **仅限学术地址：** 我们只发往高校、研究院或医院。非学术机构地址无法发货，感谢理解。
	- **截止时间：** 2026年2月2日 17:00。
	- **发货时间：** 2月2日首批，3月2日第二批。

新的一年，愿这份小礼物能陪伴你的Paper之路。预祝各位2026年Paper High Accept，毕业求职一路绿灯！

---

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

---

相关推荐

[AAAI 2026 炸场！华人团队“鲨疯了”，5 篇杰出论文狂揽 3 席，港科大、同济等立大功！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488770&idx=1&sn=f7b255a467c8cdf2f083a89f0c56725c&scene=21#wechat_redirect)

[AAAI 2026 | Transformer不再被MLP吊打！EMAformer穿上“嵌入装甲”杀回来了，重夺时序预测SOTA！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488735&idx=1&sn=7b24c54ab163d6923adf00c87c8ae5a4&scene=21#wechat_redirect)

[炼狱级开局！AAAI 2026 录用率暴跌至 17% ，快手斩获 3 篇 Oral](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488713&idx=1&sn=53cdf9c110b2431a376122da25ce3dab&scene=21#wechat_redirect)

[2025时序分析风向标：左手TimeCAP语义增强，右手TIMEMIXER++全能SOTA，这波你站谁？](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488701&idx=1&sn=429e6eb7aaf5e12be077f3733cf01d47&scene=21#wechat_redirect)

[VLDB 2025 | 时间序列相关论文篇盘点（附原文源码）！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488580&idx=1&sn=2a926758f17aa935e408e64206ce23fa&scene=21#wechat_redirect)

[两篇论文硬核解析！从综述到实战，彻底讲透“时空+扩散模型”！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488562&idx=1&sn=7a5117ab4da698dd87084cd3b03af8ab&scene=21#wechat_redirect)

[AAAI 2026 | 时序预测再进化：自适应容量调整+双域并行预测，MDMLP-EIA全面领先现有SOTA模型！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488552&idx=1&sn=5b2fb2b5483d6add7eb601ef3fe70f98&scene=21#wechat_redirect)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

作者提示: 个人观点，仅供参考

阅读原文

继续滑动看下一个

时序之心

向上滑动看下一个